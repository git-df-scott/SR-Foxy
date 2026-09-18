"""Algebraic meridian-winding family; no claim of a drawn band/actual collar."""
from pathlib import Path
import sympy as s,json,resource
resource.setrlimit(resource.RLIMIT_CPU,(60,65))
ROOT=Path(__file__).resolve().parents[2];z,k,l=s.symbols('z k l');R=z**6+3*z**5+5*z**4+4*z**3+2*z**2+z+1
C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
red=lambda a:s.rem(s.expand(a),R,z)
def mm(a,b):return (a*b).applyfunc(red)
def inv(a):return s.Matrix([[a[1,1],-a[0,1]],[-a[1,0],a[0,0]]])
source={int(i):s.Matrix(2,2,[sum(c*z**j for j,c in enumerate(p)) for p in v]) for i,v in C['source_matrices'].items()}
def val(w,img):
 a=s.eye(2)
 for x in w:a=mm(a,img[x] if x>0 else inv(img[-x]))
 return a
for w in C['source_relators']:assert val(w,source)==s.eye(2)
col={int(i)+1:val(w,source) for i,w in C['boundary_arc_images'].items()}
mu=col[5];N=mu-s.eye(2);assert mm(N,N)==s.zeros(2)
segments=[json.loads(line) for line in (ROOT/'results/night_2026_09_18/axis_segments.jsonl').read_text().splitlines()]
traces=[];words=[]
for row,v in zip(segments,[k,l]):
 seg=row['segments'];ix=[j for j,a in enumerate(seg) if a['side']=='lower'];a,b=min(ix),max(ix)
 assert all(x['side']=='lower' for x in seg[a:b+1])
 pre=[c for q in seg[:a] for c in q['word']];low=[c for q in seg[a:b+1] for c in q['word']];post=[c for q in seg[b+1:] for c in q['word']]
 assert sum(1 if c>0 else -1 for c in low)==0
 T=mm(mm(mm(mm(val(pre,col),s.eye(2)+v*N),val(low,col)),s.eye(2)-v*N),val(post,col))
 traces.append(red(s.trace(T)));words.append({'prefix':pre,'lower':low,'suffix':post,'inserted_meridian_generator':5})
diff=red(traces[0]-traces[1]);assert diff.subs({k:0,l:0})==0
restricted=s.expand(diff.subs(k,l+2));coeff=[s.expand(restricted).coeff(z,i) for i in range(6)]
gcd=s.gcd_list(coeff)
print(json.dumps({'status':'ALGEBRAIC_WORD_FAMILY_ONLY_Q0_NOT_GEOMETRICALLY_IDENTIFIED','word_segments':words,'trace_difference':str(diff),'dependence_line':'k-l=2','restricted_coefficients_ascending_z':[str(c) for c in coeff],'gcd_in_Q_l':str(gcd),'has_common_complex_root':bool(s.degree(gcd,l)>0),'trace_at_zero_agrees':True},indent=2))
