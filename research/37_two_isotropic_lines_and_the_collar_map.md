# Two isotropic lines explain the remaining geometric problem

18 September 2026. **No counterexample, annulus, or disk is certified.** This
is a bounded continuation of research/35, using the saved algebraic collar
maps rather than asserting that they are the actual geometric collar.

## Exact question

Why can the 0110 band repair preserve the target polynomial but fail the
disk-group gate? Compute its boundary Alexander class and its image under the
saved q0. A useful result is a structural distinction between polynomial
cancellation and disk-exterior cancellation, with an exact reproducible map.

Write L=Q[t,t^-1], d=t^4-3t^3+5t^2-3t+1, and F=L/(d). In the boundary
module F^2 use the marked native axes e_U,e_L from research/35. The archived
source presentation has an Alexander module whose tensor with F has dimension
one. The generator of this one-dimensional quotient is chosen to be q0(e_U).

## 1. The saved collar map has the opposite sign from the repaired line

Exact Fox reduction of the nine-generator source presentation gives

    q0(e_U)=1,      q0(e_L)=-1.

Both companion native axes map to t^-1 times their respective images. This
was calculated directly from the saved boundary-to-source words. Every source
relator and every mapped boundary Fox relator vanishes in the quotient; direct
images of the final axis words agree with their coordinate pushforwards.

Conjugating the lower factor by the seam meridian to power n multiplies its
Alexander class by t^n. Therefore the saved q_n induces

    (a,b) -> a-t^n b,        kernel = span_F((t^n,1)).

The two previously studied band choices have the following exact classes:

| Choice | First axis | Second axis | q0 images |
|---|---|---|---|
| 0000 | (1,-t^-1) | (t^-1,-1) | 1+t^-1, 1+t^-1 |
| 0110 | (1,-1) | t^-1(1,-1) | 2, 2t^-1 |

Thus 0110 collapses the boundary span to the line (1,-1), while the saved q0
kills the different line (1,1). More generally (1,-1) is transverse to every
saved q_n kernel: dependence would require t^n=-1 in F. No root of d lies on
the unit circle, as shown in research/35, so this is impossible for nonzero n;
n=0 would give 1=-1 in characteristic zero.

**A limited but rigorous geometric consequence:** if a saved q_n is identified
with the actual inclusion into a disk exterior, neither 0110 axis can bound
an individual disk in that exterior. Its nonzero Alexander-module image
already prevents nullhomotopy. This does **not** obstruct an annulus between
the two nontrivial curves. Indeed their module images differ by t^-1, exactly
the effect permitted by conjugating a zero-exponent word by an element of
abelianization -1 (with the convention taking axis 1 to axis 2). The earlier
nonabelian trace obstruction is strictly stronger here.

## 2. The polynomial cancellation is cancellation of the boundary pairing

The native Blanchfield pairing, in the conventions of research/35, has the
following representative modulo L:

    H = (t^2/d) diag(1,-1).

This follows from an exact matrix identity. Let

    M = [[1,-t^-1],[t^-1,-1]],    h=t(t^2-1)/d.

Then M H M* = [[0,h],[-h,0]], the previously computed longitude response,
where * is transpose and t -> t^-1. The matrix M is invertible modulo d, so
this identifies H as a pairing on the d-torsion module. We are **not** claiming
that M is invertible over all of L; its determinant is t^-2-1. Inverting it
modulo d is sufficient, because the pairing takes values in the d-torsion
part of Q(t)/L. The equivalence between equivariant linking modulo L and
Blanchfield pairing uses Proposition 3.8 of Conway--Piccirillo--Powell, with
the conventions and source caveat already recorded in research/35.

Both the kernel line (t^n,1) and the repaired line (1,-1) are isotropic: the
pairing restricted to either line is zero. They are different isotropic
lines, and isotropy alone does not say that a curve dies in the disk exterior.
The exact rational response of the actual 0110 link is zero, a stronger fact
than vanishing of the pairing modulo L.

For the word-level windings of research/35 the two vectors are

    v1=(1,-t^(k-1)),       v2=(t^-1,-t^l).

Their self-pairings under H are zero. Their mutual pairing is

    (t^2/d) (t-t^(k-l-1)) modulo L.

It vanishes precisely when k-l=2: otherwise divisibility by d would imply
a nontrivial integral power of a root of d equals 1. On that line v2=t^-1 v1,
and q_n(v1)=1+t^(n+l+1) is nonzero for every pair of integers n,l. Hence this
whole winding repair family also misses every saved kernel line. This is an
all-parameter statement, not a search over exponent bounds.

## 3. What a new connector must accomplish

