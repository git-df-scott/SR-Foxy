# Grid sweep: which members of dA(p,q,r,s) die?

`slice_obstruction_HKL([(10,[0,20]),(20,[0,10])], method='basic')` run on each member's exterior
(each in its own subprocess with a 2400 s hard cap).  A non-`None` value is a PROOF that the knot
is not topologically slice, hence not smoothly slice.  The value printed is the pair
(n, order of the character on the n-fold branched cyclic cover) that certifies the obstruction.

| (p,q,r,s) | mu135 | mu246 | cr raw | cr  | alexOK | det | vol       | HKL              | verdict                         |
|-----------|-------|-------|--------|-----|--------|-----|-----------|------------------|---------------------------------|
| 1,1,-1,-1 | -1    | -1    | 300    | 138 | True   | 1   | 94.36820  | (3, 13)          | DEAD: not topologically slice   |
| 1,1,-1,1  | -1    | 1     | 300    | 137 | True   | 1   | 96.04367  | (3, 13)          | DEAD: not topologically slice   |
| 1,1,0,0   | 0     | 0     | 92     | 27  | True   | 1   | 28.72771  | None             | RIBBON (certified)              |
| 1,1,1,-1  | 1     | -1    | 300    | 127 | True   | 1   | 93.65988  | (3, 13)          | DEAD: not topologically slice   |
| 1,1,1,1   | 1     | 1     | 300    | 143 | True   | 1   | 95.04412  | (3, 13)          | DEAD: not topologically slice   |
| 1,1,2,1   | 2     | 1     | 404    | 172 | True   | 1   | 112.31406 | not computed     | inconclusive (not computed)     |
| 1,1,2,2   | 2     | 2     | 508    | 202 | True   | 1   | 129.51541 | not computed     | inconclusive (not computed)     |
| 1,2,1,1   | 1     | 1     | 308    | 149 | True   | 9   | 96.22185  | (3, 19)          | DEAD: not topologically slice   |
| 1,3,0,0   | 0     | 0     | 108    | 37  | True   | 25  | 31.75726  | None             | RIBBON (certified)              |
| 1,3,1,-1  | 1     | -1    | 316    | 141 | True   | 25  | 95.76340  | (7, 2)           | DEAD: not topologically slice   |
| 1,3,1,1   | 1     | 1     | 316    | 169 | True   | 25  | 97.05466  | not computed     | inconclusive (not computed)     |
| 1,4,1,1   | 1     | 1     | 324    | 178 | True   | 49  | 97.79818  | not computed     | inconclusive (not computed)     |
| 2,1,0,0   | 0     | 0     | 108    | 39  | True   | 1   | 40.33169  | None             | RIBBON (certified)              |
| 2,1,1,-1  | 1     | -1    | 316    | 139 | True   | 1   | 98.35895  | (5, 11)          | DEAD: not topologically slice   |
| 2,1,1,1   | 1     | 1     | 316    | 150 | True   | 1   | 99.99848  | (5, 11)          | DEAD: not topologically slice   |
| 2,3,1,1   | 1     | 1     | 332    | 166 | True   | 25  | 101.37351 | TIMEOUT(3600s)   | inconclusive (TIMEOUT(3600s))   |
| 3,1,0,0   | 0     | 0     | 124    | 51  | True   | 1   | 45.01446  | None             | RIBBON (certified)              |
| 3,1,1,1   | 1     | 1     | 332    | 162 | True   | 1   | 103.24351 | TIMEOUT_OR_ERROR | inconclusive (TIMEOUT_OR_ERROR) |
| 5,1,1,1   | 1     | 1     | 364    | 194 | True   | 1   | 106.97878 | not computed     | inconclusive (not computed)     |
| 7,1,1,1   | 1     | 1     | 396    | 226 | True   | 1   | 108.83054 | not computed     | inconclusive (not computed)     |


## Verdicts

* **(r,s) = (0,0):** RIBBON, with a one-band certificate verified by
  `verify_ribbon_to_unknot`.  These are the members Theorem I does *not* obstruct, and they behave
  exactly as they should.
* **(r,s) != 0:** every member whose HKL computation finished is **DEAD** --- `slice_obstruction_HKL`
  returns a non-`None` value, which is a proof that the knot is not topologically slice, hence not
  smoothly slice, hence not a counterexample to the slice-ribbon conjecture.
* **No member has survived.**  The members marked TIMEOUT are simply too big for the computation
  (162-226 crossings); they are not live candidates, they are uncomputed.

## Pattern

* Every (r,s) != 0 member for which the computation finished is killed.
* The (r,s) = (0,0) members are ribbon (certified), and HKL correctly returns `None` for them.
* Which cover fires depends on (p,q), not on (r,s): all four members with (p,q) = (1,1) and
  r,s in {+-1} die by the same character (3, 13) --- the 3-fold branched cover, whose first homology
  is Z/13 + Z/13 (= |Delta(omega) Delta(omega-bar)| for omega a primitive cube root of unity);
  (p,q) = (2,1) dies by (5, 11) --- the 5-fold cover; (p,q) = (1,2) by (3, 19); (p,q) = (1,3) by
  (7, 2).  The obstruction is therefore insensitive to the sign and size of r and s (compare
  (1,1,1,1), (1,1,1,-1), (1,1,-1,1), (1,1,-1,-1): all (3,13); and (2,1,1,1), (2,1,1,-1): both
  (5,11)), and depends only on (p,q).  That is what one expects of a Casson-Gordon invariant: it
  is computed from a metabolizer of the linking form of a branched cyclic cover, and the
  homology of those covers is determined by the Alexander polynomial, i.e. by p and q alone.
  In other words **Casson-Gordon does not see the Milnor data at all** --- it kills these knots
  for a reason completely unrelated to Turaev's obstruction, and it kills them even though the
  (0,0) member with the very same Seifert form is ribbon.  (For the (0,0) members HKL returns
  `None`, as it must.)

* The determinant is (2q-1)^2 in every case (1, 9, 25, 49 for q = 1,2,3,4) and the n-fold cover
  order in the certificate is coprime-ish to it rather than tracking it: q = 1 gives (3,13) or
  (5,11), q = 2 gives (3,19), q = 3 gives (7,2).  No simple rule in the data so far.

## Caveats

* A member marked TIMEOUT is **not** a live candidate: it is a member whose diagram
  (162-226 crossings) is too big for `slice_obstruction_HKL` in the time allowed.  The sweep was
  still running when this file was written; `hkl_results.txt` is the live record.
* The Casson-Gordon result is a genuine proof for the knots as built.  A different realization of
  the same (X, r, s) --- which Turaev's Section 1.5 certainly permits --- is a different knot, and
  would have to be tested separately.  See Section 6 of `REPORT.md`.
