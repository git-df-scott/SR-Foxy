#!/usr/bin/env python3
"""Independent screen of the connected-prefix lemma's necessary condition.

research/19: a two-component link L occurring as the top of a CONNECTED movie
prefix of a concordance must be link-concordant to a split knot/unknot pair,
hence (granting the concordance invariance of the generic Alexander rank, which
research/19 flags as needing a primary source) must have generic Alexander
module rank one, equivalently vanishing multivariable Alexander polynomial.

This computes Delta_L(t_1,t_2) directly from each stored link diagram, via the
link exterior, independently of any triangulation-group calculation.

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
    L = snappy.Link([tuple(c) for c in pd])
    L.simplify('global')
    return L.exterior().alexander_polynomial()

# --- calibration: both directions must fire ---
cal = {}
cal['split_3_1_U_4_1'] = str(split_union('3_1', '4_1').exterior().alexander_polynomial())
cal['hopf_L2a1'] = str(snappy.Link('L2a1').exterior().alexander_polynomial())
cal['whitehead_L5a1'] = str(snappy.Link('L5a1').exterior().alexander_polynomial())
ok = (cal['split_3_1_U_4_1'] == '0'
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
       'meaning': ('Delta = 0 passes the necessary condition of research/19. It is not a '
                   'concordance, not a splitness proof and not a counterexample.'),
       'zero': [], 'nonzero': 0, 'errors': []}
t0 = time.time(); n = 0
for run in d['runs']:
    for m in run['matches']:
        if cap and n >= cap: break
        n += 1
        try:
            p = delta(m['link_pd'])
            if str(p) == '0':
                rec['zero'].append({'index': run['index'], 'band': m['band'],
                                    'link_pd': m['link_pd']})
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
