#!/usr/bin/env python3
"""Produce a finite, replayable group identity. No topology engine required.
Usage: python build_certificate.py > fresh_certificate.json
Reads fixed local inputs; never edits the repository or writes output itself.
"""
import hashlib,json
from functools import lru_cache
from pathlib import Path
from free_words import red,inv,mul,sub,eliminate
ROOT=Path(__file__).resolve().parent
raw=(ROOT/'inputs_extended.json').read_bytes();d=json.loads(raw)
rels=[[-s*(b+1),i+1,s*(b+1),-o-1] for i,o,b,s,c in d['boundary_relations']]
gens,remaining,images,steps=eliminate(rels[1:9],keep=(3,))
if gens!={3,5} or len(remaining)!=1:raise ValueError('Unexpected Tietze result')
# Actual final factors discovered by the bounded cut search.
a=[4,-3,-3,1];b=[4,-9,-1,3,-1,8,-5,-8,1,1]
O=20

def schreier(w):
    height=0;letters=[]
    for x in w:
        if abs(x) not in (3,5):raise ValueError('Unexpected generator')
        if abs(x)==5:
            k=height if x>0 else height-1
            if k+O<=0:raise ValueError('Schreier encoding out of range')
            letters.append((k+O)*(1 if x>0 else -1))
        height+=1 if x>0 else -1
    if height:raise ValueError('Nonzero total exponent')
    return red(letters)

r=schreier(remaining[0]);lo,hi=-1,2
rules={}
@lru_cache(None)
def evaluate_y(k):
    if lo<=k<=hi:return (k-lo+1,)
    sh=k-2 if k>hi else k+2
    shifted=tuple((abs(x)+sh)*(1 if x>0 else -1) for x in r)
    positions=[i for i,x in enumerate(shifted) if abs(x)==k+O]
    if len(positions)!=1:raise ValueError('Unique-extremum condition failed')
    i=positions[0]
    rhs=inv(shifted[i+1:]+shifted[:i])
    if shifted[i]<0:rhs=inv(rhs)
    result=red(q for x in rhs for q in (evaluate_y(abs(x)-O) if x>0 else inv(evaluate_y(abs(x)-O))))
    rules[k]={'level':k,'relator_shift':sh,'shifted_relator':shifted,
              'occurrence':i,'replacement':rhs,'basis_image':result}
    return result

def in_basis(w):
    return red(q for x in w for q in (evaluate_y(abs(x)-O) if x>0 else inv(evaluate_y(abs(x)-O))))
words={}
for name,w in [('original_delta',d['original_boundary_delta']),('short_delta',d['boundary_delta_short']),('A',a),('B',b)]:
    tw=sub(w,images);sw=schreier(tw);fw=in_basis(sw)
    words[name]={'boundary_word':w,'two_generator_word':tw,'schreier_word':sw,'basis_word':fw}
f=words['A']['basis_word'];g=words['B']['basis_word']
comm=mul(f,g,inv(f),inv(g))
if words['original_delta']['basis_word']!=comm or words['short_delta']['basis_word']!=comm:
    raise ValueError('Final free identity failed')
if any(sum(1 if x>0 else -1 for x in w)!=0 for w in (a,b)):raise ValueError('Nonzero handle exponent')
cert={'format':'sr-foxy-one-commutator-v1','source_commit':d['source_commit'],
      'input_sha256':hashlib.sha256(raw).hexdigest(),
      'claim':'original boundary correction delta = [A,B] in the supplied boundary presentation',
      'commutator_convention':'[A,B]=A B A^-1 B^-1',
      'original_boundary_relators':rels,'relators_used_indices':list(range(1,9)),
      'tietze_steps':steps,'tietze_images':images,'remaining_relator':remaining[0],
      'schreier_meridian':3,'schreier_other_generator':5,'schreier_offset':O,
      'schreier_definition':'y_k=x3^k x5 x3^(-k-1)',
      'schreier_relator':r,'basis_levels':[lo,hi],
      'finite_schreier_rules':[rules[k] for k in sorted(rules)],'words':words,
      'commutator_expansion_basis':comm,'CE':False,
      'limits':['This is an identity in the specified presentation, not a geometric marked inclusion.',
                'One commutator supplies a genus-one mapped correction, not an embedded modifying annulus.',
                'A different realization of the same correction word may change the surgery boundary.']}
print(json.dumps(cert,indent=2))
