import json, subprocess, sys, time, resource
from pathlib import Path
from geometry import oriented_components, best_order
P=Path(__file__).parent

def classify(raw,p):
    import sympy as S
    x=S.symbols('x');pol=sum(S.Integer(c)*x**i for i,c in enumerate(raw['coefficients_x']))
    quotient,remainder=S.div(pol,(x*x+1)**p,x)
    qroot=S.rem(S.expand(quotient*(-x)**p),(x*x+1),x) # delta=-(x^2+1)/x
    # Multiplication by (-x)^p converts h-quotient to delta-quotient.
    a=int(qroot.coeff(x,0));b=int(qroot.coeff(x,1))
    rc=[int(remainder.coeff(x,i)) for i in range(2*p)]
    mod=raw['modulus'];exact=mod is None
    return {'exact':exact,'divisibility_remainder':rc,'exact_divisible':not any(rc) if exact else None,'quotient_at_x_i':[a,b] if exact and not any(rc) else None,'quotient_at_x_i_mod32':[a%32,b%32],'remainder_mod32':[c%32 for c in rc]}

def run(name,exact=False,timeout=240):
    obj=json.loads((P/(name+'.json')).read_text());pd=obj['pd'];w=obj['writhe'];order=obj['order']
    inp=f'{len(pd)} {w} 0\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order))+'\n'
    mode='exact' if exact else 'mod32';out=P/(name+'.'+mode+'.json');log=P/(name+'.'+mode+'.log');ip=P/(name+'.input.txt')
    if out.exists():raise FileExistsError(out)
    if not ip.exists():ip.write_text(inp)
    def limits():resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
    start=time.monotonic()
    with log.open('w') as err:
        try:
            result=subprocess.run([str(P/('frontier_exact' if exact else 'frontier_mod32'))],input=inp,text=True,capture_output=False,stdout=subprocess.PIPE,stderr=err,timeout=timeout,preexec_fn=limits)
            if result.returncode!=0:record={'status':'ERROR_UNKNOWN','exit_code':result.returncode,'log':log.name}
            else:
                raw=json.loads(result.stdout);record={'status':'COMPUTED','raw':raw,'evaluation':classify(raw,obj['p'])}
        except subprocess.TimeoutExpired:record={'status':'TIMEOUT_UNKNOWN'}
    record['wall_seconds']=time.monotonic()-start;record['input_file']=ip.name;record['memory_cap_mib']=3072;record['timeout_seconds']=timeout
    out.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
    return record
if __name__=='__main__':run(sys.argv[1], '--exact' in sys.argv, int(sys.argv[sys.argv.index('--timeout')+1]) if '--timeout' in sys.argv else 240)
