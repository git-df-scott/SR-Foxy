#!/usr/bin/env python3
"""Time-boxed BREADTH probe over wild Miyazaki pairs.

Rationale.  A ribbon disk, when one exists, is usually found quickly: this
repository's own calibration found K_B's disk in 0.87 s on the first diagram,
and Dunfield-Gong report most of their disks at <= 2 bands.  What is expensive
is EXHAUSTING a box to prove absence -- and absence is not what this lane wants.
A counterexample needs one hit.  So spend a fixed small budget per target and
move on, covering many targets instead of exhausting few.

For distinct prime fibered J, J' sharing one irreducible Alexander polynomial,
D = J # (-J') is certified NOT homotopy-ribbon (Miyazaki Thm 5.5, primality by
Lemma P).  By Teichner, a VERIFIED ribbon certificate for D # J0 with J0 ribbon
proves D slice -- slice and not ribbon, a counterexample outright.

Both mirror orientations are tried: a census entry names a knot only up to
mirror, so D = J # (-J') and D = J # J' are both legitimate Miyazaki targets.

*** LABELLING, which this repository is strict about ***
A target that returns no certificate within its budget is recorded as
`timeout`, which is NOT coverage of its box and supports NO conclusion --
neither that D is non-slice nor that the box is empty.  Only `completed`
targets are coverage, and only `certificate_verified` is a result.

Usage: wild_pair_breadth_probe.py <out.jsonl> <budget_s> <n_targets> [start]
Env: PROBE_J (default 6_1), PROBE_BANDS (2), PROBE_LEN (4), PROBE_TWISTS (2)
"""
import json, os, subprocess, sys, time, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

WORKER = r'''
import json, os, sys
sys.path.insert(0, %r)
import snappy, sagefree_slice_filter as sff
import spherogram.links.bands.search as _bs
# PROBE_FILTER: 'full'  = sagefree_slice_filter.could_be_strongly_slice
#                         (linking numbers + Seifert signature + Fox-Milnor)
#               'cheap' = linking numbers only.
# Both are NECESSARY conditions for a link to be strongly slice, so both can
# only reject links the real filter would also reject -- neither can lose a
# ribbon disk.  'cheap' is ~48x faster here because 'full' builds a Seifert
# matrix for every candidate band, via an isotopy to a braid.
_MODE = os.environ.get('PROBE_FILTER', 'cheap')
def _f(l):
    try:
        if _MODE == 'cheap':
            return sff.linking_nums_all_zero(l)
        return sff.could_be_strongly_slice(l)
    except Exception:
        return True
_bs.could_be_strongly_slice = _f
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot
A, B, mirror_B, J0, nb, ml, tw = json.loads(sys.argv[1])
a = snappy.Link(A)
b = snappy.Link(B)
if mirror_B:
    b = b.mirror()
D = a.connected_sum(b); D.simplify('global')
S = D.connected_sum(snappy.Link(J0)); S.simplify('global')
res = ribbon_concordant_links(S, max_bands=nb, max_twists=tw, max_band_len=ml,
                              paths='shortest', certify=True)
ok = False; cert = None
if 'unknot' in res:
    cert = res['unknot']
    ok = bool(verify_ribbon_to_unknot(S, cert))
print(json.dumps(dict(D_crossings=len(D.crossings), sum_crossings=len(S.crossings),
                      endpoints=sorted(map(str, res.keys())),
                      unknot_endpoint_found='unknot' in res,
                      certificate_verified=ok,
                      certificate=cert if ok else None)))
''' % (HERE,)


def main():
    out, budget, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    J0 = os.environ.get('PROBE_J', '6_1')
    nb = int(os.environ.get('PROBE_BANDS', 2))
    ml = int(os.environ.get('PROBE_LEN', 4))
    tw = int(os.environ.get('PROBE_TWISTS', 2))

    # Prefer the Levine-Tristram-filtered survivor list when it exists: a pair
    # LT killed is PROVED not concordant, so its D is proved not slice.
    lt = os.path.join(HERE, '..', 'results', 'ce_hunt_2026_09_19', 'lt_filter_full.json')
    if os.path.exists(lt):
        d = json.load(open(lt))
        if d.get('controls_pass'):
            pairs = d['survivors']
            src = 'levine-tristram survivors'
        else:
            raise SystemExit('LT filter controls did not pass; refusing to use it')
    else:
        import wild_pair_teichner_hunt as wp
        pairs = wp.load_pairs(os.path.join(HERE, '..', 'data', 'sweeps',
                                           'miyazaki_pair_sweep.jsonl.gz'))
        src = 'unfiltered pair list'

    # one target per (pair, orientation)
    targets = []
    for p in pairs:
        for orient in p.get('lt_surviving_orientations', ["J # (-J')", "J # J'"]):
            targets.append((p, orient, orient == "J # (-J')"))
    targets = targets[start:start + n]

    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                r = json.loads(line)
            except Exception:
                continue
            done.add((r['A'], r['B'], r['orientation'], r['J0'],
                      r['box']['bands'], r['box']['len'], r['box']['twists']))

    box = dict(bands=nb, len=ml, twists=tw, paths='shortest',
               filter=os.environ.get('PROBE_FILTER', 'cheap'))
    print(f'# source: {src}; targets [{start}:{start+n}] of this slice; '
          f'budget {budget}s; box {box}', flush=True)
    fh = open(out, 'a')
    t0 = time.time()
    hits = comp = to = err = 0
    for p, orient, mirror_B in targets:
        key = (p['A'], p['B'], orient, J0, nb, ml, tw)
        if key in done:
            continue
        arg = json.dumps([p['A'], p['B'], mirror_B, J0, nb, ml, tw])
        ts = time.time()
        status, payload = 'completed', {}
        try:
            r = subprocess.run([sys.executable, '-c', WORKER, arg],
                               capture_output=True, text=True, timeout=budget)
            if r.returncode != 0:
                status, payload = 'error', {'stderr': r.stderr.strip()[-300:]}
                err += 1
            else:
                payload = json.loads(r.stdout.strip().splitlines()[-1])
                comp += 1
        except subprocess.TimeoutExpired:
            status = 'timeout'
            to += 1
        except Exception as e:
            status, payload = 'error', {'exc': repr(e)[:300]}
            err += 1
        row = dict(A=p['A'], B=p['B'], orientation=orient, J0=J0, box=box,
                   cr_sum=p.get('cr_sum'), genus=p.get('genus'),
                   status=status, seconds=round(time.time() - ts, 1),
                   when=datetime.datetime.utcnow().isoformat() + 'Z', **payload)
        fh.write(json.dumps(row) + '\n'); fh.flush(); os.fsync(fh.fileno())
        if row.get('certificate_verified'):
            hits += 1
            print('*** VERIFIED RIBBON CERTIFICATE *** '
                  f'{p["A"]} {orient} {p["B"]} # {J0} -- REPLAY IT', flush=True)
        print(f'[{time.time()-t0:7.1f}s] {status:9s} {p["A"]} {orient} {p["B"]} '
              f'# {J0}  {row["seconds"]}s  (hits={hits} completed={comp} '
              f'timeout={to} err={err})', flush=True)
    fh.close()
    print(f'# finished: hits={hits} completed={comp} timeout={to} error={err}', flush=True)


if __name__ == '__main__':
    main()
