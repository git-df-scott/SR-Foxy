# Boundary knot of the stored genus-one surgery — Opus session, 20 September 2026

**NO SLICE–RIBBON COUNTEREXAMPLE.** Read `REPORT.md`.

One-paragraph summary. The stored `+1/-1` surgery on the auxiliary pair `(a,b')`
in the complement of `R = K_0 # (-K_0) = 6_3 # 6_3` is **not an annulus twist of
`R`**: `a` and `b'` are not freely homotopic in `S^3 ∖ R` in either orientation,
so they cobound no annulus there, not even an immersed one. An explicit `A_5`
certificate is in `annulus_obstruction_certificate.json`, checkable by
`python3 code/verify_certificate.py` with SymPy and the standard library only.
This removes the mechanism that would have made the surgery boundary an
Abe–Tagami knot, and leaves the Alexander polynomial `d^2` as the only property
linking it to `D_{0,1}`. The identity of the surgery boundary itself remains
**unresolved**: a discriminator that does separate `K_0#(-K_0)` from `D_{0,1}`
(`#Hom(π_1,A_5)` = 1020 vs 2220; degree-5 covers = 9 vs 21) was built and
validated end-to-end — it reproduces `K_1` from the genuine Abe–Tagami annulus
twist and `R` from meridian fillings — but could not be evaluated on the actual
`±1` filling within the session.

## Reproduce

```
python3 code/verify_certificate.py        # the obstruction certificate, standalone
python3 code/certificate.py              # regenerate it from the frozen files
python3 code/knotcounts.py               # reference representation counts
python3 code/covers.py                   # surgery pipeline + its positive controls
```

Run from a copy of this directory with `results/astra_genus_one_2026_09_18/`
reachable at the path hard-coded in the scripts (`/home/user/SR-Foxy/...`); adjust
`D=` / `DATA=` if your checkout is elsewhere. `code/covers.py` and the `tri*.py`
routes need SnapPy, spherogram and Regina; `verify_certificate.py` needs neither.

## Status of every claim

`proved` / `computationally supported` / `unresolved` are separated in `REPORT.md`
§9. Nothing here constructs a slice disk, a non-ribbon certificate, or an
identification with `D_{0,1}`. Routes that did not finish are listed with their
timings in §8 so they are not retried blindly.
