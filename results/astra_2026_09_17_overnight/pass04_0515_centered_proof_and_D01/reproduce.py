#!/usr/bin/env python3
"""Reproduce in a new directory. No overwrite, network or topology library.
--audit-only checks the corrected algebra and original saved jet identities.
The default also recomputes the nine source/control/D01 jets serially.
"""
from pathlib import Path
import argparse, json, shutil, subprocess, sys, time
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output_dir',type=Path)
    ap.add_argument('--audit-only',action='store_true')
    ap.add_argument('--compiler',default='g++')
    args=ap.parse_args()
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    for d in ('deps','inputs','results'):(out/d).mkdir()
    for n in ('audit_centered_kernel.py','check_jet_composition.py','run_target.py','validate_target_geometry.py'):
        shutil.copy2(HERE/n,out/n)
    for n in ('targets.json','D01.json'):shutil.copy2(HERE/'inputs'/n,out/'inputs'/n)
    for n in ('geometry.py','frontier_jet.cpp'):shutil.copy2(HERE/'deps'/n,out/'deps'/n)
    original=json.loads((HERE/'RESULTS.json').read_text())
    report={'status':'RUNNING','mode':'saved-jet audit' if args.audit_only else 'fresh computations','counterexample_found':False,'commands':[]}
    def record():
        (out/'reproduction_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    def run(cmd,timeout):
        row={'command':cmd,'status':'UNKNOWN'};start=time.monotonic()
        try:
            cp=subprocess.run(cmd,cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
            row.update(status='COMPLETED' if cp.returncode==0 else 'ERROR_UNKNOWN',returncode=cp.returncode,output=cp.stdout)
        except subprocess.TimeoutExpired as e:
            row.update(status='TIMEOUT_UNKNOWN',output=str(e.stdout or ''))
        row['wall_seconds']=time.monotonic()-start;report['commands'].append(row);record()
        print(json.dumps({'command':cmd,'status':row['status']}),flush=True)
        if row['status']!='COMPLETED':raise RuntimeError('Reproduction stopped; see explicit unknown/error record')
    try:
        run([sys.executable,'audit_centered_kernel.py','--output','results/centered_kernel_audit.json'],20)
        if args.audit_only:
            for key,recorded in original['runs'].items():
                dest=out/'results'/key;dest.mkdir()
                (dest/'result.json').write_text(json.dumps(recorded,indent=2)+'\n')
        else:
            run([args.compiler,'-O3','-std=c++17','-DEXACT','-DFIXED128','deps/frontier_jet.cpp','-o','deps/jet_exact'],60)
            for target in ('K0','K1','D01'):
                for p in (1,2,3):
                    run([sys.executable,'run_target.py',target,str(p)],45)
                    fresh=json.loads((out/f'results/{target}_p{p}/result.json').read_text())
                    old=original['runs'][f'{target}_p{p}']
                    if fresh['status']!='COMPUTED' or not fresh.get('exact_divisible') or fresh.get('root_quotient')!=old['root_quotient']:
                        raise RuntimeError(f'Reproduction mismatch or UNKNOWN: {target} p={p}')
            run([sys.executable,'validate_target_geometry.py','--output','results/geometry_validation.json'],20)
        run([sys.executable,'check_jet_composition.py'],20)
        report['status']='ARITHMETIC_AUDIT_COMPLETED' if args.audit_only else 'RECORDED_VALUES_REPRODUCED'
    except Exception as e:
        report.update(status='STOPPED_UNKNOWN_OR_MISMATCH',error=str(e));record();raise
    record()
if __name__=='__main__':main()
