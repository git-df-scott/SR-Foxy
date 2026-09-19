"""Standalone PD utilities. No topology-library calls; exact combinatorial data.

PD ports are cyclic (0,1,2,3), opposite ports are one strand. The bracket
A-smoothing pairs (0,1),(2,3), B-smoothing pairs (0,3),(1,2).
Parallel construction replaces a crossing by the obvious p by p crossing grid
and reverses boundary lane order along each joining ribbon.
"""
from collections import defaultdict, Counter
import random

def occurrences(pd):
    occ=defaultdict(list)
    for i,c in enumerate(pd):
        if len(c)!=4: raise ValueError('Not a four-port crossing')
        for j,e in enumerate(c): occ[e].append((i,j))
    if any(len(v)!=2 for v in occ.values()): raise ValueError('Every edge must occur twice')
    return occ

def oriented_components(pd):
    occ=occurrences(pd); across={}
    for pair in occ.values():
        a,b=pair;across[a]=b;across[b]=a
    unused=set(across); comps=[]; incoming=set(); component={}
    while unused:
        start=min(unused); cur=start; ports=[]
        while cur not in incoming:
            i,j=cur;other=(i,(j+2)%4)
            if cur not in unused or other not in unused: raise ValueError('Bad strand orbit')
            incoming.add(cur);ports.extend([cur,other]);unused.remove(cur);unused.remove(other)
            component[cur]=component[other]=len(comps)
            cur=across[other]
        if cur!=start: raise ValueError('Unexpected orientation collision')
        comps.append(ports)
    signs=[]
    for i,c in enumerate(pd):
        inc={j for j in range(4) if (i,j) in incoming}
        if inc in ({0,3},{1,2}): signs.append(1)
        elif inc in ({0,1},{2,3}): signs.append(-1)
        else: raise ValueError(('Bad orientation',inc))
    linking=[[0]*len(comps) for _ in comps]
    for i,s in enumerate(signs):
        a,b=component[(i,0)],component[(i,1)]
        if a!=b:linking[a][b]+=s;linking[b][a]+=s
    if any(v%2 for row in linking for v in row):raise ValueError('Odd signed crossing count')
    return {'components':len(comps),'writhe':sum(signs),'self_writhes':[sum(s for i,s in enumerate(signs) if component[(i,0)]==component[(i,1)]==a) for a in range(len(comps))], 'linking_matrix':[[v//2 for v in row] for row in linking], 'component_of_port':component,'crossing_signs':signs}

def sublink(pd,keep):
    info=oriented_components(pd); comp=info['component_of_port'];occ=occurrences(pd)
    parent={e:e for e in occ}
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):parent[root(a)]=root(b)
    retained=[]
    for i,c in enumerate(pd):
        if comp[(i,0)] in keep and comp[(i,1)] in keep:retained.append(c)
        else:
            union(c[0],c[2]);union(c[1],c[3])
    labels={}
    def label(e):
        e=root(e)
        if e not in labels:labels[e]=len(labels)
        return labels[e]
    return [[label(e) for e in c] for c in retained]

def add_curl(pd,sign):
    pd=[list(c) for c in pd];occ=occurrences(pd);e=min(occ);new=max(occ)+1
    i,j=occ[e][1];pd[i][j]=new+1
    # Both choices insert one knot arc with exactly one R1 crossing.
    pd.append([e,new+1,new,new] if sign==1 else [e,new,new,new+1])
    return pd

def zero_writhe(pd):
    w=oriented_components(pd)['writhe']
    for _ in range(abs(w)):pd=add_curl(pd,-1 if w>0 else 1)
    assert oriented_components(pd)['writhe']==0
    return pd

def blackboard_parallel(pd,p):
    if p<1:raise ValueError('p must be positive')
    occ=occurrences(pd); nxt=0;ext={}
    for e,pair in sorted(occ.items()):
        ids=list(range(nxt,nxt+p));nxt+=p
        ext[pair[0]]=ids;ext[pair[1]]=ids[::-1]
    out=[]
    for i,c in enumerate(pd):
        # r increases from north to south; c increases west to east.
        horizontal={};vertical={}
        for r in range(p):
            for col in range(p-1):horizontal[r,col]=nxt;nxt+=1
        for r in range(p-1):
            for col in range(p):vertical[r,col]=nxt;nxt+=1
        for r in range(p):
            for col in range(p):
                west=ext[i,0][p-1-r] if col==0 else horizontal[r,col-1]
                north=ext[i,1][col] if r==0 else vertical[r-1,col]
                east=ext[i,2][r] if col==p-1 else horizontal[r,col]
                south=ext[i,3][p-1-col] if r==p-1 else vertical[r,col]
                out.append([west,north,east,south])
    occurrences(out)
    return out

def greedy_order(pd,seed):
    rng=random.Random(seed);n=len(pd);es=[Counter(c) for c in pd]
    unvisited=set(range(n));b=set();order=[];width=0;energy=0
    while unvisited:
        # Max overlap reduces the frontier first; random tie breaks.
        scores={i:len(b.symmetric_difference({e for e,v in es[i].items() if v%2})) for i in unvisited}
        best=min(scores.values());ties=[i for i in unvisited if scores[i]==best]
        i=rng.choice(sorted(ties));unvisited.remove(i);order.append(i)
        b.symmetric_difference_update({e for e,v in es[i].items() if v%2});width=max(width,len(b));energy+=2**(len(b)//2)
    assert not b
    return order,(width,energy)

def best_order(pd,seeds=100):
    best=None
    for seed in range(seeds):
        o,score=greedy_order(pd,seed)
        if best is None or score<best[0]:best=(score,o,seed)
    return {'order':best[1],'max_frontier':best[0][0],'energy':best[0][1],'seed':best[2],'seeds_tested':seeds}

def planar_order(pd,start,seed):
    """Greedy disk-frontier order, following Spherogram's consecutive-overlap
    construction (exhaust.py). Only the order is used by our independent DP.
    """
    rng=random.Random(seed);occ=occurrences(pd);across={}
    for a,b in occ.values():across[a]=b;across[b]=a
    frontier=[(start,j) for j in (3,2,1,0)];order=[start];visited={start};width=4;energy=4
    while len(order)<len(pd):
        overlaps=defaultdict(list)
        for i,cs in enumerate(frontier):overlaps[across[cs][0]].append(i)
        choices=[]
        for c,indices in overlaps.items():
            if c in visited:raise ValueError('Self-edge not supported by this layout heuristic')
            if indices==list(range(indices[0],indices[-1]+1)):choices.append((len(indices),indices[0],c))
        if not choices:raise ValueError('No consecutive extension')
        m=max(v[0] for v in choices);k,i,c=rng.choice([v for v in choices if v[0]==m])
        entry=across[frontier[i]][1]
        frontier[i:i+k]=[(c,(entry-s-1)%4) for s in range(4-k)]
        order.append(c);visited.add(c);width=max(width,len(frontier));energy+=2**(len(frontier)//2)
    assert not frontier
    return order,(width,energy)
