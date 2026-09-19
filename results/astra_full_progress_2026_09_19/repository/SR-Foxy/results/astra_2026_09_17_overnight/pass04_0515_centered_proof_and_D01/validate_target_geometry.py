#!/usr/bin/env python3
"""Recheck exact PD structure, file provenance, and a small full state sum.
These are arithmetic/combinatorial checks, not a knot-identification proof.
"""
from pathlib import Path
from collections import defaultdict
import argparse, hashlib, json, sys
import sympy as S
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from geometry import oriented_components, sublink

def normalize(pd):
    labels={}
    return [[labels.setdefault(e,len(labels)) for e in c] for c in pd]

def planar_euler(pd):
    occ=defaultdict(list)
    for i,c in enumerate(pd):
        for j,e in enumerate(c):occ[e].append((i,j))
    if any(len(v)!=2 for v in occ.values()):raise ValueError('bad edge multiplicity')
    across={}
    for u,v in occ.values():across[u]=v;across[v]=u
    unseen=set(across);faces=0
    while unseen:
        d=min(unseen);start=d
        while d in unseen:
            unseen.remove(d);i,j=across[d];d=(i,(j+1)%4)
        if d!=start:raise ValueError('bad face permutation')
        faces+=1
    return len(pd)-len(occ)+faces

def full_state_sum(pd,writhe):
    x=S.symbols('x');delta=-x-x**-1;out=S.Integer(0)
    edges=sorted({e for c in pd for e in c});N=len(pd)
    if N>8:raise ValueError('small controls only')
    for mask in range(1<<N):
        parent={e:e for e in edges}
        def root(e):
            while parent[e]!=e:parent[e]=parent[parent[e]];e=parent[e]
            return e
        for i,(a,b,c,d) in enumerate(pd):
            pairs=((a,d),(b,c)) if mask>>i&1 else ((a,b),(c,d))
            for u,v in pairs:parent[root(u)]=root(v)
        loops=len({root(e) for e in edges})
        out+=x**(N-mask.bit_count())*delta**loops
    exponent=-N-3*writhe
    if exponent%2:raise ValueError('nonintegral x normalization')
    return S.expand((-1)**writhe*x**(exponent//2)*out)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.output.exists():ap.error('refusing overwrite')
    checks=[]
    for f in sorted((HERE/'results').glob('*_p*/result.json')):
        r=json.loads(f.read_text());data=json.loads((f.parent/'diagram.json').read_text());pd=data['parallel_pd'];p=r['parallel']
        if r['status']!='COMPUTED':raise RuntimeError('unknown target result')
        src=HERE/('inputs/D01.json' if r['target']=='D01' else 'inputs/targets.json')
        if hashlib.sha256(src.read_bytes()).hexdigest()!=r['source_subset_sha256']:raise RuntimeError('source hash mismatch')
        if hashlib.sha256((f.parent/'input.txt').read_bytes()).hexdigest()!=r['input_sha256']:raise RuntimeError('input hash mismatch')
        checks.append({'name':f.parent.name,'input_and_source_hashes_match':True})
        info=oriented_components(pd)
        if info['components']!=p or info['writhe']!=0 or any(v for row in info['linking_matrix'] for v in row):raise RuntimeError('framing failed')
        if planar_euler(pd)!=2:raise RuntimeError('nonplanar rotation system')
        checks.append({'name':f.parent.name,'planar_euler':2,'components':p,'zero_writhe_and_pairwise_linking':True})
        expected=normalize(data['zero_writhe_pd'])
        for i in range(p):
            if normalize(sublink(pd,{i}))!=expected:raise RuntimeError(('component not source diagram',f.parent.name,i))
        checks.append({'name':f.parent.name,'each_component_reduces_to_zero_writhe_source':True,'components_checked':p})
    # This is an independent 64-state evaluation, not the frontier contraction.
    pd=json.loads((HERE/'inputs/targets.json').read_text())['K0']['pd']
    pol=full_state_sum(pd,oriented_components(pd)['writhe']);x=S.symbols('x');h=x*x+1
    reduced=S.rem(S.expand(pol*x**20),h**5,x)
    reduced=S.rem(reduced*S.invert(x**20,h**5,x),h**5,x)
    saved=json.loads((HERE/'results/K0_p1/result.json').read_text())['raw']['coefficients_x']
    if reduced!=sum(c*x**i for i,c in enumerate(saved)):raise RuntimeError('full state sum disagrees')
    checks.append({'name':'K0_64_state_full_polynomial','polynomial':str(pol),'exact_jet_match':True})
    bad=[c[:] for c in pd];bad[0][0]=9999
    try:planar_euler(bad)
    except ValueError:checks.append({'name':'tampered_edge_multiplicity','rejected':True})
    else:raise RuntimeError('invalid PD accepted')
    out={'status':'GEOMETRY_PROVENANCE_AND_FULL_SMALL_CONTROL_PASS','checks_passed':len(checks),'checks':checks,'scope':'Rotation system, cabling components, file hashes and small bracket arithmetic only. Source knot identity and smooth surfaces are not certified by these checks.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks_passed':len(checks)},indent=2))
if __name__=='__main__':main()
