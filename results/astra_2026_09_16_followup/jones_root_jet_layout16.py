#!/usr/bin/env python3
"""Exact Jones ribbon congruence probe in Z/32[q]/((q^2+1)^(m+1)).

Compute only the root jet needed for Eisermann's necessary conditions.
Nonzero residue obstructs ribbonness; zero is inconclusive. This does not
certify the satellite framing or smooth sliceness of its input.
"""
from math import comb
import json
import sys


class Jet:
    order = 4
    def __init__(self, coefficients=0):
        if isinstance(coefficients, int): coefficients = [coefficients]
        d = list(coefficients)
        N = 2*self.order
        for k in range(len(d)-1, N-1, -1):
            c = d[k] % 32
            for j in range(self.order+1):
                d[k-N+2*j] -= c*comb(self.order, j)
        self.d = tuple((d[i] if i < len(d) else 0) % 32 for i in range(N))
    def __add__(self, other):
        if isinstance(other, int): other = Jet(other)
        if not isinstance(other, Jet): return NotImplemented
        return Jet([a+b for a,b in zip(self.d,other.d)])
    __radd__ = __add__
    def __neg__(self): return Jet([-a for a in self.d])
    def __sub__(self, other): return self + (-other)
    def __mul__(self, other):
        if isinstance(other,int): other=Jet(other)
        if not isinstance(other,Jet): return NotImplemented
        d=[0]*(len(self.d)*2-1)
        for i,a in enumerate(self.d):
            if a:
                for j,b in enumerate(other.d):
                    if b: d[i+j]+=a*b
        return Jet(d)
    __rmul__=__mul__
    def __pow__(self,n):
        base=self
        if n<0:
            if self != Jet([0,1]): raise ValueError('Only q inverse needed')
            d=[0]*(2*self.order)
            for j in range(1,self.order+1): d[2*j-1]=-comb(self.order,j)
            base=Jet(d);n=-n
        ans=Jet(1)
        while n:
            if n%2:ans=ans*base
            base=base*base;n//=2
        return ans
    def __eq__(self, other):
        if isinstance(other,int):other=Jet(other)
        return isinstance(other,Jet) and self.d==other.d
    def __bool__(self):return any(self.d)


class Ring:
    def one(self):return Jet(1)
    def zero(self):return Jet(0)
    def __call__(self,x):return x if isinstance(x,Jet) else Jet(x)
    def __contains__(self,x):return isinstance(x,(int,Jet))


def probe(link, expected_product):
    """expected_product uses signed Jones determinants V(K_i)(i), not abs."""
    from spherogram.links import jones
    from sagefree_jones import PerfectMatching
    m=len(link.link_components)+link.unlinked_unknot_components
    Jet.order=m+1
    original=(jones.R,jones.q,jones.PerfectMatching)
    try:
        jones.R=Ring();jones.q=Jet([0,1]);jones.PerfectMatching=PerfectMatching
        # Use the same skein contraction, discarding coefficients that are
        # exactly zero in the quotient ring after each event. Full-polynomial
        # code retains these states, which defeats much of the truncation.
        from spherogram.links import exhaust
        # Deterministic layout selection; crossing order can change cost by
        # orders of magnitude while leaving the invariant unchanged.
        starts=list(link.crossings)
        starts=starts[::max(1,len(starts)//16)][:16]
        choices=[exhaust.MorseExhaustion(link,c) for c in starts] if starts else [exhaust.MorseExhaustion(link)]
        encoded=exhaust.MorseEncoding(min(choices,key=lambda e:e.width))
        value=jones.VElement()
        max_states=1
        for event in encoded:
            if event.kind=='cup':value=value.insert_cup(event.min)
            elif event.kind=='cap':value=value.cap_off(event.min)
            elif event.a<event.b:value=value.add_positive_crossing(event.min)
            else:value=value.add_negative_crossing(event.min)
            value.dict={key:c for key,c in value.dict.items() if c}
            max_states=max(max_states,len(value.dict))
        empty=PerfectMatching([])
        assert not (set(value.dict)-{empty})
        value=value.dict.get(empty,Jet(0))
        signs=[c.sign for c in link.crossings]
        minus,plus=signs.count(-1),signs.count(1)
        value=(-1)**minus*jones.q**(plus-2*minus)*value
    finally:
        jones.R,jones.q,jones.PerfectMatching=original
    d=list(value.d);quot=[0,0]
    # Divide by (q^2+1)^m over Z/32. The divisor is monic.
    for k in range(len(d)-1,2*m-1,-1):
        c=d[k]%32;quot[k-2*m]=c
        for j in range(m+1):d[k-2*m+2*j]-=c*comb(m,j)
    remainder=[x%32 for x in d[:2*m]]
    # delta=q^-1(q^2+1); convert h-quotient to delta-quotient.
    product=Jet(quot)*Jet([0,1])**m
    a=sum(c*(-1)**(i//2) for i,c in enumerate(product.d) if i%2==0)%32
    b=sum(c*(-1)**(i//2) for i,c in enumerate(product.d) if i%2)%32
    return {'components':m,'crossings':len(link.crossings),'jet_mod_32':list(value.d),
            'morse_width':encoded.width,'max_retained_states':max_states,'exhaustion_starts_tested':len(choices),
            'divisibility_remainder_mod_32':remainder,
            'quotient_at_i_mod_32':[a,b], 'expected_mod_32':expected_product%32,
            'ribbon_obstructed_mod_32':bool(any(remainder) or b or a!=expected_product%32),
            'scope':'Necessary ribbon conditions only; zero residue is inconclusive.'}


if __name__=='__main__':
    import snappy
    data=json.load(sys.stdin)
    link=snappy.Link(data['pd'])
    print(json.dumps(probe(link,data['expected_product'])),flush=True)
