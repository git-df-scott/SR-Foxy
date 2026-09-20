"""Exact-to-reduction audit and explicit non-norm witness for all81 pairs."""
from pathlib import Path
import json,hashlib
import snappy,sympy as S
from flint import fq_default_ctx,fq_default_poly_ctx
root=Path(__file__).resolve().parent;old=root.parent/'astra_seven_hour_2026_09_20'
exact=json.loads((old/'EXACT_SMALL_DIFFERENCE_v2.json').read_text())['rows']
raw=json.loads((old/'SMALL_DIFFERENCE_SCREEN.json').read_text())
out=root/'SMALL_DIFFERENCE_AUDIT.json';assert not out.exists()
rows=[];witnesses={};allpairs={(a,b) for a in range(1,10) for b in range(1,10)}
for rd in raw['rounds']:
 ell=rd['ell'];assert S.isprime(ell) and ell%19==18
 F=fq_default_ctx(ell,2,'u');R=fq_default_poly_ctx(F)
 def bar(f):return R([c**ell for c in reversed(f.coeffs())]).monic()
 def parse(s):return eval(s.replace('^','**'),{'__builtins__':{}},{'x':R.gen(),'u':R([F.gen()])}).monic()
 pols=[]
 for ki in range(2):
  er=exact[ki];assert er['degree']==2 and er['all_coefficients_integral']
  es=er['coefficients_in_z_ascending'];assert es[0]==es[2]==['1']
  vals=[]
  for r in rd['records'][ki]:
   scale=r['character_scale']
   z=eval(r['root'].replace('^','**'),{'__builtins__':{}},{'u':F.gen()})
   assert z**19==1 and z!=1 and z**ell==z**-1
   reconstructed=R([sum((F(int(c))*z**(scale*j) for j,c in enumerate(cs)),F(0)) for cs in es])
   actual=parse(r['reduced_twisted_polynomial'])
   matches=[k for k in range(1,10) if R([sum((F(int(c))*z**(k*j) for j,c in enumerate(cs)),F(0)) for cs in es])==actual]
   assert matches,'Exact Galois orbit fails to match modular polynomial'
   assert bar(reconstructed)==reconstructed
   vals.append(reconstructed);rows.append({'ell':ell,'knot':er['label'],'modular_scale':scale,'matching_exact_scales':matches})
  pols.append(vals)
 for a,b in sorted(allpairs-set(witnesses)):
  product=pols[0][a-1]*pols[1][b-1];fs=list(product.factor()[1])
  for f,m in fs:
   fb=bar(f);other=next((n for h,n in fs if h==fb),0)
   if (f==fb and m%2) or m!=other:
    witnesses[(a,b)]={'pair':[a,b],'ell':ell,'product':str(product),'bad_factor':str(f),'multiplicity':m,'conjugate_factor':str(fb),'conjugate_multiplicity':other};break
assert set(witnesses)==allpairs
hom=[]
for name in ('K7a2','K10n4'):
 M=snappy.Link(name).exterior();tors=[int(x) for x in M.covers(2,cover_type='cyclic')[0].homology().elementary_divisors() if x]
 assert tors==[19];hom.append({'knot':name,'double_cover_H1':[19]})
# Characteristic-zero conjugation invariance makes independent signs redundant.
z=S.Symbol('z');phi=S.Poly(sum(z**j for j in range(19)),z)
for row in exact:
 for cs in row['coefficients_in_z_ascending']:
  f=sum(int(c)*z**j for j,c in enumerate(cs));g=sum(int(c)*z**((-j)%19) for j,c in enumerate(cs))
  assert S.rem(f-g,phi.as_expr(),z)==0
result={'exact_reduction_checks':len(rows),'all81_pairs_excluded':True,'pair_witnesses':[witnesses[k] for k in sorted(witnesses)],'homology':hom,'checks':rows,'conjugation_invariance_exact':True,'source_hashes':{f:hashlib.sha256((old/f).read_bytes()).hexdigest() for f in ('EXACT_SMALL_DIFFERENCE_v2.json','SMALL_DIFFERENCE_SCREEN.json')},'scope':'Arithmetic certificate. The report supplies the norm-specialization, connected-sum and metabolizer argument; independent mathematical review remains appropriate.'}
out.write_text(json.dumps(result,indent=2)+'\n');print({'exact_reduction_checks':len(rows),'pair_witnesses':len(witnesses),'double_cover_groups':hom})
