#!/usr/bin/env python3
"""Cyclic-cover H1 directly from PD, without a knot or 3-manifold package.

Contract a spanning tree in the lifted Wirtinger presentation complex.
The remaining signed edge counts give an integral relation matrix for H1.
SymPy supplies only integer Smith normal form. All meridians map to +1.
This computes a KNOT INVARIANT, not a smooth concordance obstruction.
"""
from __future__ import annotations
from collections import defaultdict
import json
from pathlib import Path
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

def require(x,message):
    if not x: raise ValueError(message)

def wirtinger(pd):
    require(bool(pd),'Nonempty diagram required')
    occ=defaultdict(list)
    for c,row in enumerate(pd):
        require(len(row)==4,'PD row is not four-valent')
        for p,e in enumerate(row):occ[e].append((c,p))
    require(all(len(v)==2 for v in occ.values()),'Each arc must occur twice')
    adj={a:b for pair in occ.values() for a,b in [pair,pair[::-1]]}
    ports=sorted(adj);seen=set();incoming=set();components=0
    for start in ports:
        if start in seen:continue
        components+=1;x=start;visited=set()
        while x not in visited:
            visited.add(x);incoming.add(x);c,p=x;other=(c,(p+2)%4)
            seen.update([x,other]);x=adj[other]
        require(x==start,'Strand failed to close')
    require(components==1,'Expected one knot component')
    parent={x:x for x in ports}
    def root(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a,b=root(a),root(b)
        if a!=b:parent[max(a,b)]=min(a,b)
    for a,b in adj.items():union(a,b)
    for c in range(len(pd)):union((c,1),(c,3))
    roots=sorted({root(x) for x in ports});ids={x:i for i,x in enumerate(roots)}
    arc={p:ids[root(p)] for p in ports};rels=[];crossing_data=[]
    for c in range(len(pd)):
        inc={p for p in range(4) if (c,p) in incoming}
        require(inc in ({0,3},{1,2},{0,1},{2,3}),'Crossing orientation is invalid')
        sign=1 if inc in ({0,3},{1,2}) else -1
        u=next(p for p in (0,2) if (c,p) in incoming);v=(u+2)%4
        a,b,o=arc[c,u]+1,arc[c,v]+1,arc[c,1]+1
        rels.append([-sign*o,a,sign*o,-b])
        crossing_data.append({'crossing':c,'incoming_under_port':u,'sign':sign,'under_in':a,'under_out':b,'over':o})
    require(len(roots)==len(pd),'Unexpected Wirtinger-generator count')
    # Euler characteristic of the ribbon rotation system, not a visual guess.
    faces=[];seen=set()
    for a in ports:
        if a in seen:continue
        face=[];x=a
        while x not in seen:
            seen.add(x);face.append(list(x));c,p=adj[x];x=(c,(p+1)%4)
        require(x==a,'Invalid face permutation')
        faces.append(face)
    require(len(pd)-len(occ)+len(faces)==2,'PD rotation system is not a sphere')
    return {'generator_count':len(roots),'relators':rels,'crossing_data':crossing_data,'faces':faces}

def cover_matrix(presentation,degree):
    require(isinstance(degree,int) and degree>=1,'Positive covering degree required')
    n=presentation['generator_count'];tree={(s,0) for s in range(degree-1)}
    edges=[(s,g) for s in range(degree) for g in range(n) if (s,g) not in tree]
    index={e:i for i,e in enumerate(edges)};rows=[]
    for start in range(degree):
        for word in presentation['relators']:
            sheet=start;row=[0]*len(edges)
            for x in word:
                if x>0:edge=(sheet,x-1);sheet=(sheet+1)%degree;sign=1
                else:sheet=(sheet-1)%degree;edge=(sheet,-x-1);sign=-1
                if edge not in tree:row[index[edge]]+=sign
            require(sheet==start,'Lifted relator does not close')
            rows.append(row)
    return rows,edges,sorted(tree)

def calculate(pd,degree=4,certificate=False):
    presentation=wirtinger(pd);rows,edges,tree=cover_matrix(presentation,degree)
    M=Matrix(rows)
    if certificate:
        dm=DomainMatrix.from_Matrix(M).convert_to(ZZ)
        D,U,V=smith_normal_decomp(dm);dm=D.to_Matrix();u=U.to_Matrix();v=V.to_Matrix()
        require(u*M*v==dm,'Smith multiplication certificate failed')
        require(abs(u.det(method='domain-ge'))==1 and abs(v.det(method='domain-ge'))==1,'Smith transformations not unimodular')
    else:dm=smith_normal_form(M,domain=ZZ)
    diag=[int(dm[i,i]) for i in range(min(dm.shape))];rank=sum(x!=0 for x in diag)
    factors=[abs(x) for x in diag if abs(x)>1]+[0]*(len(edges)-rank)
    nonzero=[abs(x) for x in diag if x]
    require(all(b%a==0 for a,b in zip(nonzero,nonzero[1:])),'Smith diagonal not in divisibility order')
    result={'degree':degree,'h1_elementary_divisors':factors,'matrix_shape':list(M.shape),'smith_diagonal':diag,'spanning_tree_edges':[list(e) for e in tree]}
    if certificate:
        result.update(pd=pd,presentation=presentation,non_tree_edges=[list(e) for e in edges],relation_matrix=rows,left_unimodular=u.tolist(),right_unimodular=v.tolist())
        result=json.loads(json.dumps(result,default=int))
    return result

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('--degree',type=int,default=4);ap.add_argument('--certificate',action='store_true');a=ap.parse_args()
    data=json.loads(a.input.read_text());p=data if isinstance(data,list) else data['pd']
    print(json.dumps(calculate(p,a.degree,a.certificate),indent=2))
