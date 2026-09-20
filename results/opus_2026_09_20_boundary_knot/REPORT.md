# The boundary knot of the stored genus-one surgery: what it is not, and the one
# thing still missing

20 September 2026, Opus session. **NO SLICE–RIBBON COUNTEREXAMPLE.** Nothing
below produces a slice disk, a non-ribbon certificate, or an identification of
the surgery boundary with `D_{0,1}`.

## 0. Bottom line

Write `R = K_0 # (-K_0)`, `(a,b')` for the stored auxiliary pair, and `K_new` for
the knot obtained from `R` by the stored `(1,1)`/`(-1,1)` surgeries on `(a,b')`.

1. **Proved (new).** `a` and `b'` are **not freely homotopic in `S^3 \ R`**, in
   either orientation. Hence they cobound **no annulus at all — not even an
   immersed one — in `S^3 \ R`**. Therefore the stored `+1/-1` surgery is **not
   an annulus twist of `R`**. An explicit, independently checkable `A_5`
   certificate is in `annulus_obstruction_certificate.json`; the verifier is
   `code/verify_certificate.py`.
   *Consequence:* the mechanism that makes the Abe–Tagami family exist — an
   annulus twist, which preserves the 0-surgery — is unavailable here. So there
   is no structural reason for `K_new` to be any `D_{n,m}`, and the **only**
   property currently linking `K_new` to `D_{0,1}` is the Alexander polynomial
   `d^2` (plus its module structure, §7). That is exactly the kind of evidence
   the campaign's own rules forbid treating as an identification.
2. **Proved (new).** The Alexander module of `K_new` is `Λ/(d) ⊕ Λ/(d)`
   (`E_0 = (d^2)`, `E_1 = (d)`, `E_2 = (1)`, from honest minors — §7). This
   **agrees** with both `K_0 # (-K_0)` and `D_{0,1}`, so it does not separate
   them. By contrast each **single** twist gives the **cyclic** module `Λ/(d^2)`
   (`E_1 = (1)`), which rigorously excludes both candidates for the intermediate
   knots.
3. **Proved (new).** `R` is a connected sum of two copies of `6_3`, reconstructed
   from the frozen integer polygons alone and identified by SnapPy.
4. **Built and validated, but not evaluated on the target.** A nonabelian
   discriminator that *does* separate the two candidates
   (`#Hom(π_1, A_5)`; degree-5 cover census) was validated end-to-end on the
   genuine Abe–Tagami annulus twist and on meridian fillings of the stored
   surgery link. Its value on the actual `+1/-1` filling is **UNRESOLVED**: the
   filled triangulation sits at 219–256 tetrahedra and every group-simplification
   route I tried exceeded the session budget (§8).
5. `check_exact_independent.mjs` replays clean (16/16). Its scope is narrower than
   its headline: one step is an *assertion read from input*, not a derivation
   (§3). One genuine gap in the published argument is closed here (§4).

## 1. Exact inputs

Repository `git-df-scott/SR-Foxy`, working branch `claude/cool-hamilton-6u656m`
at the requested start commit

```
84402e64133e181844ce83ce88b4ae27c08876a5   (== origin/main at session start)
```

No newer commits on `origin/main` were examined; none exist. Two facts worth
recording: `git fetch` reported a **forced update** of the remote-tracking ref
`f7ba251 -> 84402e6`, i.e. remote `main` history was rewritten at some point
before this session; and the *local* `main` branch in this checkout sits at a
different tip, `f7ba251` ("Document whisker branch gate sources and scope"),
which is **not** an ancestor of `84402e6` and which I did **not** use. All work
below reads only files as they exist at `84402e6`.

SHA256 of every frozen file actually read:

```
b1ec94ba104508f5422918aa3af9155f25faad857acc99e5b9551cf5daebd6c8  results/astra_genus_one_2026_09_18/surgery_diagram.json
f4e5f6981d41ab72fdcae838ffa98a41dedc8d4b0b15f3acd81ff73fe2623b52  results/astra_genus_one_2026_09_18/framed_fox_boundary.json
48feda4654828ff7ece8c9d911992911f315b5e6cb3ecf29c98ce5a42ea5399a  results/astra_genus_one_2026_09_18/auxiliary_group_certificate.json
771b9d29021f4df63468c4794ea1588e818b922c6fdec004df7e04697dc6ef8b  results/astra_genus_one_2026_09_18/check_exact_independent.mjs
788d2ea1c11a2c69593313d2821f7be9beabe70b0d11be49478dd049ee0bd228  results/astra_genus_one_2026_09_18/spatial_model.json
ea5183d62fd75514b3076430f557900ae3d029028666681e0d0ed861646437bc  results/astra_genus_one_2026_09_18/surgery_link.json
d1dbf3903721ea92a9458032d868ef4627cdf9f566291490f6de66690f261705  results/astra_genus_one_2026_09_18/correction_cobordism_mesh.json
f433a4c9b65eab762207ea215f6110aaecd86aba1d65604c57e3011fc215ef1d  data/knots/AbeTagami_D_0_1.json
431379bc23a2dd019bdfb629adbac8130f3d7c301007cf268934e086d590ca5d  data/knots/AbeTagami_K_1.json
1c9916334ea4bc7616be3eb4b225140d8f44a6aa701e4fc083413242fca665c4  data/knots/AbeTagami_K_0_K_-1__6_3.json
e242f97d5da7ca97ef035c36c9db82e519e6bf11580bad3fa5cd8b57238d43ab  data/knots/AbeTagami_L_63_c1_c2.json
```

