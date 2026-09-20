"""Check the empirical mod16 relation with signed knot determinants."""
import json,collections,math
from pathlib import Path
p=Path(__file__).parent;rows=json.loads((p/'sources/teeth_rows.json').read_text());counts=collections.Counter();fail=[]
for r in rows:
 product=math.prod(d if d%4==1 else -d for d in r['dets']);residue=(r['det_V']-product)%16;counts[residue]+=1
 if residue:fail.append({**r,'signed_product':product,'difference_mod16':residue})
out={'population':len(rows),'signed_difference_counts_mod16':dict(counts),'counterexamples':fail,'normalization':'The symmetrized Alexander polynomial normalized by Delta(1)=1 has Delta(-1)=1 mod4. Thus signed Jones knot determinant is +D if D=1 mod4 and -D if D=3 mod4, where D is positive determinant.','scope':'Finite census evidence, not a universal theorem.'}
(p/'SIGNED_MOD16_SCREEN_REPRODUCED.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
