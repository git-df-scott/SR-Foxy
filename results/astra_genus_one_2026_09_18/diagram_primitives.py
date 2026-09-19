"""Transcribed marked scaffold and independently coded diagram primitives.
Source: git-df-scott/SR-Foxy, ceb83c2, archived pass09 diagram_core.py.
The selected PD and band values are literal transcriptions; this is NOT a
byte-identical copy of the source file. Tests compare the resulting marked
relations and axis words to the previously archived input certificate.
"""
from collections import defaultdict
SCAFFOLD=[[31,22,32,23],[19,66,20,67],[1,18,2,19],[0,8,1,7],[6,0,7,67],[30,4,31,3],[29,85,30,84],[28,68,29,75],[27,10,28,11],[81,27,82,26],[72,26,73,25],[13,24,14,25],[2,24,3,23],[86,21,87,22],[20,87,21,76],[69,16,70,17],[78,17,79,18],[15,70,16,71],[14,79,15,80],[73,12,74,13],[82,11,83,12],[68,10,69,9],[77,9,78,8],[5,77,6,76],[85,5,86,4],[83,75,84,74],[71,81,72,80],[41,33,42,32],[65,45,66,44],[45,63,46,62],[56,63,57,64],[64,57,65,58],[60,33,61,34],[103,35,104,34],[94,36,95,35],[53,37,54,36],[37,101,38,100],[38,92,39,91],[39,51,40,50],[40,61,41,62],[42,105,43,106],[106,43,107,44],[47,88,48,89],[46,97,47,98],[89,48,90,49],[98,49,99,50],[51,92,52,93],[52,101,53,102],[54,88,55,95],[55,97,56,96],[107,59,96,58],[59,105,60,104],[93,102,94,103],[99,90,100,91]]
BAND1={'along_top':[(15,2),(16,2),(2,2),(41,0)],'arc_is_under':[False,True]}
BAND2={'along_top':[(13,2),(27,0),(32,2),(52,0)],'arc_is_under':[True,False]}
def adjacency(pd):
 occ=defaultdict(list)
 for c,row in enumerate(pd):
  for p,e in enumerate(row):occ[e].append((c,p))
 a={c:[None]*4 for c in range(len(pd))}
 for edge,pair in occ.items():
  if len(pair)!=2:raise ValueError('bad incidence')
  u,v=pair;a[u[0]][u[1]]=v;a[v[0]][v[1]]=u
 return a

def connect(a,u,v):a[u[0]][u[1]]=v;a[v[0]][v[1]]=u

def band(a,bb):
 a={k:v[:] for k,v in a.items()}; path=bb['along_top'];bits=bb['arc_is_under'];X,Z=path[0],path[-1];Y,W=a[X[0]][X[1]],a[Z[0]][Z[1]]
 mids=path[1:-1];opps=[a[c][p] for c,p in mids];nextid=max(a)+1;Bs=list(range(nextid,nextid+len(mids)));Cs=list(range(nextid+len(mids),nextid+2*len(mids)))
 for c in Bs+Cs:a[c]=[None]*4
 for j,((ac,ap),(dc,dp)) in enumerate(zip(mids,opps)):
  B,C=Bs[j],Cs[j]
  if bits[j]:connect(a,(ac,ap),(B,2));connect(a,(dc,dp),(C,0));connect(a,(B,0),(C,2))
  else:connect(a,(ac,ap),(B,3));connect(a,(dc,dp),(C,1));connect(a,(B,1),(C,3))
 u,v=X,Y
 for j,bit in enumerate(bits):
  B,C=Bs[j],Cs[j]
  if bit:connect(a,u,(B,3));connect(a,v,(C,3));u,v=(B,1),(C,1)
  else:connect(a,u,(B,0));connect(a,v,(C,0));u,v=(B,2),(C,2)
 connect(a,u,Z);connect(a,v,W)
 return a

def compdata(a):
 unvisited={(c,p) for c in a for p in range(4)};cs=[];incoming=set();cm={}
 while unvisited:
  start=min(unvisited);cur=start;oriented=[]
  while cur not in incoming:
   oriented.append(cur);incoming.add(cur);c,p=cur;cur=a[c][(p+2)%4]
  cc=set(oriented)|{(c,(p+2)%4) for c,p in oriented};cs.append(cc);unvisited-=cc
  for x in cc:cm[x]=len(cs)-1
 signs={}
 for c in a:
  inc={p for p in range(4) if (c,p) in incoming}
  signs[c]=1 if inc in ({0,3},{1,2}) else -1 if inc in ({0,1},{2,3}) else None
  if signs[c] is None:raise ValueError('bad crossing')
 return cs,cm,incoming,signs

def Rdata(a):
 cs,cm,incoming,signs=compdata(a);parent={x:x for x in cs[0]}
 def root(x):
  if parent[x]!=x:parent[x]=root(parent[x])
  return parent[x]
 def join(u,v):
  u,v=root(u),root(v)
  if u!=v:parent[u]=v
 for x in list(parent):join(x,a[x[0]][x[1]])
 for c in a:
  co={cm[c,p] for p in range(4)}
  if 0 not in co:continue
  if co=={0}:join((c,1),(c,3))
  else:
   pp=[p for p in range(4) if cm[c,p]==0];join((c,pp[0]),(c,pp[1]))
 roots=sorted({root(x) for x in parent});rid={x:i for i,x in enumerate(roots)};arcs={x:rid[root(x)] for x in parent};rels=[]
 for c in a:
  if all(cm[c,p]==0 for p in range(4)):
   ui=next(p for p in (0,2) if (c,p) in incoming);rels.append([arcs[c,ui],arcs[c,(ui+2)%4],arcs[c,1],signs[c],c])
 return {'arcs':arcs,'relations':rels,'components':cs,'incoming':incoming,'signs':signs,'cmap':cm}

def build():
 a=adjacency(SCAFFOLD);q0=Rdata(a);a=band(band(a,BAND1),BAND2);q=Rdata(a);mp={}
 for x,f in q['arcs'].items():
  if x in q0['arcs']:
   if f in mp and mp[f]!=q0['arcs'][x]:raise ValueError('arc mismatch')
   mp[f]=q0['arcs'][x]
 words=[]
 for ci in (1,2):
  cur=min(q['components'][ci]);seen=set();w=[]
  while cur not in seen:
   seen.add(cur);c,p=cur
   if p in (0,2) and q['cmap'][c,1]==0:w.append((mp[q['arcs'][c,1]]+1)*q['signs'][c])
   cur=a[c][(p+2)%4]
  words.append(w)
 return a,q,mp,words