Environment: Python 3.11.15, SnapPy 3.3.2, spherogram 2.4.1, Regina (python
bindings), SymPy 1.14.0, Node v22.22.2. (The producer's `environment.json`
records Python 3.13.5 / node 22.16; the frozen integer model is replayed, not
regenerated, so the version difference is immaterial — and the `.mjs` replay is
bit-identical.)

## 2. Conventions, read directly from the files

* `surgery_diagram.json` (`format: exact-polygon-projection-v1`) holds three
  closed integer polygons with common denominator `10^12`, in the order
  **0 = R, 1 = a, 2 = b'**. That ordering is not an assumption: component 1 and 2
  are precisely the two whose marked words are stored in
  `expected_marked_axis_words`, and `integer_polygons[0]` is the axis those words
  are read against.
* `projection = [u,p,v,q]`: the generic projection `(x,y,z) ↦ (x + (u/p)z,
  y + (v/q)z)`, realised exactly over the common denominator `p·q`. Over/under is
  decided by the exact `z` at the intersection parameter; the replay throws on
  collinearity, passage through a vertex, a triple point, or an actual spatial
  intersection. There are **675** crossings.
* Orientation of each component = the cyclic order of its polygon's vertex list.
  `gauss_words[c]` is the ordered list `[crossing id, 'O'|'U', sign]` along that
  orientation.
* `framed_fox_boundary.json` generators are the **arcs** of the whole 3-component
  diagram: 250 on `R`, 66 on `a`, 359 on `b'` (675 total), with
  `meridians = [1, 251, 317]` the first arc of each component.
* Wirtinger relator convention: `relators[k] = [-s·b, i, s·b, -o]`, i.e.
  `x_out = x_over^{-s} x_in x_over^{s}`.
* **Longitudes are the preferred (Seifert, 0-framed) longitudes**: the product of
  the signed over-arc generators at every undercrossing of the component,
  corrected by `|w|` copies of the meridian's inverse where `w` is the component's
  self-writhe. Self-writhes are `(0, 0, -1)`; all pairwise linking numbers are 0.
  The `.mjs` negative control "incorrect b-prime zero-framing is rejected" is what
  pins this down.
* `weights` sends `R`-meridians to `t` and both auxiliary meridians to `1`; so the
  Fox calculus is over `Λ = Z[t,t^{-1}]` with the abelianisation "linking with R".
* **Surgery slopes are `(1,1)` on `a` and `(-1,1)` on `b'` in
  `(meridian, preferred-longitude)` coordinates**, i.e. coefficients `+1` and
  `-1` relative to the 0-framing; equivalently the two filled relators
  `μ_a λ_a` and `μ_{b'}^{-1} λ_{b'}`, exactly as `check_exact_independent.mjs`
  line 83 builds them. Since all pairwise linking numbers vanish, the 0-framing
  computed inside the auxiliary sublink and inside the full link agree, so the
  coefficients are unambiguous.

## 3. Replaying `check_exact_independent.mjs`: what it proves, what it asserts

`node check_exact_independent.mjs` in a fresh copy: **PASS, 16/16, 0.33 s**, output
byte-identical to the stored `independent_exact_check.json`.

**Genuinely derived from the integer polygons** (the checker recomputes and throws
on disagreement, so reading the stored answer is not a loophole):

* all 675 crossings with over/under and sign, and the genericity of the
  projection;
* the three Gauss words, hence the 675 Wirtinger generators, `meridians`, all 675
  relators, all three preferred longitudes and the self-writhes;
* the integer Laurent Fox derivative rows over `Λ`;
* all 670 unit pivots — each is *validated* to be `±t^k` in the current matrix
  before being used, so the stored pivot list is a certificate being checked, not
  data being trusted;
