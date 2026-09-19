#!/usr/bin/env python3
import json
from pathlib import Path
import numpy as np
from polygon_diagram import project,reduce_gauss,sublink
P=Path(__file__).resolve().parent
def red(w):
 out=[]
 for x in w:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return out
def inverse(w):return [-x for x in w[::-1]]
d=json.loads((P/'spatial_model.json').read_text());b=np.array(d['base_components'][2]);k=np.array(d['correction_boundary']);eps=d['band_half_width']
cb=(b[-1]+b[0])/2;ck=(k[-1]+k[0])/2;wb=(b[0]-b[-1])/40;wk=np.array([0.,1.,0.])
core=[cb,np.array([*cb[:2],600.]),np.array([ck[0]-10,ck[1],600.]),np.array([ck[0]-10,ck[1],ck[2]]),ck]
frames=[wb,wk,wk,wk,wk];plus=[c+eps*w for c,w in zip(core,frames)];minus=[c-eps*w for c,w in zip(core,frames)]
# Start at the old axis immediately before the inserted correction.
new=[minus[0]]+minus[1:]+list(k)+[plus[-1]]+plus[-2::-1]+list(b)
polys=d['base_components'][:2]+[[x.tolist() for x in new]]
result={'status':'EXPLICIT_POLYGON_SURGERY_INPUT_PENDING_CHECKS','source_commit':d['source_commit'],'components':polys,'splice_core':[x.tolist() for x in core],'splice_width_vectors':[x.tolist() for x in frames],'splice_half_width':eps,'orientation':'b_prime = correction_boundary then old b, based at the incoming old-axis splice endpoint','preferred_surgery_slopes':{'axis_a':[1,1],'axis_b_prime':[-1,1]},'basepoint_indices':[0,0,0]}
(P/'surgery_link.json').write_text(json.dumps(result,indent=2)+'\n')
pd=project(polys);cs={x['id']:x for x in pd['crossings']};ww=[]
for ci in [1,2]:
 w=[]
 for ii,kind,s in pd['gauss_words'][ci]:
  x=cs[ii]
  if kind=='U' and x['over'][0]==0:w.append(s*d['base_segment_generators'][0][x['over'][1]])
 ww.append(red(w))
A=d['A_word'];B=d['B_word'];comm=red(A+B+inverse(A)+inverse(B));old=json.loads((P/'prior/astra_one_commutator_2026_09_18/inputs_extended.json').read_text())
expected=[old['axis1'],red(comm+old['axis2'])]
pd['read_marked_axis_words']=ww;pd['expected_marked_axis_words']=expected;pd['word_checks']=[ww[i]==expected[i] for i in range(2)];pd['auxiliary_gauss_reduction']=reduce_gauss(sublink(pd,[1,2]));pd['surgery_slopes']=[[1,1],[-1,1]]
(P/'surgery_diagram.json').write_text(json.dumps(pd,indent=2)+'\n')
print('surgery crossings',len(pd['crossings']),'word checks',pd['word_checks'],flush=True);print('actual words',ww,flush=True);print('expected',expected,flush=True);print('auxiliary remainingcr',sum(len(w) for w in pd['auxiliary_gauss_reduction']['remaining'])//2)
