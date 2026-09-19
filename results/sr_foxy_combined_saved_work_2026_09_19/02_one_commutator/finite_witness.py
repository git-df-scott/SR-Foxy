#!/usr/bin/env python3
"""Exact finite representation; reads only. Print a witness to stdout."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
d=json.loads((P/'inputs_extended.json').read_text())
c=json.loads((P/'boundary_handle_certificate.json').read_text())
def mm(A,B,p):return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%p for i in range(2) for j in range(2))
def inv(A,p):return (A[3],-A[1]%p,-A[2]%p,A[0])
def value(w,im,p):
 a=(1,0,0,1)
 for x in w:a=mm(a,im[abs(x)] if x>0 else inv(im[-x],p),p)
 return a
out=[]
for p,z in [(11,6),(17,1),(17,9),(23,5),(23,21)]:
 im={1:(1,1,0,1),2:(1,0,z,1)};I=(1,0,0,1)
 for a,b,x,s in d['source_matrix_propagation']:
  h=im[b] if s==1 else inv(im[b],p)
  im[a]=mm(mm(h,im[x],p),inv(h,p),p)
 if any(value(r,im,p)!=I for r in d['source_relators']):raise ValueError('bad source representation')
 bim={int(k)+1:value(w,im,p) for k,w in d['q0_images'].items()}
 rels=[[-s*(b+1),i+1,s*(b+1),-o-1] for i,o,b,s,cross in d['boundary_relations']]
 if any(value(r,bim,p)!=I for r in rels):raise ValueError('bad boundary representation')
 A,B=[value(c['pairs'][0][key],bim,p) for key in ('a','b')]
 v=value(d['original_boundary_delta'],bim,p)
 if v!=value(d['boundary_delta_short'],bim,p):raise ValueError('delta input mismatch')
 if v!=mm(mm(mm(A,B,p),inv(A,p),p),inv(B,p),p):raise ValueError('commutator mismatch')
 rec={'prime':p,'z':z,'source_images':im,'boundary_images':bim,'A':A,'B':B,'delta':v,'delta_nontrivial':v!=I,'source_relators_checked':len(d['source_relators']),'boundary_relators_checked':len(rels)}
 out.append(rec)
print(json.dumps({'witnesses':out,'CE':False,'scope':'Finite representation nontriviality of specified boundary word; not an annulus obstruction or proof of geometric q0'},indent=2))
