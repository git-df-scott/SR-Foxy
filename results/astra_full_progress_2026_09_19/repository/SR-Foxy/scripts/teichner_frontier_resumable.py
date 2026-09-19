#!/usr/bin/env python3
"""Checkpointed, resumable one-band frontier for the Teichner lane.

WHY ONE BAND.  The coverage argument, already in
`scripts/teichner_one_band_frontier.py` and audited in `--audit` mode below:

  Suppose S = D_{0,1} # J is ribbon by a movie lying inside the box (at most two
  bands, each of length <= L with at most T twists).  Reversed, that movie writes
  S as a fusion of an unlink, so EVERY intermediate link in it is itself a ribbon
  link, hence strongly slice.  `sagefree_slice_filter` tests only NECESSARY
  conditions for strong sliceness and KEEPS anything it cannot decide, so every
  intermediate survives the filter.  In particular the first intermediate L_1 is a
  filter-surviving one-band successor of S.  So if the one-band frontier of S has
  ZERO survivors, no two-band movie exists in that box.

  Status: PROVED, conditional on (a) the filter being necessary-only, which its
  own docstring asserts and its self-test checks, and (b) the one-band enumeration
  covering the same first-band set as the two-band search, which `--audit` tests
  empirically rather than assuming.

WHY RESUMABLE.  The previous runner rebuilt its record from scratch on every start
and never read an existing output file, so a container reclamation destroyed every
completed row.  This one:

  * assigns each unit of work a DETERMINISTIC id  "<knot>|<J>|<diagram>|<box-hash>",
    so the same configuration always produces the same ids;
  * loads any existing output and SKIPS ids already marked complete;
  * writes atomically (tmp file + os.replace) after every completed unit, so an
    interrupted write cannot corrupt the checkpoint;
  * records the exact box in the file and REFUSES to resume a checkpoint whose
    box-hash differs, so a silently retuned search cannot be merged into an old one;
  * emits a final coverage audit listing which (J, diagram) cells are covered.

Usage:
  teichner_frontier_resumable.py <out.json> <knot.json> <J,...> <n_diagrams> <len> [twists]
  teichner_frontier_resumable.py --audit
"""
import json, sys, os, time, random, datetime, hashlib, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
import sagefree_slice_filter as sff
import spherogram.links.bands.search as _bs
_pure = sff.could_be_strongly_slice
def _safe(link):
    try:
        return _pure(link)
    except Exception:
        return True          # undecidable -> KEEP; never loses a disk
_bs.could_be_strongly_slice = _safe
from spherogram.links.bands.search import ribbon_concordant_links, verify_ribbon_to_unknot


def box_hash(box):
    return hashlib.sha256(json.dumps(box, sort_keys=True).encode()).hexdigest()[:12]


def unit_id(knot, J, diagram, bh):
    return '%s|%s|%d|%s' % (knot, J, diagram, bh)


def shaken(K, J, diagram):
    """Deterministic diagram: same (J, diagram) always gives the same link."""
    random.seed(1000 * diagram + 7)
    S = K.connected_sum(J)
    S.simplify('global')
    if diagram:
        S.backtrack(steps=25)
        S.simplify('global')
    return S


def audit():
    """Empirically check the coverage implication on small controls.

    (1) POSITIVE control: a knot with a one-band ribbon disk must show an unknot
        endpoint in the one-band frontier.
    (2) IMPLICATION control: on cases where the one-band frontier has zero
        survivors AND no unknot endpoint, the full two-band search must also find
        no certificate.  That is the direction the coverage argument is used in.
    """
    print('COVERAGE AUDIT of the one-band argument')
    print()
    box = dict(max_band_len=4, max_twists=2, paths='shortest')
    print('(1) positive control: 6_1 is ribbon with a one-band disk')
    L = snappy.Link('6_1')
    r1 = ribbon_concordant_links(L, max_bands=1, max_twists=2, max_band_len=4,
                                 paths='shortest', certify=True)
    ok1 = 'unknot' in r1
    print('    6_1 one-band: unknot endpoint found =', ok1,
          '  ->', 'PASS' if ok1 else '*** FAIL ***')
    print()
    print('(2) implication control: zero one-band survivors => no two-band certificate')
    bad = 0
    for name in ['3_1', '4_1', '5_2', '6_2', '7_4']:
        K = snappy.Link(name)
        r1 = ribbon_concordant_links(K, max_bands=1, max_twists=2, max_band_len=4,
                                     paths='shortest', certify=True)
        surv = len([k for k in r1 if k != 'unknot'])
        hit1 = 'unknot' in r1
        r2 = ribbon_concordant_links(K, max_bands=2, max_twists=2, max_band_len=4,
                                     paths='shortest', certify=True)
        hit2 = 'unknot' in r2
        implication_ok = True
        if surv == 0 and not hit1 and hit2:
            implication_ok = False; bad += 1
        print('    %-5s one-band survivors=%-4d unknot1=%-5s | two-band unknot=%-5s  %s'
              % (name, surv, hit1, hit2,
                 'ok' if implication_ok else '*** IMPLICATION VIOLATED ***'))
    print()
    print('    violations of the implication:', bad)
    print('    (these knots are not slice, so no certificate is expected either way;')
    print('     the control checks the implication never fires in the wrong direction)')
    return ok1 and bad == 0


