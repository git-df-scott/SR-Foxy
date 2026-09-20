"""Replay every elementary move, then check a component-coloured planar dart map."""
import json,hashlib,collections,copy,sys
from pathlib import Path
import regina,networkx as nx
p=Path(__file__).parent
n=int(sys.argv[1]) if len(sys.argv)>1 else 1

def replay(h,side):
 L=regina.Link.fromPD([[v+1 for v in row] for row in h['inputs'][side]])
 for step,move in enumerate(h['paths'][side]):
  kind,i,*rest=move
  assert 0<=i<L.size(),(step,move)
  assert getattr(L,f'r{kind}')(L.crossing(i),*rest),(step,move)
  assert L.countComponents()==4
 assert L.pd()==h['end_pd'][side]
 return L

def graph(L):
 pd=L.pdData();labels={e for row in pd for e in row};parent={e:e for e in labels}
 def root(e):
  while e!=parent[e]:e=parent[e]
  return e
 def union(a,b):parent[root(a)]=root(b)
 for a,b,c,d in pd:union(a,c);union(b,d)
 groups={r:[] for r in set(map(root,labels))}
 for e in labels:groups[root(e)].append(e)
 roots=sorted(groups,key=lambda r:min(groups[r]));col={e:roots.index(root(e)) for e in labels}
 G=nx.MultiDiGraph();occ={}
 for i,row in enumerate(pd):
  for j,e in enumerate(row):
   v=4*i+j;G.add_node(v,component=col[e],parity=j%2);G.add_edge(v,4*i+(j+1)%4,kind='r');occ.setdefault(e,[]).append(v)
 for e,ds in occ.items():
  assert len(ds)==2;a,b=ds;G.add_edge(a,b,kind='a');G.add_edge(b,a,kind='a')
 return G

h=json.loads((p/f'MOVIE_SEARCH_n{n}_rot.json').read_text())['hit'];A=replay(h,0);B=replay(h,1)
result={'status':'NO_COLOURED_ENDPOINT_MATCH','moves':[dict(collections.Counter(str(x[0]) for x in arr)) for arr in h['paths']],'end_crossings':[A.size(),B.size()],'scope':'Certifies two stored four-component surgery diagrams are isotopic with colours fixed; source transcription and full-twist convention remain external inputs.'}
for rotate in [False,True]:
 C=regina.Link(A)
 if rotate:C.rotate()
 G,H=graph(C),graph(B)
 gm=nx.algorithms.isomorphism.MultiDiGraphMatcher(G,H,node_match=nx.algorithms.isomorphism.categorical_node_match(['component','parity'],[-1,-1]),edge_match=nx.algorithms.isomorphism.categorical_multiedge_match('kind',None))
 if gm.is_isomorphic():
  result.update(status='PASS_COLOURED_REIDEMEISTER_CERTIFICATE',rotate_first_endpoint=rotate,dart_bijection={str(k):v for k,v in gm.mapping.items()});break
# Deliberately impossible crossing index must be rejected by the verifier.
bad=copy.deepcopy(h);bad['paths'][0][0][1]=10**6
try:replay(bad,0)
except AssertionError:result['invalid_move_rejected']=True
else:raise AssertionError('Invalid move accepted')
(p/f'SOURCE_MOVIE_CERTIFICATE_n{n}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='dart_bijection'}))
assert result['status']=='PASS_COLOURED_REIDEMEISTER_CERTIFICATE'
