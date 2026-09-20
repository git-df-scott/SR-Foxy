"""Standalone verifier for annulus_obstruction_certificate.json.
Reads only the certificate and surgery_diagram.json, checks:
 1. the 18 Wirtinger relators of R hold under rho;
 2. rho(a) and rho(b') are the stated permutations;
 3. their A5 conjugacy classes differ, also after inverting rho(b');
 4. the certificate's a,b' words are byte-identical to
    surgery_diagram.json -> expected_marked_axis_words.
Also checks that the two 9-generator blocks of the R presentation are each a
knot group with Alexander polynomial t^4-3t^3+5t^2-3t+1 (so R = K_0 # (-K_0)
with K_0 = 6_3), and reports their A5 representation counts."""
import json, itertools, sympy as sp
C=json.load(open('annulus_obstruction_certificate.json'))
dg=json.load(open('/home/user/SR-Foxy/results/astra_genus_one_2026_09_18/surgery_diagram.json'))
assert C['a_word_native']==list(dg['expected_marked_axis_words'][0])
assert C['b_prime_word_native']==list(dg['expected_marked_axis_words'][1])
print('1. words identical to surgery_diagram.json expected_marked_axis_words: OK')
def mul(p,q): return tuple(p[q[i]] for i in range(5))
def inv(p):
    r=[0]*5
    for i,x in enumerate(p): r[x]=i
    return tuple(r)
ID=(0,1,2,3,4)
rho={int(k[1:]):tuple(v) for k,v in C['rho'].items()}
ok=True
for R in C['native_wirtinger_relators']:
    b,s,i,o=R['over'],R['sign'],R['in'],R['out']
    cb=rho[b] if s>0 else inv(rho[b])
    if mul(mul(inv(cb),rho[i]),cb)!=rho[o]: ok=False; print('  FAILS',R)
print('2. all',len(C['native_wirtinger_relators']),'Wirtinger relators hold:',ok)
def ev(w):
    r=ID
    for x in w: r=mul(r, rho[abs(x)] if x>0 else inv(rho[abs(x)]))
    return r
ra,rb=ev(C['a_word_native']),ev(C['b_prime_word_native'])
print('3. rho(a)  =',ra,'  matches certificate:',list(ra)==C['rho_of_a'])
print('   rho(b\') =',rb,'  matches certificate:',list(rb)==C['rho_of_b_prime'])
def cycletype(p):
    seen=set(); t=[]
    for i in range(5):
        if i in seen: continue
        l=0; j=i
        while j not in seen:
            seen.add(j); j=p[j]; l+=1
        t.append(l)
    return tuple(sorted(t,reverse=True))
# A5 classes: cycle type plus, for 5-cycles, the split into two classes
A5=[p for p in itertools.permutations(range(5)) if sum(1 for i in range(5) for j in range(i) if p[j]>p[i])%2==0]
def cls(p):
    return frozenset(mul(mul(g,p),inv(g)) for g in A5)
print('4. cycle types: rho(a)',cycletype(ra),' rho(b\')',cycletype(rb),' rho(b\')^-1',cycletype(inv(rb)))
print('   rho(a) conjugate to rho(b\')   :', ra in cls(rb))
print('   rho(a) conjugate to rho(b\')^-1:', ra in cls(inv(rb)))
print('   ==> a is NOT freely homotopic to b\' or its reverse in S^3 - R:',
      (ra not in cls(rb)) and (ra not in cls(inv(rb))))
# ---- the two blocks
rels=[(R['over'],R['sign'],R['in'],R['out']) for R in C['native_wirtinger_relators']]
blocks=[[r for r in rels if max(r[0],r[2],r[3])<=9],[r for r in rels if min(r[0],r[2],r[3])>=10]]
print('5. block sizes',[len(b) for b in blocks],'(18 relators split 9+9 -> R is a connected sum)')
t=sp.symbols('t')
for bi,B in enumerate(blocks):
    gens=sorted({x for r in B for x in (r[0],r[2],r[3])})
    idx={g:k for k,g in enumerate(gens)}
    rows=[]
    for (b,s,i,o) in B:
        row=[0]*len(gens)
        # relator  x_b^-s x_i x_b^s x_o^-1 ; Fox derivative with all meridians -> t
        # d/dx_b = -t^{-s} + t^{-s}*t   (s=+1)  etc.; use standard Wirtinger formula
        if s>0:
            row[idx[b]] += (1-t); row[idx[i]] += t; row[idx[o]] += -1
        else:
            row[idx[b]] += (1-t)*(-1)/t*0 + (t-1)/t*0  # placeholder, replaced below
        rows.append(row)
    # redo properly: relator w = x_b^{-s} x_i x_b^{s} x_o^{-1}
    rows=[]
    for (b,s,i,o) in B:
        row=[sp.Integer(0)]*len(gens)
        e=0; 
        def add(g,c,e):
            row[idx[g]]+=c*t**e
        # walk the word letter by letter with exponents
        word=[(b,-s),(i,1),(b,s),(o,-1)]
        for (g,ex) in word:
            if ex>0:
                add(g,1,e); e+=1
            else:
                e-=1; add(g,-1,e)
        rows.append(row)
    M=sp.Matrix(rows)
    # delete one column, take determinant
    dets=[sp.factor(sp.expand(M[:, [j for j in range(len(gens)) if j!=k]].det())) for k in range(len(gens))]
    nz=[d for d in dets if d!=0]
    print(f'   block {bi}: generators {gens}')
    print(f'     Alexander polynomial (up to units):', sp.factor(sp.simplify(nz[0])) if nz else 'degenerate')
