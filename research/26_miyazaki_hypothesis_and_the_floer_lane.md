# What the fibered-partner exclusion cost, and why the Floer lane on `K_0`/`K_1` is already closed

16 September 2026. **No counterexample to the Slice-Ribbon Conjecture was
found.** This note records one theorem-level correction with a consequence,
one lane that was already closed and is being re-proposed, and two smaller
findings about what this container can and cannot do.

---

## 1. Miyazaki Thm 5.5 cannot obstruct a Teichner sum, ever

Registered as `ERRATA_2026-09-16.md` (E16-1); the exact hypotheses are now in
`SOURCES.md` [S07]. Summary of the mathematics, because the general form is more
useful than the three-partner correction that prompted it.

Five sites in this repository excluded the fibered ribbon partners `8_9`, `8_20`,
`9_27` from the Teichner lane a priori. The reasoning was that `D_{0,1} # J` with
`J` fibered is a connected sum of prime fibered knots in which `K_0` and `-K_1`
cannot pair, so Miyazaki's pairing theorem returns non-ribbon and no certificate
can exist.

Miyazaki's Theorem 5.5 requires **every** prime fibered summand to satisfy one of

* **(a)** `K_i` is minimal with respect to `≥` (homotopic ribbon concordance)
  among all fibered knots in homology spheres;
* **(b)** there is no `f(t) ∈ Z[t] \ {±t^k}` with `f(t)f(t^{-1}) | Δ_{K_i}(t)`.

**Proposition.** *Let `J` be a nontrivial ribbon knot. Then `J` satisfies neither
(a) nor (b). Consequently Theorem 5.5 does not apply to any connected sum having
`J` as a prime summand, and in particular cannot obstruct the ribbonness of
`K # J` for any `K`.*

*Proof.* (a): `J` ribbon gives a ribbon concordance `U → J`, hence `J ≥ U`, and a
ribbon concordance is in particular a homotopic ribbon concordance. `U` is a
fibered knot in `S^3` and `U ≠ J`, so `J` is not minimal. (Gordon's Lemma 3.4,
in the form Hom–Park use, gives the same thing via `g(J) > g(U) = 0`.) (b): `J`
ribbon is slice, so Fox–Milnor gives `Δ_J(t) = f(t)f(t^{-1})` up to units. `J` is
nontrivial and fibered, so `deg Δ_J = 2g(J) > 0` and `f ∉ {±t^k}`; `f` is then an
explicit witness against (b). ∎

Note what the proposition does *not* require: primality of `J`, fiberedness of
`J`, or anything about `K`. It applies to `J` itself as a summand.

This is not an accident of these three knots. It says Miyazaki 5.5 is
*constitutionally* unable to obstruct a Teichner sum — which is exactly what the
Teichner lane needs to be true, since `K # J` ribbon must not imply `K` ribbon or
the lane would be vacuous. The old claim was therefore in tension with this
repository's own reason for running the lane.

### 1.1 The rule that is correct, which is not the negation of the wrong one

> Miyazaki 5.5 excludes `D_{0,1} # J` **iff every prime summand of `J`** satisfies
> (a) or (b).

Both directions have content.

* A **prime fibered ribbon** `J` is never excluded: it fails at itself. `8_9`,
  `8_20`, `9_27` are exactly this case, and are now running.
* `J = L # (-L)` **is** excluded. Smallest case: the square knot
  `Sq = 3_1 # (-3_1)`, whose prime summands `±3_1` are fibered with irreducible
  `Δ = t² - t + 1`, which satisfies (b). So `K_0 # (-K_1) # 3_1 # (-3_1)` is
  inside the theorem, `3_1` pairs with `-3_1`, and `K_0` would have to pair with
  `-K_1`. No band search on such a `J` can ever return a certificate, and
  `scripts/teichner_mirror_partners.py` now says so in its docstring.

### 1.2 The repository already held the disproof of the unqualified version

