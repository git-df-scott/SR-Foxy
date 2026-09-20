"""Falsify sliceness of the census Jones violators; retain deficient ranks as unknown."""
import json,sys,snappy
from pathlib import Path
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from colored_link_rank import fox_matrix,rank_minor
rows=json.loads((p/'sources/teeth_rows.json').read_text());out=[]
for r in rows:
 ps=1
 for d in r['dets']:ps*=d if d%4==1 else -d
 if (r['det_V']-ps)%32==0:continue
 name=r['name'].split('(')[0];L=snappy.Link(name);checks=[]
 for vals,prime in [([2,2],101),([3,3],103),([2,3],107)]:
  mat,colors=fox_matrix(L,vals,prime);a=rank_minor(mat,len(colors),prime);a.update(component_values=vals,prime=prime);checks.append(a)
  if a['maximal_minor_nonzero']:break
 out.append({**r,'signed_product':ps,'checks':checks,'classical_rank_obstruction_found':any(a['maximal_minor_nonzero'] for a in checks)})
result={'population':len(rows),'signed_violators':len(out),'classically_rejected':sum(x['classical_rank_obstruction_found'] for x in out),'survivors':[x for x in out if not x['classical_rank_obstruction_found']],'rows':out,'scope':'Nonzero maximal minors certify nonzero Alexander data. Deficient specializations are only unresolved, not proof of Alexander vanishing or sliceness.'}
(p/'SIGNED_VIOLATOR_SLICE_SCREEN.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['rows','survivors']});print('survivors',[(x['name'],x['dets']) for x in result['survivors']])
