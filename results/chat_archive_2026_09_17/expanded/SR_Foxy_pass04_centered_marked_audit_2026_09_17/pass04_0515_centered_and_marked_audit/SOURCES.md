# Sources and exact use in this pass

Checked 17 September 2026 UTC. Only the pages/sections listed were checked;
this is not an exhaustive source-paper or repository review.

1. Michael Eisermann, *The Jones polynomial of ribbon links*, Geometry &
   Topology 13 (2009), 623–660. Theorems 1–2 (ribbon-link nullity and reduced
   determinant congruence), Lemma 1 (upper nullity bound), Definition 6.12,
   Proposition 6.13, Corollary 6.15, Example 6.16, and section 7.1. Author PDF
   pages 29–30, printed 30–31, inspected as images for the satellite statements,
   numerical ribbon control and stable-ribbon observation. Its questions are
   not treated as theorems.
   https://pnp.mathematik.uni-stuttgart.de/igt/eiserm/publications/ribbonlinks.pdf

2. Charles Livingston, *A survey of classical knot concordance*, Handbook of
   Knot Theory (2005), 319–347; arXiv:math/0307077v4 (2004 preprint). Section 2.1
   immediately after Definition 2.3 records the Casson observation that a slice
   knot has a ribbon stabilizer making its sum ribbon. PDF page 3, printed 4,
   inspected as an image. This is a smooth-knot statement, not an asserted
   theorem about arbitrary slice links.
   https://arxiv.org/pdf/math/0307077

3. H. R. Morton and P. Strickland, *Jones polynomial invariants for knots and
   satellites*, Math. Proc. Cambridge Philos. Soc. 109 (1991), 83–103.
   Theorem 1.1 and Corollary 1.2, printed 87, supply the scalar tangle/closure
   normalization; Theorem 2.1 and Corollaries 2.2–2.3, printed 92, supply cabling
   via tensor products. Both pages inspected as images. A further screenshot
   request for the following page returned HTTP 429 and is not claimed read.
   The Chebyshev coefficients and connected-sum formulas in our notes are
   derived using these generic identities, before root specialization.
   Author-uploaded paper:
   https://www.researchgate.net/profile/Hugh-Morton/publication/232015440_Jones_polynomial_invariants_for_knots_and_satellites/links/5ba287fd92851ca9ed15cead/Jones-polynomial-invariants-for-knots-and-satellites.pdf

4. Sakie Suzuki, *On colored Jones polynomials of ribbon links, boundary links
   and Brunnian links*, arXiv:1111.6408 (2011). Theorem 2.2, PDF page 2/printed 3,
   inspected. It treats ribbon and boundary links in the same divisibility
   statement. This was already the previous checkpoint's subject; it is NOT
   reported as a new elimination in this pass.
   https://arxiv.org/pdf/1111.6408

5. Megan du Preez, Bryan Silva, Eric Yu and Sherry Gong, *Connections between
   common slice obstructions and the Eisermann ribbon obstruction*, Texas A&M
   REU report, July 2025. Theorem 5.10 on printed page 18 has its proof marked
   WIP, confirmed in the page image. We do not import the stronger all-knot
   assertion as a proved theorem.
   https://artsci.tamu.edu/mathematics/_files/_docs/reu/results/2025/dupreez-silva-yu-report.pdf

6. Spherogram source, `spherogram_src/links/invariants.py`, blob
   `a0103e578ac924a8443380b4a19b66ffb01ea85d`. Lines 1–210 read via the GitHub
   connector; the `knot_group` method provides an explicit check of the
   positive/negative Wirtinger-relation convention. The direct-PD scripts
   neither import nor execute that method. The longitude transport rule is
   explained directly in our certificate note.
   https://github.com/3-manifolds/Spherogram/blob/master/spherogram_src/links/invariants.py

7. SR-Foxy at `7a74678daccd9f3148b25a22a3f84a82eb1d374b`: complete PD input cards
   `data/knots/AbeTagami_K_0_K_-1__6_3.json`, `AbeTagami_K_1.json`,
   `AbeTagami_D_0_1.json`, and `AbeTagami_L_63_c1_c2.json`. The latter is the
   marked three-component link whose diagram is the input to the new
   Wirtinger certificate. Input cards' knot-to-paper claims are retained as
   dependencies, not independently certified by matching scalar invariants.
   https://github.com/git-df-scott/SR-Foxy/tree/7a74678daccd9f3148b25a22a3f84a82eb1d374b/data/knots

8. The local conversation attachment `PROPOSED_TRANSFER_THEOREM.md` was read
   in full. Its equation (2) is corrected in this package; it is model-derived
   research, not a primary published source. The earlier code/report bundle
   was inspected selectively for the portable cabler/frontier engine and
   prior checker. We did not rerun its earlier 4,832 tests or large controls.
