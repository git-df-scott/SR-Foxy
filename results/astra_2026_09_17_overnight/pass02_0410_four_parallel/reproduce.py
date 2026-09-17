#!/usr/bin/env python3
"""Reproduce the standalone four-parallel gate, not the SnapPy-based runner.
Requires a C++17 compiler, Boost headers, Python 3 and SymPy. No network.
"""
from pathlib import Path
import argparse, hashlib, json, resource, subprocess, time
import sympy as S
from geometry import blackboard_parallel, zero_writhe, oriented_components
HERE=Path(__file__).resolve().parent

def evaluate(raw,p):
    x=S.symbols('x')
    pol=sum(S.Integer(c)*x**i for i,c in enumerate(raw['coefficients_x']))
    q,r=S.div(pol,(x*x+1)**p,x)
    v=S.rem(S.expand(q*(-x)**p),x*x+1,x)
    rc=[int(r.coeff(x,i)) for i in range(2*p)]
    a,b=int(v.coeff(x,0)),int(v.coeff(x,1))
    exact=raw['modulus'] is None
    return {'exact_divisible':not any(rc) if exact else None,
            'exact_remainder':rc if exact else None,
            'quotient_at_i':[a,b] if exact and not any(rc) else None,
            'remainder_mod32':[c%32 for c in rc],
            'quotient_mod32':[a%32,b%32]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output_dir',type=Path)
    ap.add_argument('--timeout',type=int,default=40)
    ap.add_argument('--compiler',default='g++')
    ap.add_argument('--controls-only',action='store_true')
    args=ap.parse_args()
    if args.timeout<=0:ap.error('timeout must be positive')
    out=args.output_dir;out.mkdir(parents=True,exist_ok=False)
    cert=json.loads((HERE/'certificate.json').read_text())
    for mode,flags in [('exact',['-DEXACT','-DFIXED128']),('mod32',[])]:
        subprocess.run([args.compiler,'-O3','-std=c++17',*flags,str(HERE/'frontier_jet.cpp'),'-o',str(out/('jet_'+mode))],check=True,timeout=60)
    jobs=[('ribbon61_3',3,'exact',1785),('ribbon61_4',4,'exact',19681)]
    if not args.controls_only:jobs += [('KDG_4',4,'mod32',1),('KDG_4_reverse',4,'exact',106081)]
    report={'status':'RUNNING','counterexample':False,'runs':[]}
    for name,p,mode,expected in jobs:
        base=cert['source_KDG_PD'] if name.startswith('KDG') else cert['source_ribbon61_PD']
        pd=blackboard_parallel(zero_writhe(base),p)
        meta=oriented_components(pd)
        if meta['components']!=p or meta['writhe']!=0 or any(v for row in meta['linking_matrix'] for v in row):
            raise RuntimeError('Parallel component/framing checks failed')
        order=cert['orders'][name]
        if sorted(order)!=list(range(len(pd))):raise RuntimeError('Bad crossing order')
        inp=f'{len(pd)} 0 0\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order))+'\n'
        (out/(name+'.input.txt')).write_text(inp)
        row={'name':name,'mode':mode,'crossings':len(pd),'input_sha256':hashlib.sha256(inp.encode()).hexdigest(),'status':'UNKNOWN'}
        def limits():resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
        start=time.monotonic()
        with (out/(name+'.log')).open('w') as err:
            try:
                run=subprocess.run([str((out/('jet_'+mode)).resolve())],input=inp,text=True,stdout=subprocess.PIPE,stderr=err,timeout=args.timeout,preexec_fn=limits)
                if run.returncode:row.update(status='ERROR_UNKNOWN',exit_code=run.returncode)
                else:
                    raw=json.loads(run.stdout);evaluation=evaluate(raw,p)
                    row.update(status='COMPUTED',raw=raw,evaluation=evaluation)
                    ok=(evaluation['exact_divisible'] and evaluation['quotient_at_i']==[expected,0]) if mode=='exact' else (not any(evaluation['remainder_mod32']) and evaluation['quotient_mod32']==[expected,0])
                    row['matches_recorded_value']=bool(ok)
            except subprocess.TimeoutExpired:row['status']='TIMEOUT_UNKNOWN'
        row['wall_seconds']=time.monotonic()-start
        report['runs'].append(row)
        (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['status']!='COMPUTED' or not row.get('matches_recorded_value'):
            report['status']='STOPPED_UNKNOWN_OR_REPRODUCTION_MISMATCH';break
    else:report['status']='RECORDED_RESULTS_REPRODUCED_NO_COUNTEREXAMPLE'
    (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
