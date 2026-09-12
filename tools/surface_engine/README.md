# turaev2 -- the engine, and how to re-run it

Three files are the reusable part and are self-contained.  They realize an
arbitrary Seifert matrix as an explicit diagram and implement Milnor's
ribbon-linking move; nothing in them is specific to Turaev's family except
`build.build` itself.

| file | what it is | needs | self-test |
|---|---|---|---|
| `bands.py` | disk-with-bands surface -> boundary knot PD code | spherogram | `python3 bands.py` |
| `build.py` | Turaev's A(p,q,r,s); Milnor's move (Turaev Fig. 4) | `bands` | `python3 build.py` |
| `milnor.py` | mu-bar(i,j,k) of the band cores, from the braid word | `build` | `python3 milnor.py` |

All three self-tests pass and print `ALL CHECKS PASSED`.  Read the module
docstrings first: `bands.py` explains the surface model, the foot layout, the
`(pos, flag)` braid letter convention and the clasp/travel calculus;
`build.py` explains how X splits into clasps and how Figure 4 is implemented;
`milnor.py` explains the Magnus-coefficient computation.

## Minimal use

```python
import build, bands, milnor

c = build.build(p=1, q=1, r=1, s=-1)   # the surface, as a braid word on 12 strands
c.linking_matrix()                     # Seifert data actually realized, from crossing signs
milnor.mu(c, 1, 3, 5)['mu']            # == r      (independent of any knot software)
milnor.mu(c, 2, 4, 6)['mu']            # == s

L = bands.boundary_link(c)             # the boundary knot, a spherogram.Link
L.simplify('global')
pd = L.PD_code(KnotTheory=False)
```

For a different Seifert matrix, keep `bands.py` and write your own `build`:
choose `feet` so that the interleaved pairs are exactly the ones with non-zero
alt(V), then add one clasp per unit of linking number and one letter per handle.
`Core.linking_matrix()` tells you what you actually built.

## The rest of the directory

`phaseA.py` builds and hard-simplifies every grid member; `hkl_one.py` +
`phaseB2.sh` run `slice_obstruction_HKL` on each in its own subprocess with a
hard time cap (needed because the Sage/SnapPy call does not respond to a
Python-level alarm); `run.py` runs the full battery on the small members;
`ribbon.py` / `ribbon2.py` run the Dunfield-Gong band search;
`mkgrid.py` / `mkreport.py` regenerate `grid_table.md`, `GRID.md`, `REPORT.md`
and `pd_codes.json` from the live data.

Results: **`REPORT.md`** (construction, verbatim Figure-4 transcription,
verification, battery) and **`GRID.md`** (the sweep).  Read the "Bottom line"
at the top of `REPORT.md` first -- in particular, a member whose HKL entry says
`TIMEOUT` is uncomputed, **not** a surviving candidate.

Data: `pd_codes.json` (the PD codes), `grid_hkl.json`, `knots.json`,
`hkl_results.txt` (live record of the sweep), `ribbon_cert_*.json` (the
verified one-band ribbon certificates for the (r,s) = (0,0) members).
