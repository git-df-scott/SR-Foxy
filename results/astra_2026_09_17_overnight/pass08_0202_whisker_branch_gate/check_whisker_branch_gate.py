#!/usr/bin/env python3
"""Exact SL(2,F5) branch gate for the pass06/pass07 crossed-axis bands.

This deliberately does not guess the missing based lower-to-upper whisker map.
It enumerates every finite-quotient branch compatible with the recorded
free-homotopy witness data and asks which branches separate eta1 from eta2.
"""
from collections import defaultdict, Counter
import json

MOD=5
SOURCE_COMMIT='0439e8fa002f2c107fa699df6e57e5a313ffd23a'
BAND1={'along_top':[(15,2),(16,2),(2,2),(41,0)],'arc_is_under':[False,False],'twist':0,'compressed_spec':'a40a423e_0_0'}
BAND2={'along_top':[(13,2),(27,0),(32,2),(52,0)],'arc_is_under':[False,False],'twist':0,'compressed_spec':'d0826c36_0_0'}
SCAFFOLD=[
[31,22,32,23],[19,66,20,67],[1,18,2,19],[0,8,1,7],[6,0,7,67],[30,4,31,3],
[29,85,30,84],[28,68,29,75],[27,10,28,11],[81,27,82,26],[72,26,73,25],[13,24,14,25],
[2,24,3,23],[86,21,87,22],[20,87,21,76],[69,16,70,17],[78,17,79,18],[15,70,16,71],
[14,79,15,80],[73,12,74,13],[82,11,83,12],[68,10,69,9],[77,9,78,8],[5,77,6,76],
[85,5,86,4],[83,75,84,74],[71,81,72,80],[41,33,42,32],[65,45,66,44],[45,63,46,62],
[56,63,57,64],[64,57,65,58],[60,33,61,34],[103,35,104,34],[94,36,95,35],[53,37,54,36],
[37,101,38,100],[38,92,39,91],[39,51,40,50],[40,61,41,62],[42,105,43,106],[106,43,107,44],
[47,88,48,89],[46,97,47,98],[89,48,90,49],[98,49,99,50],[51,92,52,93],[52,101,53,102],
[54,88,55,95],[55,97,56,96],[107,59,96,58],[59,105,60,104],[93,102,94,103],[99,90,100,91]]
MERIDIAN=(4,1,2,2); I=(1,0,0,1)

def mm(A,B):
 a,b,c,d=A;e,f,g,h=B
 return ((a*e+b*g)%5,(a*f+b*h)%5,(c*e+d*g)%5,(c*f+d*h)%5)
def inv(A):a,b,c,d=A;return(d%5,(-b)%5,(-c)%5,a%5)
def pw(A,n):
 if n<0:return pw(inv(A),-n)
 r=I
 while n:
  if n&1:r=mm(r,A)
  A=mm(A,A);n//=2
 return r
def tr(A):return(A[0]+A[3])%5
def order(A):
 r=I
 for k in range(1,121):
  r=mm(r,A)
  if r==I:return k
 raise RuntimeError('bad order')
def sl2():
 out=[]
 for a in range(5):
  for b in range(5):
   for c in range(5):
    for d in range(5):
     if (a*d-b*c)%5==1:out.append((a,b,c,d))
 assert len(out)==120;return out
G=sl2()
def conj(A,B):
 bi=inv(B)
 return any(mm(mm(inv(X),A),X) in (B,bi) for X in G)

def adjacency(pd):
 occ=defaultdict(list)
 for c,row in enumerate(pd):
  for p,e in enumerate(row):occ[e].append((c,p))
 assert all(len(v)==2 for v in occ.values())
 A={c:[None]*4 for c in range(len(pd))}
 for a,b in occ.values():A[a[0]][a[1]]=b;A[b[0]][b[1]]=a
 return A
def components(A):
 nodes={(c,p) for c in A for p in range(4)};seen=set();out=[]
 for start in sorted(nodes):
  if start in seen:continue
  cc=set();stack=[start]
  while stack:
   x=stack.pop()
   if x in cc:continue
   cc.add(x);seen.add(x);c,p=x
   for y in (A[c][p],(c,(p+2)%4)):
    if y not in cc:stack.append(y)
  out.append(cc)
 return out
