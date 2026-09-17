"""Independent small full-state sums and exact PD/normalization controls."""
import hashlib, itertools, json, subprocess
from collections import Counter
from pathlib import Path
import sympy as S
from geometry import occurrences, oriented_components, best_order, blackboard_parallel, zero_writhe, sublink, add_curl
P=Path(__file__).parent;x=S.symbols('x')

def braid_pd(word,n):
    # Positive sigma_i: left input over right input. Ports chosen so the
    # bracket convention in geometry.py assigns writhe +1.
    top=list(range(n));active=top[:];nxt=n;pd=[]
    for a in word:
        i=abs(a)-1;l,r=active[i:i+2];bl,br=nxt,nxt+1;nxt+=2
        pd.append([r,l,bl,br] if a<0 else [l,bl,br,r])
        active[i],active[i+1]=bl,br
    parent=list(range(nxt))
    def root(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for a,b in zip(active,top):parent[root(a)]=root(b)
    labels={}
    def lab(a):
        a=root(a)
        if a not in labels:labels[a]=len(labels)
        return labels[a]
    return [[lab(a) for a in c] for c in pd]

def full_state_jet(pd,extra=0):
    # No frontier contraction and no truncated-ring arithmetic during states.
    edges=sorted(occurrences(pd));index={e:i for i,e in enumerate(edges)};poly=Counter();n=len(pd)
    for smooth in itertools.product(range(2),repeat=n):
        parent=list(range(len(edges)))
        def root(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        def join(a,b):parent[root(index[a])]=root(index[b])
        for c,s in zip(pd,smooth):
            pairs=((0,1),(2,3)) if s==0 else ((0,3),(1,2))
            for a,b in pairs:join(c[a],c[b])
        loops=len({root(i) for i in range(len(edges))})+extra
        w=oriented_components(pd)['writhe'] if pd else 0
        # A^{n-2*B} (-A^2-A^-2)^loops (-A^3)^-w.
        for j in range(loops+1):
            power=n-2*sum(smooth)+2*(loops-2*j)-3*w
            assert power%2==0
            poly[power//2]+=(-1 if (loops+w)%2 else 1)*int(S.binomial(loops,j))
    q=0
    for e,c in poly.items():q+=c*S.invert(x,(x*x+1)**5)**(-e) if e<0 else c*x**e
    rem=S.rem(q,(x*x+1)**5,x)
    return [int(rem.coeff(x,i)) for i in range(10)],dict(sorted(poly.items()))

def contract(pd,extra=0):
    info=oriented_components(pd) if pd else {'writhe':0}
    order=best_order(pd,10)['order'] if pd else []
    inp=f'{len(pd)} {info["writhe"]} {extra}\n'+'\n'.join(' '.join(map(str,c)) for c in pd)+'\n'+' '.join(map(str,order))+'\n'
    proc=subprocess.run([str(P/'frontier_exact')],input=inp,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=10)
    return json.loads(proc.stdout)

def planar_euler(pd):
    occ=occurrences(pd);across={}
    for a,b in occ.values():across[a]=b;across[b]=a
    todo=set(across);faces=0
    while todo:
        p=min(todo)
        while p in todo:
            todo.remove(p);i,j=across[p];p=(i,(j+1)%4)
        faces+=1
    # For all tested inputs the projection graph is connected.
    return len(pd)-len(occ)+faces

def diagram_key(pd):
    info=oriented_components(pd)
    assert info['components']==1
    occ=occurrences(pd);across={}
    for a,b in occ.values():across[a]=b;across[b]=a
    candidates=[]
    for start in across:
        cur=start;seq=[];labels={}
        while True:
            i,j=cur
            if i not in labels:labels[i]=len(labels)
            seq.append((labels[i],j%2,info['crossing_signs'][i]))
            cur=across[(i,(j+2)%4)]
            if cur==start:break
        candidates.append(tuple(seq))
    return min(candidates)

checks=[]
inputs=json.loads((P/'source_pd.json').read_text())
source_payload=json.dumps({'pd':inputs['ribbon61_3_saved'],'expected_product':729})+'\n'
gitsha=hashlib.sha1(f'blob {len(source_payload.encode())}\0'.encode()+source_payload.encode()).hexdigest()
assert gitsha=='00135706508cf045df4fb19f5a6f6186df156a9a'
checks.append({'source_control_input_git_blob_sha':gitsha,'matches_remote':True})
small=[('U1',[],1),('U2',[],2),('U4',[],4),('curl_plus',[[0,1,2,2]],0),('hopf',braid_pd([1,1],2),0),('trefoil',braid_pd([1,1,1],2),0),('figure8',braid_pd([1,-2,1,-2],3),0),('ribbon61',sublink(inputs['ribbon61_3_saved'],{0}),0)]
# Closed one-crossing unknot controls.
small[3]=('curl_plus',[[0,0,1,1]],0)
small.append(('curl_minus',[[0,1,1,0]],0))
for name,pd,extra in small:
    jet,full=full_state_jet(pd,extra);raw=contract(pd,extra)
    assert raw['coefficients_x']==jet,(name,raw,jet)
    checks.append({'name':name,'crossings':len(pd),'full_state_count':2**len(pd),'full_polynomial_in_x':full,'exact_jet_matches':True})
    if pd and len(pd)<=8:
        for sign in [-1,1]:
            cp=add_curl(pd,sign);r=contract(cp)
            assert r['coefficients_x']==jet,(name,sign,'RI invariance failure')
            checks.append({'name':name,'R1_sign':sign,'invariance':True})
for name in ['KDG_4','ribbon61_4','ribbon61_3']:
    obj=json.loads((P/(name+'.json')).read_text());pd=obj['pd'];base=obj['zero_writhe_source_pd']
    assert planar_euler(pd)==2
    meta=oriented_components(pd);assert meta['writhe']==0
    assert all(v==0 for row in meta['linking_matrix'] for v in row)
    for j in range(meta['components']):
        s=sublink(pd,{j});assert diagram_key(s)==diagram_key(base)
    checks.append({'name':name,'planar_rotation_system_euler':2,'component_diagrams_equal_source':True,'components':meta['components'],'zero_framing_linking_matrix':meta['linking_matrix']})
# An intentionally nonribbon Hopf link must fail exact required nullity.
h=contract(braid_pd([1,1],2));pol=sum(c*x**i for i,c in enumerate(h['coefficients_x']));rem=S.rem(pol,(x*x+1)**2,x)
assert rem!=0
checks.append({'negative_control':'Hopf link','required_h_squared_remainder':str(rem),'obstruction_detected':True})
# The published ribbon control and target use different crossing orders for
# exact and mod-32 runs. Agreement is a consistency check, not independence.
a=json.loads((P/'KDG_4.mod32.json').read_text())['raw']['coefficients_x'];b=json.loads((P/'KDG_4_reverse.exact.json').read_text())['raw']['coefficients_x']
assert a==[v%32 for v in b]
checks.append({'target_mod32_different_order_matches_exact':True})
summary={'status':'ALL_CONTROLS_PASSED','number_of_checks':len(checks),'checks':checks,'exact_engine':'Boost checked 128-bit signed integer; overflow throws, it is never silently truncated','limitation':'Not a proof assistant; KDG identity and smooth disk remain upstream source dependencies. No independent full 288-crossing polynomial.'}
(P/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');print('checks',len(checks),'PASS')
