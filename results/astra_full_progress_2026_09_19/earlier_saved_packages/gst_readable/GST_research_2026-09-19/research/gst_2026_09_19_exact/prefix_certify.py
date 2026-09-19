"""Certify finite first-band exclusions by exact specialized Alexander minors.
A nonzero specialization proves the minor is a nonzero polynomial; it is not
being treated as a signature value at the real number 2.
"""
import json,collections,time
from pathlib import Path
from pd_algebra import *
ROOT=Path(__file__).parent

def bareiss_det(M):
    """Fraction-free integer determinant, independent of SymPy determinant code."""
    a=[[int(x) for x in row] for row in M];n=len(a)
    if not n:return 1
    sign=1;prev=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=a[i][j]*p-a[i][k]*a[k][j]
                q,r=divmod(v,prev)
                if r:raise ArithmeticError('Bareiss division is not exact')
                a[i][j]=q
            a[i][k]=0
        prev=p
    return sign*a[-1][-1]

def get_result(pd,record):
    new=[q[:] for q in pd];a,b=record['swapped_incoming_darts']
    new[a[0]][a[1]],new[b[0]][b[1]]=new[b[0]][b[1]],new[a[0]][a[1]]
    return new

if __name__=='__main__':
    pd=json.loads((ROOT/'gst48.json').read_text())['pd'];rec=json.loads((ROOT/'face_band_results.json').read_text())['records'];out=[];start=time.time()
    for r in rec:
        new=get_result(pd,r);A=fox_matrix(new,s.Integer(2),require_knot=False)
        M=[[int(x) for x in row] for row in A[:-1,:-1].tolist()]
        d=bareiss_det(M)
        symdet=int(s.Matrix(M).det(method='domain-ge'));assert symdet==d
        result={'edge_labels':r['edge_labels'],'face':r['face'],'specialization':2,'deleted_row':47,'deleted_column':47,'minor_determinant':d,'independent_integer_determinant_agrees':True,'generic_alexander_rank':0 if d else None}
        if not d:
            A=fox_matrix(new,s.Integer(3),require_knot=False);M=[[int(x) for x in row] for row in A[:-1,:-1].tolist()];d=bareiss_det(M)
            result.update(specialization=3,minor_determinant=d,generic_alexander_rank=0 if d else None)
            assert int(s.Matrix(M).det(method='domain-ge'))==d
        if r['edge_labels'] in [[41,79],[40,80]]:result['specialized_matrix']=M
        out.append(result)
    print('TOTAL',len(out),'NONZERO',sum(r['minor_determinant']!=0 for r in out),'seconds',time.time()-start)
    print('exceptional',[(r['edge_labels'],r['minor_determinant']) for r in out if r['specialization']!=2])
    (ROOT/'prefix_certificates.json').write_text(json.dumps({'scope':'Fixed 48-crossing diagram; one orientable untwisted band with core inside a single face; distinct edge attachments. This is a prefix exclusion, not a global non-ribbon proof.','total':len(out),'excluded_by_nonzero_Alexander_minor':sum(r['minor_determinant']!=0 for r in out),'records':out},indent=2)+'\n')