* that both auxiliary longitude rows annihilate the stated rational kernel vector
  `S` (`E = 0`), by polynomial multiplication;
* the five filled maximal minors `0, 0, -t^{-4}d^2, t^{-2}d^2, -t^{-3}d^2`, and
  their independence of the two slope parameters by multiaffinity plus four exact
  corner evaluations;
* the auxiliary sublink's own Wirtinger presentation (377 generators, extracted
  from the crossings with neither strand on `R`) and the 375 Tietze eliminations
  killing both preferred longitudes.

**Read from input, not derived.** Line 49 reads the *native* generator label of
each `R`-segment out of `spatial_model.json`
(`base_segment_generators[0]`). So the check "the actual axes read the intended
`a` and `[A,B]b` words" verifies that the geometry reproduces the **stored** word
under the **stored** labelling. The labelling itself, and the identification of
that 18-crossing marked scaffold with Abe–Tagami's figures, are *not* verified
there — the producer's own `REPORT.md` §2 says so ("The paper-figure-to-scaffold
correspondence was not reaudited in this session"). §5 below removes half of that
dependency by reconstructing the scaffold and identifying `R` without using the
stored labels at all.

**Not claimed by the checker, and correctly flagged in the package:** that the
ambient manifold after filling is `S^3` (that is a separate theorem-based
argument, §6), anything four-dimensional, and any identification of the knot. The
`.mjs` file's own `scope` string says exactly this.

The unlink argument itself is sound: `λ_a = λ_{b'} = 1` in the *auxiliary* link
group, so by the boundary form of Dehn's lemma each preferred longitude bounds an
embedded disk in the exterior; capping through the collar gives a spanning disk
for each component missing the other, so `(a,b')` is the 2-component unlink and
`±1` surgery on it returns `S^3`. That much is a proof.

## 4. Independent reimplementations, and one closed gap

Four independent implementations now agree on the peripheral data:

1. the producer's Python (`framed_fox_boundary.py`),
2. the producer's own JavaScript checker,
3. **new:** `code/periph.py`, a Python port written from the Gauss words, which
   reproduces `framed_fox_boundary.json` **exactly** — `n_generators = 675`,
   `meridians = [1,251,317]`, all 675 relators as ordered lists, all three
   preferred longitudes, `self_writhes = (0,0,-1)`;
4. **new:** `code/gaussbuild.py`, which rebuilds the link as a spherogram object
   from the Gauss words (validated by round-tripping 12 library knots and links,
   including 3-component ones, on crossing signs, linking matrix, writhe,
   Alexander polynomial and hyperbolic identification).

**Gap closed.** The `.mjs` checker verifies only that the two auxiliary longitude
rows vanish on one *hardcoded* vector `S`. That establishes `E = 0` only if `S`
spans the whole kernel — which needs `rank = 2`. A separate exact SymPy
computation on `reduced_rows`/`reduced_longitudes` confirms

```
rank(M) = 2,   dim ker(M) = 2,   both longitude rows vanish identically on ker(M),
five maximal minors = 0, 0, -d^2/t^4, d^2/t^2, -d^2/t^3,   det(K_new) = d(-1)^2 = 169.
```

so `E = 0` is genuine and not an artefact of a lucky test vector.

## 5. `R` is `6_3 # 6_3`, reconstructed from the polygons

Exactly **18** of the 675 crossings have both strands on component 0. Restricting
component 0's Gauss word to those gives an 18-crossing knot diagram — this *is*
the "archived marked scaffold" the report refers to, recovered without using any
stored label. Building it and asking spherogram/SnapPy:

```
R as a knot: 18 crossings, writhe 0
deconnect_sum -> two 9-crossing pieces
each piece simplifies to 6 crossings, exterior volume 5.6930210913,
SnapPy identify -> [s912, 6_3, K6_43, K6a1]
6_3 exterior volume 5.6930210913
```

So `R = 6_3 # 6_3` (`6_3` is amphichiral, so `K_0 # (-K_0)` is unambiguous here).
Two further independent confirmations: the 18-generator presentation splits into
two 9-generator blocks joined by two seam crossings, each block having Alexander
polynomial `d = t^4-3t^3+5t^2-3t+1`; and `#Hom(π_1(S^3∖R) → A_5)` with the
meridian pinned to a fixed 3-cycle is **49 = 7^2**, where `7` is the same count for
`6_3` (§7).

## 6. Main new result: the surgery is not an annulus twist

### 6.1 The statement

Let `A` be an annulus, embedded or merely immersed, in `S^3 ∖ R` with
`∂A = a ∪ b'`. Its core is freely homotopic in `S^3 ∖ R` to `a` and to `b'` (one of
them reversed, depending on the boundary orientation). Hence the word of `a` would
have to be conjugate in `π_1(S^3 ∖ R)` to the word of `b'` or to its inverse.

