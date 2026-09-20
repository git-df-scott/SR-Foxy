"""Standalone certificate builder.

Derives, from the frozen files only:
  * the 18-generator Wirtinger presentation of pi_1(S^3 - R), R = K_0 # (-K_0),
    in the repository's OWN native generator labels x_1..x_18;
  * the native words of the auxiliary curves a and b' (identical to
    surgery_diagram.json's expected_marked_axis_words);
  * an explicit homomorphism rho : pi_1(S^3 - R) -> A_5 with rho(a) and rho(b')
    in different conjugacy classes, even allowing inversion.

Consequence: a and b' are not freely homotopic in S^3 - R in either orientation,
so they cobound no annulus (embedded or immersed) there; the stored +1/-1 surgery
is therefore not an annulus twist of R."""
import json, collections, periph, homcount as H, solver2
D='/home/user/SR-Foxy/results/astra_genus_one_2026_09_18/'
dg=json.load(open(D+'surgery_diagram.json')); sp=json.load(open(D+'spatial_model.json'))
gw=[[list(c) for c in w] for w in dg['gauss_words']]
byid={c['id']:c for c in dg['crossings']}; segs=sp['base_segment_generators'][0]
owner=collections.defaultdict(list)
for c,w in enumerate(gw):
    for cid,t,s in w: owner[cid].append(c)
selfR={cid for cid,o in owner.items() if o==[0,0]}
w0=gw[0]; nU=sum(1 for cid,t,s in w0 if t=='U' and cid in selfR)
assert nU==18
# walk R: my arcs 1..18, native label by majority vote of the segments it carries
arcpos=[]; cur=1; cr={}; votes=collections.defaultdict(collections.Counter)
for cid,t,s in w0:
    arcpos.append(cur)
    e=byid[cid]['over'][1] if t=='O' else byid[cid]['under'][1]
    votes[cur][segs[e]]+=1
    if cid in selfR:
        if t=='O': cr.setdefault(cid,{})['b']=cur
        else:
            nxt=1+cur%nU; cr.setdefault(cid,{}).update(i=cur,o=nxt,s=s); cur=nxt
assert cur==1
sigma={k:votes[k].most_common(1)[0][0] for k in votes}
assert sorted(sigma.values())==list(range(1,19)), sigma
relsR=[(cr[k]['b'],cr[k]['s'],cr[k]['i'],cr[k]['o']) for k in sorted(cr)]
nat_rels=sorted((sigma[b],s,sigma[i],sigma[o]) for (b,s,i,o) in relsR)
over_arc={cid:arcpos[p] for p,(cid,t,s) in enumerate(w0) if t=='O' and cid not in selfR}
mywords=[periph.reduce_w([s*over_arc[cid] for cid,t,s in gw[ci] if t=='U' and cid in over_arc]) for ci in (1,2)]
natwords=[[ (1 if x>0 else -1)*sigma[abs(x)] for x in w] for w in mywords]
stored=[list(x) for x in dg['expected_marked_axis_words']]
assert natwords==stored, (natwords,stored)
print('native words reproduced exactly:',natwords==stored)
print('relabelling (internal arc -> native x_i):',dict(sorted(sigma.items())))
print('meridian used to pin: native x%d'%sigma[1])
print('native Wirtinger relators  x_out = x_over^-s x_in x_over^s :')
for b,s,i,o in nat_rels: print(f'    over=x{b:<3d} sign={s:+d}  in=x{i:<3d} out=x{o}')
A5=H.alt(5); C=solver2.Counter(A5); mul,inv,e=A5.mul,A5.inv,A5.e
cl3=[c for c in A5.classes if len(c)==20][0]
def ev(w,val):
    r=e
    for x in w:
        v=val[abs(x)]; r=mul[r][v if x>0 else inv[v]]
    return r
sols=[]
dom={x:cl3 for x in range(1,19)}; dom[1]=[cl3[0]]
C.count(18,relsR,[],dom,on_solution=lambda v: sols.append(v))
print('reps with x%d -> a fixed 3-cycle: %d'%(sigma[1],len(sols)))
wit=[]
for v in sols:
    va,vb=ev(mywords[0],v),ev(mywords[1],v)
    ca,cb,cbi=A5.classof[va],A5.classof[vb],A5.classof[inv[vb]]
    if ca!=cb and ca!=cbi: wit.append((v,va,vb))
print('non-conjugate witnesses among them:',len(wit))
wit.sort(key=lambda z: 0 if z[2]==e else 1)
v,va,vb=wit[0]
rho={sigma[g]:list(A5.elts[v[g]]) for g in range(1,19)}
cert={'group':'A_5 on {0,1,2,3,4}; each permutation p is listed as [p(0),...,p(4)]',
 'native_wirtinger_relators':[{'over':b,'sign':s,'in':i,'out':o} for b,s,i,o in nat_rels],
 'relation_convention':'x_out = x_over^(-sign) x_in x_over^(sign)',
 'a_word_native':stored[0],'b_prime_word_native':stored[1],
 'rho':{('x%d'%k):rho[k] for k in sorted(rho)},
 'rho_of_a':list(A5.elts[va]),'rho_of_b_prime':list(A5.elts[vb]),
 'class_size_of_rho_a':len(A5.classes[A5.classof[va]]),
 'class_size_of_rho_b_prime':len(A5.classes[A5.classof[vb]]),
 'count_of_non_conjugate_witnesses_in_this_family':len(wit),
 'total_reps_in_family':len(sols),
 'conclusion':'rho(a) and rho(b\') lie in different A_5 conjugacy classes, and so do rho(a) and rho(b\')^{-1}; hence a is not freely homotopic to b\' or to its reverse in S^3 - R.'}
json.dump(cert,open('annulus_obstruction_certificate.json','w'),indent=1)
print('rho(a)  =',A5.elts[va],'  rho(b\') =',A5.elts[vb])
for k in sorted(rho): print('   x%-2d ->'%k, rho[k])
print('certificate written')
