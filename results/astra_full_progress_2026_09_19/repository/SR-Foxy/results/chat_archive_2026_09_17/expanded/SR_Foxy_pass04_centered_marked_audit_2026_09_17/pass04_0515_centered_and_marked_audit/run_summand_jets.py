#!/usr/bin/env python3
"""One resource-bounded exact PD cable evaluation, using prior audited engine.
This is not independent knot identification; input diagrams are upstream data.
"""
import argparse, hashlib, json, resource, subprocess, sys, time
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'upstream/dependencies/pass02'))
from geometry import blackboard_parallel, zero_writhe, oriented_components, best_order, sublink, occurrences

def canonical_labels(pd):
    labels={}
    return [[labels.setdefault(e,len(labels)) for e in c] for c in pd]

def euler(pd):
    across={}
    for a,b in occurrences(pd).values():across[a]=b;across[b]=a
    left=set(across);faces=0
    while left:
        x=next(iter(left));start=x
        while x in left:
            left.remove(x);i,j=across[x];x=(i,(j+1)%4)
        if x!=start: raise ValueError('Bad face orbit')
        faces+=1
    return -len(pd)+faces

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('knot',choices=['K0','K1','D01']);ap.add_argument('parallel',type=int,choices=[1,2,3,4])
    ap.add_argument('output',type=Path);ap.add_argument('--timeout',type=int,default=30)
    ap.add_argument('--reverse',action='store_true');ap.add_argument('--seeds',type=int,default=24)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    data=json.loads((HERE/'inputs.json').read_text());base=data[args.knot]['pd'];zero=zero_writhe(base)
    pd=blackboard_parallel(zero,args.parallel);meta=oriented_components(pd)
    if meta['components']!=args.parallel or meta['writhe'] or any(v for row in meta['linking_matrix'] for v in row):
        raise ValueError('Component/writhe/linking check failed')
    if euler(pd)!=2:raise ValueError('Nonplanar rotation system')
    for i in range(args.parallel):
        if canonical_labels(sublink(pd,{i}))!=canonical_labels(zero):raise ValueError('Component PD does not reduce to source')
    order=best_order(pd,args.seeds)
    if args.reverse:order['order'].reverse()
    text=f'{len(pd)} 0 0\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order['order']))+'\n'
    (args.output/'input.txt').write_text(text)
    record={'knot':args.knot,'parallel':args.parallel,'status':'UNKNOWN','counterexample':False,'order':order,'crossings':len(pd),'components':meta['components'],'writhe':0,'linking_matrix':meta['linking_matrix'],'planar_euler':2,'all_components_equal_zero_writhe_source_pd':True,'input_sha256':hashlib.sha256(text.encode()).hexdigest(),'arithmetic':'arbitrary-precision cpp_int','timeout_seconds':args.timeout,'memory_bytes':2*1024**3}
    (args.output/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    def limit():
        resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    start=time.monotonic()
    with (args.output/'stderr.log').open('w') as err:
        try:
            p=subprocess.run([str(HERE/'jet_exact')],input=text,text=True,stdout=subprocess.PIPE,stderr=err,preexec_fn=limit,timeout=args.timeout)
            (args.output/'stdout.txt').write_text(p.stdout)
            if p.returncode:record.update(status='ERROR_UNKNOWN',exit_code=p.returncode)
            else:
                raw=json.loads(p.stdout);x=s.symbols('x');h=x*x+1
                polynomial=sum(s.Integer(v)*x**i for i,v in enumerate(raw['coefficients_x']))
                quotient,remainder=s.div(polynomial,h**args.parallel,x)
                value=s.rem(s.expand(quotient*(-x)**args.parallel),h,x)
                record.update(status='COMPUTED',raw=raw,exact_divisible=remainder==0,exact_remainder=str(remainder),e_value=[int(value.coeff(x,0)),int(value.coeff(x,1))])
                record['e_mod32']=[v%32 for v in record['e_value']]
        except subprocess.TimeoutExpired:record['status']='TIMEOUT_UNKNOWN'
    record['wall_seconds']=time.monotonic()-start
    (args.output/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='order'},indent=2))
if __name__=='__main__':main()
