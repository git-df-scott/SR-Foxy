# Tooling: environment, data, and the first scripts

Condensed from `research/04_computational_tooling.md` (2026-09-11), where every entry carries a VERIFIED / PARTIALLY VERIFIED / UNVERIFIED label. Numbers below marked "run" were reproduced twice in this session with snappy 3.3.2 and regina 7.4.

## Non-negotiable facts

0. **[16 Sep] This container has no SageMath and cannot get one** (no conda, no Sage package; `ams.org` and some other hosts are also 403 behind the proxy). What *does* pip-install and work on bare CPython 3.11: `snappy==3.3.2` (including `spherogram.links.bands.search`, `knot_floer_homology`, `connected_sum`, `PD_code`) and `sympy`. So the usable paths are `scripts/teichner_certify_nosage.py` and `scripts/sagefree_*.py`; `Link.jones_polynomial` still needs patching from `sagefree_jones.py` because the `@sage_method` decorator is bound at import. Fact 1 below remains true of the *stock* pipeline.

1. **SageMath is mandatory.** SnapPy's entire Dunfield–Gong band pipeline (`Link.ribbon_concordant_links`, `Link.add_band`, `RibbonLinks`, `spherogram.links.bands.verify_ribbon_to_unknot`), the HKL Casson–Gordon obstruction (`Manifold.slice_obstruction_HKL`), `Link.seifert_matrix`, `Link.signature`, `Manifold.alexander_polynomial` and `Manifold.hyperbolic_torsion` are `@sage_method` and raise `SageNotAvailable` in bare CPython (run). Write `env_assert.py` first.
2. **The target knot is in hand** (`data/knots/18nh00000601.json`): Burton census row, knot signature, PD codes, braid word, HFK, volume, branched-cover homology. Genus 5 and fiberedness confirmed independently of the literature (run).
3. **No complete band search exists.** Every tool is a bounded search; negative results are coverage statements. DG's own search stopped at 4 bands.
4. **Rigorous unlink certification** goes through Regina normal surfaces: `Link.complement().simplify()` then `isSolidTorus()` (unknot) or `isHandlebody(n)` (n-component unlink). Regina 7.4 has no `isUnknot`/`isUnlink`. This step is the measured bottleneck: `ExampleLink.gordian()` exceeded 110 s. `TIMEOUT` is a distinct outcome, never coerced to `NOT_UNLINK`.
5. **Metabolizers are not the bottleneck for K_G.** H₁(Σ₂) = Z/25 is cyclic, so the double-branched-cover linking form has exactly one candidate metabolizer; Σ₃ ≤ 8, Σ₅ ≤ 32. The integral rank-5 Lagrangian problem in Z¹⁰ is infinite (Sp(10,Z) acts transitively) and any enumeration must be bounded and reported as such. The real cost is realizing a class as an embedded multicurve on the genus-5 fiber and recognizing the derivative link.
6. **Explicit monodromy at genus 5 is a research subproject.** SnapPy gives fiberedness and genus, not the surface. flipper/curver/Twister go from mapping class to manifold, so extraction is an inverse search certified by `is_isometric_to` against the 14-tetrahedron exterior. Agol–Ren released no code; their compression enumeration is the most valuable unbuilt tool.
7. **Regina's built-in `ExampleLink.gst()`** (48 crossings, docstring: GST Figure 2) computes as genus 10, **non-fibered**, Δ of degree 16, volume 23.8448997956 (run). ~~the object must be reconciled with GST Figure 2 by hand before use.~~ **[16 Sep] Reconciled as far as invariants can: the flagged discrepancy is not one.** GST prove `B_{3,1}` slice, and the stored object passes *every* slice necessary condition computable here — `τ = ν = ε = 0`, `det = 1` (a square), `deg Δ = 16 ≤ 2g = 20`, and **Fox–Milnor with an explicit witness**, `Δ ≐ f·f*` with `f = t^8 - 2t^7 + t^6 + t^5 - 2t^4 + t^3 - 1` irreducible. Non-fibered with `deg Δ < 2g` is exactly what a non-fibered knot looks like, and fiberedness of `B_{3,1}` was already `UNKNOWN`. This is **consistency, not identification**: it does not prove the object is `B_{3,1}`, it proves it is not disqualified. See `research/27`.

## Environment spec