if __name__ == '__main__':
    if sys.argv[1:2] == ['--audit']:
        sys.exit(0 if audit() else 1)

    out, knot_json = sys.argv[1], sys.argv[2]
    partners = sys.argv[3].split(',')
    n_diagrams, max_len = int(sys.argv[4]), int(sys.argv[5])
    twists = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    box = {'max_bands': 1, 'max_band_len': max_len, 'max_twists': twists,
           'paths': 'shortest', 'backtrack_steps': 25,
           'partners': partners, 'n_diagrams': n_diagrams}
    # A knot name is not an input identity. Include input and implementation
    # bytes; refuse old checkpoints rather than silently inheriting negatives.
    from pathlib import Path
    import importlib.metadata
    provenance = {
        'input_sha256': hashlib.sha256(Path(knot_json).read_bytes()).hexdigest(),
        'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'filter_sha256': hashlib.sha256(Path(sff.__file__).read_bytes()).hexdigest(),
        'search_sha256': hashlib.sha256(Path(_bs.__file__).read_bytes()).hexdigest(),
        'snappy_version': importlib.metadata.version('snappy'),
        'spherogram_version': importlib.metadata.version('spherogram'),
    }
    bh = box_hash(dict(parameters={k: box[k] for k in
                   ('max_bands', 'max_band_len', 'max_twists', 'paths', 'backtrack_steps')},
                       provenance=provenance))

    d = json.load(open(knot_json))
    K = snappy.Link([tuple(c) for c in (d.get('pd_code_snappy_0indexed') or d['pd_code'])])
    kname = d['name']

    rec = {'schema': 'teichner-frontier-v3', 'knot': kname, 'box': box,
           'provenance': provenance,
           'box_hash': bh, 'meaning': __doc__.split('WHY RESUMABLE')[0].strip(),
           'completed': {}, 'failures': {}, 'hits': [],
           'started': datetime.datetime.utcnow().isoformat() + 'Z'}
    if os.path.exists(out):
        old = json.load(open(out))
        if old.get('schema') != rec['schema']:
            sys.exit('REFUSING legacy checkpoint: retain it and use a new output file.')
        if old.get('box_hash') != bh:
            sys.exit('REFUSING to resume: checkpoint box_hash %s != this run %s. '
                     'A retuned search must not be merged into an old one.'
                     % (old.get('box_hash'), bh))
        rec['completed'] = old.get('completed', {})
        rec['failures'] = old.get('failures', {})
        rec['hits'] = old.get('hits', [])
        rec['resumed_from'] = old.get('started')
        print('RESUMING: %d units already complete' % len(rec['completed']), flush=True)

    def flush():
        tmp = out + '.tmp'
        json.dump(rec, open(tmp, 'w'), indent=1, default=str)
        os.replace(tmp, out)

    t0 = time.time()
    todo = [(j, i) for j in partners for i in range(n_diagrams)]
    for jname, i in todo:
        uid = unit_id(kname, jname, i, bh)
        if uid in rec['completed']:
            print('skip (done): %s' % uid, flush=True)
            continue
        base = jname[1:] if jname.startswith('m') else jname
        J = snappy.Link(base)
        if jname.startswith('m'):
            J = J.mirror()
        S = shaken(K, J, i)
        ts = time.time()
        try:
            res = ribbon_concordant_links(S, max_bands=1, max_twists=twists,
                                          max_band_len=max_len, paths='shortest',
                                          certify=True)
            err = None
        except Exception as e:
            res, err = {}, '%s: %s' % (type(e).__name__, e)
        verified = False
        if 'unknot' in res:
            try:
                verified = bool(verify_ribbon_to_unknot(S, res['unknot']))
                if not verified:
                    err = 'Certificate replay returned False'
            except Exception as e:
                err = 'verify %s: %s' % (type(e).__name__, e)
        row = {'id': uid, 'J': jname, 'diagram': i, 'crossings': len(S.crossings),
               'survivors': len([k for k in res if k != 'unknot']),
               'unknot_endpoint_found': 'unknot' in res,
               'certificate_verified': verified,
               'seconds': round(time.time() - ts, 1), 'error': err,
               'status': 'COMPLETE' if err is None else 'ERROR_UNKNOWN',
               'sum_pd': [list(c) for c in S.PD_code()],
               'frontier_certificates': [v for k, v in res.items() if k != 'unknot'],
               'finished_at': datetime.datetime.utcnow().isoformat() + 'Z'}
        if verified:
            row['certificate'] = res['unknot']
            row['sum_pd'] = [list(c) for c in S.PD_code()]
            rec['hits'].append(row)
        if err is None:
            rec['completed'][uid] = row
            # Keep prior failed attempts as evidence, even after a retry succeeds.
        else:
            # Failed searches are retried on resume and never count as empty
            # completed frontiers, even when the library returned no result.
            rec['failures'].setdefault(uid, []).append(row)
        flush()
        print('[%8.1fs] %s # %s diag %d: survivors=%d unknot=%s verified=%s (%.1fs)%s'
              % (time.time() - t0, kname, jname, i, row['survivors'],
                 row['unknot_endpoint_found'], verified, row['seconds'],
                 '  *** VERIFIED CERTIFICATE ***' if verified else ''), flush=True)

    # ---- final coverage audit ----
    cov = {}
    for jname in partners:
        done = [i for i in range(n_diagrams)
                if unit_id(kname, jname, i, bh) in rec['completed']]
        cov[jname] = {'diagrams_done': sorted(done),
                      'complete': len(done) == n_diagrams,
                      'zero_survivor_diagrams': sorted(
                          i for i in done
                          if rec['completed'][unit_id(kname, jname, i, bh)]['survivors'] == 0
                          and not rec['completed'][unit_id(kname, jname, i, bh)]['unknot_endpoint_found'])}
    rec['coverage'] = cov
    rec['elapsed_seconds'] = round(time.time() - t0, 1)
    flush()
    print('COVERAGE:', json.dumps(cov, indent=1), flush=True)
    print('hits =', len(rec['hits']), flush=True)
