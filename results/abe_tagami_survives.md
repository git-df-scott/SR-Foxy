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