```yaml
name: sr-foxy
channels: [conda-forge]
dependencies:
  - python=3.11
  - sage=10.7
  - openjdk>=23          # KnotJob jar
  - pip
  - pip:
      - snappy==3.3.2
      - snappy_15_knots
      - regina==7.4.1
      - knot-floer-homology
      - numpy
      - networkx
      - requests
```

Separate installs: GAP 4.13+ with `nq` and `lpres` (nilpotent quotients, Milnor invariants of derivative links); KnotJob (Java 23 GUI, no documented batch mode; provides s̃_c, X-torsion order); KLO 0.979 alpha (Windows/macOS-Intel GUI only, interactive Kirby calculus); `ruehlef/ribbon` (GHMR ML search, Python 3.8–3.10, own venv; heuristic only); `hanselman/CFK-immersed-curves` (Python 2.7, no license; port needed); flipper, curver, Twister (PyPI). Avoid Magma; DG Lemma 3.19 shows how.

Data to stage: Dunfield–Gong `plausibly_slice_V1.zip` (1.02 GB, Harvard Dataverse doi:10.7910/DVN/YBDTBT; contains PD codes for the 286 named knots and the ribbon certificates); Burton `18n-hyp.csv.bz2` (1.33 GB, supports HTTP Range; row 602 is K_G) and `all_13-16.tar.bz2`; Owens–Swenton `.rb` ribbon-disk files (alternating only).

## What exists, what does not

| need | tool | status |
|---|---|---|
| HFK, τ, ε, ν, genus, fibered | `snappy.Link.knot_floer_homology()` (Szabó) | run; < 0.01 s at 18 crossings, 0.6 s at 48 |
| UV = 0 complex | same, `complex=True` | run; whether γ₀ / Υ are determined by CFK_{UV=0} is **unverified**, settle before scripting |
| band search + certificates | `Link.ribbon_concordant_links(..., certificates=True)` | Sage only; DG's search shipped |
| certificate checker | `spherogram.links.bands.verify_ribbon_to_unknot` | Sage only; documented to fail on non-hyperbolic intermediates, back with Regina |
| HKL / Casson–Gordon | `Manifold.slice_obstruction_HKL` | Sage only; DG report HKL 6.6× as effective as all smooth obstructions combined |
| twisted Alexander | `Manifold.hyperbolic_torsion()` and variants | Sage only; there is no `snappy.twisted_alexander` |
| Fox calculus | `snappy.snap.fox_milnor` | present, undocumented |
| **Δ and Fox–Milnor without Sage** | `scripts/fox_milnor_sagefree.py` | **[16 Sep] built.** Δ from the HFK Euler characteristic (`Δ = Σ (-1)^M rk HFK(A,M) t^A`), factored over `Z` with sympy; decides `Δ ≐ f(t)f(1/t)` exactly. 11 controls pass (6 ribbon read norm, 5 non-slice read not-norm). Needs no Seifert matrix and no Sage, so it works in this container where `Link.alexander_polynomial` does not. |
| s, s̃_c, Khovanov, X-torsion | KnotJob | **batch mode IS documented** — `KnotJob/README.TXT` in the distributed zip lists every flag (`-s0`, `-sgr`, `-scr`, `-sbls3`, `-kb0`, `-kx0`, `-ns`, `-nf`), and `knotjob/KnotJobCommand.java` implements it. The **jar** needs Java 23 (class-file major 67); the **source** is Java 11 compatible and compiles clean under `javac 21` (283 files, no errors), which is how the 16 Sep runs were done. A source build is a different build from the sha256-pinned jar: recalibrate the full control set, do not assume equivalence. [16 Sep] |
| Υ, ν⁺, d-invariants of Σ₂ | none confirmed | assemble by hand or by literature lookup |
| Milnor invariants of links | none; build from GAP `nq`/`lpres` | needed only for derivative links |
| metabolizer enumeration | none; ~100 lines of Sage | see fact 5 |
| monodromy of K_G | flipper/curver/Twister inverse search | research subproject |
| Agol–Ren compression enumeration | no code | build |
| Diao–Pan–Yan GST link builder | no public code; ask authors | |
| annulus twists A_n(K) | none; PD surgery script | exact construction |
| 4-manifold recognition | none (Regina `Triangulation4` bookkeeping only) | KLO by hand |
| instanton invariants | none | do not plan a lane on them |

## First ten scripts (dependency order)

