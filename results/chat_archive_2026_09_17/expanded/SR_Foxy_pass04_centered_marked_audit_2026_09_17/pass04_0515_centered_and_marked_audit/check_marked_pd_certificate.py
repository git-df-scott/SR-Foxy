#!/usr/bin/env python3
"""Independent replay of the PD-to-finite-group certificate.

Does NOT import the finder, SnapPy, Sage, Spherogram, or the saved a,b group.
Checks per-edge matrices directly against each original crossing and traces
longitudes using the explicitly verified increasing-label orientations.
"""
from __future__ import annotations
from copy import deepcopy
from itertools import product
from pathlib import Path
import argparse, hashlib, json

I=[[1,0],[0,1]]
def mat(xs):return [list(xs[:2]),list(xs[2:])]
def flatten(a):return tuple(v for row in a for v in row)
def multiply(a,b):
    cols=list(zip(*b))
    return [[sum(x*y for x,y in zip(row,col))%5 for col in cols] for row in a]
def inverse(a):return [[a[1][1],(-a[0][1])%5],[(-a[1][0])%5,a[0][0]]]
def trace(a):return (a[0][0]+a[1][1])%5
def determinant(a):return (a[0][0]*a[1][1]-a[0][1]*a[1][0])%5

def replay(pd,arc_edges,arc_images,expected=None):
    if len(arc_edges)!=len(arc_images):raise ValueError('arc table length')
    edge_images={}
    for group,values in zip(arc_edges,arc_images):
        a=mat(values)
        if determinant(a)!=1:raise ValueError('matrix determinant')
        for e in group:
            if e in edge_images:raise ValueError('duplicate edge color')
            edge_images[e]=a
    if sorted(edge_images)!=list(range(54)):raise ValueError('edge-color coverage')
    occur={e:[] for e in range(54)}
    for i,c in enumerate(pd):
        for j,e in enumerate(c):
            if e not in occur:raise ValueError('unknown edge')
            occur[e].append((i,j))
    if any(len(o)!=2 for o in occur.values()):raise ValueError('edge multiplicity')
    ranges=[range(0,34),range(34,42),range(42,54)]
    component={e:k for k,r in enumerate(ranges) for e in r}
    succ={e:r[(j+1)%len(r)] for r in ranges for j,e in enumerate(r)}
    incoming={};crossing_sign={}
    for i,c in enumerate(pd):
        for p,q in ((0,2),(1,3)):
            if component[c[p]]!=component[c[q]]:raise ValueError('component crosses at crossing')
            if succ[c[p]]==c[q]:incoming[i,p%2]=p
            elif succ[c[q]]==c[p]:incoming[i,p%2]=q
            else:raise ValueError('strand orientation')
        under,over=incoming[i,0],incoming[i,1]
        # Coordinate determinant of oriented under and over tangents.
        vx=1 if under==0 else -1
        vy=-1 if over==1 else 1
        sign=vx*vy;crossing_sign[i]=sign
        if edge_images[c[1]]!=edge_images[c[3]]:raise ValueError('overpass not constant')
        g=edge_images[c[1]]
        if sign<0:g=inverse(g)
        lhs=edge_images[c[(under+2)%4]]
        rhs=multiply(multiply(inverse(g),edge_images[c[under]]),g)
        if lhs!=rhs:raise ValueError(f'crossing relation {i}')
    if any(edge_images[e]!=I for e in range(34,54)):raise ValueError('auxiliary filling')
    longitudes=[];edge_words=[]
    for k,r in enumerate(ranges):
        value=deepcopy(I);word=[];visited=[]
        for e in r:
            positions=[(i,p) for i,p in occur[e] if incoming[i,p%2]==p]
            if len(positions)!=1:raise ValueError('incoming edge incidence')
            i,p=positions[0]
            if pd[i][(p+2)%4]!=succ[e]:raise ValueError('longitude traversal')
            visited.append((i,p))
            if p%2==0:
                oe=pd[i][1];sgn=crossing_sign[i];g=edge_images[oe]
                if sgn<0:g=inverse(g)
                value=multiply(value,g);word.append([oe,sgn])
        meridian=edge_images[r[0]]
        if multiply(meridian,value)!=multiply(value,meridian):raise ValueError('longitude not peripheral')
        longitudes.append(value);edge_words.append(word)
    if expected is not None:
        if list(map(flatten,longitudes))!=list(map(tuple,expected)):raise ValueError('reported longitude mismatch')
    return longitudes,edge_words,edge_images

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    here=Path(__file__).resolve().parent
    ap.add_argument('--input',type=Path,default=here/'marked_pd.json')
    ap.add_argument('--certificate',type=Path,default=here/'marked_pd_certificate.json')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():ap.error('refusing overwrite')
    source=json.loads(args.input.read_text());cert=json.loads(args.certificate.read_text())
    if cert['status']!='WITNESS_FOUND':raise ValueError('no witness in certificate')
    if cert['input_sha256']!=hashlib.sha256(args.input.read_bytes()).hexdigest():raise ValueError('input hash')
    w=cert['witness'];pd=source['pd'];checks={}
    vals,words,images=replay(pd,cert['arc_edges'],w['arc_images'],w['longitude_values'])
    checks['original_crossing_relations']=len(pd)
    checks['filled_auxiliary_edge_meridians']=20
    checks['preferred_longitude_correction_trivial_on_filled_components']=2
    # Full matrix conjugacy test, not only the trace criterion used by finder.
    group=[mat(v) for v in product(range(5),repeat=4) if determinant(mat(v))==1]
    orbit={flatten(multiply(multiply(g,vals[1]),inverse(g))) for g in group}
    if flatten(vals[2]) in orbit or flatten(inverse(vals[2])) in orbit:raise ValueError('axes not separated')
    checks['direct_conjugacy_tests']=2*len(group)
    if trace(vals[1])==trace(vals[2]):raise ValueError('trace separation absent')
    checks['trace_separation']=1
    # A positive test: a conjugated copy of the same axis must lie in the orbit.
    g=group[7];copy=multiply(multiply(g,vals[1]),inverse(g))
    if flatten(copy) not in orbit:raise ValueError('positive conjugacy control')
    checks['positive_conjugacy_control']=1
    # Every cyclic choice of longitude basepoint retains its trace.
    for k,word in enumerate(words):
        for shift in range(len(word)):
            v=deepcopy(I)
            for e,sgn in word[shift:]+word[:shift]:
                g=images[e] if sgn>0 else inverse(images[e]);v=multiply(v,g)
            if trace(v)!=trace(vals[k]):raise ValueError('basepoint control')
            checks['cyclic_basepoint_controls']=checks.get('cyclic_basepoint_controls',0)+1
    # Abelian coloring is valid but must NOT claim the axes are separated.
    m=mat((4,1,2,2))
    abelian=[flatten(m if min(es)<34 else I) for es in cert['arc_edges']]
    av,_,_=replay(pd,cert['arc_edges'],abelian)
    if av[1]!=I or av[2]!=I:raise ValueError('zero-linking abelian control')
    checks['abelian_negative_control']=1
    # Mutate real data and ensure checker returns failure.
    bad=deepcopy(w['arc_images']);bad[0]=[0,0,0,0]
    try:replay(pd,cert['arc_edges'],bad,w['longitude_values'])
    except ValueError:checks['rejected_matrix_mutation']=1
    else:raise ValueError('failed to reject matrix mutation')
    badpd=deepcopy(pd);badpd[0][0]=999
    try:replay(badpd,cert['arc_edges'],w['arc_images'],w['longitude_values'])
    except ValueError:checks['rejected_PD_mutation']=1
    else:raise ValueError('failed to reject PD mutation')
    badvals=deepcopy(w['longitude_values']);badvals[1]=list(flatten(I))
    try:replay(pd,cert['arc_edges'],w['arc_images'],badvals)
    except ValueError:checks['rejected_longitude_mutation']=1
    else:raise ValueError('failed to reject longitude mutation')
    def order(a):
        cur=deepcopy(I)
        for n in range(1,121):
            cur=multiply(cur,a)
            if cur==I:return n
        raise ValueError('no finite order')
    result={'status':'DIRECT_PD_CERTIFICATE_REPLAYED','counterexample_found':False,
            'checks_by_family':checks,'checks_passed':sum(checks.values()),
            'axis_traces':[trace(vals[1]),trace(vals[2])],
            'axis_orders':[order(vals[1]),order(vals[2])],
            'longitude_edge_words':words,'longitude_images':[flatten(a) for a in vals],
            'group_order':len(group),'same_axis_conjugacy_class_size':len(orbit),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            'dependencies':['Stored PD matches the marked annulus presentation in the paper (not checked here).','Product-disk exterior interpretation when applying to a 4D disk (separate).'],
            'non_dependency':'No saved SnapPy group generators, peripheral words, triangulation, or old finite witness used by replay.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
