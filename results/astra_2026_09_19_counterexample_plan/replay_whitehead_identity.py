"""Compare oriented connected-sum factors; isolate the invertible 6_3 reversal."""
import json,random
from pathlib import Path
from spherogram import Link
import regina
P=Path(__file__).parent;random.seed(20260919)
def reg(L):return regina.Link.fromPD([[a+1 for a in q] for q in L.PD_code()])
def factors(pd):
 rows=[]
 for f in Link(pd).deconnect_sum():
  f.simplify('basic')
  if not f.crossings:continue
  r=reg(f)
  if r.size()==7:r.simplifyExhaustive(1)
  rows.append({'crossings':r.size(),'unoriented_sig':r.sig(False,True,True),'oriented_sig':r.sig(False,False,True),'pd':r.pdData()})
 return rows
movie=json.loads((P/'WHITEHEAD_SPLIT_MOVIE.json').read_text())
target=json.loads((P/'whitehead_TARGETS.json').read_text())['T']['pd']
a=factors(movie['result_pd']);b=factors(target)
assert sorted(x['unoriented_sig'] for x in a)==sorted(x['unoriented_sig'] for x in b)
small=reg(Link('6_3')).sig(False,True,True)
for x in a:
 y=next(z for z in b if z['unoriented_sig']==x['unoriented_sig'])
 assert x['oriented_sig']==y['oriented_sig'] or x['unoriented_sig']==small
out={'status':'PASS','output_factors':a,'target_factors':b,'reflection_allowed':False,'rotation_allowed':True,'orientation_note':'Only possible oriented-factor mismatch is exact 6_3 diagram. Use established invertibility of 6_3 to reverse that summand; this is not the square knot.','scope':'Uses Spherogram connected-sum decomposition and Regina simplification. The factor simplification is not recorded as an elementary movie.'}
(P/'WHITEHEAD_IDENTITY_REPLAY.json').write_text(json.dumps(out,indent=2))
print('PASS: exact factor matches; only 6_3 orientation reversal requires invertibility.')