def oriented(A):
 cs=components(A);cmap={};incoming=set()
 for i,cc in enumerate(cs):
  for x in cc:cmap[x]=i
  cur=min(cc)
  while cur not in incoming:
   incoming.add(cur);c,p=cur;cur=A[c][(p+2)%4]
 signs={}
 for c in A:
  s={p for p in range(4) if (c,p) in incoming}
  signs[c]=1 if s in ({0,3},{1,2}) else -1 if s in ({0,1},{2,3}) else None
  assert signs[c] is not None,(c,s)
 return cs,cmap,incoming,signs
def connect(A,a,b):A[a[0]][a[1]]=b;A[b[0]][b[1]]=a
def band(A,B):
 A={c:list(v) for c,v in A.items()};along=B['along_top'];bits=B['arc_is_under']
 X,Z=along[0],along[-1];Y,W=A[X[0]][X[1]],A[Z[0]][Z[1]];mid=along[1:-1];opp=[A[c][p] for c,p in mid]
 n=max(A)+1;Bs=list(range(n,n+len(mid)));Cs=list(range(n+len(mid),n+2*len(mid)))
 for c in Bs+Cs:A[c]=[None]*4
 for i,((ac,ap),(dc,dp)) in enumerate(zip(mid,opp)):
  b,c=Bs[i],Cs[i]
  if bits[i]:connect(A,(ac,ap),(b,2));connect(A,(dc,dp),(c,0));connect(A,(b,0),(c,2))
  else:connect(A,(ac,ap),(b,3));connect(A,(dc,dp),(c,1));connect(A,(b,1),(c,3))
 upper,lower=X,Y
 for i,bit in enumerate(bits):
  b,c=Bs[i],Cs[i]
  if bit:connect(A,upper,(b,3));connect(A,lower,(c,3));upper,lower=(b,1),(c,1)
  else:connect(A,upper,(b,0));connect(A,lower,(c,0));upper,lower=(b,2),(c,2)
 connect(A,upper,Z);connect(A,lower,W);return A

def quotient(A):
 cs,cmap,incoming,signs=oriented(A);parent={x:x for x in cs[0]}
 def root(x):
  if parent[x]!=x:parent[x]=root(parent[x])
  return parent[x]
 def union(a,b):
  a,b=root(a),root(b)
  if a!=b:parent[a]=b
 for x in list(parent):
  y=A[x[0]][x[1]]
  if y in parent:union(x,y)
 for c in A:
  comp={cmap[(c,p)] for p in range(4)}
  if 0 not in comp:continue
  if comp=={0}:union((c,1),(c,3))
  else:
   rp=[p for p in range(4) if cmap[(c,p)]==0];assert len(rp)==2 and abs(rp[0]-rp[1])==2
   union((c,rp[0]),(c,rp[1]))
 roots=sorted({root(x) for x in parent});rid={r:i for i,r in enumerate(roots)};arc={x:rid[root(x)] for x in parent};rels=[]
 for c in A:
  if all(cmap[(c,p)]==0 for p in range(4)):
   ui=next(p for p in (0,2) if (c,p) in incoming);rels.append((arc[(c,ui)],arc[(c,(ui+2)%4)],arc[(c,1)],signs[c],c))
 return dict(arcs=arc,relations=rels,cmap=cmap,incoming=incoming,signs=signs,components=cs)

def solve(q):
 n=1+max(q['arcs'].values());rels=q['relations'];by=defaultdict(list)
 for r in rels:
  for a in r[:3]:by[a].append(r)
 cls=[]
 for X in G:
  v=mm(mm(inv(X),MERIDIAN),X)
  if v not in cls:cls.append(v)
 sol=[]
 def propagate(v):
  changed=True
  while changed:
   changed=False
   for i,o,b,s,_ in rels:
    if i in v and b in v:
     z=mm(mm(pw(v[b],-s),v[i]),pw(v[b],s))
     if o in v and v[o]!=z:return False
     if o not in v:v[o]=z;changed=True
    elif o in v and b in v:
     z=mm(mm(pw(v[b],s),v[o]),pw(v[b],-s))
     if i in v and v[i]!=z:return False
     if i not in v:v[i]=z;changed=True
  return all(not(i in v and o in v and b in v) or v[o]==mm(mm(pw(v[b],-s),v[i]),pw(v[b],s)) for i,o,b,s,_ in rels)
 def dfs(v):
  v=dict(v)
  if not propagate(v):return
  if len(v)==n:sol.append(tuple(v[i] for i in range(n)));return
  best=max((a for a in range(n) if a not in v),key=lambda a:sum(sum(x in v for x in r[:3]) for r in by[a]))
  for x in cls:dfs({**v,best:x})
 dfs({0:MERIDIAN});return list(dict.fromkeys(sol))

