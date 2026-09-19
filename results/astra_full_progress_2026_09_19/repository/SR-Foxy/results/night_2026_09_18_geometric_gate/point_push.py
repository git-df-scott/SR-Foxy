"""Four-strand local test: three R strands (weight t), one axis (weight 1).

Pure braids explicitly insert the smallest commutator. Meridian Fox data and
the preferred-longitude Fox data are both retained; the latter is essential.
No full-scaffold splice or geometric annulus is asserted.
"""
from pathlib import Path
import itertools
import json
import resource

resource.setrlimit(resource.RLIMIT_CPU,(30,35))
ROOT=Path(__file__).resolve().parents[2]
S=json.loads((ROOT/'results/night_2026_09_18_surface/surface_certificate.json').read_text())

def free(word):
    ans=[]
    for x in word:
        if ans and ans[-1]==-x:ans.pop()
        else:ans.append(x)
    return ans
def inv(word):return [-x for x in word[::-1]]
def product(*words):return free(x for w in words for x in w)
def fox(word):
    height=0; rows=[{} for _ in range(4)]
    for x in word:
        weight=0 if abs(x)==4 else 1
        k=height if x>0 else height-weight
        row=rows[abs(x)-1];row[k]=row.get(k,0)+(1 if x>0 else -1)
        height+=weight if x>0 else -weight
    return [{k:v for k,v in sorted(row.items()) if v} for row in rows]
def pure_generator(i):
    return list(range(3,i,-1))+[i,i]+[-j for j in range(i+1,4)]
def run_braid(braid):
    labels=[1,2,3,4]; whiskers=[[],[],[],[]]; meridians=[[i] for i in labels]
    for z in braid:
        i=abs(z)-1;j=i+1
        if z>0:
            wi=product(meridians[i],whiskers[j]);wj=whiskers[i]
        else:
            wi=whiskers[j];wj=product(inv(meridians[j]),whiskers[i])
        labels[i],labels[j]=labels[j],labels[i]
        whiskers[i],whiskers[j]=wi,wj
        for k in (i,j):
            meridians[k]=product(whiskers[k],[labels[k]],inv(whiskers[k]))
        assert max(map(len,meridians))<100000
    assert labels==[1,2,3,4]
    return meridians,whiskers

if __name__=='__main__':
    f=S['commutators'][9]
    original=product(f['left_boundary_word'],f['right_boundary_word'],
                     inv(f['left_boundary_word']),inv(f['right_boundary_word']))
    assert original==[-3,4,-1,3,-4,1]
    inverse_theta={i:list(range(3,i,-1))+[i]+[-j for j in range(i+1,4)] for i in (1,2,3)}
    P={i:pure_generator(i) for i in (1,2,3)}
    cases=[]
    for permutation in itertools.permutations((1,2,3)):
        mapping=dict(zip((3,4,1),permutation))
        target=[mapping[abs(x)]*(1 if x>0 else -1) for x in original]
        # The point-pushing convention is an anti-homomorphism, and each
        # P_i carries a suffix-conjugated meridian. Calibrate both explicitly.
        push=product(*(inverse_theta[x] if x>0 else inv(inverse_theta[-x])
                       for x in inv(target)))[::-1]
        braid=product(*(P[x] if x>0 else inv(P[-x]) for x in push))
        meridians,whiskers=run_braid(braid)
        # Our Artin convention is x_out=w x_in w^-1, whereas the
        # Wirtinger transport convention uses longitude^-1 x longitude.
        longitude=inv(whiskers[3])
        assert sum(1 if x>0 else -1 for x in longitude if abs(x)==4)==0
        assert free(x for x in longitude if abs(x)!=4)==target
        J=[fox(w) for w in meridians]
        assert J==[[{0:1} if i==j else {} for j in range(4)] for i in range(4)]
        LF=fox(longitude)
        assert LF[:3]==[{},{},{}]
        assert LF[3] in ({-1:-1,0:2,1:-1},{-1:1,0:-2,1:1})
        cases.append({'boundary_to_local_generators':mapping,'target_commutator':target,
            'point_push_letters':push,'braid_word':braid,'braid_crossings':len(braid),
            'preferred_longitude':longitude,'meridian_Fox_matrix':J,
            'longitude_Fox_row':LF,'ordinary_self_coefficient':sum(LF[3].values())})
    print(json.dumps({'scope':'Local braid model only; actual scaffold splice is not constructed',
        'weights':{'R_generators':[1,2,3],'axis_generator':4,'R_weight':'t','axis_weight':1},
        'source_factor_number':10,'source_factor_word':original,'cases':cases,
        'conclusion':'Every ordering has nonzero longitude defect +/- (2-t-t^-1), despite identity meridian Fox matrix'},indent=2))
