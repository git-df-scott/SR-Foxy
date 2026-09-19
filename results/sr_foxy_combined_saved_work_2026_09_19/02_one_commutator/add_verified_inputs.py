"""Record selected fields actually read from pinned GitHub sources.
These are transcribed integer fields, not byte-identical remote files.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
d=json.loads((P/'inputs.json').read_text())
s=[6,-5,-8,5,6,-5,8,5,-6,-5,6,-5,-8,5,-6,5,-6,8,
6,-5,8,5,-6,-8,5,6,-5,8,5,-6,-5,6,-5,-8,5,-6,
5,6,-5,8,5,-6,5,6,-5,-8,5,-6,-5,8,6,-5,-8,-8,
5,-6,-8,6,-5,8,6,-5,8,5,-6,-8,5,6,-5,8,5,-6,
-5,6,-5,-8,5,-6,-5,6,-5,8,5,-6,5,6,-5,-8,5,-6,
-5,8,6,-5,8,5,-6,5,6,-5,-8,5,-6,-6]
if len(s)!=104:raise ValueError('source transcription length mismatch')
lift={5:3,6:4,8:8}
d['original_boundary_delta']=[(1 if x>0 else -1)*lift[abs(x)] for x in s]
d['original_source_delta']=s
d['original_delta_blob_sha1']='61b9d404f3ac98b2e97e8424d9550b483e8f34ce'
d['original_delta_path']='results/night_2026_09_18/word_correction.json'
d['q0_images']={
0:[6,-5,8,5,-6,5,6,-5,-8,5,-6],1:[-5,8,5],2:[5],3:[6],
4:[6,-5,8,5,-6],5:[6,-5,8,6,-5,8,5,-6,-8,5,-6],
6:[6,-5,8,5,-6,-5,6,-5,8,5,-6,5,6,-5,-8,5,-6],7:[8],
8:[6,-5,8,5,6,-5,-8,5,-6],9:[6,-5,8,5,-6,5,6,-5,-8,5,-6],
10:[8],11:[5,6,-5,8,5,-6,-5],12:[5,6,-5],
13:[6,-5,8,5,-6,-8,5,6,-5,8,5,-6,-5,6,-5,-8,5,-6,5,6,-5,8,5,-6,5,6,-5,-8,5,-6,-5,8,6,-5,-8,5,-6],
14:[6,-5,8,5,-6],15:[6,-5,8,5,-6,-8,5,-6,8],16:[5],17:[-8,5,6,-5,8]}
d['source_matrix_propagation']=[[3,2,1,1],[5,3,2,-1],[6,2,5,-1],[4,6,3,-1],[9,3,6,1],[7,9,1,1],[8,2,9,1]]
d['axis1']=[4,-1,3,-4,11,14,-15,-11,1,-9]
d['axis2']=[4,-1,-15,14,-13,17,3,-4]
d['seam_meridian']=5
# Output separate from the original input snapshot.
(P/'inputs_extended.json').write_text(json.dumps(d,indent=2)+'\n')
