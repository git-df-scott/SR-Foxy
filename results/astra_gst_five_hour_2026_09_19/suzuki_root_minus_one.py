#!/usr/bin/env python3
"""Truncated unreduced Jones in F101[x]/(x^r), v=10+x.

Compute the root jet used by the Suzuki (3,3) q=-1 condition.
Nonzero residue obstructs ribbonness; zero is inconclusive. This does not
certify the satellite framing or smooth sliceness of its input.
"""
from math import comb
import json
import sys


class Jet:
    order=5
    def __init__(self, coefficients=0):
        if isinstance(coefficients,int):coefficients=[coefficients]
        self.d=tuple((coefficients[i] if i<len(coefficients) else 0)%101 for i in range(self.order))
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
            if self != Jet([10,1]):raise ValueError('Only v inverse supported')
            base=Jet([(-1)**i*pow(10,-(i+1),101) for i in range(self.order)]);n=-n
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


def probe(link,precision=5):
    """Return the unreduced Jones jet at v=10+x at the requested precision."""
    from spherogram.links import jones
    from sagefree_jones import PerfectMatching, install
    install()
    m=len(link.link_components)+link.unlinked_unknot_components
    Jet.order=precision
    original=(jones.R,jones.q,jones.PerfectMatching)
    try:
        jones.R=Ring();jones.q=Jet([10,1]);jones.PerfectMatching=PerfectMatching
        # Use the same skein contraction, discarding coefficients that are
        # exactly zero in the quotient ring after each event. Full-polynomial
        # code retains these states, which defeats much of the truncation.
        from spherogram.links import exhaust
        # Seeded layout selection; crossing order can change cost by
        # orders of magnitude while leaving the invariant unchanged.
        starts=list(link.crossings)
        starts=starts  # Exhaust every starting crossing, preserving the exact PD.
        import random
        saved_rng=random.getstate();choices=[]
        try:
            for seed in [20260920,20260921,20260922,20260923]:
                random.seed(seed)
                choices.extend(exhaust.MorseExhaustion(link,c) for c in starts)
        finally:random.setstate(saved_rng)
        def cost(e):return (e.width,sum(comb(k,k//2)//(k//2+1) for k in e.frontier_lengths))
        chosen=min(choices,key=cost)
        chosen_index=choices.index(chosen)
        encoded=exhaust.MorseEncoding(chosen)
        value=jones.VElement()
        max_states=1
        for event in encoded:
            if event.kind=='cup':value=value.insert_cup(event.min)
            elif event.kind=='cap':value=value.cap_off(event.min)
            elif event.a<event.b:value=value.add_positive_crossing(event.min)
            else:value=value.add_negative_crossing(event.min)
            value.dict={key:c for key,c in value.dict.items() if c}
            max_states=max(max_states,len(value.dict))
            if max_states>20000:raise RuntimeError("STATE_CAP_20000_INCONCLUSIVE")
        empty=PerfectMatching([])
        assert not (set(value.dict)-{empty})
        value=value.dict.get(empty,Jet(0))
        signs=[c.sign for c in link.crossings]
        minus,plus=signs.count(-1),signs.count(1)
        value=(-1)**minus*jones.q**(plus-2*minus)*value
    finally:
        jones.R,jones.q,jones.PerfectMatching=original
    return {'coefficients_mod101':list(value.d),'crossings':len(link.crossings),'morse_width':encoded.width,'max_retained_states':max_states,'chosen_layout_index':chosen_index,'morse_events':chosen.events,'layout_seeds':[20260920,20260921,20260922,20260923],'layout_score':cost(chosen),'starts_tested':len(choices),'scope':'Unreduced Jones in F101[x]/x^precision atv=10+x; modularzero is inconclusive.'}
