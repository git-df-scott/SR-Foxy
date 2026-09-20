"""Experimental transcription of GST source Figure `example`.
Pixel coordinates are straightened from the saved primary PDF rendering.
Not yet certified as GST: validate crossings, twists, framings, and n=1 first.
"""
from fractions import Fraction as F
import json, math
from pathlib import Path


def braid(x0,x1,ys,turns):
    # Positive generator: upper lane crosses over the lower lane, left to right.
    paths=[[(F(x0),F(y))] for y in ys]; lanes=list(range(len(ys)))
    word=list(range(len(ys)-1))*len(ys)*abs(turns)
    hints=[]
    for j,g in enumerate(word):
        xa=F(x0)+F(x1-x0)*(2*j+1)/(2*len(word)+1)
        xb=F(x0)+F(x1-x0)*(2*j+2)/(2*len(word)+1)
        for lane,st in enumerate(lanes): paths[st].append((xa,F(ys[lane])))
        hints.append(((xa+xb)/2,F(ys[g]+ys[g+1])/2,1 if turns>0 else -1))
        lanes[g],lanes[g+1]=lanes[g+1],lanes[g]
        for lane,st in enumerate(lanes): paths[st].append((xb,F(ys[lane])))
    for lane,st in enumerate(lanes): paths[st].append((F(x1),F(ys[lane])))
    assert lanes==list(range(len(ys)))
    return paths,hints


def build(n,k=1):
    L,hl=braid(200,350,[400,500,580],k)
    R,hr=braid(1000,1150,[420,520,580],-k)
    N,hn=braid(600,750,[670,740],n)
    D,hd=braid(600,750,[1015,1050],-n)
    def join(*parts):
        out=[]
        for part in parts:
            for point in part:
                q=tuple(map(F,point))
                if not out or out[-1]!=q:out.append(q)
        if out[-1]!=out[0]:out.append(out[0])
        return out
    top=[(200,400),(100,370),(40,290),(40,200),(80,140),(160,90),(260,70),(1100,70),(1230,95),(1340,170),(1370,270),(1320,350),(1250,400),(1150,420)]
    rhair=[(1000,420),(890,430),(830,450),(805,475),(830,500),(890,520),(1000,520)]
    rdown=[(1150,520),(1260,560),(1360,680),(1400,820),(1350,950),(1250,1020),(1120,1050),(750,1050)]
    lup=[(600,1050),(250,1050),(120,1010),(30,920),(0,790),(25,650),(100,550),(200,500)]
    lhair=[(350,500),(440,505),(510,495),(565,475),(575,455),(550,430),(480,412),(350,400)]
    inner=[(750,670),(840,640),(900,580),(920,500),(915,400),(890,320),(820,250),(750,215),(700,200),(650,215),(580,250),(500,320),(460,400),(450,500),(465,580),(520,635),(600,670)]
    bleft=[(350,580),(385,640),(440,690),(520,730),(600,740)]
    bright=[(750,740),(850,725),(920,680),(970,610),(1000,580)]
    bdown=[(1150,580),(1230,610),(1310,700),(1350,810),(1320,900),(1250,975),(1120,1015),(750,1015)]
    bup=[(600,1015),(260,1015),(150,985),(75,910),(40,805),(65,695),(125,610),(200,580)]
    small=[(720,5),(750,25),(770,80),(772,150),(760,224),(730,250),(700,250),(675,230),(660,180),(655,120),(665,50),(690,10),(720,5)]
    curves={'A':join(top,R[0][::-1],rhair,R[1],rdown,D[1][::-1],lup,L[1],lhair,L[0][::-1]),
            'I':join(N[0],inner),'B':join(L[2],bleft,N[1],bright,R[2],bdown,D[0][::-1],bup),
            'M':join(small)}
    hints=hl+hr+hn+hd
    def cross(v,w):return v[0]*w[1]-v[1]*w[0]
    def sub(p,q):return (p[0]-q[0],p[1]-q[1])
    seg=[(c,j,a,b) for c,pts in curves.items() for j,(a,b) in enumerate(zip(pts,pts[1:]))]
    crossings=[]
    for ii,(c,j,a,b) in enumerate(seg):
        v=sub(b,a)
        for d,h,e,f in seg[ii+1:]:
            w=sub(f,e);den=cross(v,w)
            if not den:continue
            t=cross(sub(e,a),w)/den;u=cross(sub(e,a),v)/den
            if not(0<t<1 and 0<u<1):continue
            x,y=a[0]+t*v[0],a[1]+t*v[1]
            hint=[hh for hh in hints if hh[:2]==(x,y)]
            if hint:
                sg=hint[0][2];over=0 if (v[1]/v[0]>0)==(sg>0) else 1
                kind='twist'
            else:
                pair={c,d};kind='outside'
                if pair=={'A','I'}:who='I' if y<470 else 'A'
                elif 'M' in pair and pair <= {'A','I','M'}:who='M' if x<720 else next(z for z in pair if z!='M')
                else:raise ValueError(('unexpected crossing',c,j,d,h,float(x),float(y)))
                over=0 if c==who else 1
            crossings.append({'a':(c,j,t),'b':(d,h,u),'point':(x,y),'over':over,'kind':kind})
    assert sum(x['kind']=='outside' for x in crossings)==8
    assert len(crossings)==8+12*abs(k)+4*abs(n)
    along={c:[] for c in curves}
    for i,c in enumerate(crossings):
        for side in ['a','b']:
            name,j,t=c[side];along[name].append((j+t,i,side))
    edge={};idx=0
    for name,arr in along.items():
        arr.sort();count=len(arr)
        for j,(_,i,side) in enumerate(arr):edge[(i,side)]=(idx+(j-1)%count,idx+j)
        idx+=count
    pd=[]
    for i,c in enumerate(crossings):
        ov='a' if c['over']==0 else 'b';un='b' if ov=='a' else 'a'
        def direction(side):
            name,j,_=c[side];return sub(curves[name][j+1],curves[name][j])
        # Negative determinant because page y points downward.
        det=-cross(direction(un),direction(ov));ui,uo=edge[(i,un)];oi,oo=edge[(i,ov)]
        pd.append([ui,oi,uo,oo] if det>0 else [ui,oo,uo,oi])
    result={'status':'EXPERIMENTAL_SOURCE_TRANSCRIPTION','n':n,'k':k,'component_order':['A outer red +1','I inner red -1','B large black 0','M small black 0'],'pd':pd,'curves':{c:[[str(x),str(y)] for x,y in pts] for c,pts in curves.items()},'crossings':[{**c,'a':[str(z) for z in c['a']],'b':[str(z) for z in c['b']],'point':[str(z) for z in c['point']]} for c in crossings]}
    return result

if __name__=='__main__':
    import argparse,snappy
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=1);args=ap.parse_args()
    r=build(args.n);K=snappy.Link(r['pd']);r['linking_matrix']=K.linking_matrix();r['components']=len(K.link_components)
    # Map component by the edge intervals in construction, not an assumed SnapPy order.
    counts={c:sum(1 for cr in r['crossings'] for side in ['a','b'] if cr[side][0]==c) for c in ['A','I','B','M']}
    off=0;labels={}
    for c,count in counts.items():
        labels[c]=next(i for i,comp in enumerate(K.link_components) if off in [z.strand_label() for z in comp]);off+=count
    r['cusp_labels']=labels
    out=Path(__file__).parent/f'PREBLOW_n{args.n}.json';out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({key:r[key] for key in ['n','components','cusp_labels','linking_matrix']}))
