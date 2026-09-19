# Suzuki colored-Jones divisibility: no-go for plain zero-framed parallels

**Verdict:** do not compute Suzuki Theorem 2.2 on a fifth or higher plain zero-framed KDG parallel. The condition is already forced by boundary-link topology, independently of whether KDG is ribbon.

## Primary theorem

Suzuki's Theorem 2.2 states the strengthened integrality/divisibility containment for the reduced colored-Jones combinations of an `n`-component **ribbon or boundary link** with zero framing. Ribbon and boundary links occur in the same theorem with the same target ideal.

Source: Sakie Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, arXiv:1111.6408, Theorem 2.2:
https://arxiv.org/abs/1111.6408

## Why a zero-framed parallel is automatically a boundary link

Let `K` be any oriented knot and let `F` be an oriented Seifert surface. Choose `n` distinct levels in a small product neighborhood `F × [-epsilon,epsilon]`. The translates

`F_i = F × {t_i}`

are pairwise disjoint embedded Seifert surfaces. Their boundaries are pairwise parallel copies of `K` taken with the surface/zero framing. Hence the `n`-component zero-framed parallel `K^(n)` is a boundary link.

This argument does not use sliceness, handle-ribbonness, or ribbonness of `K`.

Therefore Suzuki Theorem 2.2 applies to `KDG^(n)` for every `n` solely because it is a zero-framed parallel. A failure is impossible if the link/cabling/framing identification and colored-Jones computation are correct.

## Consequence for the overnight campaign

The ordinary Jones 2-, 3-, and 4-parallel calculations were legitimate tests of Eisermann's ribbon-link conditions. The exact 4-parallel test has now passed. It would be tempting to move to a stronger colored-Jones divisibility test on `KDG^(5)` or another plain parallel. Suzuki's theorem shows that this would spend compute on a necessary condition that is automatic for this topology.

So:

- no fifth plain parallel for Suzuki Theorem 2.2;
- no enumeration of larger plain parallels for that ideal;
- a nonzero result would diagnose a convention/implementation error, not a counterexample.

## What is not closed

Suzuki's theorem can still be relevant if we construct a **different** multi-component ribbon-preserving satellite pattern `P` such that:

1. `P(U)` is ribbon, with the exact framing and markings certified;
2. ribbonness of a companion implies ribbonness of `P(companion)`;
3. `P(KDG)` is not automatically a boundary link for a reason independent of ribbonness;
4. the colored-Jones ideal supplies information not already forced by sliceness/handle-ribbonness.

No such pattern was produced in this pass. A Bing-type construction is not automatically acceptable: its axes, component count, framing, ribbon control, and boundary-link status must all be checked before compute.

## Relation to the previous four-parallel work

This note does not invalidate the exact result in `pass02_0410_four_parallel`. It changes resource allocation after that result. The four-parallel calculation remains a completed Eisermann gate; Suzuki simply tells us that a stronger colored-Jones continuation on the same **plain parallel** family cannot become a ribbon-only separator.