`research/24` §2 observes that for the square knot `Sq`, the cable
`C = C_{p,q}(Sq)` is fibered and concordant to `T(p,q)` by a *satellited ribbon*
concordance, so `C # (-T(p,q))` is **ribbon**. It uses this to argue that
satellite routes are circular. Read the other way round it is a direct
counterexample to the unqualified restatement: `C` and `T(p,q)` are both prime
and fibered, `C` is a satellite and `T(p,q)` is not, so they do not pair — yet
the sum is ribbon. It is consistent with the *real* theorem only because
`Δ_C(t) = Δ_{Sq}(t^p)·Δ_{T(p,q)}(t)` carries the nonunit norm factor
`Δ_{Sq}(t^p)`, so (b) fails for `C`. That is precisely the hypothesis the five
planning sites deleted. `research/24` even notes the `Δ` mismatch, but files it
as a second independent reason the satellite route fails rather than as evidence
about the theorem's hypotheses.

### 1.3 Machine check and controls

`scripts/miyazaki_hypothesis_check.py` decides (b) exhaustively over `Z`, with no
floating point. Enumeration is complete because `f | Δ` forces
`lead(f) | lead(Δ)` and `f(0) | Δ(0)`. A **FAIL** verdict is a positive
certificate exhibiting `f` and needs no completeness; a **PASS** verdict is
bounded by `MIDDLE_BOUND` and is reported as such.

| knot | `Δ` | monic (⇒ fibered possible) | (b) |
|---|---|---|---|
| `6_1` | `2 - 5t + 2t²` | no | **FAIL**, `f = 2t - 1` |
| `8_8` | `2 - 6t + 9t² - 6t³ + 2t⁴` | no | **FAIL**, `f = 2t² - 2t + 1` |
| `8_9` | `1 - 3t + 5t² - 7t³ + 5t⁴ - 3t⁵ + t⁶` | yes | **FAIL**, `f = t³ - 2t² + t - 1` |
| `8_20` | `1 - 2t + 3t² - 2t³ + t⁴` | yes | **FAIL**, `f = t² - t + 1` |
| `9_27` | `1 - 5t + 11t² - 15t³ + 11t⁴ - 5t⁵ + t⁶` | yes | **FAIL**, `f = t³ - 3t² + 2t - 1` |
| `K_n = A_n(6_3)` | `1 - 3t + 5t² - 3t³ + t⁴` | yes | **PASS** |
| `3_1` | `1 - t + t²` | yes | **PASS** (control) |
| `4_1` | `1 - 3t + t²` | yes | **PASS** (control) |

Controls behave: the two non-slice knots and `K_n` pass, every slice knot fails,
as Fox–Milnor demands. `K_n` passing is the reason the **non-ribbon certificate
on `D_{n,m}` is untouched** by this correction — its `Δ` is irreducible, which
supplies (b) for both of its summands.

An earlier draft of that table mistyped `Δ(8_8)` as `Δ(K_n)`; the built-in
determinant cross-check caught it (`13` against the tabulated `25`). A first
version of the enumeration also assumed unit leading coefficients, which is
unsound for non-monic `Δ`, and wrongly passed `6_1` and `8_8`. Both are fixed;
recorded here because the controls are the only reason either was noticed.

Fiberedness of all three partners confirmed locally with `snappy` 3.3.2
`knot_floer_homology()`: `8_9` fibered genus 3, `8_20` fibered genus 2, `9_27`
fibered genus 3. The old claim's *premise* was correct throughout. Only the
inference failed.

### 1.4 What was not obtained

The AMS original of Miyazaki 1994 was **not** retrieved: `ams.org` returns a
Cloudflare 403 to this container, as `SOURCES.md` already records for [S29]. Both
restatements used above are secondary, though one is the restatement this
repository has always cited as [S06, Thm 4.1], and the [S07] evidence level is
accordingly **downgraded** from `PEER-REVIEWED PRIMARY` to
`SECONDARY RESTATEMENT ×2` — the previous "checked through the original" cannot
be substantiated from anything in this clone. The correction does not rest on the
bibliography: for it to fail, the *alternatives themselves* would have to be
misquoted identically by two independent papers, one of whose proofs is
load-bearing on the quantifier.

