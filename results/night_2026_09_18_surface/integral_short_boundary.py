"""Produce an integral Laurent 2-chain bounding the correction's lifted loop.

This certifies membership in G'' for the PRESENTED source/boundary groups,
not a geometrically embedded surface or disk.
"""
from pathlib import Path
import json
import resource
import sympy as s

resource.setrlimit(resource.RLIMIT_CPU,(60,65))
ROOT=Path(__file__).resolve().parents[2]
t=s.symbols('t')
C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
W=json.loads((ROOT/'results/night_2026_09_18/word_correction.json').read_text())
W['correction_boundary_word']=json.loads((ROOT/'results/night_2026_09_18_surface/short_boundary.json').read_text())['final_word']
core={}
exec((ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py').read_text(),core)
q=core['quotient_R_wirtinger'](core['adjacency_from_pd'](core['SCAFFOLD']))
boundary_rel=[[-sg*(b+1),i+1,sg*(b+1),-(o+1)] for i,o,b,sg,c in q['relations']]

def fox(w,N):
    row=[0]*N
    p=0
    for x in w:
        row[abs(x)-1]+=(1 if x>0 else -1)*t**(p if x>0 else p-1)
        p+=1 if x>0 else -1
    assert p==0
    return [s.expand(v) for v in row]

def integral_laurent(v):
    v=s.cancel(v)
    num,den=s.fraction(v)
    c,e=den.as_coeff_exponent(t)
    if c not in (1,-1) or not e.is_Integer:
        return False
    return all(term.as_coeff_Mul()[0].is_Integer for term in s.Add.make_args(s.expand(v)))

out=[]
for label,rels,word,N in [('source',C['source_relators'],W['correction_source_word'],9),('boundary',boundary_rel,W['correction_boundary_word'],18)]:
    original=[fox(w,N) for w in rels]
    M=[row[1:] for row in original]
    m=len(M)
    transform=[[s.Integer(i==j) for j in range(m)] for i in range(m)]
    target=fox(word,N)
    residual=target[1:]
    coeff=[s.Integer(0)]*m
    cols=list(range(N-1))
    rank=0
    for j in cols:
        a=next((i for i in range(rank,m) if M[i][j]!=0 and M[i][j].as_coeff_exponent(t)[0] in (1,-1) and M[i][j].as_coeff_exponent(t)[1].is_Integer),None)
        if a is None:
            continue
        M[rank],M[a]=M[a],M[rank]
        transform[rank],transform[a]=transform[a],transform[rank]
        pivot=M[rank][j]
        M[rank]=[s.expand(v/pivot) for v in M[rank]]
        transform[rank]=[s.expand(v/pivot) for v in transform[rank]]
        u=residual[j]
        residual=[s.expand(v-u*w) for v,w in zip(residual,M[rank])]
        coeff=[s.expand(v+u*w) for v,w in zip(coeff,transform[rank])]
        for i in range(rank+1,m):
            u=M[i][j]
            M[i]=[s.expand(v-u*w) for v,w in zip(M[i],M[rank])]
            transform[i]=[s.expand(v-u*w) for v,w in zip(transform[i],transform[rank])]
        rank+=1
    # A small exact rational solve nominates the remaining coefficients;
    # integrality and the entire unreduced Fox identity are checked below.
    tail=s.Matrix(M[rank:]).T
    sol,params=tail.gauss_jordan_solve(s.Matrix(residual))
    sol=sol.subs({p:0 for p in params})
    coeff=[s.cancel(v+sum(sol[i]*transform[rank+i][j] for i in range(len(sol)))) for j,v in enumerate(coeff)]
    assert all(integral_laurent(v) for v in coeff)
    assert all(s.expand(target[j]-sum(coeff[i]*original[i][j] for i in range(m)))==0 for j in range(N))
    out.append({'group':label,'generators':N,'unit_pivots':rank,'remaining_matrix_shape':[len(M)-rank,N-1],'relators':rels,'correction_word':word,'integral_Laurent_coefficients':[str(v) for v in coeff],'all_full_Fox_columns_verified':True,'membership':'correction lies in second derived subgroup of this presented group','geometric_disk':False})
print(json.dumps(out,indent=2))
