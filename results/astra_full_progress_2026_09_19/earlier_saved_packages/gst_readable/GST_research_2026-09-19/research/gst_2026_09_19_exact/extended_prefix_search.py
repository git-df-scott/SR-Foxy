"""Bounded explicit band search with exact one-sided link-sliceness filters.
No negative global ribbon claim is made. Modular nonzero minors are exact
certificates that the corresponding integer polynomial is nonzero.
"""
import json,time,collections,argparse
from pathlib import Path
import spherogram
from spherogram.links.bands import core
from pd_algebra import fox_matrix,structure,linking_numbers
ROOT=Path(__file__).parent

def detmod(M,p):
    a=[[int(x)%p for x in row] for row in M];n=len(a);d=1
    assert all(len(row)==n for row in a)
    for c in range(n):
        pivot=next((i for i in range(c,n) if a[i][c]),None)
        if pivot is None:return 0
        if pivot!=c:a[c],a[pivot]=a[pivot],a[c];d=-d
        z=a[c][c];d=d*z%p;iv=pow(z,-1,p)
        for i in range(c+1,n):
            if a[i][c]:
                f=a[i][c]*iv%p
                for j in range(c+1,n):a[i][j]=(a[i][j]-f*a[c][j])%p
                a[i][c]=0
    return d%p

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-length',type=int,default=3);parser.add_argument('--max-twists',type=int,default=1);args=parser.parse_args()
    pd=json.loads((ROOT/'gst48.json').read_text())['pd'];K=spherogram.Link(pd);start=time.time()
    bands=core.simple_bands(K,max_twists=args.max_twists,max_band_len=args.max_length);result=[];survivors=[];p=1000003
    for i,b in enumerate(bands):
        L=K.add_band(b);q=[list(z) for z in L.PD_code()];assert len(L.link_components)==2
        lk=int(L.linking_number());record={'band':b.compressed_spec(),'length':len(b.cs_along_top),'twists':b.num_twist,'crossings':len(q),'linking_number':lk}
        if lk:record.update(status='excluded_nonzero_linking')
        else:
            st=structure(q);assert linking_numbers(q,st).get((0,1),0)==0
            for point in [2,3,5]:
                A=fox_matrix(q,point,require_knot=False);nr,nc=A.shape
                assert nr>=nc-1
                # Use fixed first nc-1 rows/columns: failure only means inconclusive.
                M=A[:nc-1,:nc-1].tolist();d=detmod(M,p)
                if d:
                    record.update(status='excluded_nonzero_Fox_minor',specialization=point,modulus=p,minor_size=nc-1,determinant_mod_p=d)
                    break
            else:
                record.update(status='inconclusive_specializations_zero',pd=q)
                survivors.append(record)
        result.append(record)
        if (i+1)%400==0:print('processed',i+1,dict(collections.Counter(a['status'] for a in result)),'seconds',round(time.time()-start,2),flush=True)
    summary={'scope':'Spherogram simple dual paths, fixed source PD, bounded length and half-twists; not a global ribbon decision. Surviving specializations are NOT a sliceness result.', 'max_length':args.max_length,'max_twists':args.max_twists,'count':len(bands),'status_counts':dict(collections.Counter(a['status'] for a in result)),'elapsed_seconds':time.time()-start,'records':result}
    name=f'extended_prefix_L{args.max_length}_T{args.max_twists}.json';(ROOT/name).write_text(json.dumps(summary,indent=2)+'\n')
    print({k:v for k,v in summary.items() if k!='records'},flush=True)
    print('surviving_bands',[(a['band'],a['length'],a['twists']) for a in survivors],flush=True)
if __name__=='__main__':main()
