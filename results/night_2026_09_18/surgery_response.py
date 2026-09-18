"""Exact two-slope Alexander presentation for the archived mixed-axis link.
No enumeration. Read the archived extractor, stopping before its numeric run.
"""
from pathlib import Path
import hashlib,json,signal,resource
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
resource.setrlimit(resource.RLIMIT_CPU,(90,95))
# macOS does not reliably implement RLIMIT_AS; this is a small sparse matrix job.
p=ROOT/'results/astra_2026_09_17_collar_boundary_audit/check_surgery_alexander.py'
src=p.read_text().split('out=[]\nfor n in [0,1]:')[0]
ns={'__file__':str(p)}
exec(compile(src,str(p),'exec'),ns)
t=ns['t']; x,y=sp.symbols('x y')
N=ns['N']; reference=ns['reference']; fox=ns['fox']
rr=[fox(w) for w in ns['rels']]
for comp,z in [(1,x),(2,y)]:
    row=[z*v for v in fox(ns['longs'][comp])]
    row[ns['meridians'][comp]-1]+=1
    rr.append(row)
M=[[sp.expand(v) for j,v in enumerate(row) if j!=reference-1] for row in rr]
shape=[len(M),len(M[0])]; pivots=[]
while M and M[0]:
    found=None
    for ai,row in enumerate(M):
        for bi,v in enumerate(row):
            c,e=v.as_coeff_exponent(t)
            if c in [1,-1] and e.is_Integer: found=(ai,bi,v);break
        if found:break
    if not found:break
    ai,bi,pivot=found;pivots.append(str(pivot))
    M=[[sp.expand(M[i][j]-M[i][bi]*M[ai][j]/pivot) for j in range(len(M[0])) if j!=bi] for i in range(len(M)) if i!=ai]
M=[row for row in M if any(v!=0 for v in row)]
print(json.dumps({'initial_shape':shape,'reduced_shape':[len(M),len(M[0])], 'matrix':[[str(v) for v in row] for row in M], 'pivot_count':len(pivots),'linking_sums':ns['linking']}),flush=True)
# All maximal minors, not an arbitrary chosen minor.
import itertools
minors=[]
for rows in itertools.combinations(range(len(M)),len(M[0])):
    d=sp.factor(sp.det(sp.Matrix([M[i] for i in rows])))
    minors.append(d)
cleared_minors=[sp.expand(v*t**6) for v in minors]
gcd=sp.factor(sp.gcd_list(cleared_minors))
Delta=t**4-3*t**3+5*t**2-3*t+1
expected=Delta**2+x*y*t**2*(t**2-1)**2
assert sp.expand(gcd-expected)==0
assert [sp.simplify(v/expected) for v in minors]==[0,0,-t**-6,t**-6,-t**-6,t**-6,-t**-5]
print(json.dumps({'maximal_minors':[str(v) for v in minors],'gcd':str(gcd),'opposite':str(sp.factor(gcd.subs(y,-x)))}),flush=True)