def loop(A,q,col,comp):
 cmap,inc,sgn,arc=q['cmap'],q['incoming'],q['signs'],q['arcs'];cur=min(q['components'][comp]);seen=set();v=I
 while cur not in seen:
  seen.add(cur);c,p=cur
  if p in (0,2) and cmap[(c,1)]==cmap[(c,3)]==0 and (c,p) in inc:v=mm(v,pw(col[arc[(c,1)]],sgn[c]))
  cur=A[c][(p+2)%4]
 return v
def final_map(q0,qf):
 m={}
 for (c,p),af in qf['arcs'].items():
  if c<len(SCAFFOLD) and (c,p) in q0['arcs']:
   a=q0['arcs'][(c,p)];assert af not in m or m[af]==a;m[af]=a
 assert len(m)==18;return m

def main():
 A=adjacency(SCAFFOLD);F=band(band(A,BAND1),BAND2);q0,qf=quotient(A),quotient(F)
 assert len(q0['relations'])==len(qf['relations'])==18
 sols=solve(q0);assert len(sols)==49
 names={1:'c2_upper',2:'c1_upper',3:'c2_lower',4:'c1_lower'};dist=Counter();wit=[]
 for s in sols:
  v={names[i]:loop(A,q0,s,i) for i in range(1,5)};t=(tr(v['c1_upper']),tr(v['c2_upper']),tr(v['c1_lower']),tr(v['c2_lower']));dist[t]+=1
  if t==(1,4,1,4):wit.append((s,v))
 assert dist==Counter({(1,4,1,4):36,(1,4,2,2):6,(2,2,1,4):6,(2,2,2,2):1})
 fmap=final_map(q0,qf);out=Counter();ex={}
 for s,v in wit:
  fs=tuple(s[fmap[i]] for i in range(18));a,b=loop(F,qf,fs,1),loop(F,qf,fs,2);k=(tr(a),tr(b),order(a),order(b),conj(a,b));out[k]+=1;ex.setdefault(k,(a,b))
 expected=Counter({(2,2,5,5,True):6,(4,4,3,3,True):6,(0,2,4,5,False):6,(2,0,5,4,False):6,(4,0,3,4,False):6,(0,3,4,2,False):6});assert out==expected
 for _,v in wit:assert conj(v['c1_upper'],v['c1_lower']) and conj(v['c2_upper'],v['c2_lower'])
 sep=sum(n for k,n in out.items() if not k[-1]);surv=sum(n for k,n in out.items() if k[-1]);assert(sep,surv)==(24,12)
 result={'status':'BRANCH_GATE_PARTIAL_24_OF_36_SEPARATED_NO_COUNTEREXAMPLE','source_commit':SOURCE_COMMIT,'bands':[BAND1['compressed_spec'],BAND2['compressed_spec']],'sl2_f5_order':120,'fixed_meridian':list(MERIDIAN),'R_wirtinger_arcs':18,'all_colourings_with_fixed_meridian':49,'end_trace_distribution':[{'traces':list(k),'count':v} for k,v in sorted(dist.items())],'witness_witness_branches':36,'eta_outcomes':[{'eta1_trace':k[0],'eta2_trace':k[1],'eta1_order':k[2],'eta2_order':k[3],'conjugate_up_to_inversion':k[4],'count':n,'example_eta1':list(ex[k][0]),'example_eta2':list(ex[k][1])} for k,n in sorted(out.items())],'branches_separated_by_F5':24,'branches_surviving_F5':12,'positive_control':'Every witness/witness branch makes each corresponding original upper/lower axis pair conjugate up to inversion in SL(2,F5).','interpretation':'Unbased end-circle data do not select the actual product-disk based-whisker branch. Four of six relative branch types are killed; two survive. Compute the based lower-to-upper whisker map before deciding this explicit candidate.','counterexample':False}
 print('PASS SL(2,F5) order 120')
 print('PASS 49 fixed-meridian colourings; 36 witness/witness branches')
 print('PASS corresponding original axes are compatible in all 36 branches')
 print('PASS eta branch gate: 24 separated, 12 survive')
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
