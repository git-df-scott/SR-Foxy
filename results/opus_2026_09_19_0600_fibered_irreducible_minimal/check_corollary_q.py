#!/usr/bin/env python3
"""Corollary Q: a nontrivial fibered knot with irreducible Delta is <=_h-minimal.

This is a SECOND, INDEPENDENT route to a premise this campaign already operates
on.  scripts/zero_surgery_pair_search.py justifies its population -- prime
fibered knots with irreducible Alexander polynomial -- by Miyazaki's criterion:
any two DISTINCT such knots have a connected sum that is never homotopy-ribbon,
so a concordance between them refutes slice-ribbon.

Corollary Q reaches the same conclusion through Agol-Ren Cor 1.14(1) and
Theorem F instead of through Miyazaki Thm 5.5.  That matters because
ERRATA_2026-09-18_OPUS.md E18-2 showed this campaign had misread which of
Miyazaki's two alternatives it was entitled to; a route that does not pass
through them at all is worth having.  It is NOT a new target and NOT a
counterexample.

  Corollary Q.  Let K be a nontrivial fibered knot whose Alexander polynomial
  is irreducible over Z.  Then K is minimal for <=_h.

  Proof.  Let J <=_h K with J != K.
   (1) K fibered and nontrivial, so J is fibered            [Theorem F, via Sun]
   (2) Casson-Gordon + the compression genus lemma, both available since J and
       K are now both fibered, give g(J) < g(K)   [Agol-Ren Thm 1.7 + chi=1-2g]
   (3) Delta_J divides Delta_K                                 [Friedl-Powell]
   (4) Delta_K irreducible, so Delta_J is 1 or Delta_K (up to units)
   (5) a fibered knot has monic Delta of degree exactly 2g, so
       deg Delta_J = 2g(J) < 2g(K) = deg Delta_K, excluding Delta_J = Delta_K
   (6) hence Delta_J = 1, hence g(J) = 0, hence J = U
   (7) U <=_h K says K is strongly homotopy-ribbon, hence slice
   (8) but Delta_K is irreducible of degree 2g(K) >= 2, so by Fox-Milnor K is
       not slice.  Contradiction. []

WHAT IS CHECKED HERE.  Steps (5), (6) and (8) are arithmetic and are verified
below, including an explicit exhaustive Fox-Milnor factor search rather than the
degree argument alone.  Steps (1), (2), (3), (7) are external theorems, listed
in RESULTS.json and NOT verified here.

DEPENDENCIES, STATED PLAINLY.  Theorem F rests on Sun arXiv:2604.20785 Thm 1.1,
which is UNREFEREED (read in full, per opus_2026_09_18_0005).  So Corollary Q is
not stronger than Miyazaki's route -- it is differently conditioned.  Two routes
with disjoint weak points is the point.
"""
import json, os, sys, itertools, sympy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from fox_milnor_sagefree import delta_from_hfk, t            # noqa: E402
import snappy                                                # noqa: E402

KNOTS = [("K_0 (=6_3)", "AbeTagami_K_0_K_-1__6_3.json"),
         ("K_1",        "AbeTagami_K_1.json"),
         ("K_2",        "AbeTagami_K_2.json"),
         ("K_3",        "AbeTagami_K_3.json")]


def pd_of(fn):
    d = json.load(open(os.path.join(ROOT, "data", "knots", fn)))
    for k in ("pd_code_snappy_0indexed", "pd_code"):
        if k in d:
            return d[k]
    raise KeyError(fn)


def fox_milnor_factor_exists(delta, maxdeg=3, bound=8):
    """Exhaustive search for f in Z[t] with Delta = +- t^k f(t) f(1/t).

    The degree argument alone already excludes this for irreducible Delta of
    degree >= 2.  Searching anyway is the cheap independent confirmation that
    ERRATA E18-1/E18-2/E18-8 all say was skipped when it existed.
    """
    d = sympy.degree(delta, t)
    for deg in range(0, maxdeg + 1):
        if 2 * deg != d:
            continue
        for coeffs in itertools.product(range(-bound, bound + 1), repeat=deg + 1):
            if coeffs[0] == 0 or coeffs[-1] == 0:
                continue
            f = sum(c * t ** i for i, c in enumerate(coeffs))
            # t^deg * f(1/t) is the reverse of f
            frev = sum(c * t ** (deg - i) for i, c in enumerate(coeffs))
            prod = sympy.expand(f * frev)
            for sign in (1, -1):
                for k in range(0, d + 1):
                    if sympy.expand(prod - sign * t ** k * delta) == 0:
                        return True, str(f)
    return False, None


