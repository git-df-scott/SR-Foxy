#!/usr/bin/env python3
"""Teichner search over BOTH chiralities of every non-fibered ribbon partner.

research/20 ("Second: exploit the specific mirror-partner lead") records that
the long 6_1 run used 6_1 and not its mirror, that both 6_1 and D01 are chiral
by Jones, and that mirrored partners must therefore not be dropped.  This
closes that gap for every partner, and shakes the connected-sum diagram the way
the K_B calibration did, since diagram choice dominated there.

Teichner: K is smoothly slice iff some ribbon J makes K # J ribbon.  D01 is
already non-ribbon by the Miyazaki/Abe-Tagami audit, so a verified certificate
here is a counterexample to the slice-ribbon conjecture.  It would still need
the checks research/20 demands before being called one: `are_same_link` allows
mirror equivalence, so a hit requires an orientation-compatible identification
of every intermediate link, not just this replay.

WITHDRAWN [16 Sep 2026], see ERRATA_2026-09-16.md (E16-1).  This docstring used
to say: "Fibered partners are excluded on purpose: for prime fibered J, D01 # J
is a connected sum of prime fibered knots and Miyazaki's pairing theorem forbids
it from being homotopy-ribbon."  That is wrong.  Miyazaki Thm 5.5 requires EVERY
prime fibered summand to be minimal in the homotopy-ribbon order or to have no
nonunit norm factor of Delta, and a nontrivial ribbon J fails both (it sits above
the unknot in the ribbon order, and Fox-Milnor makes Delta_J itself a nonunit
norm).  So the theorem does not apply to D01 # J and cannot obstruct any Teichner
sum.  8_9, 8_20 and 9_27 are legitimate partners and are included below.

The rule that IS correct: the sum is excluded iff every prime summand of J
satisfies one of the two alternatives.  That never excludes a prime fibered
ribbon J, and it does exclude J = L # (-L) -- the square knot 3_1 # (-3_1) being
the smallest case, since 3_1 has irreducible Delta = t^2 - t + 1 -- for which no
run can ever produce a certificate.  Do not add such a J to PARTNERS.

Each case runs in its own process under a wall-clock cap, so one slow case
cannot consume the whole budget -- breadth across partners and diagrams is the
point of this run.
"""
import json, os, subprocess, sys, time, datetime

PARTNERS = os.environ.get('TM_PARTNERS',
            '6_1,9_46,10_3,8_8,9_41,10_22,10_87,8_9,8_20,9_27').split(',')
BANDS = int(os.environ.get('TM_BANDS', 2))
BAND_LEN = int(os.environ.get('TM_LEN', 6))
DIAGRAMS = int(os.environ.get('TM_DIAGRAMS', 6))
BACKTRACK = int(os.environ.get('TM_BACKTRACK', 25))
CASE_CAP = int(os.environ.get('TM_CASE_SECONDS', 420))
DEADLINE = float(os.environ.get('TM_SECONDS', 30000))
PYTHON = os.environ.get('TM_PYTHON', sys.executable)
SCRATCH = os.environ.get('TM_SCRATCH', '/tmp/teichner_case.json')


def main(out_path):
    if os.path.exists(out_path):
        sys.exit('refusing to overwrite %s' % out_path)
    rec = {'date': datetime.datetime.utcnow().isoformat() + 'Z',
           'target': 'D_{0,1} = K_0 # (-K_1)',
           'box': {'max_bands': BANDS, 'max_band_len': BAND_LEN,
                   'max_twists': 2, 'diagrams_per_partner': DIAGRAMS,
                   'backtrack_steps': BACKTRACK,
                   'case_cap_seconds': CASE_CAP,
                   'deadline_seconds': DEADLINE},
           'partners': PARTNERS, 'runs': [],
           'certified_slice': False, 'stop': None,
           'scope': ('Bounded search. A timed-out case is UNKNOWN, never a '
                     'negative. No hit is a non-existence proof, and a hit '
                     'needs the oriented whole-link checks of research/20 '
                     'before it is called a counterexample.')}
    t0 = time.time()
    for diagram in range(DIAGRAMS):          # breadth-first over diagrams
        for name in PARTNERS:
            for mirrored in (0, 1):
                if time.time() - t0 > DEADLINE:
                    rec['stop'] = 'deadline'
                    json.dump(rec, open(out_path, 'w'), indent=1, default=str)
                    print('STOP: deadline', flush=True)
                    return
                if os.path.exists(SCRATCH):
                    os.unlink(SCRATCH)
                cmd = [PYTHON, 'scripts/teichner_mirror_worker.py', name,
                       str(mirrored), str(diagram), str(BANDS),
                       str(BAND_LEN), str(BACKTRACK), SCRATCH]
                label = ('mirror(%s)' if mirrored else '%s') % name
                try:
                    subprocess.run(cmd, timeout=CASE_CAP,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                except subprocess.TimeoutExpired:
                    pass
                if os.path.exists(SCRATCH):
                    row = json.load(open(SCRATCH))
                else:
                    row = {'partner': label, 'diagram': diagram,
                           'completed': False, 'certified_slice': False,
                           'outcome': 'timed_out_or_crashed_UNKNOWN',
                           'cap_seconds': CASE_CAP}
                rec['runs'].append(row)
                if row.get('certified_slice'):
                    rec['certified_slice'] = True
                    print('*** TEICHNER CERTIFICATE ***', label,
                          'diagram', diagram, flush=True)
                rec['elapsed_seconds'] = round(time.time() - t0, 1)
                json.dump(rec, open(out_path, 'w'), indent=1, default=str)
                print(json.dumps({k: v for k, v in row.items()
                                  if k not in ('certificate', 'sum_pd_code',
                                               'partner_certificate')}),
                      flush=True)
    rec['stop'] = 'enumeration_finished'
    json.dump(rec, open(out_path, 'w'), indent=1, default=str)
    print('CERTIFIED:', rec['certified_slice'], flush=True)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'results/teichner_mirror_partners.json')
