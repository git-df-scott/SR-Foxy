"""Independent Laurent first-jet calculation; no long-word Artin substitution."""
from pathlib import Path
import json
import copy

def add(a,b):
    c=dict(a)
    for k,v in b.items():c[k]=c.get(k,0)+v
    return {k:v for k,v in c.items() if v}
def shift(a,n,sign=1):return {k+n:sign*v for k,v in a.items()}
def times(a,b):
    e,F=a;f,G=b
    return e+f,[add(x,shift(y,e)) for x,y in zip(F,G)]
def inverse(a):
    e,F=a
    return -e,[shift(x,-e,-1) for x in F]
ONE=(0,[{},{},{},{}])
GEN=[(1 if i<3 else 0,[{0:1} if j==i else {} for j in range(4)]) for i in range(4)]
def jet_word(word):
    ans=ONE
    for x in word:
        g=GEN[abs(x)-1]
        ans=times(ans,g if x>0 else inverse(g))
    return ans
def braid_jets(braid):
    mer=copy.deepcopy(GEN); wh=[ONE]*4; labels=[1,2,3,4]
    for z in braid:
        i=abs(z)-1;j=i+1
        a,b=mer[i],mer[j]
        if z>0:
            nwi,nwj=times(a,wh[j]),wh[i]
            na,nb=times(times(a,b),inverse(a)),a
        else:
            nwi,nwj=wh[j],times(inverse(b),wh[i])
            na,nb=b,times(times(inverse(b),a),b)
        mer[i],mer[j]=na,nb;wh[i],wh[j]=nwi,nwj
        labels[i],labels[j]=labels[j],labels[i]
    return mer,wh,labels
def free(w):
    w=list(w)
    i=0
    while i+1<len(w):
        if w[i]==-w[i+1]:del w[i:i+2];i=max(i-1,0)
        else:i+=1
    return w
def parse_row(row):return [{int(k):v for k,v in x.items()} for x in row]
def check(d):
    assert d['source_factor_word']==[-3,4,-1,3,-4,1]
    assert len(d['cases'])==6
    orders=[]
    for row in d['cases']:
        m={int(k):v for k,v in row['boundary_to_local_generators'].items()}
        orders.append(tuple(m[k] for k in (3,4,1)))
        target=[m[abs(x)]*(1 if x>0 else -1) for x in d['source_factor_word']]
        assert target==row['target_commutator']
        assert free(x for x in row['preferred_longitude'] if abs(x)!=4)==target
        mer,wh,labels=braid_jets(row['braid_word'])
        assert labels==[1,2,3,4] and mer==GEN
        assert [parse_row(r) for r in row['meridian_Fox_matrix']]==[g[1] for g in GEN]
        long=inverse(wh[3])
        assert jet_word(row['preferred_longitude'])==long
        assert long[0]==0 and long[1]==parse_row(row['longitude_Fox_row'])
        assert long[1][:3]==[{},{},{}]
        assert long[1][3] in ({-1:-1,0:2,1:-1},{-1:1,0:-2,1:1})
        assert sum(long[1][3].values())==row['ordinary_self_coefficient']==0
    assert len(set(orders))==6

# Convention controls use the moving colours, including the weight-one axis.
for i in (1,2,3):
    mer,wh,labels=braid_jets([i,-i])
    assert mer==GEN and wh==[ONE]*4 and labels==[1,2,3,4]
assert braid_jets([2,3,2])[0]==braid_jets([3,2,3])[0]
d=json.loads(Path(__file__).with_name('point_push_certificate.json').read_text())
check(d)
bad=copy.deepcopy(d);bad['cases'][0]['longitude_Fox_row'][3]={}
try:check(bad)
except AssertionError:pass
else:raise AssertionError('zeroed longitude defect accepted')
print(json.dumps({'all_six_calibrated_commutators':'PASS',
    'independent_Laurent_jet_replay':'PASS','inverse_and_braid_relation_controls':'PASS',
    'meridian_jacobians':'identity in all six cases',
    'longitude_defects':'nonzero +/- (2-t-t^-1) in all six cases',
    'ordinary_specialization':'0 at t=1',
    'false_zero_longitude_claim_rejected':True},indent=2))
