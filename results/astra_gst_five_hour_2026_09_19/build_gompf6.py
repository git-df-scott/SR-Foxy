"""Second manual source transcription, from gompf6.pdf rather than example.pdf.
Kept separate for falsifying source identity, not fitted to invariant values.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys
from build_preblow import braid

def build(n=1,k=1):
 L,hl=braid(250,375,[440,475,512],k);R,hr=braid(1020,1150,[440,475,520],-k)
 N,hn=braid(620,750,[324,388],n);D,hd=braid(615,743,[779,810],-n)
 def join(*parts):
  out=[]
  for part in parts:
   for q in part:
    q=tuple(map(F,q))
    if not out or out[-1]!=q:out.append(q)
  if out[-1]!=out[0]:out.append(out[0])
  return out
 al=[(250,440),(150,410),(60,330),(40,230),(60,130),(140,45),(250,3),(472,3),(472,950),(250,950),(150,920),(65,830),(38,730),(65,620),(150,540),(250,512)]
 ab=[(375,512),(400,620),(450,720),(520,782),(590,810),(615,810)]
 abr=[(743,810),(800,805),(900,760),(970,665),(1000,570),(1020,520)]
 ar=[(1150,520),(1250,550),(1330,630),(1365,735),(1330,840),(1250,920),(1140,950),(917,950),(917,3),(1140,3),(1250,40),(1340,130),(1365,230),(1330,330),(1250,410),(1150,440)]
 au=[(375,440),(430,452),(432,490),(450,550),(490,599),(550,630),(590,637),(800,637),(875,620),(925,580),(953,525),(960,480),(958,440),(1020,440)]
 ir=[(750,324),(830,345),(880,370),(903,386),(928,426),(940,460),(945,485),(936,525),(910,560),(870,585),(810,603),(750,607),(600,611),(530,598),(490,575),(465,540),(455,500),(455,470),(460,442),(480,393),(500,368),(550,341),(620,324)]
 bl=[(375,475),(402,475),(405,535),(425,620),(460,680),(505,730),(555,768),(590,779),(615,779)]
 br=[(743,779),(800,775),(860,750),(910,710),(948,655),(970,580),(981,475),(1020,475)]
 bo=[(1150,475),(1260,505),(1350,590),(1395,725),(1360,850),(1280,940),(1140,985),(859,985),(859,388),(750,388)]
 bol=[(620,388),(507,388),(507,985),(244,985),(130,950),(42,860),(3,740),(35,615),(130,520),(245,475),(250,475)]
 sm=[(665,592),(675,575),(690,570),(705,584),(716,610),(718,635),(710,660),(695,671),(680,668),(665,650),(657,625),(658,608),(665,592)]
 curves={'A':join(al,L[2],ab,D[1],abr,R[2],ar,R[0][::-1],au[::-1],L[0][::-1]),'I':join(N[0],ir),'B':join(L[1],bl,D[0],br,R[1],bo,N[1][::-1],bol),'M':join(sm)}
 hints=hl+hr+hn+hd
 def sub(p,q):return p[0]-q[0],p[1]-q[1]
 def cross(v,w):return v[0]*w[1]-v[1]*w[0]
 seg=[(c,j,a,b) for c,pts in curves.items() for j,(a,b) in enumerate(zip(pts,pts[1:]))];cr=[]
 for ii,(c,j,a,b) in enumerate(seg):
  v=sub(b,a)
  for d,h,e,f in seg[ii+1:]:
   w=sub(f,e);den=cross(v,w)
   if not den:continue
   t=cross(sub(e,a),w)/den;u=cross(sub(e,a),v)/den
   if not (0<t<1 and 0<u<1):continue
   x,y=a[0]+t*v[0],a[1]+t*v[1];hh=[z for z in hints if z[:2]==(x,y)]
   if hh:ov=0 if (v[1]/v[0]>0)==(hh[0][2]>0) else 1;kind='twist'
   else:
    kind='outside'
    if 'M' in (c,d):who='M' if x>690 else (d if c=='M' else c);ov=0 if c==who else 1
    elif {c,d}=={'A','I'}:who='A' if y<470 else 'I';ov=0 if c==who else 1
    else:
     vertical=[abs(z[0])<1 and abs(z[1])>100 for z in (v,w)]
     if sum(vertical)!=1:raise ValueError(('unclassified',c,j,d,h,float(x),float(y),v,w))
     ov=1 if vertical[0] else 0
   cr.append({'a':(c,j,t),'b':(d,h,u),'point':(x,y),'over':ov,'kind':kind})
 along={c:[] for c in curves}
 for i,r in enumerate(cr):
  for side in ['a','b']:
   c,j,t=r[side];along[c].append((j+t,i,side))
 edge={};idx=0
 for arr in along.values():
  arr.sort();m=len(arr)
  for j,(_,i,side) in enumerate(arr):edge[(i,side)]=(idx+(j-1)%m,idx+j)
  idx+=m
 pd=[]
 for i,r in enumerate(cr):
  ov='a' if r['over']==0 else 'b';un='b' if ov=='a' else 'a'
  def direction(side):
   c,j,_=r[side];return sub(curves[c][j+1],curves[c][j])
  det=-cross(direction(un),direction(ov));ui,uo=edge[(i,un)];oi,oo=edge[(i,ov)]
  pd.append([ui,oi,uo,oo] if det>0 else [ui,oo,uo,oi])
 return {'status':'INDEPENDENT_MANUAL_GOMPF6_TRANSCRIPTION','n':n,'k':k,'pd':pd,'curves':{c:[[str(x),str(y)] for x,y in pts] for c,pts in curves.items()},'crossings':[{**r,'a':[str(z) for z in r['a']],'b':[str(z) for z in r['b']],'point':[str(z) for z in r['point']]} for r in cr],'cusp_labels':{'A':0,'I':1,'B':2,'M':3}}

if __name__=='__main__':
 import snappy
 n=int(sys.argv[1]) if len(sys.argv)>1 else 1
 r=build(n);K=snappy.Link(r['pd']);r['linking_matrix']=K.linking_matrix();r['component_counts']=[len(x) for x in K.link_components]
 print(len(r['pd']),'crossings',sum(x['kind']=='outside' for x in r['crossings']),'outside',r['linking_matrix'])
 (Path(__file__).parent/f'GOMPF6_n{n}.json').write_text(json.dumps(r,indent=2)+'\n')
