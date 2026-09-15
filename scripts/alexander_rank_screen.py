#!/usr/bin/env python3
"""Independent screen of the connected-prefix lemma's necessary condition.

research/23: a two-component link L occurring as the top of a CONNECTED movie
prefix of a concordance must be link-concordant to a split knot/unknot pair,
hence (granting the concordance invariance of the generic Alexander rank, which
research/23 flags as needing a primary source) must have generic Alexander
module rank one, equivalently vanishing ORDER of the Alexander module.

This computes that order directly from each stored link diagram, via the link
exterior, independently of any triangulation-group calculation.

Note: snappy's Manifold.alexander_polynomial() on a link exterior returns the
ORDER of the Alexander module, not the classical multivariable link polynomial
Delta_L. On the Whitehead link it gives a^2b^3-ab^2-ab+1, whose b=1
specialisation is (a-1)^2, so it does not obey the Torres condition Delta_L
must satisfy. The order vanishes exactly when the module has positive rank,
which is the condition wanted here.

Calibration, checked at startup: split unions have Delta = 0, and the Hopf and
Whitehead links have Delta != 0. Without both directions firing the screen is
meaningless and the script refuses to report.

A link with Delta = 0 is NOT a concordance and NOT a counterexample. It only
passes one necessary condition that every stored match so far fails.

Usage: alexander_rank_screen.py <matches.json> <out.json> [max_links]
"""
import json, sys, time, datetime, hashlib
import snappy

def split_union(a, b):
    A = snappy.Link(a).PD_code(); B = snappy.Link(b).PD_code()
    n = max(max(c) for c in A) + 1
    return snappy.Link([tuple(c) for c in A] + [tuple([x + n for x in c]) for c in B])

def delta(pd):
    """Alexander-module order of the link exterior.

    Do NOT simplify first. Link.simplify('global') DELETES split unknot
    components: 3_1 with a split unknot (order 0, two components) becomes the
    bare trefoil (order a^2-a+1, one component). That inverts the verdict on
    exactly the links this screen is meant to accept, since a split
    knot-plus-unknot pair is the intended pass. An earlier version of this
    script simplified, and its published conclusions were wrong because of it.
    """
    L = snappy.Link([tuple(c) for c in pd])
    return L.exterior().alexander_polynomial(), len(L.link_components)

# --- calibration: both directions must fire ---
cal = {}
cal['split_3_1_U_4_1'] = str(split_union('3_1', '4_1').exterior().alexander_polynomial())
cal['hopf_L2a1'] = str(snappy.Link('L2a1').exterior().alexander_polynomial())
cal['whitehead_L5a1'] = str(snappy.Link('L5a1').exterior().alexander_polynomial())

# The calibration that actually caught the simplify bug: a knot with a SPLIT
# UNKNOT component must pass. The earlier split_union control could not catch
# it, because neither of its components is an unknot and so simplification had
# nothing to delete.
_A = snappy.Link('3_1').PD_code()
_n = max(max(c) for c in _A) + 1
_U = [(_n, _n+1, _n+1, _n+2), (_n+2, _n+3, _n+3, _n)]
_split_with_unknot = snappy.Link([tuple(c) for c in _A] + _U)
cal['split_3_1_U_unknot'] = str(_split_with_unknot.exterior().alexander_polynomial())
cal['split_3_1_U_unknot_components'] = len(_split_with_unknot.link_components)

ok = (cal['split_3_1_U_4_1'] == '0'
      and cal['split_3_1_U_unknot'] == '0'
      and cal['split_3_1_U_unknot_components'] == 2
      and cal['hopf_L2a1'] != '0'
      and cal['whitehead_L5a1'] != '0')
if not ok:
    print(json.dumps({'status': 'CALIBRATION_FAILED', 'calibration': cal}, indent=1))
    sys.exit(1)

src, out = sys.argv[1], sys.argv[2]
cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
d = json.load(open(src))

rec = {'date': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'source': src, 'source_sha256_16': hashlib.sha256(open(src,'rb').read()).hexdigest()[:16],
       'calibration': cal,
       'meaning': ('Delta = 0 passes the necessary condition of research/23. It is not a '
                   'concordance, not a splitness proof and not a counterexample.'),
       'zero': [], 'nonzero': 0, 'errors': []}
t0 = time.time(); n = 0
for run in d['runs']:
    for m in run['matches']:
        if cap and n >= cap: break
        n += 1
        try:
            p, ncomp = delta(m['link_pd'])
            if str(p) == '0':
                rec['zero'].append({'index': run['index'], 'band': m['band'],
                                    'components': ncomp, 'link_pd': m['link_pd']})
                print('ZERO DELTA', run['index'], m['band'], flush=True)
            else:
                rec['nonzero'] += 1
        except Exception as e:
            rec['errors'].append({'index': run['index'], 'band': m['band'],
                                  'error': '%s: %s' % (type(e).__name__, e)})
        if n % 50 == 0:
            rec['examined'] = n; rec['seconds'] = round(time.time()-t0, 1)
            json.dump(rec, open(out, 'w'), indent=1)
            print('... %d examined, %d zero, %d errors, %.0fs'
                  % (n, len(rec['zero']), len(rec['errors']), time.time()-t0), flush=True)
rec['examined'] = n
rec['seconds'] = round(time.time() - t0, 1)
json.dump(rec, open(out, 'w'), indent=1)
print(json.dumps({'examined': n, 'zero': len(rec['zero']),
                  'nonzero': rec['nonzero'], 'errors': len(rec['errors']),
                  'seconds': rec['seconds']}, indent=1))
