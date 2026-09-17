#!/usr/bin/env python3
"""Assemble the two low-degree D01 gates from exact saved computations.
The generic colored identities are checked symbolically before substitution.
The standalone derivation does not use the repaired all-degree moment lemma.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json
import sympy as S

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():ap.error('refusing overwrite')
    t,a1,a2,a3,b1,b2,b3=S.symbols('t a1 a2 a3 b1 b2 b3')
    B1A,B1B=t*a1,t*b1
    B2A,B2B=t*t*a2,t*t*b2
    B3A,B3B=t**3*a3,t**3*b3
    raw2=(B2A-1)*(B2B-1)/(t*t-1)+1
    raw3=(B3A-2*B1A)*(B3B-2*B1B)/(t**3-2*t)+2*B1A*B1B/t
    fact2=t*t*(t*t*a2*b2-a2-b2+1)/(t*t-1)
    fact3=t**3*(t*t*a3*b3-2*(a3*b1+a1*b3-a1*b1))/(t*t-2)
    if S.cancel(raw2-fact2)!=0 or S.cancel(raw3-fact3)!=0:
        raise RuntimeError('Generic colored connected-sum identity failed')
    lead2=S.cancel(raw2/t**2).subs(t,0)
    lead3=S.cancel(raw3/t**3).subs(t,0)
    if S.expand(lead2-a2-b2+1)!=0 or S.expand(lead3-a3*b1-a1*b3+a1*b1)!=0:
        raise RuntimeError('Low-degree root law failed')
    files={
        'K0_e1':'direct/K0_p1_signed_control/result.json',
        'K1_e1':'direct/K1_p1_signed_control/result.json',
        'K0_e2':'direct/K0_p2_control/result.json',
        'K1_e2':'direct/K1_p2_new/result.json',
        'K0_e3':'direct/K0_p3_new/result.json',
        'K1_e3':'direct/K1_p3_new/result.json',
        'D01_e2_direct':'direct/D01_p2_direct/result.json'}
    vals={};hashes={}
    for label,rel in files.items():
        path=HERE/rel;d=json.loads(path.read_text())
        if d['status']!='COMPUTED' or d['exact_divisible'] is not True or d['e_value'][1]!=0:
            raise RuntimeError('Invalid or missing exact result '+label)
        vals[label]=d['e_value'][0]
        hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
    if (vals['K0_e1'],vals['K1_e1'],vals['K0_e2'])!=(13,13,-23):
        raise RuntimeError('Known signed controls did not reproduce')
    e2=vals['K0_e2']+vals['K1_e2']-1
    e3=vals['K0_e3']*vals['K1_e1']+vals['K0_e1']*vals['K1_e3']-vals['K0_e1']*vals['K1_e1']
    if vals['D01_e2_direct']!=e2:raise RuntimeError('Direct D01 value disagrees with summand law')
    det=vals['K0_e1']*vals['K1_e1']
    rows=[]
    for n,val,method in [(2,e2,'derived and directly computed'),(3,e3,'derived, not directly computed on D01')]:
        rows.append({'n':n,'value':val,'method':method,'required_product':det**n,
                     'difference':val-det**n,'difference_mod32':(val-det**n)%32,
                     'difference_divided_by_32':(val-det**n)//32 if (val-det**n)%32==0 else None})
    if any(row['difference_mod32'] for row in rows):
        verdict='POTENTIAL_NONSLICENESS_GATE_FAILURE_REQUIRES_ADVERSARIAL_REVIEW'
    else:verdict='BOTH_TESTED_D01_GATES_PASS_NO_SLICENESS_OBSTRUCTION'
    # A deliberate altered leading invariant must fire, so a pass is not hardcoded.
    if ((e2+1)-det**2)%32==0:raise RuntimeError('Bad negative control')
    result={'status':verdict,'counterexample_found':False,'signed_determinant_D01':det,
            'summand_values':vals,'gates':rows,'direct_D01_two_parallel_matches':True,
            'symbolic_generic_identities_pass':True,'perturbed_e2_rejected':True,
            'input_sha256':hashes,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limitations':['Matching gate values are not positive evidence of concordance.','No direct D01 three-parallel calculation was run.','Knot-to-paper identification remains upstream.','All direct knot calculations share the previously audited cabler/frontier engine.']}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