**It is not.** There is an explicit homomorphism

```
ρ : π_1(S^3 ∖ R) → A_5
```

with `ρ(a)` a double transposition `(0 2)(1 4)` and `ρ(b') = 1`. Different
conjugacy classes, and inverting `ρ(b')` changes nothing. 24 of the 49
representations in the family (meridian → a fixed 3-cycle) are such witnesses.

**Therefore `a` and `b'` cobound no annulus in `S^3 ∖ R`, and the stored `+1/-1`
surgery is not an annulus twist of `R`.**

### 6.2 The certificate and how to check it

`annulus_obstruction_certificate.json` carries, in the repository's **own native
generator labels `x_1 … x_18`**:

* the 18 Wirtinger relators of `π_1(S^3 ∖ R)` in the form
  `x_out = x_over^{-sign} x_in x_over^{sign}`;
* the words `a` and `b'`, which are **byte-identical** to
  `surgery_diagram.json → expected_marked_axis_words`, namely
  `a = [4,-1,3,-4,11,14,-15,-11,1,-9]` and the 32-letter
  `b' = freely_reduce(A B A^{-1} B^{-1} b)` (independently re-derived here from
  `A, B, b`);
* `ρ(x_i)` for all 18 generators as permutations of `{0,1,2,3,4}`;
* `ρ(a) = (2,4,0,3,1)`, `ρ(b') = (0,1,2,3,4)`.

`python3 code/verify_certificate.py` checks all 18 relators, recomputes `ρ(a)` and
`ρ(b')` from the words, verifies the two conjugacy classes differ (also after
inversion), and re-derives the Alexander polynomial `d` of each of the two
9-generator blocks. It needs only SymPy and the standard library — no SnapPy, no
Regina, no group theory package. Current output:

```
1. words identical to surgery_diagram.json expected_marked_axis_words: OK
2. all 18 Wirtinger relators hold: True
3. rho(a)  = (2, 4, 0, 3, 1)   rho(b') = (0, 1, 2, 3, 4)
4. rho(a) conjugate to rho(b')   : False
   rho(a) conjugate to rho(b')^-1: False
   ==> a is NOT freely homotopic to b' or its reverse in S^3 - R: True
5. block sizes [8, 8]  -> R is a connected sum
   each block Alexander polynomial: (t^4 - 3t^3 + 5t^2 - 3t + 1) up to units
```

The internal-arc → native-label bijection was derived twice and the two agree:
once by matching the two words position by position (which pins 11 of the 18
labels), once from `spatial_model.json`'s `base_segment_generators[0]` by majority
vote over the polygon edges each arc carries (which pins all 18). It is
`1→7, 2→15, 3→16, 4→10, 5→17, 6→14, 7→18, 8→13, 9→11, 10→12, 11→5, 12→2,
13→8, 14→9, 15→4, 16→3, 17→1, 18→6`.

### 6.3 Scope — what this does and does not obstruct

* It **does** rule out any annulus, immersed included, between `a` and `b'` in the
  3-manifold `S^3 ∖ R`. So: no annulus twist; no guarantee that
  `S^3_0(K_new) ≅ S^3_0(R)`; and hence nothing tying `K_new` to the `A^n(6_3)`
  family, which is the whole source of the `D_{n,m}` candidates.
* It does **not** obstruct an annulus in a **slice-disk exterior**
  `W = B^4 ∖ D`, which is the four-dimensional object Park's annulus modification
  actually requires. My `ρ` is a representation of `π_1(S^3∖R)` and need not factor
  through `π_1(W)`. Indeed the repository's own `research/42` §5 and `research/37`
  §1 record that under the saved algebraic `q_0` one has
  `q_0(b') = μ^{-1} q_0(a) μ` — conjugate *there*, by design. The two facts are
  consistent, and together they say something precise: **the correction was
  engineered to succeed in the (algebraic) disk exterior, and it does; it was
  never arranged to succeed in `S^3 ∖ R`, and it does not.**
* And even if such a `W`-annulus exists, Park's theorem yields *sliceness* of
  `K_new` in a standard `B^4`. It says nothing about *which* knot `K_new` is. The
  knot type is a purely three-dimensional consequence of `(R, a, b')` and the
  framings — which is the computation that remains open (§8).

### 6.4 Where the intended identification fails, precisely

The repository never derives `K_new = D_{0,1}`; it derives only the *necessary*
conditions and says so (`REPORT.md` §5: "Matching `d^2` is the required
boundary-polynomial check, **not** the missing nonribbon certificate";
`VERIFICATION.json`: `identified_as_D01: false`). The failure point is therefore
not an erroneous step but a **missing** one, and §6.1 now shows that the natural
candidate for that step is unavailable:

