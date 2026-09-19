# Infection cannot make a wild Miyazaki pair — and the reason in `HANDOFF` §4 is not the right one

19 September 2026, Opus. **CE: NO.** Reasoning note, with one computational
check and two retractions, one of them mine from earlier today.

---

## 1. The reduction, stated as sharply as it goes

Every route to a counterexample that this campaign can certify runs through:

> **two distinct concordant prime fibered knots `J`, `J'` with the same
> irreducible Alexander polynomial.**

Then `D = J # (-J')` is not homotopy-ribbon (Miyazaki Thm 5.5; primality free by
Lemma P) and is slice (since `J ~ J'`). That is a counterexample outright.

Searching for such a pair is a lottery — 35,472 Levine-Tristram survivors, no
reason any particular one is concordant. **Constructing** one is the question
worth thinking about, because there is an obvious machine for it.

## 2. The obvious machine, and why it looks like it should win

**Infection.** Take `K` fibered with irreducible `Delta`, a curve `eta` in the
exterior, and infect by a knot `J`, giving `K_eta(J)`.

* If `J` is **slice**, then `K_eta(J)` is **concordant to `K`** — free, standard,
  no coincidence required. This is the step the whole lane is missing everywhere
  else.
* If `lk(eta, K) = 0` (winding number `w = 0`) then
  `Delta_{K_eta(J)}(t) = Delta_K(t) * Delta_J(t^w) = Delta_K(t)`. Irreducible
  `Delta` is preserved.
* Fibered + irreducible `Delta` gives primality by Lemma P.
* `K_eta(J) != K` for `eta` essential in the exterior.

So every condition is met except fiberedness of `K_eta(J)`. If that held, the
conjecture would have fallen decades ago — so it must fail. The question is
**where**, and the answer in this repository is not right.

## 3. `HANDOFF` §4's stated reason does not survive putting `eta` on the fiber

`HANDOFF_2026_09_18_OPUS.md` §4:

> "a winding-number-zero satellite fixes `Delta` and primality but **its genus
> grows while `deg Delta` does not**, so `deg Delta < 2g` and it is not fibered."

That argument fails for the one choice of `eta` a constructor would actually
make. Take `eta` embedded in the interior of a **minimal genus Seifert surface**
`F` of `K` (for fibered `K`, the fiber). Curves there have `lk(eta, K) = 0`, so
`w = 0` and `Delta` is unchanged. But infection along such an `eta` **does not
change the genus**: the surface `F` is re-embedded with `J` tied into the bands
running through `eta`'s disk, and re-embedding does not change a surface's genus.
So `g(K_eta(J)) <= g(K)`, and `Delta` unchanged forces
`g(K_eta(J)) >= deg Delta / 2 = g(K)`. **The genus is exactly preserved and
`deg Delta = 2g` still holds.** The stated obstruction does not bite.

## 4. The obstruction that does bite is stronger and has nothing to do with genus

> **A fibered knot's essential companion torus must be crossed a nonzero number
> of times: a fibered satellite has winding number `w != 0`.**

For a fibered knot the fiber can be isotoped to meet an essential torus `T` in
the exterior in parallel essential curves, and the number of times the pattern
runs through the companion solid torus is exactly `w`. At `w = 0` the
intersection cannot be essential, and the torus compresses. So **every**
winding-number-zero satellite is non-fibered, wherever `eta` sits and whatever
happens to the genus.

*Status: this is the standard fibered-satellite argument as I can reconstruct it;
it is **not** checked here against a primary source and should carry a `[PV]`
until it is. The conclusion it supports is the one `HANDOFF` already asserts, so
nothing downstream changes — only the reason does.*

**Why the distinction is worth writing down.** Someone reading "genus grows"
would conclude that moving `eta` onto the fiber escapes the no-go, and would
then build `K_eta(J)`, find `Delta` irreducible, genus preserved, `deg Delta = 2g`,
primality intact — every cheap test passing — and believe they had a wild pair.
They would not. The real obstruction closes it, and the cheap tests cannot see
that.

## 5. The trap this exposes, which I walked into earlier today

The construction in §3 produces, for free, a knot that is **prime, `Delta`
irreducible, monic, `deg Delta = 2g`, and NOT fibered.**

That is exactly the configuration in which `deg Delta = 2g` is a false positive
for fiberedness — and in `results/ce_hunt_2026_09_19/README.md` §12 I wrote, of
the queued wild pairs, that

> "`deg Delta = 2 * genus` in every row, which re-confirms fiberedness
> independently."

**Retracted. `deg Delta = 2g` does not imply fibered.** Fiberedness implies
`Delta` monic with `deg Delta = 2g`; the converse is false.

Checked rather than asserted, against Dunfield-Gong's own table: of 2,558
knots in `plausibly_unknown.csv` flagged `fibered = 0` with a nontrivial
`Delta`, **59 have monic `Delta` with `deg Delta = 2 * genus3`.** Six of them:

| knot | `deg Delta` | genus | `Delta` |
|---|---|---|---|
| K15n77799 | 4 | 2 | `t^4-2t^3+3t^2-2t+1` |
| 16n86850 | 8 | 4 | `t^8-4t^7+10t^6-16t^5+19t^4...` |
| 16n429842 | 4 | 2 | `t^4-2t^3+3t^2-2t+1` |
| 16n481747 | 4 | 2 | `t^4-6t^3+11t^2-6t+1` |
| 17nh_0000497 | 4 | 2 | `t^4-3t^2+1` |
| 17nh_0009552 | 4 | 2 | `t^4-6t^3+11t^2-6t+1` |

The queued targets are unaffected: their `fibered` flag comes from **HFK**, which
does decide fiberedness (Ghiggini, Ni), not from the degree. It was my
*inference* that was wrong, not the data.

## 6. What this leaves

`HANDOFF` §4's conclusion stands: *"Every cheap construction breaks exactly one
of prime / fibered / irreducible. The annulus twist is a rare machine that
preserves all three."* Infection is now closed for a sharper reason than the one
recorded.

And the annulus machine hands back the same gap the other lanes have.
`research/05` records it: Abe-Jong-Omae-Takeuchi prove `K_n` bounds a smooth disk
**in a homotopy 4-ball `W(K_n)`**, not in `B^4`, and *"Is `W(K_n)` diffeomorphic
to `B^4`?"* is their open question. So the constructive lane does not deliver a
slice disk either — it delivers a standardization problem, which is the same
thing the `KDG` lane rests on (Oliveira-Smith) and the same thing `research/33`
Theorem A produces one stabilization away.

**The honest shape of the board: every route that gets concordance for free
loses fiberedness, and every route that keeps fiberedness gets its disk only in
a homotopy 4-ball.** That is one statement, and it is the wall.
