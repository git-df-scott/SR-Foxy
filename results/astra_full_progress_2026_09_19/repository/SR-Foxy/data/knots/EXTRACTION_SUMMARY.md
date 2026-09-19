# Verified PD codes — summary

All PD codes are SnapPy/spherogram **0-indexed** PD codes (`Link.PD_code(KnotTheory=False)`), one JSON per object in this directory. Every object carries a `verification` block; nothing here is a guessed diagram.

## TASK 1 — Manolescu–Piccirillo RBG knots K_B, K_G (DONE, 10/10)

Source of the diagrams: the Mathematica notebook `DTcodes.nb` linked from the paper's companion page <http://web.stanford.edu/~cm5/RBG.html> (arXiv:2102.04391). Its `g`/`gg`/`KG`/`KB` DT-code formulas were **auto-transpiled** to Python (`../mma.py`, `../mp_auto.py`) rather than hand-copied, and DT→PD was done with `spherogram.DTcodec`.

**Pipeline validation (the crucial step):** the notebook's parameters are the *negatives* of the paper's for b,c,d,e,f — paper `(a,b,c,d,e,f)` = notebook call `KX(a,-b,-c,-d,-e,-f)`. This was pinned down by reproducing, exactly, the hyperbolic volume **and** the total HFK rank of all 22 knots listed in <http://web.stanford.edu/~cm5/RBG/PromisingKnots.txt> (44/44 numbers agree to all published digits).

**Per-pair verification:** for each of the 5 parameter tuples, the 0-surgeries of K_B and K_G are *isometric* (`M.dehn_fill((0,1)); M.is_isometric_to(N)` → True), both are knots (1 component), and the two knot exteriors are *not* isometric (so K_B ≠ K_G).

| knot | crossings (generated / after `simplify('global')`) | genus | HFK rank | vol(exterior) | Alexander |
|---|---|---|---|---|---|
| MP_KB(0,0,0,1,2,-1) | 33 / 19 | 2 | 33 | 13.824520 | +1*t^0 |
| MP_KG(0,0,0,1,2,-1) | 33 / 19 | 2 | 33 | 13.990717 | +1*t^0 |
| MP_KB(0,0,0,-1,2,1) | 33 / 27 | 2 | 97 | 20.495415 | +1*t^0 |
| MP_KG(0,0,0,-1,2,1) | 33 / 26 | 2 | 97 | 20.353874 | +1*t^0 |
| MP_KB(0,0,-2,0,0,1) | 31 / 19 | 2 | 33 | 13.824520 | +1*t^0 |
| MP_KG(0,0,-2,0,0,1) | 21 / 19 | 2 | 33 | 13.990717 | +1*t^0 |
| MP_KB(-2,0,0,-1,2,-1) | 37 / 31 | 2 | 113 | 18.955571 | +4*t^-2 -20*t^-1 +33*t^0 -20*t^1 +4*t^2 |
| MP_KG(-2,0,0,-1,2,-1) | 37 / 30 | 2 | 113 | 19.383723 | +4*t^-2 -20*t^-1 +33*t^0 -20*t^1 +4*t^2 |
| MP_KB(-1,0,-1,-1,2,-1) | 37 / 25 | 2 | 81 | 18.689290 | +3*t^-2 -12*t^-1 +19*t^0 -12*t^1 +3*t^2 |
| MP_KG(-1,0,-1,-1,2,-1) | 37 / 30 | 2 | 81 | 18.920182 | +3*t^-2 -12*t^-1 +19*t^0 -12*t^1 +3*t^2 |

All ten exteriors are hyperbolic (`all tetrahedra positively oriented`). The three r = a+b = 0 tuples (0,0,0,1,2,-1), (0,0,0,-1,2,1), (0,0,-2,0,0,1) additionally have diffeomorphic traces by Lemma 5.2(b) of arXiv:2102.04391; (-2,0,0,-1,2,-1) and (-1,0,-1,-1,2,-1) have r = -2 and -1.

Note: the GHMR repo <https://github.com/ruehlef/ribbon> was cloned (kept at `../ribbon_repo`). Its `db/sym.csv`, `db/unsym.csv` contain 11199 PD codes + volumes + crossing numbers of machine-generated ribbon-search knots, but **no** Manolescu–Piccirillo parameter tuples and no K_B/K_G labels (only Manolescu's name, as a package author). It was not usable for this task.

