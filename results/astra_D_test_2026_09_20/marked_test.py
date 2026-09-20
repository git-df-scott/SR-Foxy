from pathlib import Path
import sys,json,signal,time
import snappy,sympy as S
from spherogram.links.links_base import CrossingStrand
sys.path.insert(0,str(Path('results/astra_seven_hour_2026_09_20').resolve()))
from metabelian_probe import probe,kernel
out=Path(__file__).resolve().parent
class G:
 def __init__(self,L):
  self.gen=[chr(97+i) for i in range(len(L.crossings))];self.rel=[];pieces=L._pieces()
  for z in L.crossings:
   inds={}
   for m,p in enumerate(pieces):
    for t,corner in enumerate(p):
     if corner[0]==z:inds['j' if t==0 else 'i' if t==len(p)-1 else 'k']=m
   i,j,k=[self.gen[inds[v]] for v in ('i','j','k')]
   self.rel.append(k.upper()+i+k+j.upper() if z.sign>0 else k+i+k.upper()+j.upper())
  self.rel=self.rel[:-1]
 def generators(self):return self.gen
 def relators(self):return self.rel
class M:
 def __init__(self,G):self.G=G
 def fundamental_group(self):return self.G

def linking(L,colors,base_face=0):
 faces=L.faces();fo={corner:i for i,f in enumerate(faces) for corner in f};pieces=L._pieces();arc={c:i for i,p in enumerate(pieces) for c in p}
 edges=[]
 for c in L.crossings:
  for j,sgn in [(0,1),(1,-1)]:edges.append((fo[CrossingStrand(c,j)],fo[CrossingStrand(c,j+2)],sgn))
 white={base_face};again=True
 while again:
  old=len(white)
  for i,j,s in edges:
   if i in white or j in white:white.update([i,j])
  again=len(white)>old
 white=sorted(white);vals={white[0]:0};again=True
 constraints=[]
 for c in L.crossings:
  for j in range(4):
   a=fo[CrossingStrand(c,j)];b=fo[CrossingStrand(c,(j-1)%4)];v=colors[arc[(c,j)]];constraints.append((a,b,v))
 while again:
  old=len(vals)
  for a,b,v in constraints:
   if a in vals:vals[b]=(v-vals[a])%7
   elif b in vals:vals[a]=(v-vals[b])%7
  again=len(vals)>old
 assert len(vals)==len(faces)
 assert all((vals[a]+vals[b]-v)%7==0 for a,b,v in constraints)
 Q=S.zeros(len(white));index={v:i for i,v in enumerate(white)}
 for a,b,s in edges:
  if a in index:
   i,j=index[a],index[b];Q[i,j]+=s;Q[j,i]+=s;Q[i,i]-=s;Q[j,j]-=s
 Q=Q[1:,1:];v=S.Matrix([vals[i] for i in white[1:]])
 assert abs(Q.det())==7 and all(x%7==0 for x in Q*v)
 d=(v.T*Q*v)[0]/7;assert d.q==1
 return {'goeritz':Q.tolist(),'white_faces':white,'region_colors':vals,'character':list(v),'dual_pairing_numerator_mod7':int(d)%7,'scope':'common overall orientation sign immaterial for difference; Dehn colors normalized at white region 0'}
if __name__=='__main__':
 signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120s')));signal.alarm(120)
 rows=[]
 for name in ['K9n4','K14n282']:
  L=snappy.Link(name);grp=G(L);r=probe(name,M(grp),2,7,6,13);r['marked_linking']=linking(L,r['cocycle']);rows.append(r)
  print(name,r['cocycle'],r['reduced_twisted_polynomial'],r['marked_linking']['dual_pairing_numerator_mod7'],flush=True)
 (out/'MARKED_TEST.json').write_text(json.dumps({'rows':rows},indent=2,default=int)+'\n')
