# Graph reconstruction: what a night of compute actually establishes

**No counterexample found.** Kelly-Ulam stands. What follows is a verified tool,
a measured quantity, and one reframing that I think is the useful output.

## Why this problem and not the others

Of the candidate conjectures, graph reconstruction is the only one where a
computer search can both *reach* new territory and *certify* a hit:

* **Andrews-Curtis is categorically excluded.** A search can only ever
  trivialise a presentation. Certifying that one is *not* AC-trivial needs an
  invariant nobody has. No amount of hardware changes this.
* **Euler's sum of powers, k=6.** The counting heuristic (below) is calibrated
  against the two cases that fell and puts the first counterexample near
  y = 1e86. The 2002 frontier of 730,000 took a distributed project years.
* **Jacobian conjecture.** No search handle; expected to be true.
* **Slice-ribbon.** Infinite unstructured space, and this repository already
  established that the filters steering its search are blind to the very
  distinction they are meant to resolve.
* **Graph reconstruction.** The analogous conjectures are *known false* for
  digraphs (Stockmeyer), hypergraphs (Kocay) and infinite graphs (Fisher).
  Finite simple graphs are the last one standing, and a hit is self-certifying.

### Euler k=6 calibration

Expected unordered solutions of x1^6+..+x5^6 = y^6 with y <= N is A*ln(N),
A = (5/6)*Gamma(7/6)^5/Gamma(11/6)/120 = 0.005073. The same formula for k=4
predicts 1.31 solutions below Frye's y=422,481 (there is exactly 1) and for
k=5 predicts 0.126 below Lander-Parkin's y=144 (there is 1 - ordinary Poisson
luck). Calibrated, it gives 0.0685 expected below the 2002 frontier, so
finding nothing there was exactly on script, and one solution needs y ~ 1e86.
All three cases are Calabi-Yau hypersurfaces, degree k in P^(k-1), K = O(0);
k=4 fell to Elkies' elliptic fibration on the K3, not to search.

## The engine

`deck.py` computes exact decks using nauty `labelg` canonical forms - not
hashes, so a reported collision is real and never a birthday accident.

**python-igraph 1.0.0's `Graph.canonical_permutation()` is broken**: two
labellings of the 4-vertex path give different "canonical" forms. Do not use
it for this. See `tests/test_deck.py`.

Positive control, exhaustive: zero deck collisions for n = 3..9, and exactly
one collision at n = 2 (K2 and its complement, the classical exception). So
the engine finds real collisions and invents none.

## What was measured

Exhaustively, over every non-isomorphic graph on n vertices, the largest
number of common cards attained by a non-isomorphic pair:

| n | graphs | max common cards b(n) | **deficit n - b(n)** |
|---|---:|---:|---:|
| 4 | 11 | 3 | 1 |
| 5 | 34 | 4 | 1 |
| 6 | 156 | 5 | 1 |
| 7 | 1,044 | 5 | 2 |
| 8 | 12,346 | 6 | 2 |
| 9 | 274,668 | 6 | 3 |

A counterexample to the reconstruction conjecture is exactly a pair with
**deficit 0**. The measured deficit does not approach 0; it grows.

## The reframing

Ivanov, [arXiv:2608.11930](https://arxiv.org/abs/2608.11930) (12 August 2026),
refutes the Bowler-Brown-Fenner conjecture and builds, for every even r >= 4,
families whose common-card *fraction* tends to 1 - 1/r, so the attainable
fraction is arbitrarily close to the whole deck. That reads like the
conjecture is nearly falsified.

It is the wrong statistic. Writing n_(r,t) = r*t + r(r+1)/2 + |selector| and
the paper's bound b >= (r-1)t + r(r+1)/2 - 1, the fraction rises toward
1 - 1/r while the **absolute deficit diverges**: for r=4 it is <= 14 at t=1
and <= 1013 at t=1000. Approaching fraction 1 and reaching deficit 0 are
different problems, and every construction that improves the fraction makes
the deficit worse.

So exhaustive small-n data and the best known asymptotic family point the same
way, and it is away from a counterexample.

**Caveat that matters.** The paper's b is a *lower* bound, so the deficits
quoted for its family are *upper* bounds on the true deficit. The true deficit
could be smaller - conceivably much smaller. Computing the exact b(G,H) for
S_r(a(t)) at small (r,t) - r=4, t=1 is only 26 vertices - is therefore the one
concrete computation that could overturn this reading, and the engine here is
built to do exactly that. It is the recommended next step, and it was not done
tonight.

## Negative results worth not repeating

Cai-Furer-Immerman pairs, the standard non-isomorphic graphs that agree on all
bounded-dimension Weisfeiler-Leman statistics, were tested as counterexample
candidates over eight base graphs (n = 12 to 60). Every pair shares **0** cards
out of n. Hiding structure from local refinement does nothing once a vertex is
deleted; the deck is a far stronger invariant than bounded-dimension WL. This
axis is closed.

## Reproduce

```sh
apt-get install -y nauty
python3 -c "import deck; print(deck.find_collisions(list(deck.geng(9))))"   # {}
python3 margin.py_driver   # see RESULTS table
python3 -c "import cfi, deck; print(deck.decks(list(cfi.pair(*cfi.BASES['K4']))))"
```
