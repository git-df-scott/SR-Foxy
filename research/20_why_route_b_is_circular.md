# Why every route-B construction has failed, and the one crossing nobody has tried

14 September 2026. **No counterexample found.** This note is strategy, not
computation. It asks what the board actually looks like after a year of lanes,
and it reaches one structural conclusion and one concrete unmined lane.

## 1. Every route-B lane reduces to the same missing object

Route B is: take a knot with a **proved non-ribbon certificate** and prove it
slice. The ledger has three such certificates, from three unrelated theorems:

| certificate | object | what it needs |
|---|---|---|
| Miyazaki fibered pairing | `D_{n,m} = K_n # (-K_m)`, Abe-Tagami | `K_n`, `K_m` distinct prime **fibered**, common irreducible `Δ`, and **concordant** |
| Miyazaki, Example 2 | `K_{p,q} # -T_{p,q}` | `K_{p,q}` and `T_{p,q}` **concordant** |
| Hom-Park `γ_0`-sharp pairing | `K_{p,q_1} # -K_{p,q_2} # J_{p,q_2} # -J_{p,q_1}` | a four-term relation among cables of distinct **tight fibered** knots |

Read the right-hand column. In every case the certificate is free and the
sliceness is the whole problem, and in every case sliceness amounts to a
**concordance coincidence between distinct fibered knots**. The Hom-Park row is
the same statement with four terms instead of two; their Corollary 1.2 says so
outright, as a dichotomy: either distinct iterated cables of tight fibered knots
are linearly independent in concordance, or Slice-Ribbon is false.

**So the single object that would unlock all of route B at once is a pair of
distinct, concordant, fibered knots.** The Abe-Tagami `K_n` are exactly a
candidate such pair, which is why this campaign is pointed at them. That focus
is correct. What follows is about why the obvious ways of *manufacturing* such a
pair cannot work.

## 2. The circularity: satellite constructions inherit ribbonness

There is one construction that certifies concordance for free. If `K` is slice
and `P` is any pattern, then `K ~ U` gives `P(K) ~ P(U)`, because satellite
operations descend to concordance. Both sides are fibered whenever `K` and the
pattern are, and they are distinct whenever the satellite is essential. That
looks like exactly the missing object, and it is constructive.

It cannot produce a counterexample, for a reason worth stating plainly:

> Satelliting a **ribbon concordance** yields a ribbon concordance. Every knot
> this campaign can certify slice by construction is certified through a
> ribbon-type object: a ribbon disk, a handle-ribbon disk, or a trace
> diffeomorphism. So `P(K)` and `P(U)` are joined by a ribbon concordance, and
> the difference `P(K) # -P(U)` comes out **ribbon**, not merely slice.

Concretely: the square knot `3_1 # -3_1` is fibered, nontrivial and ribbon, so
its `(p,q)`-cable is fibered and concordant to `T(p,q)`, and the two are
distinct because the cable has a companion. It is a genuine pair of distinct
concordant fibered knots. And it is worthless here, because the concordance is
a satellited ribbon concordance and the difference is ribbon. A second and
independent reason it fails: `Δ` of the cable carries the companion factor
`Δ_{Sq}(t^p)`, so the two sides do not share an Alexander polynomial and
Miyazaki's hypothesis fails anyway.

The general shape: **to get a non-ribbon difference out of a satellite you must
start from a slice knot that is not ribbon, which is the counterexample
itself.** Every satellite route is circular.

## 3. Teichner is the unique non-circular constructive lane

This is why `teichner_certify.py` is where the compute goes, and the reason is
structural rather than tactical.

Teichner's lemma: `K` is slice iff some ribbon `J` makes `K # J` ribbon. Given
such a `J`, write `K = (K # J) # (-J)`. Both pieces are ribbon, so `K` is slice
— but the disk is assembled from a ribbon disk and a **reversed** ribbon
concordance, so it carries local maxima and `K` is not thereby ribbon, nor even
known handle-ribbon. The ledger says the same thing: this is the only known
generator whose output is not automatically handle-ribbon.

So Teichner escapes section 2 exactly where satellites do not. Applied to a knot
that already carries a non-ribbon certificate, a verified Teichner certificate
is a counterexample outright, with nothing left to prove. That is the lane, and
it is the only constructive one on the board.

Status: `6_1` and `8_8` complete with no certificate (`8_8` at 7.96 h with a
10,023-link frontier preserved); `10_3`, `10_22`, `10_87` running at 24 h;
`9_41` and `9_46` with Astra. The fibered partners `8_9`, `8_20`, `9_27` must
**not** be run: adding a fibered ribbon `J` leaves `K_0` and `-K_1` unpaired
among the fibered prime summands, so Miyazaki still gives non-ribbon for the
sum and no certificate can exist.

