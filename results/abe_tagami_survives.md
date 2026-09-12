# The Miyazaki/Abe-Tagami sums survive the tool that closed the Turaev lane
2026-09-12

## The comparison

`slice_obstruction_HKL` with the same spec, `[(10,[0,20]),(20,[0,10])]`, method
`basic`:

| knot | crossings | HKL | seconds | verdict |
|---|---|---|---|---|
| Turaev A(1,1,1,1) | 143 | **(3, 13)** | 25.3 | not topologically slice, DEAD |
| Turaev A(2,1,1,1) | ~150 | **(5, 11)** | - | DEAD |
| Turaev A(1,2,1,1) | - | **(3, 19)** | - | DEAD |
| Turaev A(1,3,1,±1) | - | **(7, 2)** | - | DEAD |
| **D_{0,1} = K_0 # (-K_1)** | **25** | **None** | **0.8** | **survives** |
| **D_{0,2} = K_0 # (-K_2)** | **47** | **None** | **0.8** | **survives** |

Nine of nine loaded Turaev members died to this obstruction. Both Abe-Tagami sums
tested survive it, in under a second.

## Where that leaves the Abe-Tagami lane

For D_{n,m} = K_n # (-K_m) with n != m and n + m != -1:

- **non-ribbon is PROVED** (Miyazaki Trans. AMS 341 (1994) Thm 5.5, via Abe-Tagami
  Cor. 4.3, using that the K_n are prime fibered with a common irreducible Alexander
  polynomial and K_n is not isotopic to K_m);
- tau = epsilon = nu = signature = 0, and H_1 of the double branched cover agrees
  across the whole family (computed here earlier);
- Casson-Gordon via HKL finds nothing;
- **smooth sliceness is open**, and is equivalent to [K_n] = [K_m].

So the standard battery is exhausted on these knots. They are the strongest route-B
candidates on the board, and the tool that just closed a forty-year-old lane in
seconds does not touch them.

This is coverage, not a proof of sliceness. HKL returning None means no obstruction
was found in the searched grid.

## The search now running, and its exact difficulty

Teichner's lemma: D is smoothly slice iff some ribbon J makes D # J ribbon. A
certificate would prove D slice, and D is already proved non-ribbon, so **a
certificate is a counterexample to the Slice-Ribbon Conjecture.**

Two things sharpen the search.

**Fibered partners are provably futile.** If J is prime and fibered, D # J is a
connected sum of prime fibered knots and Miyazaki's pairing theorem forces the
summands to match by mirror/reversal. K_n could only pair with -K_n, but K_n is not
isotopic to K_m, so D # J is not homotopy-ribbon, hence not ribbon. The partner list
is therefore restricted to verified non-fibered ribbon knots: 6_1 (genus 1), 8_8
(genus 2), 9_41 (genus 2), 10_3 (genus 1), 10_22 (genus 3), 10_87 (genus 3).

**The search is exactly as hard as the concordance question, and this should be said
plainly.** J is ribbon, so [J] = 0, and D # J ribbon implies D # J slice implies
[D] = 0. So finding J is equivalent to proving [K_n] = [K_m]. It is not a shortcut
around the open problem; it is a search for a certificate of it. If the K_n are
pairwise non-concordant, which is what most people would expect since annulus
twisting preserves the 0-surgery but has no reason to preserve concordance, then no
J exists and the search cannot succeed.

The honest framing: this is the only executable search left whose success would be a
proof, the targets have now outlived every cheap obstruction, and the probability of
success is low.

---

## Filter diagnostic: this lane's search space is genuinely non-trivial

The single most informative cheap measurement, run on one diagram at one band. An
intermediate link in a ribbon movie must itself be a ribbon link, so it must pass
linking number, signature and Fox-Milnor:

| target | one-band results | lk != 0 | sig != 0 | Fox-Milnor fail | **survive** |
|---|---:|---:|---:|---:|---:|
| 18nh00000601 | 2161 | 1704 | 387 | 68 | **2, both trivial bands** |
| D_{0,1} # 6_1 (31 cr) | 9427 | 7649 | 1658 | 76 | **33** |

For 18nh00000601 the one-band stage kills everything, so no two-band search can even
start: there is nothing to extend. For the Miyazaki sum there are **33 genuine
branches** to continue from. That is a real structural difference between the two
lanes and it is why compute is now pointed here rather than there.

It does not make success likely. As recorded above, a certificate here is equivalent
to proving [K_n] = [K_m], which is the open problem itself. But the search is at
least not vacuous, which is more than can be said for the flagship lane.

## The Teichner search: one completed pair, and a cost verdict

| target | partner | sum | time | certificate |
|---|---|---|---|---|
| D_{0,1} | 6_1 (non-fibered, genus 1) | 31 crossings | **4.2 hours** | **none** |

Box: 2 bands, band length <= 5, twists <= 2, one diagram. The container restarted
during the second pair; the script checkpoints per pair, so this one result survived
and the rest was lost.

**Cost verdict.** At 4.2 hours per pair, the full intended sweep of 6 non-fibered
partners across 3 targets is roughly 75 hours of single-core time, and that is for
one diagram each at band length 5. Widening to the band lengths that would make a
negative meaningful, or to multiple shaken diagrams, multiplies it again. **This
search is beyond the compute budget available here**, and the honest statement is
that it was sampled rather than run.

What the one completed pair establishes is narrow and should not be inflated: within
that box, on that diagram, with that partner, no ribbon disk exists for
D_{0,1} # 6_1. Since a certificate would have been equivalent to proving
[K_0] = [K_1], its absence is exactly what one would expect whether or not the knots
are concordant, and it discriminates between those cases not at all.
