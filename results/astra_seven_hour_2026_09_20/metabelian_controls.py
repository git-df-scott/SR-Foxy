"""Independent published polynomial comparison and ribbon controls."""
import json,snappy
from pathlib import Path
from flint import fq_default_ctx,fq_default_poly_ctx
from metabelian_probe import probe
p=Path(__file__).resolve().parent;out=p/'METABELIAN_CONTROLS.json';assert not out.exists()
r=probe('K12n224_published',snappy.Manifold('K12n224'),3,7,4,13)
# Parse via recomputation using polynomial coefficients supplied by FLINT.
# The source uses a particular cocycle and primitive root. Compare all Galois
# conjugates; scalar cocycle changes permute the six nontrivial characters.
F=fq_default_ctx(13,2,'u');R=fq_default_poly_ctx(F);z=(F.gen())**24
assert z**7==1 and z!=1
# Safe evaluation of our generated FLINT polynomial string in its own field.
# No external or repository text is evaluated here.
actual=eval(r['reduced_twisted_polynomial'].replace('^','**'),{'__builtins__':{}},{'x':R.gen(),'u':R([F.gen()])}).monic()
options=[]
for k in range(1,7):
 w=z**k;A=-4*w**4-4*w**2-4*w
 options.append(R([1,-A-1,6,A-5,1]).monic())
assert actual in options or R(list(reversed(actual.coeffs()))).monic() in options,'Published exact polynomial reduction mismatch'
r['matches_published_polynomial_up_to_Galois_and_reversal']=True
controls=[r]
for knot,q,ell in [('6_1',3,5),('8_8',5,19)]:
 r=probe(knot,snappy.Link(knot).exterior(),2,q,q-1,ell)
 assert not r['not_norm_mod_reduction'],'Known ribbon control rejected'
 controls.append(r)
out.write_text(json.dumps({'controls':controls,'scope':'Two known ribbon controls plus explicit HKL Section10.6 polynomial, as recorded in SnapPy3.3.2 rep_theory.py. Finite-field arithmetic, no sliceness claim on a passing target.'},indent=2)+'\n')
print([(r['label'],r['not_norm_mod_reduction'],r.get('matches_published_polynomial_up_to_Galois_and_reversal')) for r in controls])
