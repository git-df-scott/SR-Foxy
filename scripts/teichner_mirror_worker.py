#!/usr/bin/env python3
"""One (partner, chirality, diagram) Teichner case; run under an external timeout.

Called by teichner_mirror_partners.py.  Kept in its own process so a slow case
costs its own time cap and nothing else -- the repository's earlier probes used
the same worker pattern for the same reason.

Usage: teichner_mirror_worker.py <partner> <0|1 mirrored> <diagram> <bands>
                                 <band_len> <backtrack> <out.json>
"""
import json, sys, time
import snappy
from spherogram.links.bands.search import (ribbon_concordant_links,
                                           verify_ribbon_to_unknot)
import snappy.sage_helper as sh
assert sh._within_sage, 'needs SnapPy inside Sage'

import spherogram.links.bands.search as _bs
_orig_filter = _bs.could_be_strongly_slice
def _safe_filter(link):
    try:
        return _orig_filter(link)
    except ValueError:
        return True
_bs.could_be_strongly_slice = _safe_filter


def certified(link, result):
    if 'unknot' not in result:
        return False
    return bool(verify_ribbon_to_unknot(link, result['unknot']))


def main():
    name, mirrored, diagram, bands, band_len, backtrack, out = (
        sys.argv[1], bool(int(sys.argv[2])), int(sys.argv[3]),
        int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
    import os
    target = os.environ.get('TM_TARGET', 'data/knots/AbeTagami_D_0_1.json')
    if target.startswith('census:'):          # positive-control targets
        D = snappy.Link(target.split(':', 1)[1])
    else:
        data = json.load(open(target))
        D = snappy.Link([tuple(c) for c in
                         (data.get('pd_code_snappy_0indexed') or data['pd_code'])])
    J = snappy.Link(name)
    if mirrored:
        J = J.mirror()
    label = ('mirror(%s)' if mirrored else '%s') % name

    pres = ribbon_concordant_links(J, max_bands=bands, max_twists=2,
                                   max_band_len=band_len, certify=True)
    partner_ok = certified(J, pres)

    import random; random.seed(20260914 + diagram)
    S = D.connected_sum(J)
    S.simplify('global')
    if diagram:
        S.backtrack(backtrack)
        S.simplify('global')

    t = time.time()
    res = ribbon_concordant_links(S, max_bands=bands, max_twists=2,
                                  max_band_len=band_len, certify=True)
    row = {'target': target, 'partner': label, 'diagram': diagram,
           'sum_crossings': len(S.crossings), 'endpoints': len(res),
           'partner_ribbon_verified': partner_ok,
           'seconds': round(time.time() - t, 1), 'certified_slice': False,
           'completed': True}
    if 'unknot' in res:
        row['certificate_verified'] = certified(S, res)
        row['certified_slice'] = row['certificate_verified'] and partner_ok
        row['certificate'] = res['unknot']
        row['sum_pd_code'] = S.PD_code()
        row['partner_certificate'] = pres.get('unknot')
        if row['certified_slice']:
            print('*** TEICHNER CERTIFICATE ***', target, '#', label,
                  'diagram', diagram, flush=True)
    json.dump(row, open(out, 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in row.items()
                      if k not in ('certificate', 'sum_pd_code',
                                   'partner_certificate')}), flush=True)


if __name__ == '__main__':
    main()