---

## 2. The Floer lane on `K_0`/`K_1` was closed on 12 September, in the negative

A proposal reached this session to compute `CFK^∞` for `K_0` and `K_1` up to local
equivalence — `Υ`, `ε`, the `φ_{i,j}` of Dai–Hom–Stoffregen–Truong — on the
ground that this is the one thing the shared 0-surgery does not determine and
that it "has never been computed here."

**It has been computed here, and it does not separate them.**
`research/11_involutive_local_equivalence.md` establishes that the stored `K_0`
and `K_1` have the **same involutive knot-Floer local-equivalence class**, namely
the figure-eight's. `research/09_full_ring_floer_audit.md` supplies the full-ring
lift: `K_0` admits no mixed differential terms, `K_1` has 18 possible terms with
8 free bits, and all **256** completions retract onto the same complex.

Re-verified today. `scripts/verify_involutive_structure.py`, a separate
standard-library implementation, reproduces
`INDEPENDENT_EXHAUSTIVE_OPERATOR_VERIFICATION_PASSED` **bit-for-bit**, same input
`sha256 e2e011057a18…`, 256 mixed gauges, 2048 + 16384 diagonal matrices
brute-forced to exactly 2 + 2 solutions, 4096 full-iota projection cases.

**Therefore, and this is the answer to the proposal:** every invariant that
factors through the involutive local equivalence class agrees on `K_0` and `K_1`.
That includes `τ`, `ε`, `ν`, `ν⁺`, `Υ_K(t)` and the `φ_{i,j}`. There is nothing
left to compute in that package, and no separation is available from it —
*conditionally* on the stated input/lifting dependency, which is the same
condition `research/09` and `research/11` carry and which has not been removed.

`Υ ≡ 0` for both, for the same reason: the class is the figure-eight's, `Υ` is a
local-equivalence invariant, and for a thin knot with `τ = 0` it vanishes
identically. Labelled **proved modulo the stated lifting condition**.

Directly computed today with `snappy` 3.3.2, as an independent consistency check
rather than a new result:

| knot | crossings | fibered | genus | `τ` | `ν` | `ε` | L-space |
|---|---|---|---|---|---|---|---|
| `K_0 = 6_3` | 6 | yes | 2 | 0 | 0 | 0 | no |
| `K_1` | 19 | yes | 2 | 0 | 0 | 0 | no |
| `K_2` | 41 | yes | 2 | 0 | 0 | 0 | no |

No separation, as expected.

### 2.1 One genuinely new datum, and one claim not to repeat

`HFK-hat` was computed for all three. The **Alexander-graded ranks are identical**
— `(1, 3, 5, 3, 1)`, the absolute values of the coefficients of the shared
`Δ = 1 - 3t + 5t² - 3t³ + t⁴` — but the **Maslov gradings differ**:

* `K_0`: all generators on `δ = M - A = 0` (thin; `6_3` is alternating with
  `σ = 0`).
* `K_1`: generators on `δ = 0` and `δ = -2`; e.g. rank 1 at `(A,M) = (-2,-4)`
  where `K_0` has rank 1 at `(-2,-2)`.
* `K_2`: the same shape as `K_1`, shifted further (`(-2,-8)`, `(2,-4)`).

Each satisfies the `HFK` symmetry `rk(A,M) = rk(-A, M-2A)`, so the tables are
internally consistent. This is **not** a concordance obstruction — `HFK-hat` is
not a concordance invariant — and it is the reason the local-equivalence
calculation was necessary in the first place: the complexes are genuinely
different and only become equivalent after localisation.

A claim that arrived with the proposal and that this note does **not** endorse:
that the shared 0-surgery forces agreement of "the whole Heegaard Floer
`d`-invariant package, all surgery `d`-invariants, hence `ν⁺`". The published
obstruction of that shape is Miller–Piccirillo [S28], which is about
diffeomorphic **0-traces**, not 0-surgeries, and it is an *obstruction to
concordance* rather than a statement that invariants must agree. `ν⁺` agreeing
here is a **consequence of the local-equivalence computation above**, which is
solid, and not of any 0-surgery argument, which is not established in this
repository. Do not cite the 0-surgery for it. Marked **UNKNOWN** as stated.