* `D_{0,1} = K_0 # (-K_1)` is reached from `R = K_0 # (-K_0)` by the order-1
  annulus twist inside the second summand. The stored annulus-twist link
  `data/knots/AbeTagami_L_63_c1_c2.json` makes this explicit: auxiliary pair
  `c'_1 ∪ c'_2` a **Hopf link** (`lk = 1`, exterior isometric to `L2a1`),
  annulus framing `+1` off Seifert, and preferred-longitude slopes
  `(n+1, n), (n-1, n)` — for `n = 1`, `(2,1)` and `(0,1)`.
* The stored pair `(a,b')` has `lk(a,b') = 0` and slopes `(1,1), (-1,1)`. Those
  *are* the right coefficients for an order-1 twist along a **0-framed** annulus,
  so the coefficient assignment is internally consistent and correct as written —
  but §6.1 shows the required 0-framed annulus in `S^3∖R` does not exist.
* Consequently the two surgery descriptions are not related by the annulus-twist
  mechanism, and `Δ = d^2` is the only surviving link between `K_new` and
  `D_{0,1}`.

## 7. Discriminators that do separate the two candidates, and their validation

### 7.1 Representation counts

For a knot `K` and finite `G`, `n_K(g) = #{ρ : π_1(S^3∖K) → G, ρ(μ) = g}` is a knot
invariant, uniform on conjugacy classes, multiplicative under connected sum
(`π_1(K#K') = π_1(K) *_{⟨μ⟩} π_1(K')`), and blind to mirroring. Computed with my
own backtracking counter (`code/homcount.py`, controls: 3-colourings of `3_1`→3,
`4_1`→1, `6_3`→1, `8_18`→9) on the stored PD codes:

| `G` / class | `6_3` | `K_1` | `K_0#(-K_0)` = sq. | `D_{0,1}` = product | stored `D_{0,1}` diagram |
|---|---|---|---|---|---|
| `A_5`, 3-cycles (20) | 7 | 13 | **49** | **91** | **91** |
| `A_5`, involutions (15) | 1 | 9 | **1** | **9** | **9** |
| `A_5`, 5-cycles (12) | 1 | 11 | **1** | **11** | **11** |
| `S_5`, 3-cycles (20) | 7 | 13 | 49 | 91 | 91 |
| `S_5`, 6-cycles (20) | 1 | 7 | 1 | 7 | 7 |
| `A_4`, `S_4` (all classes) | 1 | 1 | 1 | 1 | 1 |

The last column is computed from the stored 25-crossing `D_{0,1}` diagram and
matches the product prediction exactly — an independent check of both the counter
and the amalgamation formula. Totals over all of `A_5`:
`K_0#(-K_0) → 1020`, `D_{0,1} → 2220` (and `6_3 → 180`, `K_1 → 660`).
`A_4`/`S_4` are useless here; `A_5` is the cheapest group that separates.

### 7.2 Degree-5 cover census

Computed straight from a triangulation with `Triangulation.covers(5)` — no
presentation simplification needed:

| knot | #degree-5 covers | `H_1` multiset |
|---|---|---|
| `6_3` | 2 | `Z^3`, `(Z/4)^4+Z` |
| `K_1` | 8 | `Z^2 ×2`, `Z^3 ×2`, `Z/2+Z/24+Z`, `Z/3+Z^3`, `Z/33+Z`, `(Z/4)^4+Z` |
| `K_0#(-K_0)` | **9** | `Z^5 ×6`, `(Z/4)^8+Z`, `Z/7+Z/7+Z^3 ×2` |
| `D_{0,1}` | **21** | richer; includes `Z/13+Z/39+Z^3`, `Z/7+Z/91+Z^2`, `(Z/4)^3+Z/132+Z`, … |

### 7.3 End-to-end validation of the surgery pipeline

Every step was checked on cases with known answers, **using the same code path as
the target**:

| case | expected | obtained |
|---|---|---|
| stored AT link `L`, meridian fillings `(1,0),(1,0)` | `6_3` | 180 homs; 2 covers; `(Z/4)^4+Z` — **yes** |
| stored AT link `L`, **genuine annulus twist** `(2,1),(0,1)` | `K_1` | 660 homs; 8 covers, full multiset match; filled triangulation isometric to the `K_1` exterior, vol 9.1200065008 — **yes** |
| stored surgery link, meridian fillings `(1,0),(1,0)` | `R = 6_3#6_3` | 1020 homs; 9 covers, full multiset match; 49 for the 3-cycle class — **yes** |

