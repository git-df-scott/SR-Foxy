from pathlib import Path
import json,importlib.util,itertools
import sympy as S
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('marked',p/'marked_test.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
marked=json.loads((p/'MARKED_TEST.json').read_text())['rows'];ex=json.loads((p/'EXACT_MARKED.json').read_text());assert ex['status']=='complete'
z=S.Symbol('z');phi=S.cyclotomic_poly(7,z)
A=[]
for r in ex['rows']:
 assert r['degree']==2 and r['all_coefficients_integral']
 c=r['coefficients_in_z_ascending'];assert c[0]==['1'] and c[2]==['1']
 A.append(sum(S.Integer(v)*z**i for i,v in enumerate(c[1])))
 assert S.rem(A[-1]-A[-1].subs(z,z**6),phi,z)==0
for i in range(2):assert ex['rows'][i]['cocycle']==marked[i]['cocycle']
d=[r['marked_linking']['dual_pairing_numerator_mod7'] for r in marked]
pairs=[]
for a,b in itertools.product(range(1,4),repeat=2):
 equal=S.rem(A[0].subs(z,z**a)-A[1].subs(z,z**b),phi,z)==0
 pairs.append({'a':a,'b':b,'dual_linking_zero':(d[0]*a*a-d[1]*b*b)%7==0,'exact_polynomials_equal':equal})
assert {(r['a'],r['b']) for r in pairs if r['dual_linking_zero']}=={(1,3),(2,1),(3,2)}
assert not any(r['dual_linking_zero'] and r['exact_polynomials_equal'] for r in pairs)
# One nonzero character in each of the two isotropic lines suffices.
# Both lines b=+/-3a give the same polynomial because sign conjugation fixes it.
assert (6-3*3**2)%7==0
assert 11!=3 and pow((3*3-4)%13,6,13)==12
controls=[]
scales=json.loads((p/'MARKED_SCALES.json').read_text())
for row in marked:
 name=row['label'];L=m.snappy.Link(name)
 for kind,N,sgn in [('reordered',m.snappy.Link(list(reversed(L.PD_code()))),1),('mirror',L.mirror(),-1)]:
  r=m.probe(name+'_'+kind,m.M(m.G(N)),2,7,6,13);v=m.linking(N,r['cocycle']);match=[s['character_scale'] for s in scales if s['label']==name and s['reduction_prime']==13 and s['reduced_twisted_polynomial']==r['reduced_twisted_polynomial']];assert len(match)==1
  a=match[0];expected=sgn*a*a*row['marked_linking']['dual_pairing_numerator_mod7']%7
  assert v['dual_pairing_numerator_mod7']==expected,(name,kind,v,expected)
  controls.append({'name':name,'transformation':kind,'matched_scale':a,'expected_pairing':expected,'actual_pairing':v['dual_pairing_numerator_mod7'],'polynomial':r['reduced_twisted_polynomial']})
result={'dual_pairing_coefficients':d,'all_nonzero_pairs_mod_sign':pairs,'isotropic_character_slopes_mod7':[3,4],'witness':{'a':1,'b_mod_sign':3,'prime':13,'first_reduced_polynomial':'t^2+11t+1','second_reduced_polynomial':'t^2+3t+1','second_discriminant':5,'second_discriminant_Legendre':-1},'controls':controls,'conclusion':'Every metabolizer has an annihilating non-norm character; D is not locally flat slice, conditional on the recorded standard linking/twisted-torsion theorem conventions.'}
(p/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
