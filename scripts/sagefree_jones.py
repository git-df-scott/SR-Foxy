#!/usr/bin/env python3
"""The Jones polynomial without Sage, by replacing two small Sage objects.

`Link.jones_polynomial()` is Sage-only, which in this repository is not a
convenience problem: Eisermann's two theorems are, per `research/02`, the ONLY
genuinely ribbon-only obstructions in the whole catalog that are also
computable, and both are read off the Jones polynomial.  Without it the
`L_{3,1}` lane cannot be finished even once the link is in hand.

`spherogram/links/jones.py` is otherwise pure Python: it runs a Morse
exhaustion of the diagram and contracts Temperley-Lieb elements, which are
non-crossing perfect matchings with Laurent-polynomial coefficients.  Its only
Sage imports are `LaurentPolynomialRing(ZZ, 'q')` and `PerfectMatching(s)`.
Both are small, so this module supplies them and injects them into that module.

Nothing about the algorithm changes: the exhaustion, the skein relations and
the normalisation are spherogram's own code, unmodified.  Only the coefficient
ring and the matching class are swapped.

Self-check: `python3 scripts/sagefree_jones.py` reproduces the values in
spherogram's own doctests for the trefoil bracket, the 4-component unlink
bracket, the Jones polynomial of `8_5`, and `V(O^n) = (q + 1/q)^(n-1)`.
"""
import itertools


class LaurentPoly:
    """Sparse Laurent polynomial in q over Z: {exponent: coefficient}."""
    __slots__ = ('d',)

    def __init__(self, d=None):
        if d is None:
            d = {}
        elif isinstance(d, int):
            d = {0: d} if d else {}
        self.d = {e: c for e, c in d.items() if c}

    @staticmethod
    def _coerce(x):
        if isinstance(x, LaurentPoly):
            return x
        if isinstance(x, int):
            return LaurentPoly(x)
        return NotImplemented

    def __add__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        d = dict(self.d)
        for e, c in o.d.items():
            d[e] = d.get(e, 0) + c
        return LaurentPoly(d)

    __radd__ = __add__

    def __neg__(self):
        return LaurentPoly({e: -c for e, c in self.d.items()})

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __mul__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        d = {}
        for e1, c1 in self.d.items():
            for e2, c2 in o.d.items():
                d[e1 + e2] = d.get(e1 + e2, 0) + c1 * c2
        return LaurentPoly(d)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            # (c q^e)^n = c^n q^(en); invertible only for a unit monomial.
            if len(self.d) != 1:
                raise ValueError('only monomials have negative powers')
            (e, c), = self.d.items()
            if c not in (1, -1):
                raise ValueError('non-unit monomial')
            coeff = 1 if c == 1 else (-1) ** (n % 2)
            return LaurentPoly({e * n: coeff})
        out = LaurentPoly(1)
        for _ in range(n):
            out = out * self
        return out

    def __floordiv__(self, other):
        """Exact division; the caller in spherogram asserts exactness."""
        o = self._coerce(other)
        num = dict(self.d)
        den = dict(o.d)
        if not den:
            raise ZeroDivisionError
        dmax = max(den)
        dlead = den[dmax]
        quot = {}
        while num:
            nmax = max(num)
            e = nmax - dmax
            c, r = divmod(num[nmax], dlead)
            if r:
                raise ValueError('inexact division')
            quot[e] = quot.get(e, 0) + c
            for de, dc in den.items():
                k = e + de
                num[k] = num.get(k, 0) - c * dc
                if not num[k]:
                    del num[k]
        return LaurentPoly(quot)

    def __eq__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self.d == o.d

    def __hash__(self):
        return hash(tuple(sorted(self.d.items())))

    def __bool__(self):
        return bool(self.d)

    def substitute_complex(self, value):
        return sum(c * value ** e for e, c in self.d.items())

    def valuation_at(self, value, max_order=20):
        """(order of vanishing at q = value, leading coefficient).

        Divides by (q - value) repeatedly over the complex numbers, which is
        all Eisermann's `null V` and `det V` need.
        """
        num = dict(self.d)
        order = 0
        while order <= max_order:
            if abs(complex(sum(c * value ** e for e, c in num.items()))) > 1e-7:
                break
            shift = min(num)
            poly = {e - shift: c for e, c in num.items()}
            deg = max(poly)
            new = {}
            rem = 0 + 0j
            for e in range(deg, 0, -1):
                rem = poly.get(e, 0) + rem * value
                new[e - 1] = rem
            check = poly.get(0, 0) + rem * value
            if abs(complex(check)) > 1e-6:
                break
            num = {e + shift: c for e, c in new.items()}
            order += 1
        return order, sum(c * value ** e for e, c in num.items())

    def __repr__(self):
        if not self.d:
            return '0'
        parts = []
        for e in sorted(self.d):
            c = self.d[e]
            parts.append(f'{c}*q^{e}')
        return ' + '.join(parts)