So the machinery reproduces a real Abe–Tagami annulus twist and the unmodified
knot, from the very same pipeline, with several independent invariants. This is
the positive control the identification question needs.

### 7.4 The Alexander module, honestly computed

From `reduced_rows`/`reduced_longitudes` with denominators cleared (SymPy, gcd of
all minors after stripping unit powers of `t`):

| filling | `E_0` (4×4) | `E_1` (3×3) | `E_2` (2×2) | module |
|---|---|---|---|---|
| meridian, `= R` | `d^2` | `d` | 1 | `Λ/d ⊕ Λ/d` |
| **target `(1,1),(-1,1)`** | `d^2` | **`d`** | 1 | **`Λ/d ⊕ Λ/d`** |
| `+1` on `a` only | `d^2` | **1** | 1 | **`Λ/(d^2)` (cyclic)** |
| `-1` on `b'` only | `d^2` | **1** | 1 | **`Λ/(d^2)` (cyclic)** |

This confirms the producer's `filled_smith_diagonal` for the target and adds the
single-twist rows. Since `K_0#(-K_0)` and `D_{0,1}` both have module
`Λ/d ⊕ Λ/d`, the module does **not** separate them — but it *does* rigorously
exclude both for each single twist. Independent corroboration: the 5-fold cyclic
cover of the `+1`-on-`a`-only knot has torsion `(Z/16)^4`, whereas both candidates
give `(Z/4)^8` (same order `4^8`, different group) — two different methods,
same conclusion.

## 8. What is known about `K_new`, and what blocked the identification

Known, and consistent with **both** candidates:
`Δ = d^2 = t^8-6t^7+19t^6-36t^5+45t^4-36t^3+19t^2-6t+1`; `det = 169`;
Alexander module `Λ/d ⊕ Λ/d`; ambient manifold `S^3`; `E = 0`.

Not obtained: the `A_5` count / cover census of `K_new`. What was tried, and how it
failed (so nobody repeats it):

| route | outcome |
|---|---|
| spherogram simplification of the 675-crossing link | 675 → 200 crossings, then a hard floor; ~1800 randomised restarts with backtracking never beat 200 (`logs/minimize.log`, `logs/multi.log`) |
| SnapPy `filled_triangulation` + `simplify` | target: 249 tets; `+1`-on-`a`-only: **33 tets** (so the machinery works when the answer is small) |
| persistent randomised simplification of the target's filled triangulation | 249 → **219** tets in ~40 min and still descending one tet at a time (`logs/shrink.log`); saved as `data/target_filled_219tet.tri` |
| Regina `intelligentSimplify` on the filled triangulation | no reduction at all from 219/238; already at a local minimum |
| Regina `GroupPresentation` on the 675- and 200-generator Wirtinger presentations plus the two surgery relators | meridian control collapses in **0.3 s** to 3 generators; the `±1` case did not finish in 30 min (the 292-letter `λ_{b'}` is the obstacle) |
| SnapPy `fundamental_group()` on the filled manifold, and Regina `Triangulation3.group()` on 219–238 tets | both exceeded 20 min |
| my own arc-based backtracking count with the two surgery relators as word relations | meridian control: 49 in **77 nodes**; the `±1` case must enumerate the representations of the whole 3-component link group before the long surgery words become checkable, and did not terminate |
| `Triangulation.covers(5)` on the 219-tet target | did not finish within the session; on the 33-tet single-twist cases it finished in **0.8 s** |

### 8.1 The right tool, and the exact step that blocks it

Added after the first write-up. The Dunfield–Obeidin–Rudd algorithm
(`Manifold.exterior_to_link`, arXiv:2112.03251) converts a filled triangulation
straight back into a planar diagram, and on **both** positive controls it lands
exactly right:

| input | result | check |
|---|---|---|
| stored AT link filled `(2,1),(0,1)` (11 tets) | a **19-crossing knot** | degree-5 cover census = `K_1`'s exact multiset (8 covers) |
| stored surgery link, meridian fillings (18 tets) | a **12-crossing knot** | `deconnect_sum` splits it into two 6-crossing pieces; census = `R`'s exact multiset (9 covers) |

So the route is correct and it reproduces a genuine diagram of the answer,
including an explicit 19-crossing diagram of `K_1` obtained from the annulus twist
rather than from the stored file.

On the target it fails at one identified internal step, in about 11 s:

```
Finding link for Regina_Triangulation
    Finding moves to base triangulation of S^3...
RuntimeError: Could not simplify to standard triangulation of S^3
```

