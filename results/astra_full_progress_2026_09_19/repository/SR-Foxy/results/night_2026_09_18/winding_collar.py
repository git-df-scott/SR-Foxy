"""Combine explicit winding-word model with all integer saved collar maps."""
from pathlib import Path
import sympy as s,json,resource
resource.setrlimit(resource.RLIMIT_CPU,(60,65))
p=Path(__file__).with_name('winding_trace.py');ns={'__file__':str(p)}
exec(compile(p.read_text().split('traces=[];words=[]')[0],str(p),'exec'),ns)
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})
n=s.symbols('n');H=s.eye(2)+n*N;Hi=s.eye(2)-n*N
lower=[4,9,10,11,12,13,14,15,16,17]
cn={j:mm(mm(H,m),Hi) if j-1 in lower else m for j,m in col.items()}
traces=[]
for row,v in zip(segments,[l+2,l]):
 seg=row['segments'];ix=[j for j,a in enumerate(seg) if a['side']=='lower'];a,b=min(ix),max(ix)
 pre=[c for q in seg[:a] for c in q['word']];low=[c for q in seg[a:b+1] for c in q['word']];post=[c for q in seg[b+1:] for c in q['word']]
 T=mm(mm(mm(mm(val(pre,cn),s.eye(2)+v*N),val(low,cn)),s.eye(2)-v*N),val(post,cn))
 traces.append(red(s.trace(T)))
diff=red(traces[0]-traces[1]);coeff=[s.expand(diff).coeff(z,i) for i in range(6)]
G=s.groebner(coeff,n,l)
mult=[s.sympify(v) for v in ['6175*l/80464 + 3295*n/40232 + 31459/80464','1749*l/40232 + 495*n/10058 + 1795/40232','3291*l/80464 - 1315*n/40232 + 17043/80464','-1749*l/20116 - 495*n/20116 - 11643/40232','1749*l/40232 + 3267/40232','0']]
assert s.expand(sum(a*b for a,b in zip(mult,coeff)))==1
print(json.dumps({'scope':'Algebraic q_n family and inserted-generator-5 windings only; no geometric collar identified','constraint':'k-l=2','coefficients_ascending_z':[str(v) for v in coeff],'groebner_lex_n_l':[str(p.as_expr()) for p in G.polys],'no_common_complex_zero':list(G)==[1],'bezout_multipliers':[str(v) for v in mult],'bezout_identity':'sum(multiplier_i * coefficient_i) = 1'},indent=2))
