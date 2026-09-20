# Checkpoint6 — exact mixed-colour completion and ideal structure

2026-09-20 01:57UTC. No counterexample. Campaign remains active until04:41:43UTC; baseline7%, total14 extra percentage points, stop with buffer at20%. Usage14% at start,15% at finish. Local3e4461e and remote2a07128 remain unchanged. One tracked bibliography correction is described below. No remote searches restarted; all local jobs completed.

## Exact result for both n3 component choices

Both provisional n3,k1 GST links' mixed-colour assignments(2,1) and(1,2) now pass Suzuki's exact ideal condition. This supersedes checkpoint5's unresolved full-polynomial computations and modular-only conclusions for this particular condition. It does not establish ribbonness or settle higher colours.

The saving is mathematical as well as computational. In checkpoint5's notation, the reduced invariant is v^3*N/D with D=(q-1)^2(q^2-1), q=v^2. Habiro's theorem guarantees J=H2*F with F in Z[q,q^-1] for the actual zero-framed, algebraically split input; H2=(q^5-1)(q^4-1)(q^3-1)/(q-1). H2 has order2 atq=1; D has order3. Suzuki adds precisely one factor(q-1). Therefore F(1)=0 is equivalent to N vanishing to order at least6 atv=1. Since F is already integral Laurent, F(1)=0 implies divisibility byq-1 in that same ring (multiply by a Laurent unit and apply the factor theorem). The change q=v^2 has nonzero derivative2 atv=1. Thus an **integer**, not merely modular, six-term Taylor calculation suffices for the full extra ideal condition. We use Habiro's baseline theorem explicitly; no claim to have computed the whole coloured polynomial is made.

Exact unreduced cable coefficients through(v-1)^5:

| n3 cycle | coefficients | numerator N coefficients | condition |
|---|---|---|---|
| 0 | [8,0,-2100,2100,315874,-633848] | [0,0,0,0,0,0] | passes |
| 1 | [8,0,-1332,1332,89378,-180088] | [0,0,0,0,0,0] | passes |

The positive obstruction control L10n57cycle1 gives fifth numerator coefficient-3840, and GSTn1cycle0 gives0. Integer Taylor results agree with the full Regina polynomials on both completed controls.

## Ordering improvement and reproducibility correction

Initially, trying every starting crossing recovered n3cycle0 modulo101 in4.4seconds (9724states). Integer arithmetic hit the20000-state cap on one subsequent layout. Inspecting Spherogram's `Frontier.biggest_all_consecutive_overlap` revealed randomized tie breaking inside MorseExhaustion. Previous reports calling the layout choice deterministic were inaccurate; exact polynomial values are unaffected, but runtime/order were not completely reproducible.

The corrected version seeds four layout rounds(20260920 through20260923), restores global RNG state afterward, tests all148 starts per round, and saves the complete chosen Morse-event list. Ordering is scored by maximum frontier size, then the sum of Catalan state bounds along the frontier. The selected cycle0 layout finished in5.7seconds with16154states below the original20000 cap. Its Morse events reconstruct the same input diagram signature with mirror reflection prohibited (`MORSE_DIAGRAM_CHECK.json`). Cycle1's integer run took3.8seconds and4862states. Do not repeat the old45second full-polynomial jobs or interpret their failure as obstruction.

Artifacts: `suzuki_taylor_integer*.py`, `check_suzuki_taylor_integer*.py`, `check_saved_morse.py`, and `suzuki_mixed/GST3_c0/TAYLOR_INTEGER_SEEDED_RESULT.json`, `suzuki_mixed/GST3_c1/TAYLOR_INTEGER_RESULT.json`. Earlier modular/state-cap outputs remain intact. The first ideal-table command used the system Python lacking SymPy; the saved script uses the established scratch runtime and passes.

## Literature finding that changes the next target

Sakie Suzuki, *On the colored Jones polynomials of ribbon links, boundary links and Brunnian links*, Banach Center Publications100(2014),213–222, DOI10.4064/bc100-0-12, arXiv:1111.6408. Primary preprint https://www.kurims.kyoto-u.ac.jp/preprint/file/RIMS1733.pdf; publication metadata https://www.impan.pl/en/publishing-house/banach-center-publications/all/100/0/86724/on-the-colored-jones-polynomials-of-ribbon-links-boundary-links-and-brunnian-links . Checked September19MDT2026; PDF/hash saved.

Theorem3.1 proves the ideals are principal with generator product_m Phi_m(q)^(max(0,floor((l+1)/m)-1)). Theorem2.2 gives the condition for ribbon **or boundary** links. The boundary result also has its own primary paper, Suzuki, arXiv:1103.2204 (submitted2011-03-11), https://arxiv.org/abs/1103.2204. Do not extend this to all slice links or assume GST is a boundary link.

Our symbolic gcd checks throughl=8 match the formula; principality over Z relies on Suzuki's theorem, not a gcd calculation over Q. In particular I1=(q-1), I2=(q-1)^2, I3=(q-1)^3(q+1). Hence for a two-component link the extra ideal factor in colours with minimum colour1 or2 only probesq=1. The first additionalq=-1 factor requires BOTH colours at least3. This is a structural reason to distinguish a(2,2)Taylor experiment from a(3,3)root-of-unity experiment.

`research/02_ribbon_only_obstructions.md` incorrectly attributed arXiv1111.6408 to Habiro–Massuyeau. Corrected both occurrences to Suzuki with publication metadata and theorem scope; other concurrent research files untouched.

## Next experiment and limits

A bounded(2,2)calculation can reuse all smaller traces and needs one new J(AABB). Its prefactor denominator has order4 atq=1; H2 contributes2 and I2 contributes2, so the numerator must vanish through order7 atv=1. The baseline again reduces this to exact integer Taylor data rather than a full polynomial. First estimate the all-starts seeded frontier widths and calibrate controls; avoid an unbounded four-parallel computation. It remains unproved here whether this low-order consequence is already forced by classical sliceness data.

For a genuinely new non-q=1 condition, plan a(3,3)calculation atq=-1 with explicit representation/cabling normalization and boundary-link controls. No implementation has been completed. Suzuki's boundary theorem means ordinary boundary-link constructions automatically pass, even for nonribbon companions; it does not close every ribbon-preserving satellite pattern or GST.

The search also located Meilhan–Suzuki, *The universal sl2 invariant and Milnor invariants*, arXiv1405.3062, https://arxiv.org/abs/1405.3062. Its abstract relates a reduction to Milnor concordance invariants, but the precise reduction needed for our Taylor coefficients was not verified. This is a source to audit, not a theorem that our condition is redundant. Literal GST dotted-band transport remains the independent geometric lead. Standard-B4 sliceness and global nonribbonness must still concern the same precisely identified knot.