i.e. the algorithm fills the remaining cusp with its meridian — giving a
triangulation of `S^3` with ~219 tetrahedra — and its Pachner search cannot reduce
that to the standard one-tetrahedron `S^3`. **This is a search failure, not a
mathematical obstruction**, and it is now the single concrete computational
blocker. Attempts that did not clear it: `pachner_search_tries` at 10/40/120 over
three seeds on the saved 219-tetrahedron triangulation (19 min, all nine failed);
Regina `intelligentSimplify` (no reduction at all — already a local minimum);
Regina Pachner-perturbation annealing. The two controls needed only 11 and 18
tetrahedra, so the practical target is to get the exterior well under ~80.

Two further routes tried after the first write-up, both dead ends worth recording:
a randomised-restart version of my greedy Tietze elimination reaches 14 generators
on the target but with 858,252 letters of relator (the control collapses to 3
generators and returns 1020 instantly); and a numpy-vectorised `#Hom(·,A_5)`
counter, calibrated at `6_3 → 180`, `K_1 → 660`, `R → 1020`, which is ready but
needs ≤ 5 or 6 generators to be affordable.

The common cause of all of it is a single number: `b'` is a 32-letter word in
`π_1(S^3 ∖ R)`, so any honest diagram of `R ∪ a ∪ b'` needs on the order of 200
crossings, and every presentation- or triangulation-level route inherits that.
The resistance of the target to simplification (219 tets and falling, versus 17
for `R` and ~20 for `D_{0,1}`) is *suggestive* that `K_new` is not a small
composite knot — but the same machinery also got stuck on the `-1`-on-`b'`-only
case at ~200 tets, so this is an observation about the triangulations, **not**
evidence about the knot, and it is not used in any conclusion above.

## 9. Conclusions, separated

### Proved
1. `a` and `b'` are not freely homotopic in `S^3 ∖ R` in either orientation; they
   cobound no annulus, even immersed, there; the stored `+1/-1` surgery is **not**
   an annulus twist of `R`. Explicit `A_5` certificate, self-contained verifier.
2. `R` is `6_3 # 6_3`.
3. `E = 0` for the stored pair, now including the rank-2 fact that the published
   `.mjs` check silently needs; `Δ_{K_new} = d^2`, `det = 169`, Alexander module
   `Λ/d ⊕ Λ/d`; each single twist gives the cyclic module `Λ/(d^2)` and so is
   neither `K_0#(-K_0)` nor `D_{0,1}`.
4. `(a,b')` is the 2-component unlink and the ambient manifold after the `±1`
   fillings is `S^3` (the package's Dehn-lemma argument is correct; I re-verified
   its algebraic input three ways).
5. `check_exact_independent.mjs` passes 16/16 and its derivations are genuine,
   with the one input-read step identified in §3.

### Computationally supported, not proved
6. The pipeline that would answer the identification question is correct: it
   reproduces `K_1` from the genuine Abe–Tagami annulus twist and `R` from
   meridian fillings, on several independent invariants.
7. `K_new` is plausibly not a small composite knot (219-tetrahedron local
   minimum). Weak; explicitly not used above.

### Unresolved
8. **The identity of `K_new`.** Every invariant I could actually evaluate
   (`Δ`, `det`, Alexander module, ambient `S^3`) is shared by `K_0#(-K_0)` and
   `D_{0,1}`, so none of them decides. The invariants that do decide could not be
   evaluated. So: `K_new = D_{0,1}` is **neither established nor excluded**.
9. Whether an annulus between `a` and `b'` exists in a slice-disk exterior of `R`
   (the four-dimensional object Park's construction needs). §6.1 says nothing
   about this, and the repository's `q_0` computation is consistent with it.
10. Everything the package already lists as open: the geometric identification of
    `q_0`, a non-ribbon proof for the actual `K_new`, and an embedded smooth disk
    in a standard `B^4`.

### If `K_new` did turn out to be `D_{0,1}`
What would still be required before the construction supplies an embedded smooth
disk in a **standard** `B^4`: an actual embedded annulus `A ⊂ B^4 ∖ D` with
`∂A = a ∪ b'`, satisfying Park's `l`-standard hypotheses (Definition 3.1,
arXiv:1512.00401) — with `D` an explicitly identified slice disk of `R`, the
identification of `q_0` with `π_1` of that disk exterior actually carried out, and
the relative framing recorded. None of the following is sufficient, and none may
be substituted: an immersed cap; a nullhomotopic boundary loop; the vanishing of
`E`; an `S^3` boundary; the `diag(1,-1)` 2-handle trace (which is not `B^4`); or
the conditional `π_1`-injectivity of the stored genus-one surface.

## 10. The single most valuable next proof obligation

