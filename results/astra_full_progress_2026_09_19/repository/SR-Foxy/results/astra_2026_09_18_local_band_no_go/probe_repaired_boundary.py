#!/usr/bin/env python3
"""Astra: exact local-family audit. Reads repository inputs; prints JSON only."""
import json, hashlib
from pathlib import Path
if not __debug__:raise RuntimeError("Assertions must be enabled")
REPO=Path(__file__).resolve().parents[2]
PINNED={
  "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py": "66cc09e760cbfbb6a41cc725972fb86e8af49cc3",
  "results/astra_2026_09_17_overnight/pass06_0055_explicit_unlink_bands/check_explicit_unlink_bands.py": "baf481237bbbcd9ab57c3c378a6fc8e34286c0ef",
  "results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json": "86bb4e5ec1ae5a1762f4ce724279c7c5a509fed6"
}
def pinned(path):
 raw=(REPO/path).read_bytes()
 assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==PINNED[path],path
 return raw.decode()
CORE=pinned("results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py")

import types,json,signal,inspect
import snappy
g=types.ModuleType('core');exec(CORE,g.__dict__)
g.BAND1['arc_is_under']=[False,True]
g.BAND2['arc_is_under']=[True,False]
A=g.adjacency_from_pd(g.SCAFFOLD)
D=g.add_zero_twist_band(g.add_zero_twist_band(A,g.BAND1),g.BAND2)
cs,cmap,inc,sign=g.oriented_component_data(D)
edge={};n=0
for c in sorted(D):
    for p in range(4):
        if (c,p) not in edge:
            edge[c,p]=edge[D[c][p]]=n;n+=1
pd=[[edge[c,p] for p in range(4)] for c in sorted(D)]
L=snappy.Link(pd)
cusp_map=[]
for comp in L.link_components:
    ids={cmap[x.crossing.label,x.strand_index] for x in comp}
    assert len(ids)==1;cusp_map.append(next(iter(ids)))
assert sorted(cusp_map)==[0,1,2]
M=L.exterior()
print(json.dumps({'snappy_version':snappy.__version__,'cusp_map':cusp_map,'crossings':len(pd),'linking_matrix':L.linking_matrix(),'exterior_to_link_signature':str(inspect.signature(M.exterior_to_link))}),flush=True)
def timeout(*args):raise TimeoutError('20 second triangulation/diagram conversion cap')
signal.signal(signal.SIGALRM,timeout)
out=[]
for param in [1]:
    X=M.copy()
    for cusp,comp in enumerate(cusp_map):
        if comp: X.dehn_fill((1 if comp==1 else -1,param),cusp)
    item={'parameter':param,'input_triangulation':X.triangulation_isosig(decorated=True),'remaining_cusp':cusp_map.index(0)}
    print(json.dumps({'starting_parameter':param}),flush=True)
    try:
        signal.alarm(20)
        Y=X.filled_triangulation()
        item['filled_triangulation']=Y.triangulation_isosig(decorated=True)
        K=Y.exterior_to_link(seed=1729, pachner_search_tries=1)
        K.simplify('global')
        item['deconnect_sum_crossings']=[len(p.crossings) for p in K.deconnect_sum()]
        item.update({'status':'DIAGRAM_RECOVERED','pd_code':K.PD_code(),'crossings':len(K.crossings),'components':len(K.link_components)})
    except Exception as e:item.update({'status':'UNKNOWN','reason':type(e).__name__+': '+str(e)})
    finally:signal.alarm(0)
    out.append(item)
    print(json.dumps(item),flush=True)
