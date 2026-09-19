import json,time,math,collections
from pathlib import Path
import spherogram,regina
from pd_algebra import component_pd,determinant,structure
from multivariable_prefix_certificate import multivariable_fox
from extended_prefix_search import detmod
ROOT=Path(__file__).parent

def sig(q):
    if not q:return 'EMPTY'
    lab={a:i+1 for i,a in enumerate(sorted({x for z in q for x in z}))}
    return regina.Link.fromPD([[lab[x] for x in z] for z in q]).sig(False,True,False)

def main():
    records=json.loads((ROOT/'extended_prefix_L4_T2.json').read_text())['records'];src=json.loads((ROOT/'gst48.json').read_text())['pd'];srcsig=sig(src);out=[];start=time.time()
    for r in records:
        if r['status']!='inconclusive_specializations_zero':continue
        q=r['pd'];item={'band':r['band'],'pd':q};ex=False
        for v in [[2,3],[2,4],[3,5]]:
            A,st=multivariable_fox(q,v);n=A.cols;d=detmod(A[:n-1,:n-1].tolist(),1000003)
            if d:
                item.update(status='excluded_multivariable_minor',variables=v,modulus=1000003,minor_size=n-1,determinant_mod_p=d);ex=True;break
        if not ex:
            st=structure(q);dets=[determinant(component_pd(q,i,st)) for i in range(2)];item['component_determinants']=dets
            if any(math.isqrt(d)**2!=d for d in dets):item['status']='excluded_component_determinant'
            else:
                L=spherogram.Link(q);L.simplify('global');qq=[list(z) for z in L.PD_code()]
                item.update(simplified_pd=qq,unlinked_unknot_components=L.unlinked_unknot_components,projection_parts=len(L.split_link_diagram()),simplified_crossings=len(L))
                if L.unlinked_unknot_components==1 and sig(qq)==srcsig:item['status']='trivial_split_unknot_plus_source_after_software_simplification'
                else:item['status']='unresolved'
        out.append(item)
    ans={'scope':'Follow-up to L4/T2 single-variable filter; modular nonzero entries are exact exclusions. Trivial-split tags use software Reidemeister simplification and exact final diagram identity, not saved full simplification movies. Unresolved is not slice/ribbon.','input_survivors':len(out),'status_counts':dict(collections.Counter(r['status'] for r in out)),'elapsed_seconds':time.time()-start,'records':out}
    (ROOT/'L4_followup.json').write_text(json.dumps(ans,indent=2)+'\n');print({k:v for k,v in ans.items() if k!='records'})
    for r in out:
        if r['status'] not in ['excluded_multivariable_minor','excluded_component_determinant']:print(r['band'],r['status'],r['component_determinants'],r['simplified_crossings'],r['projection_parts'],r['unlinked_unknot_components'])
if __name__=='__main__':main()
