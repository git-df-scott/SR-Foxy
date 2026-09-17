#!/usr/bin/env python3
"""Find/check finite Wirtinger colorings directly from the marked PD.

Ports 0,2 are under; 1,3 over. Oriented crossings have sign + for incoming
{0,3} or {1,2}; -. otherwise. The convention is M_out=g^-1 M_in g,
where g=M_over**crossing_sign. Along a longitude the corresponding g's
are multiplied in traversal order. All auxiliary meridians are killed.
This is a marked-diagram certificate, not independent paper identification.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from pathlib import Path
import argparse, hashlib, json, time

P=5
IDENTITY=(1,0,0,1)
def mm(a,b):
    return ((a[0]*b[0]+a[1]*b[2])%P,(a[0]*b[1]+a[1]*b[3])%P,
            (a[2]*b[0]+a[3]*b[2])%P,(a[2]*b[1]+a[3]*b[3])%P)
def inv(a):return (a[3],-a[1]%P,-a[2]%P,a[0])
def tr(a):return (a[0]+a[3])%P
def det(a):return (a[0]*a[3]-a[1]*a[2])%P

def diagram(pd):
    occ=defaultdict(list)
    for i,c in enumerate(pd):
        if len(c)!=4:raise ValueError('PD crossing must have four ports')
        for j,e in enumerate(c):occ[e].append((i,j))
    if any(len(x)!=2 for x in occ.values()):raise ValueError('PD multiplicity')
    across={}
    for a,b in occ.values():across[a]=b;across[b]=a
    remaining=set(occ);components=[];comp_of_edge={};inc=set()
    while remaining:
        marker=min(remaining)
        # In this explicitly stored PD, labels ascend along the oriented strands.
        possible=[x for x in occ[marker] if pd[x[0]][(x[1]+2)%4]==marker+1]
        if len(possible)!=1:raise ValueError('Cannot recover declared increasing-label orientation')
        start=possible[0];cur=start;cycle=[];edges=[]
        while True:
            i,j=cur;op=(i,(j+2)%4)
            if cur in inc:raise ValueError('Strand repeated prematurely')
            inc.add(cur);cycle.append(cur);edges.append(pd[i][j]);remaining.remove(pd[i][j])
            comp_of_edge[pd[i][j]]=len(components)
            cur=across[op]
            if cur==start:break
        expected=list(range(marker,marker+len(edges)))
        if edges!=expected:raise ValueError('PD labels do not follow declared orientation')
        components.append({'marker':marker,'cycle':cycle,'edges':edges})
    signs=[]
    for i,c in enumerate(pd):
        incoming={j for j in range(4) if (i,j) in inc}
        if incoming in ({0,3},{1,2}):signs.append(1)
        elif incoming in ({0,1},{2,3}):signs.append(-1)
        else:raise ValueError('Bad incoming ports')
    # Join the segments of every overpass to obtain actual Wirtinger arcs.
    parent={e:e for e in occ}
    def root(e):
        while parent[e]!=e:parent[e]=parent[parent[e]];e=parent[e]
        return e
    def union(a,b):parent[root(a)]=root(b)
    for c in pd:union(c[1],c[3])
    groups=defaultdict(list)
    for e in occ:groups[root(e)].append(e)
    groups=sorted((sorted(g) for g in groups.values()),key=lambda g:min(g))
    edge_arc={e:i for i,g in enumerate(groups) for e in g}
    arc_components=[comp_of_edge[g[0]] for g in groups]
    if any(len({comp_of_edge[e] for e in g})!=1 for g in groups):raise ValueError('Arc crosses components')
    relations=[]
    for i,c in enumerate(pd):
        incoming=0 if (i,0) in inc else 2;outgoing=(incoming+2)%4
        relations.append((edge_arc[c[incoming]],edge_arc[c[1]],edge_arc[c[outgoing]],signs[i]))
    linkings=[[0]*len(components) for c in components]
    for c,sign in zip(pd,signs):
        a,b=comp_of_edge[c[0]],comp_of_edge[c[1]]
        if a!=b:linkings[a][b]+=sign;linkings[b][a]+=sign
    if any(v%2 for row in linkings for v in row):raise ValueError('Half-integral linking')
    return {'components':components,'edge_arc':edge_arc,'arc_edges':groups,
            'arc_components':arc_components,'relations':relations,'signs':signs,
            'linking_matrix':[[v//2 for v in row] for row in linkings]}

def evaluate(pd,meta,images):
    for i,m in enumerate(images):
        if det(m)!=1:raise ValueError(f'Not SL2 at arc {i}')
        if meta['arc_components'][i]!=0 and m!=IDENTITY:raise ValueError('Auxiliary meridian not killed')
    for index,(a,b,c,sign) in enumerate(meta['relations']):
        g=images[b] if sign==1 else inv(images[b])
        if images[c]!=mm(mm(inv(g),images[a]),g):raise ValueError(f'Wirtinger relation {index} fails')
    values=[];words=[]
    for component in meta['components']:
        v=IDENTITY;w=[]
        for i,j in component['cycle']:
            if j%2==0:
                arc=meta['edge_arc'][pd[i][1]];sign=meta['signs'][i]
                g=images[arc] if sign==1 else inv(images[arc])
                v=mm(v,g);w.append((arc,sign))
        meridian=images[meta['edge_arc'][component['marker']]]
        if mm(v,meridian)!=mm(meridian,v):raise ValueError('Peripheral commutation fails')
        values.append(v);words.append(w)
    return values,words

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,default=Path(__file__).with_name('marked_pd.json'))
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seconds',type=float,default=15)
    ap.add_argument('--max-solutions',type=int,default=500)
    args=ap.parse_args()
    if args.output.exists():ap.error('refusing to overwrite')
    data=json.loads(args.input.read_text());pd=data['pd'];meta=diagram(pd)
    if [x['marker'] for x in meta['components']]!=[0,34,42]:raise ValueError('Wrong marked components')
    group=[x for x in product(range(P),repeat=4) if det(x)==1]
    meridian=(4,1,2,2)
    colors=sorted({mm(mm(inv(g),meridian),g) for g in group})
    images=colors+[IDENTITY];id_index=len(colors)
    domains=[set(range(len(colors))) if c==0 else {id_index} for c in meta['arc_components']]
    domains[meta['edge_arc'][0]]={colors.index(meridian)}
    indices={m:i for i,m in enumerate(images)}
    constraints=[]
    for a,b,c,sign in meta['relations']:
        rows=[]
        for x in domains[a]:
            for y in domains[b]:
                g=images[y] if sign==1 else inv(images[y])
                z=indices[mm(mm(inv(g),images[x]),g)]
                if z not in domains[c]:continue
                row={a:x,b:y,c:z}
                if len(row)!=len({a,b,c}):raise RuntimeError('Unexpected map error')
                if row[a]==x and row[b]==y and row[c]==z:rows.append(row)
        constraints.append(rows)
    start=time.monotonic();solutions=0;nodes=0;witness=None
    class Budget(Exception):pass
    def dfs(ds):
        nonlocal solutions,nodes,witness
        if time.monotonic()-start>args.seconds or solutions>=args.max_solutions:raise Budget()
        nodes+=1
        changed=True
        while changed:
            changed=False
            for rows in constraints:
                rows=[row for row in rows if all(v in ds[k] for k,v in row.items())]
                if not rows:return False
                for k in rows[0]:
                    choices={row[k] for row in rows};new=ds[k]&choices
                    if new!=ds[k]:ds[k]=new;changed=True
        variables=[(len(v),i) for i,v in enumerate(ds) if len(v)>1]
        if not variables:
            solutions+=1;assignment=[images[next(iter(d))] for d in ds]
            values,words=evaluate(pd,meta,assignment)
            if tr(values[1])!=tr(values[2]):
                witness={'arc_images':assignment,'longitude_values':values,
                         'longitude_arc_words':words,'axis_traces':[tr(values[1]),tr(values[2])]}
                return True
            return False
        _,i=min(variables)
        for v in sorted(ds[i]):
            new=[d.copy() for d in ds];new[i]={v}
            if dfs(new):return True
        return False
    try:found=dfs(domains);status='WITNESS_FOUND' if found else 'NO_WITNESS_IN_ENUMERATED_COLOR_CLASS'
    except Budget:status='RESOURCE_LIMIT_UNKNOWN'
    result={'status':status,'counterexample_found':False,'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seconds':time.monotonic()-start,'nodes':nodes,'full_colorings_checked':solutions,
            'group_order':len(group),'meridian_conjugacy_class_size':len(colors),
            'arc_edges':meta['arc_edges'],'arc_components':meta['arc_components'],
            'relations':meta['relations'],'component_markers':[c['marker'] for c in meta['components']],
            'linking_matrix':meta['linking_matrix'],'witness':witness,
            'scope':'Nonconjugacy of the two marked axes in the exterior of the stored knot component. Not a sliceness obstruction; source figure identification and product-disk interpretation are separate.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['arc_edges','arc_components','relations','witness']},indent=2))
    if witness:print('AXIS TRACES',witness['axis_traces'],'VALUES',witness['longitude_values'])
if __name__=='__main__':main()
