#!/usr/bin/env python3
"""Teichner ribbon-certificate hunt over WILD MIYAZAKI PAIRS.

WHY THIS IS A COUNTEREXAMPLE SEARCH AND NOT A CANDIDATE SEARCH
--------------------------------------------------------------
Let J, J' be distinct prime fibered knots sharing one irreducible Alexander
polynomial, and put D = J # (-J').

  * D is NOT homotopy-ribbon, hence not ribbon, by Miyazaki Thm 5.5:
    its prime fibered summands J and -J' do not pair, and Miyazaki's second
    alternative holds because Delta is irreducible (no nonunit f with
    f(t)f(1/t) | Delta).  Primality is free by Lemma P (a fibered knot with
    irreducible Delta is prime).  This is the criterion of
    HANDOFF_2026_09_18_OPUS.md section 4, freed from Abe-Tagami.
  * Teichner (see scripts/teichner_certify.py) : K is smoothly slice iff there
    is a ribbon J0 with K # J0 ribbon.

So a VERIFIED ribbon certificate for D # J0, with J0 a verified ribbon knot,
proves D smoothly slice.  D slice and D not ribbon is a COUNTEREXAMPLE to the
Slice-Ribbon Conjecture, outright.  Equivalently it exhibits J ~ J'.

WHAT IS NEW HERE
----------------
This repository built the wild-pair criterion and then searched only for pairs
whose 0-SURGERIES agree (P1), as a proxy for concordance; that search came back
empty over the <= 14 crossing census (results/opus_2026_09_19_0700_*).  But the
Miyazaki certificate never needed the 0-surgery: it needs only distinct, prime,
fibered, irreducible Delta.  The band search tests sliceness DIRECTLY, so it
applies to all 2,925 shared-Delta buckets, not just the 0-surgery-matched ones.
The Teichner machine has only ever been pointed at D_{0,1} (25 crossings).
The cheapest wild pair here gives a 17-crossing D -- and this repository's own
measurement is that cost roughly doubles per two crossings of the sum.

NEGATIVES ARE COVERAGE, NOT OBSTRUCTIONS.  An absent certificate says the box
held no short ribbon movie; it says nothing about D being slice or not.

Usage:
  wild_pair_teichner_hunt.py <out.jsonl> <max_bands> <max_band_len> <n_pairs> [start]
Env:
  HUNT_J        comma-separated ribbon partners (default 6_1)
  HUNT_TWISTS   max_twists (default 2)
  HUNT_PATHS    'shortest' | 'simple' (default shortest)
  HUNT_PAIRS    path to the pair list JSON
"""
import json, os, sys, time, datetime, gzip, re
from collections import defaultdict

import snappy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sagefree_slice_filter as sff
import spherogram.links.bands.search as _bs
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot
from spherogram.links.bands import normalize_crossing_labels

_pure = sff.could_be_strongly_slice
def _safe_filter(link):
    """Keep the link whenever the filter cannot decide. Never lose a disk."""
    try:
        return _pure(link)
    except Exception:
        return True
_bs.could_be_strongly_slice = _safe_filter

J_LIST = os.environ.get('HUNT_J', '6_1').split(',')
TWISTS = int(os.environ.get('HUNT_TWISTS', 2))
PATHS = os.environ.get('HUNT_PATHS', 'shortest')
assert PATHS in ('shortest', 'simple')


def crossing_number(name):
    m = re.match(r'K?(\d+)[an]', name)
    return int(m.group(1)) if m else 99