**Produce the explicit spanning-disk system for the certified unlink `(a,b')` in
`S^3`, together with its intersection pattern with `R`.** Concretely: an isotopy
of `a ∪ b'` to two round circles, carrying `R` along, recorded as a finite
sequence of diagrammatic moves; equivalently the two discs `D_a`, `D_{b'}` with
`R ∩ D_a` (10 signed points, matching the 10-letter word of `a`) and
`R ∩ D_{b'}` (32 signed points) listed in cyclic order along `R`, plus the braid
in which those strands enter each disc.

That is precisely the step the producer's own handoff named, and it is the
bottleneck for everything else: with it, the two blow-downs become two explicit
full twists on identified strand families, `K_new` gets an ordinary diagram of
manageable size, and then the Jones polynomial, the `A_5` count (49 vs 91), the
degree-5 cover census (9 vs 21) and the `Σ_2` linking form all become one-second
computations on invariants that are already calibrated and validated in §7. Note
that the theorem-based unlink certificate in `auxiliary_group_certificate.json`
supplies the discs' *existence* via Dehn's lemma but no coordinates, which is
exactly why the question is still open.

There is now also a **purely computational** path to the same answer, which any
next session should try before the geometry: get the surgered exterior's
triangulation under ~80 tetrahedra (Regina `simplifyExhaustive`, a longer Pachner
anneal, or a genuinely different diagram of the 3-component link) and then call
`Manifold.exterior_to_link`. §8.1 shows that call already returns the correct
diagram on both controls, so only the triangulation size stands in the way.

A cheap secondary obligation, worth doing first because it is nearly free: run the
`ρ`-style test of §6 on representations of `π_1` of an **explicitly identified**
slice-disk exterior of `R`, to see whether the four-dimensional annulus is
obstructed as well. If it is, the whole lane closes.

## Files

* `annulus_obstruction_certificate.json` — the §6 certificate.
* `code/verify_certificate.py` — standalone verifier (SymPy + stdlib only).
* `code/certificate.py` — regenerates the certificate from the frozen files.
* `code/periph.py` — Python port of the verified peripheral extraction; reproduces
  `framed_fox_boundary.json` exactly.
* `code/gaussbuild.py` — Gauss word ↔ spherogram link, with a 12-link round-trip
  validation harness.
* `code/homcount.py`, `code/solver2.py`, `code/pres_count.py` — representation
  counters (arc-based with propagation; presentation-based brute force).
* `code/covers.py`, `code/tri_route.py`, `code/tri2.py`, `code/tri3.py`,
  `code/single.py`, `code/pure_route.py`, `code/shrink.py`, `code/multi.py` — the
  surgery pipelines and the routes that did not finish, kept so they are not
  retried blindly.
* `code/knotcounts.py`, `code/counts2.py`, `code/wirt.py` — the reference tables of
  §7.1 with their colouring controls.
* `data/ordered_surgery_link_200cr.json` — a 200-crossing PD code of the ordered
  link `(R, a, b')`, components in that order (tracked through simplification by
  crossing-label voting, unanimous).
* `data/target_filled_219tet.tri` — the smallest filled triangulation of the
  target reached, for whoever continues.
* `code/e2l.py`, `code/e2l_retry.py`, `code/anneal.py` — the `exterior_to_link`
  route of §8.1, including the two controls that succeed (an explicit 19-crossing
  diagram of `K_1` from the annulus twist, and a 12-crossing `6_3 # 6_3`).
* `code/tietze.py`, `code/tietze3.py`, `code/tietze4.py` — my own greedy and
  randomised Tietze elimination and the numpy-vectorised `#Hom(·,A_5)` counter,
  with their calibrations against `6_3`, `K_1`, `D_{0,1}` and `R`.
* `logs/` — all runs, including the failures and the timings in §8.

## Primary sources used, and how

* **JungHwan Park, *A Construction of Slice Knots via Annulus Modifications*,
  arXiv:1512.00401.** Used only to state the outstanding four-dimensional
  requirement (Definition 3.1 / Theorem 3.3, `l`-standard annulus modification),
  exactly as the producer's report does. Not invoked as a sliceness theorem for
  anything here.
* **Abe–Tagami, arXiv:1502.01102**, via the repository's stored
  `AbeTagami_L_63_c1_c2.json` slope data `(n+1,n), (n-1,n)` and the `K_1` file.
  Used as the *calibration* of §7.3, not as an unread theorem: the annulus twist
  was re-run and it does return `K_1`.
* **Freedman–Scharlemann, arXiv:1704.05507**, boundary Dehn's lemma — as the
  producer uses it, for the unlink certificate (§3). Its statement is what makes
  §3's unlink argument a proof; I did not re-read the paper this session and flag
  that.
* No literature survey and no candidate search was run.
