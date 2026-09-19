#!/usr/bin/env python3
"""Validate Eisermann's Theorems 1 and 2 against the certified RibbonLinks census.

WHY.  research/53 sets out the GST link lane: if `det V(L_{3,1}) != 17 (mod 32)`
then L_{3,1} is slice and not ribbon, the first such object of any kind.  The
lane has been blocked all campaign because an isolated computation on a
hand-traced diagram cannot be trusted -- a tracing slip or a convention error
yields a wrong residue that looks exactly like a counterexample.

research/53 supplies two known-answer controls inside the GST family (L_{1,1}
-> 9, L_{2,1} -> 17, both known ribbon).  This script supplies the step before
those, which needs no GST object at all: run the pipeline over SnapPy's
RibbonLinks census, 12,184 links each shipping a ribbon certificate, and check
that Eisermann's theorems hold on every one.

  Theorem 1.  n-component ribbon link  =>  null V(L) = n - 1
  Theorem 2.  n-component ribbon link  =>  det V(L) = det(K_1)...det(K_n) (mod 32)

Every link here IS ribbon, so both must hold.  A single violation means the
implementation, the convention, or the normalisation is wrong -- and would have
produced a false counterexample on L_{3,1}.  A clean pass over a large sample is
the strongest statement available that the tool is sound before it is pointed at
an object whose answer nobody knows.

This is a validation, not a search: it cannot find a counterexample, only
prevent a fake one.

Usage: eisermann_validate_on_ribbon_census.py <out.jsonl> [n_links] [max_crossings]
"""
import json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snappy
from sagefree_eisermann import null_and_det_V
import sagefree_slice_filter as _sff


def component_determinants_sagefree(L):
    """det of each component, without Sage.

    sagefree_eisermann.component_determinants reaches Link.determinant(), which
    this repository already records as Sage-only -- it is what made every
    earlier fission script vacuous here.  Each component is extracted as a
    sublink and its determinant taken from a Seifert matrix instead.
    """
    out = []
    for i in range(len(L.link_components)):
        K = L.sublink([i])
        # A component that survives as a 0-crossing diagram is an unknot,
        # det 1.  Passing it to the Seifert-matrix routine raises
        # UnboundLocalError('start') from inside spherogram -- that single
        # case accounted for 65 of 73 failures in the first run of this
        # script, and is not a property of the links.
        if len(K.crossings) == 0:
            out.append(1)
            continue
        _sig, det = _sff.signature_and_det(K)
        out.append(abs(int(det)))
    return out


def main():
    out = sys.argv[1]
    n_links = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    max_cr = int(sys.argv[3]) if len(sys.argv) > 3 else 12

    done = set()
    if os.path.exists(out):
        for line in open(out):
            try:
                done.add(json.loads(line)['name'])
            except Exception:
                pass

    census = snappy.RibbonLinks
    # RibbonLinks entries are Manifolds (link EXTERIORS), not Links; .link()
    # recovers the diagram.  Names encode ribbon_<components>_<crossings>_<hash>.
    print(f'RibbonLinks census: {len(census)} certified ribbon links; '
          f'sampling up to {n_links} with <= {max_cr} crossings', flush=True)

    fh = open(out, 'a')
    t0 = time.time()
    n = ok1 = ok2 = bad1 = bad2 = err = 0
    for M in census:
        if n >= n_links:
            break
        try:
            name = M.name()
        except Exception:
            name = str(M)
        if name in done:
            continue
        try:
            L = M.link()
            if len(L.crossings) > max_cr:
                continue
            ncomp = len(L.link_components)
            if ncomp < 2:
                continue                      # Theorem 1 is vacuous for knots
            nullV, detV, _detail = null_and_det_V(L)
            dets = component_determinants_sagefree(L)
            prod = 1
            for d in dets:
                prod *= d
            interesting = (prod % 32) != 1
            t1 = (nullV == ncomp - 1)
            t2 = (detV % 32) == (prod % 32)
            ok1 += t1; ok2 += t2
            bad1 += (not t1); bad2 += (not t2)
            row = dict(name=name, crossings=len(L.crossings), components=ncomp,
                       null_V=nullV, det_V=detV, component_dets=dets,
                       product=prod, det_V_mod32=detV % 32, product_mod32=prod % 32,
                       thm1_pass=bool(t1), thm2_pass=bool(t2),
                       knotted_components=bool(interesting))
            if not (t1 and t2):
                print(f'*** VIOLATION {name}: thm1={t1} thm2={t2} '
                      f'nullV={nullV} n-1={ncomp-1} detV%32={detV%32} '
                      f'prod%32={prod%32} ***', flush=True)
        except Exception as e:
            err += 1
            row = dict(name=name, error=f'{type(e).__name__}: {e}'[:180])
        fh.write(json.dumps(row) + '\n'); fh.flush()
        n += 1
        if n % 25 == 0:
            print(f'[{time.time()-t0:7.1f}s] {n} links | Thm1 {ok1} pass / {bad1} fail'
                  f' | Thm2 {ok2} pass / {bad2} fail | {err} errors', flush=True)
    fh.close()
    import collections as _c
    rows = [json.loads(l) for l in open(out)]
    good = [r for r in rows if 'error' not in r]
    hard = [r for r in good if r.get('knotted_components')]
    print('# residue distribution det(K_1)...det(K_n) mod 32: '
          + str(dict(_c.Counter(r['product_mod32'] for r in good))), flush=True)
    print(f'# links with KNOTTED components (product != 1 mod 32): {len(hard)}; '
          f'of these Thm2 passes on {sum(r["thm2_pass"] for r in hard)}', flush=True)
    print('# links at the GST residue 17 mod 32: '
          + str(sum(1 for r in good if r['product_mod32'] == 17)), flush=True)
    print(f'# FINAL: {n} links | Theorem 1: {ok1} pass, {bad1} FAIL '
          f'| Theorem 2: {ok2} pass, {bad2} FAIL | {err} errors', flush=True)
    # The verdict must not be a bare "no failures": a run that errors on most
    # inputs and passes on a handful of UNLINK-component links has validated
    # almost nothing, and the GST test needs the KNOTTED case at residue 17.
    enough = len(good) >= 25
    knotted = len(hard) >= 5
    if bad1 or bad2:
        print('# pipeline NOT validated -- a certified ribbon link VIOLATED '
              'Eisermann. Do not point it at L_{3,1}.', flush=True)
    elif enough and knotted:
        print('# pipeline validated on a usable sample INCLUDING knotted '
              'components; sound for the GST test', flush=True)
    else:
        print(f'# INCONCLUSIVE: {len(good)} links evaluated ({len(hard)} with '
              f'knotted components), {err} tool failures. No violation seen, but '
              f'this is too small a sample to call the pipeline validated.',
              flush=True)


if __name__ == '__main__':
    main()