def load_pairs(path):
    """Distinct fibered irreducible-Delta knots sharing Delta, tau, nu, eps, genus."""
    rows = [json.loads(l) for l in gzip.open(path, 'rt')]
    rows = [r for r in rows if 'delta' in r]
    buck = defaultdict(list)
    for r in rows:
        buck[tuple(r['delta'])].append(r)
    pairs = []
    for k, v in buck.items():
        if len(v) < 2:
            continue
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                a, b = v[i], v[j]
                if (a['tau'], a['nu'], a['eps'], a['genus']) == \
                   (b['tau'], b['nu'], b['eps'], b['genus']):
                    pairs.append(dict(
                        cr_sum=crossing_number(a['name']) + crossing_number(b['name']),
                        A=a['name'], B=b['name'], genus=a['genus'],
                        deg_delta=len(k) - 1, tau=a['tau'], nu=a['nu'], eps=a['eps']))
    pairs.sort(key=lambda p: (p['cr_sum'], p['A'], p['B']))
    return pairs


def certify(link, result):
    if 'unknot' not in result:
        return False, None
    cert = result['unknot']
    return bool(verify_ribbon_to_unknot(link, cert)), cert


def main():
    out, max_bands, max_len, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    start = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    pair_path = os.environ.get(
        'HUNT_PAIRS',
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', 'data', 'sweeps', 'miyazaki_pair_sweep.jsonl.gz'))
    pairs = load_pairs(pair_path)

    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if 'A' in r:
                done.add((r['A'], r['B'], r['J'], max_bands, max_len, TWISTS, PATHS))

    box = dict(max_bands=max_bands, max_band_len=max_len,
               max_twists=TWISTS, paths=PATHS, J_list=J_LIST)
    print(f'# pairs available: {len(pairs)}; running [{start}:{start+n}]  box={box}',
          flush=True)

    partner = {}
    fh = open(out, 'a')
    t0 = time.time()
    for p in pairs[start:start + n]:
        for jname in J_LIST:
            key = (p['A'], p['B'], jname, max_bands, max_len, TWISTS, PATHS)
            if key in done:
                continue
            if jname not in partner:
                J = snappy.Link(jname)
                pr = ribbon_concordant_links(J, max_bands=max_bands, max_twists=TWISTS,
                                             max_band_len=max_len, paths=PATHS, certify=True)
                ok, cert = certify(J, pr)
                partner[jname] = ok
                print(f'[{time.time()-t0:7.1f}s] CONTROL partner {jname} verified={ok}',
                      flush=True)
            # D = A # mirror(B), then connect-sum the ribbon partner
            A = snappy.Link(p['A'])
            B = snappy.Link(p['B']).mirror()
            D = A.connected_sum(B)
            D.simplify('global')
            d_cr = len(D.crossings)
            S = D.connected_sum(snappy.Link(jname))
            S.simplify('global')
            # connected_sum leaves tuple-valued crossing labels.  REDUNDANT, not
            # a fix: ribbon_concordant_links normalizes its own copy before any
            # band generation.  Kept as belt and braces; it costs nothing.
            normalize_crossing_labels(S)
            ts = time.time()
            res = ribbon_concordant_links(S, max_bands=max_bands, max_twists=TWISTS,
                                          max_band_len=max_len, paths=PATHS, certify=True)
            ok, cert = certify(S, res)
            row = dict(p, J=jname, box=box, D_crossings=d_cr,
                       sum_crossings=len(S.crossings),
                       partner_certificate_verified=partner[jname],
                       endpoints=sorted(res.keys()),
                       unknot_endpoint_found='unknot' in res,
                       certificate_verified=ok,
                       certificate=cert if ok else None,
                       seconds=round(time.time() - ts, 1),
                       when=datetime.datetime.utcnow().isoformat() + 'Z')
            fh.write(json.dumps(row) + '\n')
            fh.flush()
            os.fsync(fh.fileno())
            print(f'[{time.time()-t0:7.1f}s] DONE {p["A"]} # -{p["B"]} # {jname}  '
                  f'D={d_cr}cr sum={len(S.crossings)}cr  unknot={row["unknot_endpoint_found"]}'
                  f'  verified={ok}  {row["seconds"]}s', flush=True)
            if ok:
                print('*** VERIFIED RIBBON CERTIFICATE -- '
                      'SLICE-RIBBON COUNTEREXAMPLE CANDIDATE, REPLAY IT ***', flush=True)
    fh.close()


if __name__ == '__main__':
    main()