For an actual physical pair with these isotropic boundary classes, the
equivariant response has no nontrivial residue modulo L; denote the remaining
Laurent matrix by E. Provided the link's surgery determinant formula and
normalization have been justified, opposite surgeries have determinant factor

    det(I+diag(r,-r) E) = 1+r(E11-E22)-r^2 det(E).

In this fixed rational normalization, this factor equals 1 **for all r**
exactly when E11=E22 and det(E)=0. Equality at one prescribed nonzero r is a
weaker condition. These statements are algebraic; polynomial equality up to
Alexander units must be normalized before using them. Vanishing residue
alone does not certify E=0 or an unchanged boundary polynomial.

This separates the remaining design work into concrete requirements:

1. Retain an isotropic boundary line and check the actual Laurent response.
2. Alter the nonabelian axis words enough to pass the actual collar's group
   condition. Inserting a conjugating word of exponent zero into a
   zero-exponent lower segment leaves its Alexander class unchanged, so it is
   one algebraically admissible kind of change; no such geometric change is
   yet constructed.
3. Track a compression or embedded annulus during that change. For the saved
   maps, individual capping disks are unavailable by the module calculation.

This is not a proposal to enumerate words of exponent zero. The next useful
object is a specific geometric connector whose cancellation can be followed
through the product collar, with its based words recorded. The algebra now
states which information such a construction must preserve and change.

## 4. A specific correction passes both module and full group gates

The preceding requirements can be met simultaneously at word level. This is
an elementary constructive correction, not evidence of an embedded annulus.
Let a,b be the actual 0110 axis words, q=q0, and mu the image of boundary
generator 5. All source words use only source generators 5,6,8. These have
literal upper-boundary lifts 3,4,8: substitution by q sends each lift to the
corresponding single source letter.

Form the source word

    delta_source = mu^-1 q(a) mu q(b)^-1,

freely reduce it, and lift every letter using that dictionary to get a
boundary word delta. Put b'=delta b. Then by direct free reduction

    q(b') = mu^-1 q(a) mu.

No faithfulness of a matrix representation or decision procedure for the knot
group is involved in this identity. The source correction has 104 letters;
the freely reduced corrected boundary word has 110. All letters and
conventions are saved in `word_correction.json`. Direct Fox evaluation in
the full two-dimensional boundary quotient gives

    [delta]=(0,0),      [b']=[b]=t^-1(1,-1).

Thus the exact group-conjugacy requirement and the isotropic boundary classes
are compatible once this more general word modification is allowed. The
pure-winding no-go theorem cannot be extended to all module-preserving word
changes. We do not infer integral membership in a second derived subgroup
merely from the computed rational Alexander class.

**A further falsification check prevents overselling the construction.** Write
the original second axis b=U L V with

    U=[4,-1], L=[-15,14,-13,17], V=[3,-4].

If this specific based b' arose solely by changing the lower connector as
U w L w^-1 V, then q(U^-1 b' V^-1) would be conjugate to q(L). In the saved
degree-six representation, their trace difference is

    -20z^5-96z^4-108z^3-52z^2-16z-36,

nonzero in Q[z]/(z^6+3z^5+5z^4+4z^3+2z^2+z+1). Hence **this based word** is not
that simple connector replacement. This does not exclude changing other
segments, free basepoint conjugation, different collars, or another correction.

An elementary existence observation further separates the tasks. Any finite
collection of free loop classes in the complement of R can be represented
by disjoint embedded circles, by general position. Crossing changes among
these circles, including self-crossing changes, can turn their underlying
link in S3 into the unlink. Each crossing change is supported in a ball
disjoint from R and is a homotopy in the complement of R, so it preserves the
individual free loop classes there. Thus abstract unlink representatives of
these corrected classes exist. This argument supplies neither a marked PD nor
control of equivariant linking: the crossing changes can change the Laurent
response E, and may leave the original two-band construction entirely.

The remaining constructive task is sharper now: realize the corrected classes
with controlled E and an embedded annulus in an **identified** disk exterior,
then verify the standard-B4 modification and resulting knot. Full group
conjugacy only provides a free homotopy (a map of an annulus), not an embedded
annulus. Nothing here bridges that central gap.

## Reproduction and limits

Run `python results/night_2026_09_18/collar_module.py` with SymPy 1.14.0.
The exact quotient coordinates and matrix identities are recorded in
`collar_module.json`. The producer reuses the archived boundary extractor and
the saved source presentation. It is not an independent figure-to-PD audit
and does not turn any q_n into an identified disk collar. All nullhomotopy
conclusions above are conditional on that identification. No knot census or
longer band-path search was run.

`python results/night_2026_09_18/word_correction.py` reproduces the correction,
its zero boundary-module class, the exact free-word identity, and the failed
simple-connector trace test. The module/form algebra and the initial word
correction were independently reviewed in `isotropic_review.md`.
