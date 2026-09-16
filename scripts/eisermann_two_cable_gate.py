"""Eisermann's ribbon-LINK theorems applied to a KNOT via its 0-framed 2-cable.

Claim being tested (stated before any computation):

  If K bounds a ribbon disk D in B^4, then the 0-framed pushoff D' is a disjoint
  ribbon disk, so the 0-framed 2-cable L = K^(2) = K u K' is a RIBBON 2-component
  link.  Contrapositive: if L is not a ribbon link, K is not a ribbon knot.

  Eisermann Thm 1 on L is VACUOUS whenever K is slice: slice K => L slice =>
  Delta(L) = 0 => null V(L) >= 1, and Lemma 1 caps null V <= n-1 = 1.
  Eisermann Thm 2 on L is NOT obviously vacuous:
        K ribbon  =>  det V(L) = det(K)*det(K) = det(K)^2   (mod 32).

This module only builds L and reports the two numbers.  Whether the congruence
has any teeth at all is an empirical question answered by the control block, not
by this docstring.
"""
import sys, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, 'scripts')
import snappy, spherogram
import sagefree_jones as SJ
import spherogram.links.links_base as lb

def _jp(self, new_convention=True, **kw):
    return SJ.jones_polynomial(self)
snappy.Link.jones_polynomial = lb.Link.jones_polynomial = _jp
import eisermann_ribbon_link_gate as G
from cable import cable_braid

def two_cable_0framed(K):
    """0-framed (Seifert-framed) 2-cable of the knot K, as a 2-component link."""
    w = K.writhe(); bw = K.braid_word()
    n = max(abs(x) for x in bw) + 1
    cw, ns = cable_braid(bw, n, 2, 0, w)
    return spherogram.Link(braid_closure=cw)

def linking_number(L):
    """lk of a 2-component link from crossing signs; Sage-free."""
    comp_of = {}
    for i, comp in enumerate(L.link_components):
        for ce in comp:
            comp_of[ce[0]] = i
    tot = 0
    for c in L.crossings:
        ends = {comp_of.get(c)}
        # a crossing joins two strands; find which components they belong to
        a = comp_of.get(c)
        if a is None:
            continue
    # fall back to the PD/sign route below
    return None


def linking_number_pd(L):
    """lk via PD code: half the signed count of inter-component crossings."""
    comps = L.link_components
    # map each crossing-strand entry to its component index
    which = {}
    for i, comp in enumerate(comps):
        for ce in comp:
            which[(ce[0], ce[1])] = i
    tot = 0
    for c in L.crossings:
        idx = [which.get((c, k)) for k in range(4)]
        idx = [x for x in idx if x is not None]
        if len(set(idx)) == 2:
            tot += c.sign
    return tot // 2


def det_from_hfk(K):
    sys.path.insert(0, 'scripts')
    from fox_milnor_sagefree import delta_from_hfk
    return abs(delta_from_hfk(K.knot_floer_homology()).eval(-1))


def report(name, K):
    L = two_cable_0framed(K)
    comps = len(L.link_components)
    try:
        lk = linking_number_pd(L)
    except Exception:
        lk = None
    detK = det_from_hfk(K)
    nv = G.nullity(L); dv = G.det_V(L, comps)
    return dict(name=name, cable_crossings=len(L.crossings), components=comps,
                linking_number=lk, det_K=detK, null_V=nv, det_V=dv)
