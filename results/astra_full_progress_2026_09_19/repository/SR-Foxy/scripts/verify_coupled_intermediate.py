#!/usr/bin/env python3
"""Find verified hyperbolicity or a nonzero Alexander minor, hence nonsplit.

A split 2-component link exterior has an essential separating sphere. A
complete finite-volume hyperbolic link exterior is irreducible. This tests
the intermediate presentation, not whether an endpoint has other movies.

Audit correction: generic Alexander nullity is concordance invariant, so the
ordinary Alexander polynomial of a VALID coupled first stage is zero. The
Alexander calculation below is therefore only a movie-consistency control;
it cannot provide the hoped-for nonsplitting certificate in this family.
"""
import argparse
import gzip
import json
from pathlib import Path
from sage.all import *
import snappy


def run(archive,output,attempts=12):
    if Path(output).exists():raise FileExistsError(output)
    first=[r for x in gzip.open(archive,'rt') if (r:=json.loads(x))['type']=='first' and not r['detected_split_unknot']]
    first.sort(key=lambda r:(len(r['simplified_intermediate_pd']),r['first_id']))
    result={'archive':archive,'status':'INTERMEDIATE_NONSPLITTING_CHECK_ONLY','checks':[],
        'Alexander_control_correction':'A valid first stage is link-concordant to K plus an unknot and has generic nullity one. A nonzero ordinary Alexander minor would contradict the movie interpretation, not establish useful new coverage.',
        'implication':'A verified complete finite-volume hyperbolic 2-component link exterior is irreducible; a split link exterior is reducible.',
        'limitations':'Depends on SnapPy interval-verification implementation and PD construction. This says nothing about alternative movie presentations of the final knot.'}
    for r in first[:attempts]:
        L=snappy.Link(r['simplified_intermediate_pd']);M=L.exterior()
        c={'first_id':r['first_id'],'placement':r['placement'],'pd':L.PD_code(),'components':len(L.link_components),'linking_number':float(L.linking_number())}
        assert c['components']==2 and c['linking_number']==0
        try:
            verified,shapes=M.verify_hyperbolicity(bits_prec=100)
            c['verified_hyperbolic']=bool(verified)
            if verified:
                v=M.volume(verified=True,bits_prec=100)
                c.update(volume_lower=str(v.lower()),volume_upper=str(v.upper()),tetrahedron_shapes=[str(s) for s in shapes],triangulation=M._to_string())
        except Exception as e:c['error']=type(e).__name__+': '+str(e)
        if not c.get('verified_hyperbolic'):
            try:
                A=L.alexander_matrix(mv=False)[0]
                B=A.apply_map(lambda p: QQ(p(2)))
                k=min(B.nrows(),B.ncols())-1
                minor=B[:k,:k];det=minor.det()
                c.update(alexander_evaluation=2,alexander_matrix=[[str(v) for v in row] for row in B.rows()],
                         deleted_last_row_and_column_minor_determinant=str(det),alexander_nonsplit=bool(det!=0))
                # Separate exact determinant implementation on exported data.
                import sympy
                independent=sympy.Matrix([[sympy.Rational(str(v)) for v in row] for row in minor.rows()]).det()
                assert str(independent)==str(det)
                c['independent_sympy_determinant_passed']=True
                if det!=0:c['movie_nullity_conflict']=True
            except Exception as e:c['alexander_error']=type(e).__name__+': '+str(e)
        result['checks'].append(c)
        print('intermediate',c['first_id'],'verified hyperbolic',c.get('verified_hyperbolic'),'nonzero Alexander minor',c.get('alexander_nonsplit'),flush=True)
        if c.get('verified_hyperbolic') or c.get('alexander_nonsplit'):break
    Path(output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('output');a=p.parse_args();run(a.archive,a.output)