---

## 3. Eisermann on `L_{3,1}`: still blocked on a figure, and one shortcut closed

The blocker recorded in `research/22` §3.3 is unchanged and was re-checked today.
Diao–Pan–Yan (arXiv:2604.17737) was fetched in full LaTeX source: **635 lines,
no PD code, no braid word, no DT code, no Gauss code, no data repository** — the
construction is entirely figure-driven, exactly as `research/22` says. Nothing in
this session makes `L_{3,1}` constructible, and it was not guessed. Per
`research/22` §3.3, guessing risks a *false* counterexample, which is the worst
available outcome.

### 3.1 The `n ≥ 3` route cannot be reached by adding split unknots

`research/22` §3.4(2) proposes a slice link with `n ≥ 3` components, where slice
gives only `null V ≥ 1` while ribbon demands `n - 1 ≥ 2`, so Theorem 1 has room
to fail. The cheapest imaginable such object is a 2-component slice link with a
split unknot added. **That cannot work.**

In Eisermann's convention the split-union factor is `δ = -q - q^{-1}`, and
`δ(i) = -i - i^{-1} = 0`. So each split component contributes exactly `1` to
`null V`, giving `null V(L ⊔ O) = null V(L) + 1`. A 2-component slice link has
`null V = 1` automatically (§3.1 of `research/22`), so `L ⊔ O` has `n = 3` and
`null V = 2 = n - 1` — automatic again, no teeth. Adding split unknots can never
make Theorem 1 testable.

Control, run today with `scripts/eisermann_ribbon_link_gate.py` driven by
`scripts/sagefree_jones.py` (Jones needs Sage otherwise), `controls_pass = True`:
`null V(O²) = 1`, `null V(O³) = 2`, `null V(O⁴) = 3`, each with `det V = 1`. That
`null V(O^n) = n - 1` rather than `0` is what pins the convention and confirms
`δ(i) = 0`. Labelled **proved modulo the standard split-union multiplicativity of
`V`**, with the convention verified at `n = 2, 3, 4`.

Consequence: §3.4(2) needs a **non-split** 3-component slice link. A literature
search for a 3-component slice link whose ribbonness is open returned nothing
usable — the small-link slice-ribbon literature is about knots and 2-component
pretzel links. **I do not know of such a link.** Reported as a null, not as a
lead.

This also connects to the repository's standing caution: `simplify('global')`
deletes split unknot components, which is precisely the operation that would
silently turn an `n`-component test back into an `(n-1)`-component one.

---

## 4. Tooling corrections

Two entries in `TOOLING.md` are wrong or stale for this container.

1. **KnotJob has a documented batch mode.** `TOOLING.md` says "GUI, no documented
   batch mode; scripting requires reading bundled source". The distributed
   `KnotJob.zip` contains `knotjob/KnotJobCommand.java` and a `README.TXT` that
   documents the non-GUI invocation and every flag (`-s0`, `-sgr`, `-scr`,
   `-sbls3`, `-kb0`, `-kx0`, `-ns`, `-nf`, …). `scripts/run_knotjob.py` was
   already using it correctly; the doc simply understates what is documented.
2. **The distributed jar needs Java 23; the source does not.** This container has
   Java 21, so `env_assert_knotjob.py` would correctly refuse the jar
   (class-file major 67). The author states the source is Java 11 compatible, and
   it compiles clean under `javac 21.0.10` — 283 files, no errors. That is how the
   `s`-invariant runs in this session were done, so they are **a different build
   from the sha256-pinned jar** used in earlier sessions and were recalibrated
   from scratch rather than assumed equivalent.
3. **SageMath is absent and cannot be installed here** (no conda, no Sage
   package). `snappy==3.3.2`, `sympy` and the band-search machinery *do* pip-install
   and work, so `scripts/teichner_certify_nosage.py` and `scripts/sagefree_*.py`
   are the only usable paths. `regina` was not needed and not installed.