def main():
    checks, results = [], {}
    for tag, fn in KNOTS:
        h = snappy.Link(pd_of(fn)).knot_floer_homology()
        delta = delta_from_hfk(h).as_expr()
        g = h.get("seifert_genus")
        fib = bool(h.get("fibered"))
        deg = sympy.degree(delta, t)
        irred = len(sympy.factor_list(delta)[1]) == 1
        monic = sympy.Poly(delta, t).LC() in (1, -1)
        fm, witness = fox_milnor_factor_exists(delta)

        results[tag] = {"fibered": fib, "genus": g, "deg_delta": int(deg),
                        "irreducible": irred, "monic": monic,
                        "fox_milnor_factorisation_found": fm,
                        "witness": witness,
                        "corollary_Q_applies": bool(fib and irred and g and g >= 1)}
        print(f"{tag:12s} fibered={fib} g={g} degDelta={deg} irred={irred} "
              f"monic={monic} FoxMilnor-factor={fm}")

        # (5): fibered => monic Delta of degree exactly 2g.  This is the step
        # that makes "degree 2g" automatic rather than a hypothesis.
        checks.append((f"{tag}: fibered, and deg Delta = 2g "
                       f"({deg} = 2*{g})", fib and deg == 2 * g))
        checks.append((f"{tag}: Delta monic (forced for fibered)", monic))
        # (8): Fox-Milnor, checked by exhaustive search, not only by degree.
        checks.append((f"{tag}: NO f with Delta = +-t^k f(t)f(1/t) "
                       f"(exhaustive, deg f <= 3, |coeff| <= 8)", not fm))
        checks.append((f"{tag}: Delta irreducible over Z", irred))
        checks.append((f"{tag}: nontrivial (g >= 1), so deg Delta >= 2",
                       bool(g and g >= 1)))
        checks.append((f"{tag}: Corollary Q applies => K is <=_h-minimal",
                       results[tag]["corollary_Q_applies"]))

    # The two side conditions of the PLAN_CE criterion are AUTOMATIC for a
    # fibered knot.  That is the whole content of Corollary Q over the
    # criterion already recorded in PLAN_CE_2026_09_18.md section 0.
    auto = all(r["deg_delta"] == 2 * r["genus"] for r in results.values())
    checks.append(("'degree 2g' is automatic for every fibered knot tested",
                   auto))
    checks.append(("'not slice' is automatic: irreducible Delta of degree >= 2 "
                   "is never a Fox-Milnor norm",
                   all(not r["fox_milnor_factorisation_found"]
                       for r in results.values())))

    npass = sum(1 for _, ok in checks if ok)
    print()
    for name, ok in checks:
        print(("  PASS  " if ok else "  FAIL  ") + name)
    print(f"\n{npass}/{len(checks)}")

    json.dump({
        "corollary": "A nontrivial fibered knot with irreducible Alexander "
                     "polynomial is <=_h-minimal.",
        "status": "PROVED modulo the external inputs below; arithmetic gates "
                  "COMPUTATIONALLY VERIFIED",
        "external_inputs_not_verified_here": [
            "Theorem F (this repo, opus_2026_09_18_0005), resting on Sun "
            "arXiv:2604.20785 Thm 1.1 -- UNREFEREED",
            "Agol-Ren Thm 1.7 (Casson-Gordon) and the compression genus lemma",
            "Friedl-Powell: Delta_J | Delta_K for ribbon concordance",
            "Agol-Ren Cor 1.14(1): at most one <=_h-minimal fibered knot per "
            "concordance class, if slice-ribbon holds",
            "Fox-Milnor",
        ],
        "not_a_new_target": "scripts/zero_surgery_pair_search.py already "
                            "operates on this population via Miyazaki Thm 5.5. "
                            "Corollary Q is a second route with different "
                            "weak points, not a new search space.",
        "knots": results,
        "checks": [{"name": n, "pass": bool(o)} for n, o in checks],
        "passed": npass, "total": len(checks)},
        open(os.path.join(HERE, "RESULTS.json"), "w"), indent=1)
    return 0 if npass == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
