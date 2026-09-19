#!/usr/bin/env python3
"""U-torsion order of HFK^- from SnapPy's UV=0 complex.

Juhasz-Miller-Zemke: for a ribbon knot J, fusion number F(J) >= Ord_U(J).
So a large torsion order is a LOWER BOUND on the number of bands in any
ribbon disk, and tells us how deep a band search must go.

Grading conventions (Zemke): gr_U(x) = M(x), gr_V(x) = M(x) - 2A(x);
U has (gr_U,gr_V) = (-2,0), V has (0,-2); the differential drops both by 1.
For an arrow a -> b carrying U^i V^j:   i = (M_b - M_a + 1)/2,
                                        j = i + (A_a - A_b),
and UV = 0 forces i = 0 or j = 0.
Setting V = 0 leaves the F[U]-complex whose homology is HFK^-.
"""
import json, sys
from fractions import Fraction

def arrows(h):
    gens = h['generators']; out = []
    for (a, b), c in h['differentials'].items():
        if c%2==0:continue
        Ma, Aa = gens[a][1], gens[a][0]
        Mb, Ab = gens[b][1], gens[b][0]
        i2 = Mb - Ma + 1
        assert i2 % 2 == 0, (a, b, Ma, Mb)
        i = i2 // 2
        j = i + (Aa - Ab)
        assert i>=0 and j>=0
        assert i == 0 or j == 0, f'UV!=0 arrow {a}->{b}: U^{i}V^{j}'
        out.append((a, b, i, j))
    return out

def monomial_smith(entries):
    """Smith exponents for a homogeneous monomial matrix over F2[U].

Pick a smallest U-power, which divides every remaining entry. Row/column
elimination leaves a smaller homogeneous monomial matrix. Homogeneity makes
equal-position terms have equal powers, so additions are exact XORs. A
matrix without this grading property is explicitly rejected.
    """
    E=dict(entries);answer=[]
    while E:
        (i,j),p=min(E.items(),key=lambda item:(item[1],item[0]))
        row={l:a for (k,l),a in E.items() if k==i and l!=j}
        col={k:a for (k,l),a in E.items() if l==j and k!=i}
        remaining={(k,l):a for (k,l),a in E.items() if k!=i and l!=j}
        for k,a in col.items():
            for l,b in row.items():
                power=a+b-p;key=(k,l)
                if key in remaining:
                    assert remaining[key]==power,'Nonhomogeneous entry needs polynomial Smith form'
                    del remaining[key]
                else:remaining[key]=power
        answer.append(p);E=remaining
    assert answer==sorted(answer)
    return answer


def torsion_order(h):
    """Compute elementary divisors, not the largest exponent of an entry.

For d^2=0 over a PID, torsion(coker d)=torsion(ker d / im d), since C/ker d
is free. Thus the nonunit Smith entries of d give the homology torsion.
    """
    ar = arrows(h)
    u = [x for x in ar if x[3] == 0 and x[2] > 0]
    v = [x for x in ar if x[2] == 0 and x[3] > 0]
    upart=[x for x in ar if x[3]==0]
    squared=set()
    for a,b,i,_ in upart:
        for c,d,j,_ in upart:
            if b==c:
                term=(a,d,i+j)
                if term in squared:squared.remove(term)
                else:squared.add(term)
    assert not squared,'The U differential does not square to zero'
    smith=monomial_smith({(b,a):i for a,b,i,_ in upart})
    torsion=[e for e in smith if e>0]
    return {'n_gens': len(h['generators']), 'n_arrows': len(ar),
            'U_arrows': len(u), 'V_arrows': len(v),
            'U_exponents': sorted({x[2] for x in u}),
            'V_exponents': sorted({x[3] for x in v}),
            'max_U_exponent': max([x[2] for x in u], default=0),
            'smith_exponents':smith,'torsion_exponents':torsion,
            'torsion_order':max(torsion,default=0),
            'localized_homology_rank':len(h['generators'])-2*len(smith)}

if __name__ == '__main__':
    import snappy
    for f in sys.argv[1:]:
        d = json.load(open(f))
        pd = d.get('pd_code_snappy_0indexed') or d['pd_code']
        K = snappy.Link([tuple(c) for c in pd])
        h = K.knot_floer_homology(complex=True)
        t = torsion_order(h)
        t['knot'] = d['name']; t['genus'] = h['seifert_genus']; t['fibered'] = h['fibered']
        t['thin_delta0'] = all(g[0] == g[1] for g in h['generators'].values())
        t['JMZ_fusion_lower_bound'] = t['torsion_order']
        print(json.dumps(t))