## 4. The crossing nobody has tried

Route A has a generator that route B has never been pointed at.

An `r = 0` super-special RBG pair `(K_B, K_G)` has **diffeomorphic 0-traces**,
so `K_B` is slice iff `K_G` is, and a ribbon disk for one certifies the other
slice **with no inherited ribbon disk**. The ledger treats this purely as a way
to make fresh Tier-A candidates: find a ribbon disk on one side, get a
certified-slice knot of unknown ribbonness on the other.

But suppose the partner already carries a non-ribbon certificate. Then:

> `K_B` ribbon (a band search can find this) **and** `K_G` certified non-ribbon
> (Miyazaki or Hom-Park) ⇒ `K_G` is slice and not ribbon ⇒ **counterexample**,
> with no concordance coincidence needed anywhere.

This crosses route A's generator with route B's certificate. I do not find it in
`CANDIDATE_LEDGER.md`, `CAMPAIGN_PLAN.md` or `STRATEGY_2026-09-11.md`: the r = 0
entry says "run ribbon search on one side", and never says to choose the side
that is already certified non-ribbon.

Note that it does **not** need two concordant fibered knots. It is the only
route on this board that escapes section 1.

### Is it live, or empty for a stupid reason?

The four `r = 0` knots in `data/knots/` all have Alexander polynomial 1, and a
fibered knot with `Δ = 1` is the unknot, so **none of them** can carry a
Miyazaki certificate. If `r = 0` forced `Δ = 1` the lane would be empty on
arrival.

It does not. Manolescu-Piccirillo searched a 6-parameter family of 3375 special
RBG links and report that **five** candidate knots have Alexander polynomial 1
and are therefore topologically slice. That is a property of the survivors of
*their* obstruction pass, not a consequence of `r = 0`. The `r = 0` condition is
about the framing on `R` making the traces diffeomorphic; it does not constrain
`Δ`.

So the lane is live, and empty only of the examples we happen to have built.

### Can it be run from this repository today? No, and here is exactly why

Two blockers, both recorded rather than worked around.

**All ten stored MP exteriors are hyperbolic.** `data/knots/EXTRACTION_SUMMARY.md`
verifies "all tetrahedra positively oriented" for every one. A hyperbolic knot is
prime and not a satellite, so none of them can be a connected sum of prime
fibered knots and none can carry a Miyazaki certificate. The filter applied to
the data we hold returns the empty set, for a reason that has nothing to do with
whether the lane is live.

**The generator is not in this repository.** The MP DT-code formulas were
auto-transpiled to `../mma.py` and `../mp_auto.py`, which lived beside the
original macOS clone. This container has only `SR-Foxy`; the parent directory
holds nothing else, and `../ribbon_repo` is gone too. So the 6-parameter family
cannot be re-swept here without re-deriving the transpiler from the notebook.

That is the real state of it: the filter is cheap, the lane is untested, and the
inputs it needs are one directory outside every clone this campaign has used.

### What it would take

1. Generate `r = 0` super-special RBG realizations beyond the MP 6-parameter
   family, or mine Dunfield-Gong's 0-friend pairs for `r = 0` (the ledger's own
   unexecuted item, needing their dataset, which is not in this repository).
2. Filter for **either** side being non-ribbon-certifiable rather than for
   `Δ = 1`. Note this inverts the search's usual taste: MP and DG both steer
   toward hyperbolic knots, and this filter wants the opposite. For Miyazaki that means a connected sum of prime fibered knots with
   a common irreducible `Δ` that do not pair, so the target is a **reducible or
   toroidal** 0-surgery, which is the opposite of the hyperbolic knots the RBG
   searches have favoured.
3. Run the band search on the partner.

Step 2 is the part that has never been asked of this data, and it is a cheap
filter: prime-summand decomposition and fiberedness are computable.

### The honest caution

Nothing above is a theorem that the lane is non-empty. RBG constructions
overwhelmingly produce hyperbolic knots, and a knot whose 0-surgery is toroidal
enough to be a connected sum of fibered knots may simply not arise there. The
claim is only that the filter has never been applied, that it costs little, and
that unlike every other route-B lane a hit needs **no** concordance coincidence.

## 5. What this note does not claim

It proves nothing about the slice-ribbon conjecture. Section 2 is an argument
about constructions available to this campaign, not a theorem that no satellite
construction can ever work; a slice-but-not-ribbon input would break it, which
is precisely the circularity. Section 4 is a proposal with an unquantified prior.
The three running Teichner searches remain the only computation on this board
whose success would be a proof.
