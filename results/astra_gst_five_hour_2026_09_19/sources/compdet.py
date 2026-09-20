"""Component knots and their determinants without Link.sublink.

sublink() dies in spherogram's Seifert path (UnboundLocalError: 'start') on most
census links, which is what stalled the Eisermann validation.  Here the other
components are spliced out directly on the crossing graph:

  * a crossing all of whose four strands lie on component i is kept;
  * a crossing component i passes through once is deleted and its two
    pass-through strands (indices a and a+2) are reconnected;
  * a crossing component i misses entirely is deleted with its component.

det(K) is then |V_K(q=i)|, computed by the repository's own sage-free Jones
code -- the same code path already validated on the Eisermann controls -- since
for a KNOT V(-1) = Delta(-1) = +-det(K).
"""
import os, sys
import spherogram

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, 'SR-Foxy', 'scripts'))
from sagefree_jones import jones_polynomial          # noqa: E402


def _eval_at_i(p):
    re = im = 0
    for e, c in p.d.items():
        m = e % 4
        if m == 0:   re += c
        elif m == 1: im += c
        elif m == 2: re -= c
        else:        im -= c
    return re, im


def knot_determinant(K):
    """|V_K(q=i)| for a one-component diagram; 1 for the empty diagram."""
    if not K.crossings:
        return 1
    re, im = _eval_at_i(jones_polynomial(K))
    return abs(re) if im == 0 else abs(complex(re, im))


def component_knot(link, i):
    """Component i of `link` as a standalone knot diagram.

    A crossing is a genuine SELF-crossing of the component exactly when the
    component runs through it twice, i.e. it contributes two CrossingStrands to
    link_components[i].  (It contributes two strand INDICES, never four -- the
    other two belong to the reverse traversal, which is not listed.  Testing
    for four indices was wrong and deleted every crossing, turning every
    component into an unknot.)
    """
    L = link.copy()
    comp = L.link_components[i]
    visits = {}
    for cs in comp:
        visits.setdefault(cs.crossing, []).append(cs.strand_index)
    keep, splice, drop = [], [], []
    for c in L.crossings:
        v = visits.get(c)
        if v is None:
            drop.append(c)
        elif len(v) >= 2:
            keep.append(c)
        else:
            splice.append((c, v[0]))
    for c, a in splice:
        x, y = c.adjacent[a % 4], c.adjacent[(a + 2) % 4]
        x[0].adjacent[x[1]] = y
        y[0].adjacent[y[1]] = x
    for c in [c for c, _ in splice] + drop:
        L.crossings.remove(c)
    if not L.crossings:
        return spherogram.Link([])
    K = spherogram.Link(L.crossings, check_planarity=False)
    K.simplify('global')
    return K


def component_determinants(link):
    out = []
    for i in range(len(link.link_components)):
        try:
            out.append(knot_determinant(component_knot(link, i)))
        except Exception as e:
            out.append(('ERR', type(e).__name__))
    return out
