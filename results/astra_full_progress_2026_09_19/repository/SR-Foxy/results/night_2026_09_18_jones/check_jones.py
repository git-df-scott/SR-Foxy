#!/usr/bin/env python3
"""Bounded exact state sums for the committed K0 and K1 PDs; no Sage/SnapPy.

<D> = sum_s A^(n-2b(s)) (-A^2-A^-2)^(circles(s)-1).
F_D(A)=(-A^3)^(-w(D)) <D>; V_D(t)=F_D(A), t=A^-4.
Every integer coefficient is accumulated with Python arbitrary-precision ints.
The C helper only counts <=2^20 states and does not do polynomial arithmetic.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib, json, math, platform, resource, subprocess, time
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
CHECKS=[]
def check(name, value):
    CHECKS.append({'name':name,'pass':bool(value)})
    if not value: raise AssertionError(name)

def normalized_pd(pd):
    labels=sorted({x for q in pd for x in q})
    assert len(labels)==2*len(pd)
    index={x:i for i,x in enumerate(labels)}
    pd=[[index[x] for x in q] for q in pd]
    assert all(len(q)==4 for q in pd)
    assert Counter(x for q in pd for x in q)==Counter({x:2 for x in range(2*len(pd))})
    return pd

def writhe_and_components(pd):
    """Orient by opposite ports, independent of numerical arc-label ordering.
    Spherogram: under ports 0,2; sign + for incoming ports (0,3) or (2,1).
    All computations here concern knots, so reversing the seed has no effect.
    """
    if not pd: return 0,1
    ends=defaultdict(list)
    for i,q in enumerate(pd):
        for p,x in enumerate(q): ends[x].append((i,p))
    assert all(len(v)==2 for v in ends.values())
    incoming=set(); visited=set(); components=0
    for i in range(len(pd)):
        for p in range(4):
            if (i,p) in visited: continue
            components+=1; start=(i,p); cur=start
            while cur not in visited:
                j,k=cur; out=(j,(k+2)%4)
                incoming.add(cur); visited.update((cur,out))
                pair=ends[pd[out[0]][out[1]]]
                cur=pair[1] if pair[0]==out else pair[0]
            assert cur==start
    signs=[]
    for i in range(len(pd)):
        u=0 if (i,0) in incoming else 2
        o=1 if (i,1) in incoming else 3
        signs.append(1 if (u,o) in ((0,3),(2,1)) else -1)
    return sum(signs),components

def histogram_c(pd, binary):
    if not pd: return {(0,1):1}
    assert len(pd)<=20
    text=str(len(pd))+'\n'+'\n'.join(' '.join(map(str,q)) for q in pd)+'\n'
    def limits(): resource.setrlimit(resource.RLIMIT_CPU,(15,15))
    proc=subprocess.run([str(binary)],input=text,text=True,capture_output=True,
                        timeout=20,check=True,preexec_fn=limits)
    h={}
    for line in proc.stdout.splitlines():
        b,l,count=map(int,line.split()); h[b,l]=count
    assert sum(h.values())==2**len(pd)
    return h

def histogram_reference(pd):
    """Independent small-case implementation: 4n port graph, DFS components.
    Unlike C's label-DSU implementation, explicitly retain every half-edge.
    """
    if not pd: return {(0,1):1}
    assert len(pd)<=8
    ends=defaultdict(list)
    for i,q in enumerate(pd):
        for p,x in enumerate(q): ends[x].append(4*i+p)
    hist=Counter()
    for state in range(1<<len(pd)):
        adj=[[] for _ in range(4*len(pd))]
        def edge(a,b): adj[a].append(b); adj[b].append(a)
        for a,b in ends.values(): edge(a,b)
        for i in range(len(pd)):
            pairs=((0,3),(1,2)) if state>>i&1 else ((0,1),(2,3))
            for a,b in pairs: edge(4*i+a,4*i+b)
        seen=set(); circles=0
        for p in range(len(adj)):
            if p in seen: continue
            circles+=1; stack=[p]; seen.add(p)
            while stack:
                for q in adj[stack.pop()]:
                    if q not in seen: seen.add(q); stack.append(q)
        hist[state.bit_count(),circles]+=1
    return dict(hist)

def bracket(n,hist):
    result=Counter()
    for (b,l),count in hist.items():
        k=l-1
        for j in range(k+1):
            exp=n-2*b+2*k-4*j
            result[exp]+=count*((-1)**k)*math.comb(k,j)
    return {e:c for e,c in sorted(result.items()) if c}

def normalize(poly,w):
    return {e-3*w:(-1 if w%2 else 1)*c for e,c in poly.items()}
def mirror(poly): return dict(sorted((-e,c) for e,c in poly.items()))
def evaluate(poly,a=2,p=1000000007):
    return sum(c*pow(a,e,p) for e,c in poly.items())%p
def compute(pd,binary):
    pd=normalized_pd(pd); w,components=writhe_and_components(pd)
    assert components==1
    h=histogram_c(pd,binary); br=bracket(len(pd),h); f=normalize(br,w)
    assert all(e%4==0 for e in f)
    return {'pd':pd,'crossings':len(pd),'states':2**len(pd),'components':components,
            'writhe':w,'bracket_A':br,'normalized_A':f,
            'Jones_t':dict(sorted((-e//4,c) for e,c in f.items())),
            'at_A2_mod_1000000007':evaluate(f),
            'mirror_at_A2_mod_1000000007':evaluate(mirror(f)),
            'state_histogram':[[b,l,c] for (b,l),c in sorted(h.items())]}

def main():
    started=time.monotonic(); binary=HERE/'state_histogram'
    compile_cmd=['cc','-std=c11','-O2','-Wall','-Wextra',str(HERE/'state_histogram.c'),'-o',str(binary)]
    subprocess.run(compile_cmd,check=True,timeout=20)
    examples={
        'unknot':[],
        'positive_RI':[[0,0,1,1]],
        'negative_RI':[[0,1,1,0]],
        'negative_trefoil':[[0,3,1,4],[2,5,3,0],[4,1,5,2]],
        'figure_eight':[[8,3,1,4],[2,6,3,5],[6,2,7,1],[4,7,5,8]],
    }
    controls={name:compute(pd,binary) for name,pd in examples.items()}
    for name,item in controls.items():
        check(name+' independent state histogram',histogram_c(item['pd'],binary)==histogram_reference(item['pd']))
    for name in ['unknot','positive_RI','negative_RI']:
        check(name+' normalized polynomial is 1',controls[name]['normalized_A']=={0:1})
    check('positive RI bracket and writhe',controls['positive_RI']['bracket_A']=={3:-1} and controls['positive_RI']['writhe']==1)
    check('negative RI bracket and writhe',controls['negative_RI']['bracket_A']=={-3:-1} and controls['negative_RI']['writhe']==-1)
    check('negative trefoil conventional Jones',controls['negative_trefoil']['Jones_t']=={-4:-1,-3:1,-1:1})
    check('figure eight conventional Jones',controls['figure_eight']['Jones_t']=={-2:1,-1:-1,0:1,1:-1,2:1})
    # A one-port cyclic rotation swaps over/under and both smoothing types.
    for name,pd in examples.items():
        mirrored=compute([q[1:]+q[:1] for q in pd],binary)
        check(name+' explicit mirrored PD',mirrored['normalized_A']==mirror(controls[name]['normalized_A']))
    inputs={}; results={}
    for name,filename in [('K0','AbeTagami_K_0_K_-1__6_3.json'),('K1','AbeTagami_K_1.json')]:
        path=REPO/'data'/'knots'/filename; raw=path.read_bytes(); data=json.loads(raw)
        inputs[name]={'relative_source':str(path.relative_to(REPO)),
                      'sha256':hashlib.sha256(raw).hexdigest(),'pd_code':data['pd_code']}
        results[name]=compute(data['pd_code'],binary)
        check(name+' V(1)=1',sum(results[name]['Jones_t'].values())==1)
        check(name+' derivative V prime(1)=0',sum(e*c for e,c in results[name]['Jones_t'].items())==0)
        check(name+' |V(-1)|=13 determinant control',abs(sum((-1 if e%2 else 1)*c for e,c in results[name]['Jones_t'].items()))==13)
    check('K0 independent Python histogram',histogram_reference(results['K0']['pd'])==histogram_c(results['K0']['pd'],binary))
    check('K0 distinct from K1',results['K0']['normalized_A']!=results['K1']['normalized_A'])
    check('K0 distinct from mirror K1',results['K0']['normalized_A']!=mirror(results['K1']['normalized_A']))
    check('K1 distinct from its mirror',results['K1']['normalized_A']!=mirror(results['K1']['normalized_A']))
    check('modular witness K0 vs K1',results['K0']['at_A2_mod_1000000007']!=results['K1']['at_A2_mod_1000000007'])
    check('modular witness K0 vs mirror K1',results['K0']['at_A2_mod_1000000007']!=results['K1']['mirror_at_A2_mod_1000000007'])
    out={'all_checks_pass':all(x['pass'] for x in CHECKS),'checks':CHECKS,
         'inputs':inputs,'controls':controls,'results':results,
         'elapsed_seconds':time.monotonic()-started,'compile_command':compile_cmd,
         'run_utc':datetime.now(timezone.utc).isoformat(),'python_version':platform.python_version(),
         'compiler_version':subprocess.check_output(['cc','--version'],text=True).splitlines()[0],
         'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ['check_jones.py','state_histogram.c']},
         'conventions':'A smoothing (0,1)(2,3); B smoothing (0,3)(1,2); delta=-A^2-A^-2; F=(-A^3)^(-w)<D>; t=A^-4',
         'limits':'C rejects >20 crossings; 15 CPU seconds / 20 wall seconds per state sum; only stored K0/K1 plus <=6-crossing controls.',
         'scope':'Exact Jones polynomials of stored PD diagrams. Does not identify those PDs with paper figures, establish sliceness, or establish concordance.'}
    (HERE/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
    (HERE/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':out['all_checks_pass'],'checks':len(CHECKS),'elapsed_seconds':out['elapsed_seconds'],
                      'results':{k:{a:v for a,v in r.items() if a in ['writhe','Jones_t','at_A2_mod_1000000007','mirror_at_A2_mod_1000000007']} for k,r in results.items()}},indent=2))

if __name__=='__main__': main()
