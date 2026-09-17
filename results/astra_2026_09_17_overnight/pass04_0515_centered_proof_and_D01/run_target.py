#!/usr/bin/env python3
"""One exact bounded parallel test, using the preserved pass02 engine.
No target is called slice from a passing value. Refuses output overwrite.
"""
from pathlib import Path
import argparse, hashlib, json, os, resource, subprocess, sys, time
import sympy as S
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from geometry import oriented_components, zero_writhe, blackboard_parallel, best_order, sublink

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(31,32))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('target',choices=['K0','K1','D01'])
    ap.add_argument('parallel',type=int,choices=[1,2,3,4])
    ap.add_argument('--reverse',action='store_true')
    ap.add_argument('--tag',default='')
    a=ap.parse_args()
    label=f'{a.target}_p{a.parallel}'+('_reverse' if a.reverse else '')+a.tag
    out=HERE/'results'/label
    out.mkdir(exist_ok=False)
    source=HERE/('inputs/D01.json' if a.target=='D01' else 'inputs/targets.json')
    original=json.loads(source.read_text())[a.target]['pd']
    zero=zero_writhe(original)
    pd=blackboard_parallel(zero,a.parallel)
    info=oriented_components(pd)
    if info['components']!=a.parallel or info['writhe']!=0 or any(v for row in info['linking_matrix'] for v in row):
        raise RuntimeError('FAILED component/framing control')
    layout=best_order(pd,seeds=50)
    order=layout['order'][::-1] if a.reverse else layout['order']
    inp=f'{len(pd)} 0 0\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order))+'\n'
    (out/'diagram.json').write_text(json.dumps({'source_pd':original,'zero_writhe_pd':zero,'parallel_pd':pd,'order':order,'layout_search':layout,'linking_matrix':info['linking_matrix']},indent=2)+'\n')
    (out/'input.txt').write_text(inp)
    record={'target':a.target,'parallel':a.parallel,'status':'UNKNOWN','input_sha256':hashlib.sha256(inp.encode()).hexdigest(),'source_subset_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crossings':len(pd),'source_writhe':oriented_components(original)['writhe'],'max_frontier':layout['max_frontier'],'memory_cap_mib':2048,'timeout_seconds':30,'engine':'pass02 C++ checked 128-bit exact; overflow throws','counterexample_found':False}
    start=time.monotonic()
    with (out/'stderr.log').open('w') as log:
        try:
            cp=subprocess.run([str(HERE/'deps/jet_exact')],input=inp,text=True,stdout=subprocess.PIPE,stderr=log,timeout=30,preexec_fn=limits)
            (out/'stdout.txt').write_text(cp.stdout)
            if cp.returncode:record.update(status='ERROR_UNKNOWN',returncode=cp.returncode)
            else:
                raw=json.loads(cp.stdout);x=S.symbols('x');h=x*x+1
                poly=sum(S.Integer(c)*x**i for i,c in enumerate(raw['coefficients_x']))
                quotient,rem=S.div(poly,h**a.parallel,x)
                lead=S.rem(S.expand(quotient*(-x)**a.parallel),h,x)
                record.update(status='COMPUTED',raw=raw,exact_divisible=(rem==0),remainder=S.sstr(rem),root_quotient=[int(lead.coeff(x,0)),int(lead.coeff(x,1))],quotient_mod32=[int(lead.coeff(x,0))%32,int(lead.coeff(x,1))%32])
                if a.target=='K0' and a.parallel==2 and (rem!=0 or lead!=-23):raise RuntimeError('PRIOR e2 CONTROL FAILED')
        except subprocess.TimeoutExpired:record['status']='TIMEOUT_UNKNOWN'
    record['wall_seconds']=time.monotonic()-start
    (out/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
if __name__=='__main__':main()
