# Conditional surgery-framing gate for the mixed-axis proposal

17 September 2026 UTC. **NO COUNTEREXAMPLE. No new surgery diagram or disk.**

This is an elementary calculation for one explicitly specified shortcut. It is NOT a rejection of the unframed scaffold, an arbitrary changed-axis construction, or Opus's current work. In particular, the stored scaffold specifies a linking matrix but **does not specify surgery framings**. The diagonal entries below are an assumption for this calculation, not newly discovered input data.

## Convention and hypothesis

Use the component order `(c1_upper,c2_upper,c1_lower,c2_lower)` from `data/knots/AbeTagami_marked_product_scaffold.json` at `b7ae7270ea6abc6976c0ec598067e2cac3602887`. Its two Hopf linking numbers are +1 and -1, with zero cross terms. Research/14 gives framings (2,0) for the n=1 trace. Suppose, specifically, that we put this trace on the upper pair and its orientation-reversed mirror on the lower pair. The full assumed matrix is

```
Q = [[2,1, 0, 0],
     [1,0, 0, 0],
     [0,0,-2,-1],
     [0,0,-1, 0]].
```

Now make genuine framed Kirby slides whose two retained handle classes are

```
v1 = e1 + e4,   v2 = e2 + e3.
```

The hypothesis is that the other two surgery components are subsequently omitted, without any further framing changes, extra handles, or justified cancellation that changes the effective surgery presentation. This omission is NOT asserted to preserve the original boundary. It defines the proposed two-component surgery that we are testing.

## Exact failure

The inherited linking matrix on these two handles is

```
B_ij = vi^T Q vj,    B = [[2,0],[0,-2]].
```

Integral surgery on a link in S3 has first homology presented by its integer linking matrix. Directly: the meridians generate the abelianization of the link exterior, the preferred longitude of component i represents the sum of its pairwise linking numbers times the other meridians, and filling kills `framing_i * meridian_i + longitude_i`. These are exactly the rows of B.

Thus this two-component surgery has

```
H1 = coker(B) = Z/2 + Z/2,
```

and is not S3. No annulus-embedding argument can repair this particular boundary homology without changing the stated surgery data.

Reversing any constituent orientations gives

```
v1 = s1 e1 + s4 e4,   v2 = s2 e2 + s3 e3,   si in {+1,-1},
B = [[2,ell],[ell,-2]],    ell = s1*s2 - s4*s3 in {0,+2,-2}.
```

The determinant is -4 or -8. The Smith diagonals are (2,2) or (2,4). The exact script checks all 16 sign assignments. None yields an integral homology sphere. This includes sign choices that might fail other geometric or group gates; they are algebraic cases, not 16 realized candidate links.

There is also an all-integer parity extension. Q is even. If x and y are any integral handle classes with x congruent to e1+e4 and y congruent to e2+e3 modulo 2, then xQx, yQy and xQy are all even. Their 2-by-2 Gram determinant is divisible by four, so cannot be +1 or -1. This statement is a consequence of bilinearity and parity, not a finite enumeration of handle slides. Its geometric use still requires proving that the proposed surviving handles have these exact mod-2 classes in this fixed form.

## What survives; constructive implication

Keeping the full four-handle link changes the test: det(Q)=1. That passes a homology test only, and does not prove the ambient trace is a product or that its handles cancel away from the disk.

Changing the two coefficients to (+1,-1), with linking zero, also gives determinant -1. That is a different surgery, not the inherited framed slide. Even if both axes form an unlink in S3, identifying the image of the marked knot is a separate obligation. Park's standard-annulus theorem offers a possible way to certify the standard ambient ball for appropriately embedded annuli, but its hypotheses must be supplied for the actual new axes; changing coefficients cannot be treated as a free move.

Therefore the useful next target is a **marked, framed** construction, not merely conjugate words. Ask for the actual pair of axes, coefficients, Kirby moves or standard-annulus certificate, and the resulting knot. A genuinely different framing or nonlocal construction is not excluded here.

## Verification and controls

Run from this directory:

```
python3 verify_framing_gate.py --output framing_rerun.json
```

The checker uses exact integer arithmetic and Python's standard library. Positive controls are the same-side Hopf block (determinant -1), independently assigned (+1,-1) framings (determinant -1), and the full four-handle matrix (determinant 1). All are expressly homology controls, not 4-ball standardness certificates. No target PD, band routing, surgery manifold or embedded annulus was generated in this check.

## Sources and scope

- SR-Foxy, `data/knots/AbeTagami_marked_product_scaffold.json`, pinned commit above: component labels and off-diagonal linking matrix. Read in full for this check. https://github.com/git-df-scott/SR-Foxy/blob/b7ae7270ea6abc6976c0ec598067e2cac3602887/data/knots/AbeTagami_marked_product_scaffold.json
- SR-Foxy, `research/14_marked_annulus_audit.md`, section 3: the n=1 (2,0) trace and its ordinary form. Mirror signs and the retained-class calculation above are deductions, not an asserted preexisting framed scaffold. https://github.com/git-df-scott/SR-Foxy/blob/b7ae7270ea6abc6976c0ec598067e2cac3602887/research/14_marked_annulus_audit.md
- JungHwan Park, *A Construction of Slice Knots via Annulus Modifications*, arXiv:1512.00401v1 (2015), sections 2-3; consulted 17 September 2026 UTC. Distinguishes the exotic/homotopy-ball conclusion from the standard-annulus smooth-slice conclusion. Not applied to an unconstructed pair here. https://arxiv.org/html/1512.00401v1

No novelty claim. No global conclusion about slice-ribbon, D01, arbitrary stabilizations or all changed-axis operations.
