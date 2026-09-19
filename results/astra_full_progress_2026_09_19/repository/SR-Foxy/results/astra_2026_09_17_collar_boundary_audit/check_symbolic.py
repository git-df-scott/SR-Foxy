#!/usr/bin/env python3
"""Astra: exact all-integer collar-map obstruction. Standard library only.
Read-only inputs from the repository; prints a fresh certificate to stdout.
No network, branch operations, or automatic output writes.
"""
from pathlib import Path
import argparse, hashlib, json, types
SOURCE_MAIN = "07c20b0fd7f40aa3dd330d66ba1107a0af446d55"
INPUT_HASHES = {
  "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py": "66cc09e760cbfbb6a41cc725972fb86e8af49cc3",
  "results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/RESULTS.json": "529b738721621f42668e98f7f40b6be696a4b63a"
}

def run(raw_inputs):
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    for path, expected in INPUT_HASHES.items():
        raw = raw_inputs[path]
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if actual != expected:
            raise ValueError("Pinned input differs: " + path)
    g = types.ModuleType("pinned_diagram_core")
    exec(compile(raw_inputs["results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py"], "pinned_diagram_core.py", "exec"), g.__dict__)
    RESULT = json.loads(raw_inputs["results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/RESULTS.json"])
    A = g.adjacency_from_pd(g.SCAFFOLD)
    q = g.quotient_R_wirtinger(A)
    D = g.add_zero_twist_band(g.add_zero_twist_band(A,g.BAND1),g.BAND2)
    qf = g.quotient_R_wirtinger(D)
    fmap = g.map_final_R_arcs_to_scaffold(q,qf)
    def boundary_word(comp):
        cur=min(qf["components"][comp]);seen=set();word=[]
        while cur not in seen:
            seen.add(cur);c,p=cur
            if p in (0,2) and qf["cmap"][c,1]==qf["cmap"][c,3]==0:
                word.append((fmap[qf["arcs"][c,1]]+1)*qf["signs"][c])
            cur=D[c][(p+2)%4]
        return word
    AXIS_WORDS=[boundary_word(1),boundary_word(2)]
    LOWER_ARCS=sorted({a for (c,p),a in q["arcs"].items() if c>=27})
    BOUNDARY_RELATIONS=q["relations"]
    
    from fractions import Fraction as F
    def trim(a):
        a=list(a)
        while a and a[-1]==0:a.pop()
        return tuple(a)
    def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
    def neg(a):return tuple(-x for x in a)
    def sub(a,b):return add(a,neg(b))
    def mul(a,b):
        c=[0]*(len(a)+len(b))
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]+=x*y
        return trim(c)
    def divrem(a,b):
        a=list(a);q=[F(0)]*max(0,len(a)-len(b)+1)
        while len(a)>=len(b) and a:
            d=len(a)-len(b);c=F(a[-1])/F(b[-1]);q[d]+=c
            for j,x in enumerate(b):a[d+j]-=c*x
            a=list(trim(a))
        return trim(q),trim(a)
    def gcd(a,b):
        while b:a,b=b,divrem(a,b)[1]
        return tuple(F(x)/a[-1] for x in a) if a else ()
    zero=();one=(1,);z=(0,1)
    I=(one,zero,zero,one)
    def mm(a,b):
        return (add(mul(a[0],b[0]),mul(a[1],b[2])),add(mul(a[0],b[1]),mul(a[1],b[3])),add(mul(a[2],b[0]),mul(a[3],b[2])),add(mul(a[2],b[1]),mul(a[3],b[3])))
    def inv(a):return a[3],neg(a[1]),neg(a[2]),a[0]
    def val(w,images):
        a=I
        for x in w:a=mm(a,images[x] if x>0 else inv(images[-x]))
        return a
    rels=RESULT['source_relators']
    images={1:(one,one,zero,one),2:(one,zero,z,one)}
    steps=[]
    while len(images)<9:
        old=len(images)
        for w in rels:
            b=abs(w[0]);i=w[1];o=-w[3];e=1 if w[0]>0 else -1
            if b not in images:continue
            h=images[b] if e==1 else inv(images[b])
            if i in images and o not in images:images[o]=mm(mm(h,images[i]),inv(h));steps.append([o,b,i,e])
            elif o in images and i not in images:images[i]=mm(mm(inv(h),images[o]),h);steps.append([i,b,o,-e])
        assert len(images)>old
    constraints=[]
    for w in rels:
        m=val(w,images)
        constraints.extend(sub(a,b) for a,b in zip(m,I) if sub(a,b))
    R=()
    for p in constraints:R=gcd(R,p)
    assert len(R)>1
    def rem(a):return divrem(a,R)[1]
    images={k:tuple(rem(p) for p in v) for k,v in images.items()}
    
    def zmm(a,b):return tuple(rem(p) for p in mm(a,b))
    def zval(w,imgs):
        a=I
        for x in w:a=zmm(a,imgs[x] if x>0 else inv(imgs[-x]))
        return a
    for w in rels:assert zval(w,images)==I
    col={int(k):zval(w,images) for k,w in RESULT['boundary_arc_images'].items()}
    m=col[4];assert m==col[14] and add(m[0],m[3])==(2,)
    N=tuple(sub(a,b) for a,b in zip(m,I))
    assert zmm(N,N)==((),(),(),())
    def nt(a):
        a=list(a)
        while a and not a[-1]:a.pop()
        return tuple(a)
    def na(a,b):return nt([add(a[i] if i<len(a) else (),b[i] if i<len(b) else ()) for i in range(max(len(a),len(b)))])
    def nn(a):return tuple(neg(x) for x in a)
    def nm(a,b):
        c=[()]*(len(a)+len(b))
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]=add(c[i+j],rem(mul(x,y)))
        return nt(c)
    def nmm(a,b):
        return (na(nm(a[0],b[0]),nm(a[1],b[2])),na(nm(a[0],b[1]),nm(a[1],b[3])),na(nm(a[2],b[0]),nm(a[3],b[2])),na(nm(a[2],b[1]),nm(a[3],b[3])))
    def ni(a):return a[3],nn(a[1]),nn(a[2]),a[0]
    def lift(m):return tuple((p,) if p else () for p in m)
    NI=lift(I)
    h=tuple(nt([a,b]) for a,b in zip(I,N))
    assert nmm(h,ni(h))==NI
    nc={a:nmm(nmm(h,lift(v)),ni(h)) if a in LOWER_ARCS else lift(v) for a,v in col.items()}
    def nv(w,imgs):
        a=NI
        for x in w:a=nmm(a,imgs[x] if x>0 else ni(imgs[-x]))
        return a
    axis=AXIS_WORDS
    es=[nv(w,{k+1:v for k,v in nc.items()}) for w in axis]
    traces=[na(e[0],e[3]) for e in es]
    difference=na(traces[0],nn(traces[1]))
    
    # All boundary relations hold as polynomial identities in n.
    for i,o,b,s,c in BOUNDARY_RELATIONS:
        w=[(b+1)*(-s),i+1,(b+1)*s,-o-1]
        assert nv(w,{k+1:v for k,v in nc.items()})==NI
    # Every source and boundary generator matrix has determinant one.
    for x in images.values():assert rem(sub(mul(x[0],x[3]),mul(x[1],x[2])))==one
    for x in nc.values():assert na(nm(x[0],x[3]),nn(nm(x[1],x[2])))==(one,)
    # Exact polynomial irreducibility proof over F2 by all small monic divisors.
    def binary_rem(a,b):
        while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
        return a
    r2=sum((int(c)%2)<<i for i,c in enumerate(R))
    divisor_checks=[{'bits':d,'remainder':binary_rem(r2,d)} for degree in (1,2,3) for d in range(1<<degree,1<<(degree+1))]
    assert len(divisor_checks)==14 and all(x['remainder'] for x in divisor_checks)
    assert R==(1,1,2,4,5,3,1)
    assert difference==((),(-10,-8,-18,-36,-34,-12),(-2,0,-2,-4,-2))
    assert difference[1][-1]==-12 and len(difference[2])<6
    assert traces[0][0]==traces[1][0]
    def ints(p):return [int(x) if x.denominator==1 else str(x) for x in map(F,p)]
    out={
     'status':'VERIFIED_ALL_NONZERO_INTEGER_PARTIAL_CONJUGATIONS_OBSTRUCTED',
     'counterexample_found':False,
     'source_main':SOURCE_MAIN,
     'input_blob_sha1':INPUT_HASHES,
     'generator_convention':'original source x1,...,x9; boundary words are one-based, signed; source relators and arc maps from pinned archive',
     'source_relators':rels,
     'propagation_steps':steps,
     'riley_polynomial_ascending':ints(R),
     'irreducibility_mod2_divisor_checks':divisor_checks,
     'source_matrices':{str(k):[ints(p) for p in v] for k,v in images.items()},
     'boundary_relations':BOUNDARY_RELATIONS,
     'boundary_arc_images':RESULT['boundary_arc_images'],
     'lower_arcs_zero_based':LOWER_ARCS,
     'seam_arcs_zero_based':[4,14],
     'axis_boundary_words':AXIS_WORDS,
     'trace_eta1_coefficients_in_n':[ints(p) for p in traces[0]],
     'trace_eta2_coefficients_in_n':[ints(p) for p in traces[1]],
     'trace_difference_coefficients_in_n':[ints(p) for p in difference],
     'nonvanishing_argument':'R has degree 6 and is irreducible mod 2, hence over Q. For integer n != 0 the reduced trace difference has z^5 coefficient -12*n != 0, so it is nonzero in Q[z]/R.',
     'geometric_limit':'No geometric realization of q0 or qn as the intended marked disk-exterior map, no embedded modifying annulus, no standardness or nonribbon boundary certificate.'
    }
    return out
    

if __name__ == "__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[2])
    args=ap.parse_args()
    print(json.dumps(run({p:(args.repo/p).read_bytes() for p in INPUT_HASHES}),indent=2))
