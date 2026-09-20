"""Enumerate every isotropic order-27 subgroup, independently of the proof.

H=Z9 x Z3 x Z3 x Z9; linking numerator xA*yA-3*xB*yB+3*xC*yC-xD*yD mod9.
Check each metabolizer has an annihilating order-three character a!=0,b=0.
Includes a 90-second bound; an exception does not establish completeness.
"""
from itertools import product
from pathlib import Path
import json, time, signal

p=Path(__file__).resolve().parent
assert not (p/'METABOLIZERS.json').exists(), 'Preserve completed output'
def limit(*_): raise TimeoutError('90 second enumeration limit')
signal.signal(signal.SIGALRM,limit);signal.alarm(90)
start=time.monotonic()
mods=(9,3,3,9)
elems=list(product(*(range(m) for m in mods)))
idx={v:i for i,v in enumerate(elems)}
zero=idx[(0,0,0,0)]
def add(i,j):return idx[tuple((a+b)%m for a,b,m in zip(elems[i],elems[j],mods))]
def pair(i,j):
    a,b,c,d=elems[i];A,B,C,D=elems[j]
    return (a*A-3*b*B+3*c*C-d*D)%9
isotropic=[i for i in range(len(elems)) if pair(i,i)==0]
cyclic={}
for g in isotropic:
    row=[zero];x=g
    while x!=zero:row.append(x);x=add(x,g)
    cyclic[g]=row
seen={frozenset([zero])};queue=list(seen);met=[]
for V in queue:
    if len(V)==27:
        met.append(V);continue
    for g in isotropic:
        if g in V or any(pair(g,h) for h in V):continue
        W=frozenset(add(h,k) for h in V for k in cyclic[g])
        assert len(W)<=27, 'Isotropic subgroup larger than square root'
        if W not in seen:seen.add(W);queue.append(W)
characters=list(product(range(3),repeat=4))
def evaluates(char,h):return sum(a*b for a,b in zip(char,elems[h]))%3
records=[]
for V in sorted(met,key=lambda v:sorted(v)):
    assert len(V)==27 and all(pair(x,y)==0 for x in V for y in V)
    witnesses=[ch for ch in characters if ch[0]!=0 and ch[1]==0 and all(evaluates(ch,h)==0 for h in V)]
    assert witnesses, 'Counterexample to proposed all-metabolizer lemma'
    records.append({'elements':[elems[h] for h in sorted(V)],'witnesses':witnesses})
assert records
signal.alarm(0)
r={'complete':True,'group_moduli':mods,'linking_numerator_diagonal':[1,-3,3,-1],
   'linking_denominator':9,'group_order':len(elems),'metabolizer_order':27,
   'isotropic_subgroups_by_order':{str(n):sum(len(V)==n for V in seen) for n in (1,3,9,27)},
   'metabolizer_count':len(records),'all_have_a_nonzero_b_zero_witness':True,
   'metabolizers':records,'seconds':time.monotonic()-start,
   'scope':'Finite algebra check only. The topological obstruction additionally requires the source formulas and discriminant argument.'}
(p/'METABOLIZERS.json').write_text(json.dumps(r,indent=2)+'\n')
print({k:v for k,v in r.items() if k!='metabolizers'})
