#!/usr/bin/env python3
"""Edge-faithful replacement for Spherogram 2.4.1 simple_bands.

It retains the source's augmented-vertex-simple path rule, twist parity and
nonminimality rule, but pins the actual attaching arcs and enumerates every
interior parallel dual edge. It returns unique Band descriptors. This is a
finite search-box expansion, NOT a claim of completeness up to band isotopy.

Use explicitly, or pass the function where an application accepts a band
builder. No installed package is patched by importing this module.
"""
from __future__ import annotations
from itertools import permutations,product
from spherogram.links.bands.core import (Band,dual_graph_as_nx,
    crossing_labels_are_normalized)
import networkx as nx

def simple_bands_multiedge(link,max_twists=2,max_band_len=None):
 if not crossing_labels_are_normalized(link):raise ValueError('Link needs normalized crossing labels')
 if max_twists<0:raise ValueError('max_twists must be nonnegative')
 if max_band_len is not None and max_band_len<2:return []
 dual=dual_graph_as_nx(link,graph_class=nx.MultiGraph);cs_to_face={}
 for f,g,info in dual.edges(data=True):
  for h,cs in info['interface'].items():cs_to_face[cs]=h
 cutoff=None if max_band_len is None else max_band_len-2
 ans={}
 for component in link.link_components:
  for cs0,cs1 in permutations(component,2):
   f0s=[cs_to_face[cs0],cs_to_face[cs0.opposite()]]
   f1s=[cs_to_face[cs1],cs_to_face[cs1.opposite()]]
   for F0,F1 in product(f0s,f1s):
    P0=f0s[1] if F0==f0s[0] else f0s[0]
    P1=f1s[1] if F1==f1s[0] else f1s[0]
    # These are exactly the forbidden repeats in the augmented vertex path.
    if P0==P1 or F0 in (P0,P1) or F1 in (P0,P1):continue
    X=cs0 if cs_to_face[cs0]==F0 else cs0.opposite()
    Z=cs1 if cs_to_face[cs1]==P1 else cs1.opposite()
    def paths(f,visited,steps):
     if f==F1:
      yield steps;return
     if cutoff is not None and len(steps)>=cutoff:return
     for g in sorted(dual[f]):
      if g in visited or g in (P0,P1):continue
      for key,info in dual[f][g].items():
       yield from paths(g,visited|{g},steps+[info['interface'][g]])
    for interior in paths(F0,{F0},[]):
     top=[X]+interior+[Z]
     desc=[(cs.crossing.label,cs.strand_index) for cs in top]
     parity=int((X==X.oriented())==(Z==Z.oriented()))
     for tw in range(-max_twists,max_twists+1):
      if tw%2!=parity:continue
      for bits in range(1<<len(interior)):
       band=Band(desc,bits,tw)
       if band.is_nonminimal(link):continue
       ans[band.compressed_spec()]=band
 return sorted(ans.values())