class _Ring:
    def one(self):
        return LaurentPoly(1)

    def zero(self):
        return LaurentPoly()

    def gen(self):
        return LaurentPoly({1: 1})

    def __call__(self, x):
        return LaurentPoly._coerce(x)

    def __contains__(self, x):
        return isinstance(x, (LaurentPoly, int))


class PerfectMatching:
    """Minimal stand-in: a set of disjoint pairs covering 0..n-1."""
    __slots__ = ('pairs', '_partner', '_key')

    def __init__(self, spec):
        pairs = []
        for a, b in spec:
            pairs.append((a, b) if a < b else (b, a))
        pairs.sort()
        self.pairs = tuple(pairs)
        self._partner = {}
        for a, b in pairs:
            self._partner[a] = b
            self._partner[b] = a
        self._key = self.pairs

    def base_set(self):
        return set(self._partner)

    def partner(self, a):
        return self._partner[a]

    def is_noncrossing(self):
        for (a, b), (c, d) in itertools.combinations(self.pairs, 2):
            if a < c < b < d:
                return False
        return True

    def __iter__(self):
        return iter(self.pairs)

    def __len__(self):
        return len(self.pairs)

    def __eq__(self, other):
        return isinstance(other, PerfectMatching) and self._key == other._key

    def __hash__(self):
        return hash(self._key)

    def __lt__(self, other):
        return self._key < other._key

    def __repr__(self):
        return repr(list(self.pairs))


def install():
    """Inject the stand-ins into spherogram's jones module."""
    from spherogram.links import jones as _j
    _j.R = _Ring()
    _j.q = _j.R.gen()
    _j.PerfectMatching = PerfectMatching
    _j.PerfectMatchings = None
    return _j


def jones_polynomial(link):
    """Jones polynomial, SnapPy's new convention, as a LaurentPoly in q."""
    j = install()
    return j.jones_polynomial(link, normalized=True)


def kauffman_bracket(link):
    j = install()
    return j.kauffman_bracket(link)


if __name__ == '__main__':
    import snappy
    j = install()
    q = j.q
    ok = True

    def check(label, got, want):
        global ok
        good = got == want
        ok = ok and good
        print(('ok  ' if good else 'FAIL') + f' {label}: {got}')

    # spherogram's own doctest values
    check('bracket T(2,3)', kauffman_bracket(snappy.Link('T(2, 3)')),
          q**-2 + LaurentPoly(1) + q**2 - q**6)
    U4 = snappy.Link(braid_closure=[1, -1, 2, -2, 3, -3])
    check('bracket U4', kauffman_bracket(U4),
          -(q**-1) - 4 * q - 6 * q**3 - 4 * q**5 - q**7)
    want85 = (LaurentPoly(1) - q**2 + 3 * q**4 - 3 * q**6 + 3 * q**8
              - 4 * q**10 + 3 * q**12 - 2 * q**14 + q**16)
    check('V(8_5)', jones_polynomial(snappy.Link('8_5')), want85)
    for n in (2, 3, 4, 5):
        word = []
        for i in range(1, n):
            word += [i, -i]
        U = snappy.Link(braid_closure=word)
        check(f'V(O^{n}) = (q+1/q)^{n-1}', jones_polynomial(U),
              (q + q**-1) ** (n - 1))
    print('ALL OK' if ok else 'FAILURES PRESENT')
