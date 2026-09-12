#!/usr/bin/env python3
"""Known ribbon concordances and an equal-rank algebraic negative control."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import snappy
from chain_map_filter import complex_data,check,check_retraction
from audit_mixed_lifts import unknot_retract,compose


def run(output):
    if Path(output).exists():raise FileExistsError(output)
    unknot={'generators':{0:(0,0)},'arrows':[],'total_rank':1}
    ribbon=snappy.Link('6_1');trefoil=snappy.Link('3_1')
    cases=[('unknot_to_stevedore',unknot,complex_data(ribbon.PD_code()),True),
           ('trefoil_to_trefoil_sum_stevedore',complex_data(trefoil.PD_code()),
            complex_data(trefoil.connected_sum(ribbon).PD_code()),True),
           ('unknot_to_mirror_stevedore',unknot,complex_data(ribbon.mirror().PD_code()),True),
           ('stevedore_to_unknot',complex_data(ribbon.PD_code()),unknot,False),
           ('trefoil_to_unknot',complex_data(trefoil.PD_code()),unknot,False)]
    # Abstract free quotient complexes, not claimed to come from knots.
    # Identical graded ranks, but d(x)=U*y in the source forces the constant
    # coefficient of F(y) to vanish when the target differential is zero.
    a={'generators':{0:(0,0),1:(1,1)},'arrows':[(0,1,1,0)],'total_rank':2}
    b=dict(a,arrows=[])
    cases.append(('equal_rank_incompatible_differential',a,b,False))
    result={'z3_solver':importlib.metadata.version('z3-solver'),'checks':[],
            'limitations':'These controls test code and conventions, not every HFK Calculator complex or the full geometric certificate.'}
    for name,source,target,expected in cases:
        forward=check(source,target);retraction=check_retraction(source,target)
        assert (forward['status']=='SAT')==expected,(name,forward['status'])
        assert retraction['status']==('SAT' if expected else 'UNSAT'),(name,retraction['status'])
        result['checks'].append({'name':name,'expected_pass':expected,'source':source,'target':target,
                                 'injective_chain_map':forward,'homotopy_retraction':retraction})
        print(name,forward['status'],retraction['status'],flush=True)
    result['full_ring_unknot_controls']=[]
    for name,knot,expected in [('stevedore',ribbon,True),('trefoil',trefoil,False),
                               ('T3_4',snappy.Link('T(3,4)'),False)]:
        c=complex_data(knot.PD_code());assert not compose(c['arrows'],c['arrows'])
        check_full=unknot_retract(c['generators'],c['arrows'])
        assert check_full['status']==('SAT' if expected else 'UNSAT')
        result['full_ring_unknot_controls'].append({'name':name,'complex':c,'check':check_full})
        print('full_ring',name,check_full['status'],flush=True)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
