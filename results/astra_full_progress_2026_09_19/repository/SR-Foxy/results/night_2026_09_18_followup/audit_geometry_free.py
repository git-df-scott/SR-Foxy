"""Recompute the stored-PD nonribbon inputs; independent Fox Alexander control.

This is a computer-assisted check, not a proof of the PD-to-paper identification.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import resource
import signal
import spherogram
import sympy as s

resource.setrlimit(resource.RLIMIT_CPU,(90,95))
ROOT=Path(__file__).resolve().parents[2]
core={}
exec((ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py').read_text(),core)
t=s.symbols('t')
target=t**4-3*t**3+5*t**2-3*t+1
old=json.loads((ROOT/'results/opus_2026_09_19_0000_geometry_free_certificate/RESULTS.json').read_text())

def timeout(*args):
    raise TimeoutError('30 second per-knot audit cap')
signal.signal(signal.SIGALRM,timeout)

def normalize(expr):
    expr=s.expand(expr)
    assert expr!=0
    lo=min(int(a.as_powers_dict().get(t,0)) for a in s.Add.make_args(expr))
    P=s.Poly(s.expand(expr*t**(-lo)),t)
    assert all(c.is_Integer for c in P.all_coeffs())
    assert P.eval(1) in (-1,1)
    return s.expand(P.as_expr()*P.eval(1))

def fox_order(pd):
    A=core['adjacency_from_pd'](pd)
    q=core['quotient_R_wirtinger'](A)
    N=1+max(q['arcs'].values())
    rel=[[-sg*(b+1),i+1,sg*(b+1),-(o+1)] for i,o,b,sg,c in q['relations']]
    assert len(rel)==N and N<80
    M=[]
    for w in rel[:-1]:
        row=[0]*N
        p=0
        for x in w:
            row[abs(x)-1]+=(1 if x>0 else -1)*t**(p if x>0 else p-1)
            p+=1 if x>0 else -1
        assert p==0
        M.append([s.expand(v) for v in row[1:]])
    initial=len(M)
    while M:
        pivot=None
        for i,row in enumerate(M):
            for j,v in enumerate(row):
                c,e=v.as_coeff_exponent(t)
                if c in (1,-1) and e.is_Integer:
                    pivot=i,j,v
                    break
            if pivot:
                break
        if not pivot:
            break
        a,b,p=pivot
        M=[[s.expand(M[i][j]-M[i][b]*M[a][j]/p) for j in range(len(M)) if j!=b] for i in range(len(M)) if i!=a]
    assert len(M)<=10
    det=s.Matrix(M).det() if M else s.Integer(1)
    return normalize(det),{'initial_square':initial,'after_unit_pivots':len(M)}

data={}
for label,stem in [('K_0','AbeTagami_K_0_K_-1__6_3'),('K_1','AbeTagami_K_1')]:
    signal.alarm(30)
    path=ROOT/'data/knots'/f'{stem}.json'
    raw=path.read_bytes()
    pd=json.loads(raw)['pd_code']
    link=spherogram.Link(pd)
    assert len(link.link_components)==1
    h=link.knot_floer_homology(prime=2)
    ranks=h['ranks']
    assert all(type(A)==type(M)==type(r)==int and r>0 for (A,M),r in ranks.items())
    g=max(A for A,M in ranks)
    assert min(A for A,M in ranks)==-g and g==h['seifert_genus']==2
    top=sum(r for (A,M),r in ranks.items() if A==g)
    assert top==1
    assert all(ranks.get((-A,M-2*A))==r for (A,M),r in ranks.items())
    euler=normalize(sum((1 if M%2==0 else -1)*r*t**A for (A,M),r in ranks.items()))
    fox,size=fox_order(pd)
    assert euler==fox==target
    assert s.Poly(fox,t).is_irreducible
    mod2=s.Poly(fox,t,modulus=2)
    assert mod2.is_irreducible
    saved={f'{A},{M}':r for (A,M),r in sorted(ranks.items())}
    assert saved==old['data'][label]['ranks']
    data[label]={'input_sha256':hashlib.sha256(raw).hexdigest(),'crossings':len(pd),'ranks':saved,'top_rank':top,'genus_from_support':g,'fox_alexander':str(fox),'hfk_euler_alexander':str(euler),'fox_size':size,'irreducible_mod_2':True,'total_rank':sum(ranks.values()),'agrees_with_opus':True}
    signal.alarm(0)

assert data['K_0']['ranks']!=data['K_1']['ranks']
print(json.dumps({'status':'PASS_FOR_STORED_PD_KNOTS','counterexample':False,'data':data,'versions':{p:importlib.metadata.version(p) for p in ('spherogram','knot_floer_homology','sympy')},'scope':'Same HFK backend as Opus, independent exact Fox/Euler agreement; no PD-to-paper identification or slice disk certified'},indent=2))
