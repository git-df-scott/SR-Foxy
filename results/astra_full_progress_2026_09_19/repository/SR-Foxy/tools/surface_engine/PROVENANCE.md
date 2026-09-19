# Surface-to-diagram engine

Salvaged from the Turaev Theorem I lane (2026-09-12). That lane closed with a
negative result, but this engine is the durable output and is reusable well beyond
it.

**What it does.** Realizes an arbitrary Seifert matrix as an explicit knot diagram: a
disk with 2g bands whose foot layout encodes the alternating part of the form, with
clasps and R2-cancelling travels perturbing exactly one linking number at a time, and
the boundary read off by doubling into a Morse diagram and converting to a PD code.
It also implements **Milnor's ribbon-linking move** (Turaev's Figure 4) as a
commutator of meridians, and derives the Milnor triple invariant mu-bar directly from
the braid word by walking the loop and taking the Magnus coefficient.

**Self-tests are real checks, not smoke tests.** `python3 build.py` verifies the
target matrix is realized exactly with all writhes zero and mu-bar equal to the
requested (r,s) across 4 values of (p,q) and 7 of (r,s); `python3 bands.py`
re-derives the handle calibration from scratch, including recovering 6_1's Alexander
polynomial 2t^2 - 5t + 2, and confirms travels change nothing. Verified to pass from
a clean interpreter inside this repository.

**Why it is worth keeping.** Going from a Seifert matrix to a verified diagram is the
step that blocked this campaign twice: Turaev never draws his surface, and Abe-Tagami
never publish a machine-readable diagram. Any future lane that specifies a knot by
its Seifert form rather than a picture needs exactly this.

Limitation, honestly stated: diagrams are large. Installing the Milnor data cost
26 core crossings per move and inflated the Turaev knots from 27 crossings to 127 at
best. A nested foot layout was designed but not built; it is described in the
engine's report and would cut roughly a third.
