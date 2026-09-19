"""Independent integer replay, including a one-relator proof of the new match."""
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def red(w):
    a=[]
    for x in w:
        if a and a[-1]==-x:a.pop()
        else:a.append(x)
    return a

def product(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def check_polynomial(p):
    x=product(p['bezout_u_ascending'],p['d_ascending'])
    y=product(p['bezout_v_ascending'],p['d_of_t_squared_ascending'])
    n=max(len(x),len(y));x+= [0]*(n-len(x));y+=[0]*(n-len(y))
    assert [a+b for a,b in zip(x,y)]==[28]+[0]*(n-1)

def trace(A,start):
    seen=[];x=start
    while x not in seen:
        seen.append(x);x=A[x[0]][(x[1]+2)%4]
    assert x==start
    return seen

def main():
    d=json.loads((HERE/'CHECKS.json').read_text())
    for item in d['inputs']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
    check_polynomial(d['polynomial_gate'])
    # Degree-four mod-2 polynomial: test both linear factors and the only
    # irreducible quadratic. No large irreducibility routine is involved.
    coefficients=[v%2 for v in d['polynomial_gate']['d_ascending']]
    assert coefficients==[1,1,1,1,1]
    assert coefficients[0] and sum(coefficients)%2
    r=coefficients[:]
    for k in range(4,1,-1):
        if r[k]:
            for j in range(3):r[k-2+j]^=1
    assert any(r[:2])
    c2=d['new_handle_identity']['c2']['boundary_word']
    wordA=d['new_handle_identity']['A']['boundary_word']
    source=ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json'
    C=json.loads(source.read_text());i,o,b,s,cross=C['boundary_relations'][7]
    rel=[-s*(b+1),i+1,s*(b+1),-(o+1)]
    assert cross==11 and rel==[1,4,-1,-3]
    assert red(c2+wordA)==rel[1:]+rel[:1]==[4,-1,-3,1]
    # This proves c2*A=x1^-1*rel*x1=1 directly, independently of Schreier.
    L=d['geometric_linking'];adj={int(c):[tuple(y) for y in row] for c,row in L['tagged_adjacency'].items()}
    for c,row in adj.items():
        for p,(e,q) in enumerate(row):assert adj[e][q]==(c,p)
    reached={min(adj)};pending=list(reached)
    while pending:
        c=pending.pop()
        for e,q in adj[c]:
            if e not in reached:reached.add(e);pending.append(e)
    assert reached==set(adj)
    occurrences={}
    for c,row in zip(sorted(adj),L['pd_code']):
        for p,label in enumerate(row):occurrences.setdefault(label,[]).append((c,p))
    assert all(len(pair)==2 for pair in occurrences.values())
    for x,y in occurrences.values():assert adj[x[0]][x[1]]==y
    unseen={(c,p) for c in adj for p in range(4)};faces=0
    while unseen:
        faces+=1;start=min(unseen);x=start
        while True:
            assert x in unseen;unseen.remove(x);x=adj[x[0]][(x[1]+1)%4]
            if x==start:break
    assert faces==len(adj)+2
    a=trace(adj,tuple(L['a_anchor']));native=trace(adj,tuple(L['c2_anchor']))
    aset=set(a)|{(c,(p+2)%4) for c,p in a}
    cset=set(native)|{(c,(p+2)%4) for c,p in native}
    incoming=set(a+native)
    terms=[]
    for c in adj:
        if ((c,0) in aset and (c,1) in cset) or ((c,0) in cset and (c,1) in aset):
            ports={p for p in range(4) if (c,p) in incoming}
            sign=1 if ports in [{0,3},{1,2}] else -1
            terms.append({'crossing':c,'sign':sign})
    assert terms==L['crossings'] and sum(x['sign'] for x in terms)==2
    protected=[{'under_port':[c,p],'over_meridian_at':[c,1],
                'sign':next(x['sign'] for x in terms if x['crossing']==c)}
               for c,p in native if p%2==0 and (c,1) in aset]
    assert protected==[{'under_port':[26,2],'over_meridian_at':[26,1],'sign':1}]
    # Projecting away a loses precisely this meridian in the c2 traversal.
    expected_under=[[19,2],[10,2],[26,2],[15,2],[21,2]]
    actual_under=[[c,p] for c,p in native if p%2==0]
    assert actual_under==expected_under
    rincoming=set(trace(adj,(0,0)))
    full_letters=[]
    for c,p in actual_under:
        ports={k for k in range(4) if (c,k) in incoming|rincoming}
        assert len(ports)==2
        exponent=1 if ports in [{0,3},{1,2}] else -1
        full_letters.append({'over_meridian_at':[c,1],
                             'component':'a' if c==26 else 'R','exponent':exponent})
    assert [x['exponent'] for x in full_letters]==[1,-1,1,1,-1]
    assert sum(x['exponent'] for x in full_letters if x['component']=='a')==1
    rejected=0
    bad=copy.deepcopy(d['polynomial_gate']);bad['bezout_u_ascending'][0]+=1
    try:check_polynomial(bad)
    except AssertionError:rejected+=1
    else:raise AssertionError('false Bezout identity accepted')
    bad=full_letters[:2]+full_letters[3:]
    try:assert sum(x['exponent'] for x in bad if x['component']=='a')==1
    except AssertionError:rejected+=1
    else:raise AssertionError('deleted protected meridian accepted')
    report={'status':'PASS','input_hashes':'PASS','polynomial_coprimality':'PASS',
            'irreducibility_mod2':'PASS','planar_rotation_system_faces':faces,
            'direct_group_identity':{'relation_index_zero_based':7,'crossing':11,
                                     'relator':rel,'reduced_c2_times_A':red(c2+wordA),
                                     'reason':'Cyclic permutation of the actual Wirtinger relator'},
            'protected_axis_underpass':protected,
            'c2_geometric_word_in_doubly_marked_exterior':full_letters,
            'protected_axis_meridional_exponent':1,'lk_c2_a':1,
            'source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'negative_controls_rejected':rejected,
            'limits':'Geometric/theorem arguments are stated separately. No actual mixed compression disk or complete annulus movie.'}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
