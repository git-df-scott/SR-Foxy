"""Two directed checks: fixed-stabilizer exclusion and an actual handle match.

No knot search. Uses the saved one-commutator proof as a checked input lemma,
then explicitly translates the newly measured native component word.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('old_transport',ROOT/'results/astra_2026_09_18_marked_annulus_construction/build_transport.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
g=old.g

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def add(a,b):
    return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]

def pd_from_adj(adj):
    labels={};pd=[]
    for c in sorted(adj):
        row=[]
        for p in range(4):
            x=(c,p);y=tuple(adj[c][p])
            if x not in labels:labels[x]=labels[y]=len(labels)//2
            row.append(labels[x])
        pd.append(row)
    return pd

def native_word(adj,q,ci):
    start=min(q['components'][ci]);x=start;word=[];steps=[]
    while True:
        c,p=x;letter=[]
        if p%2==0 and q['cmap'][c,1]==0:
            letter=[(q['arcs'][c,1]+1)*q['signs'][c]];word+=letter
        steps.append({'port':x,'letters':letter})
        x=adj[c][(p+2)%4]
        if x==start:break
    return old.red(word),steps

def main():
    out=HERE/'CHECKS.json'
    if out.exists():raise FileExistsError(out)
    paths=[ROOT/'results/astra_one_commutator_2026_09_18/BUNDLE.tar.xz',
           ROOT/'data/knots/AbeTagami_marked_product_scaffold.json',
           ROOT/'results/astra_2026_09_18_marked_annulus_construction/stabilizer.json',
           ROOT/'results/night_2026_09_18_followup/geometry_free_audit.json',
           ROOT/'results/night_2026_09_18_jones/RESULTS.json']
    with tarfile.open(paths[0]) as arc:
        cert=json.load(arc.extractfile('astra_one_commutator_2026_09_18/CERTIFICATE.json'))
    images={int(k):v for k,v in cert['tietze_images'].items()}
    rules={r['level']:r for r in cert['finite_schreier_rules']}
    lo,hi=cert['basis_levels'];offset=cert['schreier_offset']
    def schreier(word):
        height=0;out=[]
        for x in word:
            assert abs(x) in (3,5)
            if abs(x)==5:
                level=height if x>0 else height-1
                out.append((level+offset)*(1 if x>0 else -1))
            height+=1 if x>0 else -1
        assert height==0
        return old.red(out)
    def y(k):
        if lo<=k<=hi:return [k-lo+1]
        assert k in rules,'New word requires a rule outside the saved certificate'
        return rules[k]['basis_image']
    def translate(word):
        tw=old.sub(word,images);sw=schreier(tw)
        fw=old.red(v for x in sw for v in (y(abs(x)-offset) if x>0 else old.inv(y(abs(x)-offset))))
        return {'boundary_word':word,'two_generator_word':tw,'schreier_word':sw,'basis_word':fw}
    adj=g.adjacency_from_pd(g.SCAFFOLD);q=g.quotient_R_wirtinger(adj)
    word,steps=native_word(adj,q,2)
    assert word==[4,-1,3,-4]
    c2=translate(word);A=translate([4,-3,-3,1])
    assert A['basis_word']==cert['words']['A']['basis_word']
    assert c2['basis_word']==old.inv(A['basis_word'])
    band=dict(g.BAND2,arc_is_under=[True,False])
    final=g.add_zero_twist_band(adj,band);qf=g.quotient_R_wirtinger(final)
    anchor_a=min(q['components'][1]);anchor_c2=min(q['components'][2])
    ai=qf['cmap'][anchor_a];ci=qf['cmap'][anchor_c2]
    assert ai!=ci
    assert all(qf['cmap'][p]==ci for p in q['components'][2])
    assert all((p in q['incoming'])==(p in qf['incoming']) for p in q['components'][2])
    assert (anchor_a in q['incoming'])==(anchor_a in qf['incoming'])
    terms=[{'crossing':c,'sign':qf['signs'][c]} for c in final
           if {qf['cmap'][c,0],qf['cmap'][c,1]}=={ai,ci}]
    assert terms==[{'crossing':25,'sign':1},{'crossing':26,'sign':1}]
    assert sum(r['sign'] for r in terms)==2
    d=[1,-3,5,-3,1];e=[1,0,-3,0,5,0,-3,0,1]
    u=[49,60,-67,-117,37,72,-11,-24];v=[-21,87,-61,24]
    identity=add(mul(u,d),mul(v,e))
    assert identity==[28]+[0]*(len(identity)-1)
    def mod2_rem(a,b):
        while a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
        return a
    remainders={str(p):mod2_rem(31,p) for p in [2,3,7]}
    assert all(remainders.values())
    record={'CE':False,'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],
            'polynomial_gate':{'d_ascending':d,'d_of_t_squared_ascending':e,
                               'bezout_u_ascending':u,'bezout_v_ascending':v,'bezout_constant':28,
                               'identity':'u*d+v*d(t^2)=28','mod2_irreducibility_remainders':remainders},
            'new_handle_identity':{'native_component':2,'native_steps':steps,'c2':c2,'A':A,
                                   'result':'A=c2^-1 in the recorded boundary group',
                                   'method':'Saved finite Tietze/Schreier identities followed by literal free inversion; no conjugacy search'},
            'geometric_linking':{'band':band,'a_anchor':anchor_a,'c2_anchor':anchor_c2,
                                 'a_component':ai,'c2_component':ci,'crossings':terms,'lk_c2_a':1,
                                 'pd_code':pd_from_adj(final),
                                 'tagged_adjacency':{str(c):row for c,row in final.items()}},
            'construction_input':'Research42 A-handle starts in a ball disjoint a; its prescribed isotopies fix a, so lk(A_handle,a)=0.',
            'collar_trace':{'from_linking':0,'to_linking':-1,'signed_difference':-1,
                            'scope':'Any trace from A_handle to reversed c2 in a product S3 collar intersects the protected a×I algebraically by -1, with matching orientation convention.'},
            'not_claimed':['An actual genus-two compression curve with fully tracked surface connectors',
                           'A clean four-dimensional compression disk', 'A complete annulus movie or nonribbon slice boundary']}
    out.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'rational_coprimality':'PASS','new_handle_identity':'A=c2^-1',
                      'measured_lk_c2_a':1,'collar_trace_intersection':-1,'CE':False}))

if __name__=='__main__':main()
