#!/usr/bin/env python3
"""Direct small ribbon-connected-sum checks of the general leading laws.

Uses the EXISTING pass02 cabler/frontier engine, but new S#S input diagrams.
The theoretical predictions are compared only after each exact state sum.
No KDG target or prior S-parallel calculation is rerun.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,resource,subprocess,time
from pathlib import Path


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def euler(pd,geometry):
    across={}
    for a,b in geometry.occurrences(pd).values():across[a]=b;across[b]=a
    unused=set(across);faces=0
    while unused:
        start=min(unused);cur=start
        while cur in unused:
            unused.remove(cur);i,j=across[cur];cur=(i,(j+1)%4)
        if cur!=start:raise RuntimeError('Bad face cycle')
        faces+=1
    return faces-len(pd)


def connect_sum(pd,geometry):
    left=[list(c) for c in pd]; shift=max(x for c in pd for x in c)+1
    right=[[x+shift for x in c] for c in pd]
    a=min(geometry.occurrences(left));b=min(geometry.occurrences(right))
    i,j=geometry.occurrences(left)[a][1];k,l=geometry.occurrences(right)[b][1]
    left[i][j]=b;right[k][l]=a
    result=left+right
    if euler(result,geometry)!=2:raise RuntimeError('Connected-sum rotation system nonplanar')
    info=geometry.oriented_components(result)
    if info['components']!=1 or info['writhe']!=0:raise RuntimeError('Bad connected sum')
    return result,{'first_copy_cut_edge':a,'second_copy_cut_edge':b,'first_port':[i,j],'second_port':[k,l],'label_shift':shift}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('engine_dir',type=Path)
    ap.add_argument('output_dir',type=Path)
    ap.add_argument('--maximum',type=int,default=4,choices=(2,3,4))
    args=ap.parse_args();src=args.engine_dir.resolve();out=args.output_dir.resolve()
    out.mkdir(parents=True,exist_ok=False)
    geometry=load('existing_geometry',src/'geometry.py')
    # Evaluator independently divides the finite jet as an ordinary polynomial.
    import sys
    sys.path.insert(0,str(src));evaluation=load('existing_evaluation',src/'reproduce.py').evaluate
    cert=json.loads((src/'certificate.json').read_text())
    base,splice=connect_sum(geometry.zero_writhe(cert['source_ribbon61_PD']),geometry)
    build=['g++','-O3','-std=c++17','-DEXACT','-DFIXED128',str(src/'frontier_jet.cpp'),'-o',str(out/'jet')]
    compiled=subprocess.run(build,check=True,capture_output=True,text=True,timeout=40)
    report={'status':'RUNNING','source_commit':'0eb81a1a15147b2059b9028d0bbc0f4173f0ad33',
            'source_engine_sha256':hashlib.sha256((src/'frontier_jet.cpp').read_bytes()).hexdigest(),
            'source_geometry_sha256':hashlib.sha256((src/'geometry.py').read_bytes()).hexdigest(),
            'connected_sum_PD':base,'splice':splice,'compile_command':build,'runs':[],
            'limitation':'Shared pass02 geometric cabler and frontier evaluator. Independent of the colored-sum algebra, not a separate topology implementation.'}
    for p in range(2,args.maximum+1):
        pd=geometry.blackboard_parallel(base,p);info=geometry.oriented_components(pd)
        if info['components']!=p or info['writhe'] or any(x for row in info['linking_matrix'] for x in row) or euler(pd,geometry)!=2:
            raise RuntimeError('Invalid parallel metadata')
        order=geometry.best_order(pd,seeds=32)
        inp=f'{len(pd)} 0 0\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order['order']))+'\n'
        stem=f'ribbon61_sum_61_parallel_{p}';(out/(stem+'.input.txt')).write_text(inp)
        row={'p':p,'input_sha256':hashlib.sha256(inp.encode()).hexdigest(),'crossings':len(pd),
             'order':order,'planar_Euler':2,'components':p,'linking_matrix':info['linking_matrix'],
             'limit_seconds':35,'limit_address_space_mib':2048}
        def limits():resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
        start=time.monotonic()
        with (out/(stem+'.log')).open('w') as err:
            try:
                run=subprocess.run([str(out/'jet')],input=inp,text=True,stdout=subprocess.PIPE,stderr=err,timeout=35,preexec_fn=limits)
                if run.returncode:row.update(status='ERROR_UNKNOWN',returncode=run.returncode)
                else:
                    raw=json.loads(run.stdout);value=evaluation(raw,p)
                    row.update(status='COMPUTED',raw=raw,evaluation=value)
                    predicted={2:97,3:32049,4:53185}[p]
                    row['predicted_by_colored_sum_algebra']=predicted
                    row['prediction_agrees']=(value['exact_divisible'] and value['quotient_at_i']==[predicted,0])
            except subprocess.TimeoutExpired:row['status']='TIMEOUT_UNKNOWN'
        row['wall_seconds']=time.monotonic()-start;report['runs'].append(row)
        (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:row[k] for k in row if k not in ('order','linking_matrix')}),flush=True)
        if row['status']!='COMPUTED' or not row.get('prediction_agrees'):
            report['status']='STOPPED_UNKNOWN_OR_DISAGREEMENT';break
    else:report['status']='DIRECT_CONNECTED_SUM_CONTROLS_AGREE'
    (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
