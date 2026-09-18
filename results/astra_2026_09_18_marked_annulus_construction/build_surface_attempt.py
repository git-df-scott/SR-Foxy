"""Record the finite orientation checks and failed compression attempt.

This is a surface-construction ledger, NOT an immersed-annulus movie.
"""
import json
from pathlib import Path
from build_transport import g

HERE=Path(__file__).resolve().parent

def main():
    out=HERE/'surface_attempt.json'
    if out.exists():raise FileExistsError(out)
    d=json.loads((HERE/'transport.json').read_text())
    A=g.adjacency_from_pd(g.SCAFFOLD);q=g.quotient_R_wirtinger(A)
    bands=[dict(g.BAND1,arc_is_under=[False,True]),dict(g.BAND2,arc_is_under=[True,False])]
    F=g.add_zero_twist_band(g.add_zero_twist_band(A,bands[0]),bands[1]);qf=g.quotient_R_wirtinger(F)
    orientation=[]
    for ci in range(1,5):
        ports=q['components'][ci]
        final={qf['cmap'][p] for p in ports}
        signs={1 if ((p in q['incoming'])==(p in qf['incoming'])) else -1 for p in ports}
        assert len(final)==len(signs)==1
        orientation.append({'native_component':ci,'minimum_port':min(ports),
                            'final_axis':next(iter(final)),'orientation_sign':next(iter(signs))})
    assert [(r['final_axis'],r['orientation_sign']) for r in orientation]==[(1,1),(2,1),(2,-1),(1,-1)]
    mirror={tuple(r['upper']):tuple(r['lower']) for r in d['mirror_port_map']}
    for ci in [1,2]:
        assert all((p in q['incoming'])!=(mirror[p] in q['incoming']) for p in q['components'][ci])
    endpoints=[]
    for band in bands:
        ends=[tuple(band['along_top'][i]) for i in [0,-1]]
        assert all(p in q['incoming'] for p in ends)
        endpoints.append(ends)
    report={'scope':'Marked genus-one product-band surface plus research42 existence correction; failed direct compression; no annulus movie',
            'orientation_table':orientation,'mirror_reverses_both_native_orientations':True,
            'band_attachment_ports_native_incoming':endpoints,
            'product_annulus_orientations':[1,-1],
            'events':[
                {'event':'native product annuli','components':2,'boundary_components':4,'euler_characteristic':0,'disjoint_from_product_disk':True},
                {'event':'attach actual transported B1 in boundary collar','components':1,'boundary_components':3,'euler_characteristic':-1,'genus':0},
                {'event':'attach actual transported B2 in boundary collar','components':1,'boundary_components':2,'euler_characteristic':-2,'genus':1,'oriented_boundary':'a-b'},
                {'event':'glue research42 genus13 correction along b','components':1,'boundary_components':2,'euler_characteristic':-28,'genus':14,'oriented_boundary':'a-b_prime','limitation':'Correction is the existing existence construction, not a new coordinate movie'},
                {'event':'attempt compression of factor10 on u or v','status':'BLOCKED_FOR_THESE_LOOPS','reason':'Both have trace3 mod17, so neither is nullhomotopic; see transport.json'}],
            'annulus_movie':None,'annulus_double_point_labels':None,'Whitney_disks':None,
            'not_obstructed':'Other handle systems or another annulus construction are not excluded.'}
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'orientation_checks':'PASS','initial_surface_genus':1,'corrected_surface_genus':14,'annulus_constructed':False}))

if __name__=='__main__':main()
