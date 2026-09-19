"""Independent finite-data replay; no geometry or knot-library dependency.

The continuous collar argument, ribbon disk construction, and existing
nonribbon theorem hypotheses remain mathematical inputs. This script does
not certify an annulus or a Slice--Ribbon counterexample.
"""
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def inverse(w): return [-x for x in reversed(w)]
def reduce(w):
    w=list(w);i=0
    while i+1<len(w):
        if w[i]==-w[i+1]: del w[i:i+2];i=max(0,i-1)
        else:i+=1
    return w
def substitute(w,images):
    return reduce(v for x in w for v in (images[x] if x>0 else inverse(images[-x])))

def adjacency(pd):
    ports={}
    for c,row in enumerate(pd):
        assert len(row)==4
        for p,label in enumerate(row):ports.setdefault(label,[]).append((c,p))
    assert all(len(pair)==2 for pair in ports.values())
    return {x:y for pair in ports.values() for x,y in [pair,pair[::-1]]}

def mm(a,b,p=17):
    return [(a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,
            (a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p]

def verify_compressions(d,C):
    matrices={int(k):[sum(v)%17 for v in a] for k,a in C['source_matrices'].items()}
    images={int(k):v for k,v in d['boundary_meridian_images'].items()}
    def val(w):
        ans=[1,0,0,1]
        for x in w:
            a=matrices[abs(x)]
            if x<0:a=[a[3],-a[1]%17,-a[2]%17,a[0]]
            ans=mm(ans,a)
        return ans
    assert sum(C['riley_polynomial_ascending'])%17==0
    assert all((a[0]*a[3]-a[1]*a[2])%17==1 for a in matrices.values())
    assert all(val(w)==[1,0,0,1] for w in C['source_relators'])
    for item in d['compression_test']['loops']:
        w=substitute(item['boundary_word'],images)
        assert w==item['source_word']
        a=val(w)
        assert a==item['matrix_mod17'] and (a[0]+a[3])%17==item['trace_mod17']
        assert a!=[1,0,0,1]

def tag(x):return tuple(x) if isinstance(x,list) else x
def tagged_graph(diagram):
    A={tag(r['crossing']):[(tag(d),p) for d,p in r['neighbors']] for r in diagram['tagged_adjacency']}
    assert len(A)==diagram['crossings']
    for c,row in A.items():
        assert len(row)==4
        for p,(d,q) in enumerate(row):assert A[d][q]==(c,p)
    return A

def compare_fixed_crossings_up_to_even_rotations(A,B):
    assert A.keys()==B.keys()
    # The library may rotate individual undercrossing ports by 180 degrees
    # when reorienting the output diagram. Only those rotations are allowed.
    remaining=set(A)
    while remaining:
        start=min(remaining)
        successful=None
        for seed in (0,2):
            shifts={start:seed};stack=[start];valid=True
            while stack and valid:
                c=stack.pop()
                for p,(d,q) in enumerate(A[c]):
                    other,target_port=B[c][(p+shifts[c])%4]
                    if other!=d: valid=False;break
                    needed=(target_port-q)%4
                    if needed not in (0,2) or (d in shifts and shifts[d]!=needed):valid=False;break
                    if d not in shifts:shifts[d]=needed;stack.append(d)
            if valid:successful=shifts;break
        assert successful is not None
        remaining-=successful.keys()

def verify_saddle(s):
    A=tagged_graph(s['D01_connected_sum_J']);B=tagged_graph(s['prefix']['result'])
    c=tuple(s['prefix']['crossing_tag'])
    assert c==(48,2)
    old=copy.deepcopy(A)
    for item in s['prefix']['attachments']:
        a,b=item['removed_ports'];x,i=old[c][a];y,j=old[c][b]
        assert [[list(x),i],[list(y),j]]==item['join']
        A[x][i]=(y,j);A[y][j]=(x,i)
    del A[c]
    compare_fixed_crossings_up_to_even_rotations(A,B)
    # Count actual link components by alternating diagram edges and opposites.
    unseen={(c,p) for c in B for p in range(4)};count=0
    while unseen:
        count+=1;stack=[next(iter(unseen))]
        while stack:
            x=stack.pop()
            if x not in unseen:continue
            unseen.remove(x);c,p=x
            stack.extend([B[c][p],(c,(p+2)%4)])
    assert count==s['prefix']['result']['components']==2

def main():
    d=json.loads((HERE/'transport.json').read_text())
    s=json.loads((HERE/'stabilizer.json').read_text())
    for data in (d,s):
        for item in data['inputs']:
            assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
    C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
    A=adjacency(json.loads((ROOT/'data/knots/AbeTagami_marked_product_scaffold.json').read_text())['pd_code'])
    assert [(c,p,list(q)) for (c,p),q in sorted(A.items()) if c<27<=q[0]]==[tuple(v) for v in d['seams']]
    for item in d['neck_faces']:
        cyc=[tuple(x) for x in item['double_face']]
        for x,y in zip(cyc,cyc[1:]+cyc[:1]):assert A[x[0],(x[1]+1)%4]==y
    for route in d['band_routes']:
        assert sum(step['crosses_neck'] for step in route['segments'])==1
    images={int(k):v for k,v in d['boundary_meridian_images'].items()}
    for axis in d['axes']:
        letters=[]
        for step in axis['steps']:
            assert step['source_word']==substitute(step['boundary_letters'],images)
            letters+=step['boundary_letters']
        assert reduce(letters)==axis['boundary_word']
        assert substitute(letters,images)==axis['source_image']
    r=d['word_repair'];mu=r['conjugating_meridian']
    assert substitute(r['corrected_boundary_word'],images)==r['source_image']==reduce(inverse(mu)+d['axes'][0]['source_image']+mu)
    verify_compressions(d,C)
    h=json.loads((HERE/'one_handle_connection.json').read_text())
    summary=json.loads((ROOT/'results/astra_one_commutator_2026_09_18/SUMMARY.json').read_text())
    for item in h['inputs']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
    for item in h['loops']:assert item['boundary_word']==summary[item['name']]
    newer=copy.deepcopy(d);newer['compression_test']['loops']=h['loops']
    verify_compressions(newer,C)
    assert h['loops'][1]['trace_mod17']==2 and h['loops'][1]['matrix_mod17']!=[1,0,0,1]
    # Exact quarter-turn sign control: pullback, not forward, acts on whisker.
    def bridge_check(forward):
        # 2x2 rotation inverse is transpose.
        pullback_above=[forward[2],forward[3]]
        assert pullback_above==[1,0]
    bridge_check([0,-1,1,0])
    rejected=0
    try:bridge_check([0,1,-1,0])
    except AssertionError:rejected+=1
    else:raise AssertionError('wrong collar sign passed')
    bad=copy.deepcopy(d);bad['compression_test']['loops'][0]['boundary_word']=[]
    try:verify_compressions(bad,C)
    except AssertionError:rejected+=1
    else:raise AssertionError('trivialized compression loop passed')
    beta=s['R_braid'];double=[]
    for x in beta:
        j=abs(x);block=[2*j,2*j-1,2*j+1,2*j]
        if x<0:block=[-v for v in reversed(block)]
        double+=block
    assert double==s['zero_parallel_braid'] and double+[1]==s['J_braid']
    colors=[i%2 for i in range(2*(max(map(abs,beta))+1))];words=[[],[]];mixed=0
    for x in double:
        j=abs(x);a,b=colors[j-1],colors[j]
        if a==b:words[a].append((1 if x>0 else -1)*sum(c==a for c in colors[:j]))
        else:mixed+=1 if x>0 else -1
        colors[j-1],colors[j]=b,a
    assert words==s['component_braid_projection']==[beta,beta] and mixed==0
    verify_saddle(s)
    bad=copy.deepcopy(s);bad['prefix']['attachments'][0]['removed_ports']=[0,2]
    try:verify_saddle(bad)
    except AssertionError:rejected+=1
    else:raise AssertionError('wrong saddle passed')
    print(json.dumps({'input_hashes':'PASS','seam_faces':'PASS','axis_word_transport':'PASS',
                      'compression_quotient_relators_and_loops':'PASS','cable_component_projections':'PASS',
                      'actual_saddle_adjacency_and_components':'PASS','negative_controls_rejected':rejected,
                      'new_one_handle_images_and_nonidentity':'PASS',
                      'scope':'Finite data only; geometric arguments are separately stated; no CE'},indent=2))

if __name__=='__main__':main()