| # | script | in → out | rigor |
|---|---|---|---|
| 01 | `fetch_census_row.py` | Burton name → knot_sig, DT, PD (Regina and SnapPy), braid | data fidelity only; assert `fromDT(dt).knotSig() == sig` and exterior isometry |
| 02 | `invariant_card.py` | knot → genus, fibered, τ/ε/ν, ranks, Δ, det, σ, volume, `verify_hyperbolicity`, H₁(Σ_n) | HFK exact over F_p; hyperbolicity is a proof; volume is numeric, never compared for equality |
| 03 | `env_assert.py` | — → exit code | `snappy.sage_helper._within_sage is True`, Regina version, Java ≥ 23 |
| 04 | `band_search.py` | knot, parameter box (bands ≤ 5–7, twists, length, path mode, diagram corpus) → certificates or a coverage record | positive = certificate; negative = "no disk inside this box" |
| 05 | `verify_certificate.py` | certificate → PASS/FAIL/INCONCLUSIVE per step | the only script that proves ribbonness; Regina fallback mandatory |
| 06 | `unlink_certify.py` | link → UNLINK(n)/NOT_UNLINK/TIMEOUT with witness | normal-surface decision; `simplify` to 0 crossings is heuristic |
| 07 | `obstruction_battery.py` | knot list → verdict and firing test | HKL first, then s̃_c, Fox–Milnor, signatures; silence proves nothing |
| 08 | `metabolizers.py` | Seifert matrix, cover homology → metabolizers, curve systems on Σ₅, derivative links → 06 | branched-cover enumeration complete; integral enumeration bounded and labelled |
| 09 | `gst_family.py` | (n,k) or (p,q;c/d) → PD codes, cards, pairwise isometry | first task: reconcile `ExampleLink.gst()` with GST Figure 2 |
| 10 | `annulus_twist.py` | base knot with annulus presentation, n → A_n(K) | exact construction; first confirm the 6_3 presentation from [S06, §5] |

Additional scripts required by `CAMPAIGN_PLAN.md` WS2.2 and WS3: `common_upper_bound_search.py` (band K_n with unknotted components, canonicalize by isometry signature, intersect with the K_m set), `rbg_r0_filter.py` (DG 0-friend pairs → super-special r = 0 realizations), `teichner_sums.py` (K # J with small ribbon J, run 04 on the sum).

## Reproduction of the K_G card

```bash
python3 - <<'EOF'
import snappy, regina
sig="sabcdbefghijkglmhijknopqreanopqdcrmlflRSuvwT+5bdd"
L=regina.Link.fromKnotSig(sig)
K=snappy.Link([tuple(i-1 for i in c) for c in L.pdData()])
print(K.knot_floer_homology())
M=K.exterior(); M.simplify(); print(M.volume(), M.num_tetrahedra(), L.alexander())
EOF
```

## Band-count semantics of `ribbon_concordant_links` (calibrated 13 Sep 2026, evening)

`max_bands` in the Dunfield-Gong search is **not** the fusion number of the
ribbon disk, and it is not bounded below by the Seifert genus. Measured
directly, with `max_twists = 2`, `max_band_len = 5`, on small ribbon knots:

| knot | Seifert genus | bands needed to reach `unknot` |
|---|---:|---:|
| 6_1 | 1 | 1 |
| 9_46 | 1 | 1 |
| 10_3 | 1 | 1 |
| 8_8 | 2 | 1 |
| 8_20 | 2 | 1 |
| 9_41 | 2 | 1 |
| 8_9 | 3 | 1 |
| 10_22 | 3 | 1 |
| 10_87 | 3 | 1 |

One band suffices for every one of these, genus 3 included, because the search
recognizes the resulting ribbon link through the ribbon-link cache rather than
continuing to band it down.

This matters because the natural inference is the opposite one. It is tempting
to argue that a ribbon knot of fusion number `f` needs `f` bands, that
`g <= f`, and therefore that a 2-band search on a genus-6 connected sum such as
`D_{0,1} # 8_8` is futile by construction. **That argument is wrong**, and the
table above is the refutation. The hypothesis was raised and discarded in this
session before anything was written up on the strength of it; it is recorded
here so the same wrong turn is not taken again.

Consequence: the existing 2-band Teichner runs on `D_{0,1}` are genuine
coverage of their box, not vacuous.