## TASK 2 — Abe–Tagami K_n = A^n(6_3) (MOSTLY FAILED)

* **Obtained & verified:** `AbeTagami_K_0_(=K_-1)_=_6_3.json` — K_0 = 6_3 (and K_{-1} = K_0 by Abe–Tagami's d_3 computation). Checks: exterior isometric to `snappy.Manifold('6_3')`; Δ = 1−3t+5t²−3t³+t⁴; HFK says fibered, genus 2; 0-surgery = `s912(0,1)`, volume 4.059766425638614.

* **Not obtained:** K_n for n = ±2, ±3 and n = 1 (= K_{-2}), and hence the connected sums D_{n,m}. Reason and everything that *was* established (the exact definition of the twist, its surgery slopes, the compatible-fiber-surface description, the AJOT blow-down picture) are recorded in `AbeTagami_K_n_NOTES.json`. No machine-readable diagram data exists in the e-print sources of arXiv:1502.01102, arXiv:1209.0361, arXiv:1305.7492, and Dunfield–Gong arXiv:2512.21825 contains no Abe–Tagami data (its tables are RBG links). Reconstructing K_n needs a by-hand transcription of a ~30-crossing hand-drawn figure; rather than risk a fabricated PD code, none is reported.

* **Rigorous side result:** all 59937 hyperbolic knots of ≤14 crossings (`snappy.HTLinkExteriors(cusps=1)`) were 0-filled and compared with M_{6_3}(0). The *only* isometric match is 6_3 itself. So K_n (n ∉ {0,−1}) has no ≤14-crossing hyperbolic diagram and is absent from the standard tables. (K9a40 is a near-miss: 0-surgery volume 4.0597665492 vs 4.0597664256, not isometric.)

## TASK 3 — (10_17)_{2,1} (DONE)

`10_17_(2,1)-cable.json`. Built as the closure of the block-doubled braid of `snappy.Link('10_17').braid_word() = [1,-2,1,-2,-2,-2,-2,1,1,1]` (writhe w = 0) plus σ₁^{1−2w} = σ₁, i.e. the Seifert-framed (2,1)-cable; 41 crossings. Verified: 1 component; g = 8 = 2·g(10_17) = 2·4; Δ_cable(t) = Δ_{10_17}(t²) = t^{-8}−3t^{-6}+5t^{-4}−7t^{-2}+9−7t²+5t⁴−3t⁶+t⁸ (exact match); the exterior is **not** hyperbolic (`contains degenerate tetrahedra`), as a satellite must be; and the undoubled braid closure is isometric to the 10_17 exterior.

## TASK 4 — GST knot (DONE)

`GST_knot.json`. From `regina.ExampleLink.gst()` (Regina 7.4), whose documentation states it is Figure 2 of Gompf–Scharlemann–Thompson, *Geom. Topol.* 14 (2010) 2305–2347 (= arXiv:1103.1601). 48 crossings, matching the figure (`sliceknot.eps` in the e-print source, caption "A slice knot that might not be ribbon", drawn from L_{3,1}; two full-twist boxes on 4 strands = 24 crossings, plus 24 drawn crossings). Verified: 1 component; genus 10; τ = 0; and Δ satisfies Fox–Milnor, Δ(t) = −p(t)·t⁸p(1/t) with p = t⁸−2t⁷+t⁶+t⁵−2t⁴+t³−1, as it must for a slice knot.

## Files

* `10_17_(2,1)-cable.json`
* `AbeTagami_K_0_(=K_-1)_=_6_3.json`
* `AbeTagami_K_n_NOTES.json`
* `GST_knot.json`
* `MP_KB(-1,0,-1,-1,2,-1).json`
* `MP_KB(-2,0,0,-1,2,-1).json`
* `MP_KB(0,0,-2,0,0,1).json`
* `MP_KB(0,0,0,-1,2,1).json`
* `MP_KB(0,0,0,1,2,-1).json`
* `MP_KG(-1,0,-1,-1,2,-1).json`
* `MP_KG(-2,0,0,-1,2,-1).json`
* `MP_KG(0,0,-2,0,0,1).json`
* `MP_KG(0,0,0,-1,2,1).json`
* `MP_KG(0,0,0,1,2,-1).json`
* `_task1_raw.json`