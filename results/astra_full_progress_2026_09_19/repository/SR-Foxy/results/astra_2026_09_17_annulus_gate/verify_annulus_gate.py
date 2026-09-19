#!/usr/bin/env python3
"""Exact algebra audit of SR-Foxy's marked annulus words (Python stdlib only).

This certifies statements about the supplied presentation, not its extraction
from a knot diagram. It constructs no slice disk and proves no nonconcordance
of the endpoint knots. See REPORT.md for the geometric scope and proofs.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path
from typing import Iterable

Word = list[int]
Poly = dict[int, int]
Pairs = list(itertools.combinations(range(4), 2))
Class2 = tuple[tuple[int, ...], tuple[int, ...]]
IDENTITY: Class2 = ((0, 0, 0, 0), (0, 0, 0, 0, 0, 0))
BASE: list[Class2] = [
    (tuple(int(i == j) for i in range(4)), (0,) * 6) for j in range(4)
]


def require(condition: bool, message: str) -> None:
    """Do not silently disable certificate checks when Python uses -O."""
    if not condition:
        raise ValueError(message)


def inverse(word: Word) -> Word:
    return [-x for x in reversed(word)]


def reduce_word(word: Iterable[int]) -> Word:
    out: Word = []
    for x in word:
        require(isinstance(x, int) and x != 0, 'invalid free-group letter')
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out


def substitute(word: Word, images: list[Word]) -> Word:
    return reduce_word(x for letter in word for x in (
        images[letter-1] if letter > 0 else inverse(images[-letter-1])))


def cyclic_reduce(word: Word) -> Word:
    word = reduce_word(word)
    while len(word) >= 2 and word[0] == -word[-1]:
        word = word[1:-1]
    return word


def free_conjugate(a: Word, b: Word) -> bool:
    a, b = cyclic_reduce(a), cyclic_reduce(b)
    if len(a) != len(b):
        return False
    return not a or any(a == b[k:] + b[:k] for k in range(len(b)))


def inverse_letters(s: str) -> str:
    return s.swapcase()[::-1]


def schreier(word: str) -> tuple[list[tuple[int, int]], int]:
    """t=b^2 a, x=b t^-2; collect x_i=t^i x t^-i and final t exponent."""
    expansion = {'a': 'TTXTTXt', 'b': 'xtt'}
    expansion.update({k.upper(): inverse_letters(v)
                      for k, v in list(expansion.items())})
    require(set(word) <= set(expansion), 'unexpected presentation generator')
    out: list[tuple[int, int]] = []
    height = 0
    for letter in ''.join(expansion[c] for c in word):
        if letter == 't':
            height += 1
        elif letter == 'T':
            height -= 1
        else:
            q = (height, 1 if letter == 'x' else -1)
            if out and out[-1] == (q[0], -q[1]):
                out.pop()
            else:
                out.append(q)
    return out, height


def normalize_kernel_word(word: str) -> tuple[Word, int, list[tuple[int, int]]]:
    raw, height = schreier(word)
    require(height == 0, 'word not in meridian kernel')
    z = raw[:]
    while len(z) >= 2 and z[0] == (z[-1][0], -z[-1][1]):
        z = z[1:-1]
    require(bool(z), 'unexpected trivial kernel word')
    shift = -min(i for i, _ in z)
    return [s * (i + shift + 1) for i, s in z], shift, raw


def exponent_vector(word: Word) -> tuple[int, ...]:
    require(all(abs(x) <= 4 for x in word), 'not a word on four generators')
    return tuple(sum((1 if x > 0 else -1) for x in word if abs(x) == i + 1)
                 for i in range(4))


def class2_mul(g: Class2, h: Class2) -> Class2:
    a, c = g
    b, d = h
    return (tuple(a[i] + b[i] for i in range(4)),
            tuple(c[k] + d[k] - a[j] * b[i]
                  for k, (i, j) in enumerate(Pairs)))


def class2_inverse(g: Class2) -> Class2:
    a, c = g
    return (tuple(-x for x in a),
            tuple(-c[k] - a[i] * a[j] for k, (i, j) in enumerate(Pairs)))


def class2_eval(word: Word) -> Class2:
    out = IDENTITY
    for x in word:
        g = BASE[abs(x)-1]
        out = class2_mul(out, g if x > 0 else class2_inverse(g))
    return out


def magnus(word: Word) -> dict[tuple[int, ...], int]:
    """Independent truncated noncommutative-polynomial implementation.

    x_i -> 1+X_i; x_i^-1 -> 1-X_i+X_i^2, ignoring degree >=3.
    It uses neither the Malcev multiplication law nor its inverse routine.
    """
    out: dict[tuple[int, ...], int] = {(): 1}
    for x in word:
        i = abs(x)-1
        factor = {(): 1, (i,): 1} if x > 0 else {(): 1, (i,): -1, (i, i): 1}
        new: dict[tuple[int, ...], int] = {}
        for a, ca in out.items():
            for b, cb in factor.items():
                if len(a) + len(b) <= 2:
                    new[a+b] = new.get(a+b, 0) + ca * cb
        out = {m: c for m, c in new.items() if c}
    return out


def normal_form_word(g: Class2) -> Word:
    a, c = g
    out: Word = []
    for i, n in enumerate(a):
        out += [i+1 if n >= 0 else -i-1] * abs(n)
    for n, (i, j) in zip(c, Pairs):
        commutator = [i+1, j+1, -i-1, -j-1]
        out += (commutator if n >= 0 else inverse(commutator)) * abs(n)
    return out


def pclean(p: Poly) -> Poly:
    return {e: c for e, c in p.items() if c}


def padd(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, 0) + c
    return pclean(out)


def pmul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] = out.get(i+j, 0) + x*y
    return pclean(out)


def shift(p: Poly, n: int) -> Poly:
    return {e+n: c for e, c in p.items()}


def fox(word: str) -> list[Poly]:
    out: list[Poly] = [{}, {}]
    eps = {'a': -3, 'b': 2}
    height = 0
    for x in word:
        name = x.lower()
        j = int(name == 'b')
        if x.islower():
            out[j] = padd(out[j], {height: 1})
            height += eps[name]
        else:
            height -= eps[name]
            out[j] = padd(out[j], {height: -1})
    return out


def charpoly(matrix: list[list[int]]) -> Poly:
    n = len(matrix)
    out: Poly = {}
    for perm in itertools.permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term: Poly = {0: sign}
        for i, j in enumerate(perm):
            entry = {0: -matrix[i][j]}
            if i == j:
                entry[1] = 1
            term = pmul(term, pclean(entry))
        out = padd(out, term)
    return out


def matmul(a: tuple[int, ...], b: tuple[int, ...], p: int = 5) -> tuple[int, ...]:
    return ((a[0]*b[0]+a[1]*b[2]) % p, (a[0]*b[1]+a[1]*b[3]) % p,
            (a[2]*b[0]+a[3]*b[2]) % p, (a[2]*b[1]+a[3]*b[3]) % p)


def matinv(a: tuple[int, ...]) -> tuple[int, ...]:
    return (a[3], -a[1] % 5, -a[2] % 5, a[0])


def finite_eval(word: str) -> tuple[int, ...]:
    values = {'a': (0, 1, 4, 2), 'b': (0, 2, 2, 3)}
    out = (1, 0, 0, 1)
    for x in word:
        v = values[x.lower()]
        out = matmul(out, v if x.islower() else matinv(v))
    return out


def run(input_path: Path) -> dict:
    started = time.perf_counter()
    data = json.loads(input_path.read_text())
    r, u, v = (data[k] for k in ('relator', 'axis_u', 'axis_v'))
    checks: list[str] = []
    def check(condition: bool, label: str) -> None:
        require(condition, label)
        checks.append(label)

    # Exact Nielsen change of variables, expressed back in the original group.
    # It is valid before imposing the relator.
    original = {'a': [1], 'b': [2]}
    t_ab = [2, 2, 1]
    x_ab = reduce_word([2] + inverse(t_ab) * 2)
    expand_tx = {'t': t_ab, 'x': x_ab}
    expand_tx.update({k.upper(): inverse(w) for k, w in list(expand_tx.items())})
    for name, formula in {'a': 'TTXTTXt', 'b': 'xtt'}.items():
        check(reduce_word(y for c in formula for y in expand_tx[c]) == original[name],
              f'Nielsen substitution for {name}')

    R, rshift, rraw = normalize_kernel_word(r)
    check(R == [-3,-1,2,-3,2,4,-3,4,-5,-3,4,-3,2], 'Schreier relator')
    check(R.count(-5) == 1 and 5 not in R and R.count(-1) == 1 and 1 not in R,
          'unique extremal generators permit Tietze elimination')
    i = R.index(-5)
    phi = [[2], [3], [4], reduce_word(R[i+1:] + R[:i])]
    j = R.index(-1)
    x0 = reduce_word(R[j+1:] + R[:j])
    phii = [[(abs(y)-1) * (1 if y > 0 else -1) for y in x0], [1], [2], [3]]
    for k in range(4):
        check(substitute(phi[k], phii) == [k+1], f'phi inverse composition {k}')
        check(substitute(phii[k], phi) == [k+1], f'inverse phi composition {k}')
    check(substitute(R, [[1],[2],[3],[4],phi[3]]) == [], 'eliminated relator freely trivial')
    columns = [exponent_vector(w) for w in phi]
    M = [[columns[j][i] for j in range(4)] for i in range(4)]
    delta = {0:1, 1:-3, 2:5, 3:-3, 4:1}
    check(charpoly(M) == delta, 'characteristic polynomial equals Delta')
    # Delta / t^2 = (t+t^-1)^2 -3(t+t^-1)+3. On |t|=1,
    # z=t+t^-1 is real and z^2-3z+3=(z-3/2)^2+3/4>0.
    z = {-1:1, 1:1}
    identity = padd(padd(pmul(z,z), {e:-3*c for e,c in z.items()}), {0:3})
    check(identity == shift(delta,-2), 'exact unit-circle exclusion identity')
    check(4*3 - 3*3 == 3, 'positive completed-square remainder numerator')

    U, ushift, uraw = normalize_kernel_word(u)
    V, vshift, vraw = normalize_kernel_word(v)
    check(U == [-1,2] and V == [-2,3,-4,-1,2,-3,2,4], 'normalized marked words')
    check(exponent_vector(U) == exponent_vector(V) == (-1,1,0,0), 'common nonzero fiber abelianization')
    check(cyclic_reduce(U) == U and cyclic_reduce(V) == V, 'both marked words cyclically reduced')
    check(not free_conjugate(U,V) and len(U) == 2 and len(V) == 8, 'free-fiber conjugacy obstruction')
    cu, cv = class2_eval(U), class2_eval(V)
    check(cu == ((-1,1,0,0),(0,0,0,0,0,0)), 'U class-two coordinates')
    check(cv == ((-1,1,0,0),(-1,1,-1,-1,2,-1)), 'V class-two coordinates')
    check(cu[0][2:] == (0,0) and cv[1][-1] == -1 and cu[1][-1] == 0,
          'central x2-x3 conjugacy obstruction')
    mu, mv = magnus(U), magnus(V)
    check(mu.get((2,3),0) == 0 and mv.get((2,3),0) == -1,
          'independent Magnus x2-x3 obstruction')
    check(mu.get((3,2),0) == 0 and mv.get((3,2),0) == 1,
          'independent Magnus x3-x2 obstruction')
    check(fox(v) == [shift(p,-2) for p in fox(u)], 'exact metabelian blindness identity')
    fr = fox(r)
    check(fr[0] == shift(pmul({0:1,1:1}, delta),-3), 'Fox relator derivative a')
    check(fr[1] == shift(pmul({0:1,1:1,2:1}, delta),-6), 'Fox relator derivative b')

    # Independent implementations agree on every word (not just reduced words)
    # through length four. This is code validation, not geometric coverage.
    alphabet = tuple(range(1,5)) + tuple(range(-4,0))
    words_tested = 0
    for length in range(5):
        for letters in itertools.product(alphabet, repeat=length):
            w = list(letters)
            c = class2_eval(w)
            require(magnus(w) == magnus(normal_form_word(c)), 'Magnus/Malcev control failed')
            require(class2_mul(c,class2_inverse(c)) == IDENTITY, 'inverse control failed')
            words_tested += 1
    check(words_tested == 4681, '4681 exhaustive short-word arithmetic controls')

    # Positive conjugacy controls; no bounded search is used to prove rejection.
    controls = [[], [1], [-2,3], [4,1,-3,2]]
    for n, h in enumerate(controls):
        w = h + U + inverse(h)
        check(free_conjugate(U,w), f'positive free-conjugacy control {n}')
        check(class2_eval(w)[1][-1] == 0, f'positive central-invariant control {n}')
    check(free_conjugate([1,2], [2,1]), 'uv/vu positive control')
    check(finite_eval(r) == (1,0,0,1), 'existing finite representation relator independently checked')
    fu, fv = finite_eval(u), finite_eval(v)
    check(fu == (2,2,1,4) and fv == (4,3,3,0), 'existing finite axis images independently checked')
    tr = lambda m: (m[0]+m[3]) % 5
    check(tr(fu) == 1 and tr(fv) == 4 and tr(matinv(fv)) == 4,
          'finite conjugacy and inverse obstruction')
    generated = {(1,0,0,1)}
    pending = [(1,0,0,1)]
    while pending:
        g = pending.pop()
        for letter in 'abAB':
            q = matmul(g,finite_eval(letter))
            if q not in generated:
                generated.add(q)
                pending.append(q)
    check(len(generated) == 120, 'finite image order 120')
    # Detect deliberate mutations of a decisive marked word and a relator.
    check(class2_eval(U)[1][-1] != cv[1][-1], 'substituting U for V removes target central witness')
    check(finite_eval(r+'a') != (1,0,0,1), 'tampered relator negative control')

    return {
        'status': 'EXACT_ALGEBRA_VERIFIED_NO_COUNTEREXAMPLE',
        'input_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python': platform.python_version(), 'platform': platform.system(),
        'seed': None, 'deterministic': True, 'seconds': time.perf_counter()-started,
        'named_checks_passed': len(checks), 'checks': checks,
        'arithmetic_control_words': words_tested,
        'schreier': {'r':rraw,'u':uraw,'v':vraw,'shifts':[rshift,ushift,vshift], 'relation':R},
        'phi': phi, 'phi_inverse': phii, 'monodromy_matrix':M,
        'characteristic_polynomial_ascending': [delta[i] for i in range(5)],
        'normalized_axes': {'U':U,'V':V,'common_abelianization':cu[0],
                            'cyclic_lengths':[len(U),len(V)]},
        'fiber_class_two': {'pair_order':Pairs,'U':cu,'V':cv,
                            'central_23_values':[cu[1][-1],cv[1][-1]]},
        'metabelian': {'fox_u':fox(u),'fox_v':fox(v),'v_over_u_shift':-2},
        'finite_recheck': {'u':fu,'v':fv,'traces':[tr(fu),tr(fv)],'image_order':len(generated)},
        'proof_dependencies': [
            'The read repository presentation and axis markings represent the intended product-disk exterior.',
            'The free-by-cyclic Tietze argument and no-unit-circle argument are supplied in REPORT.md.',
            'The local-knotting conclusion uses the meridian-amalgam retraction proved in REPORT.md.'
        ],
        'not_verified': [
            'No independent extraction of the knot group/peripherals from the original PD diagram.',
            'No new surface movie, changed-axis embedding, surgery-boundary identification, or slice disk.',
            'No nonconcordance obstruction for K0,K1 and no global nonribbon obstruction for KDG.'
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument('--input', type=Path, default=here/'inputs.json')
    parser.add_argument('--output', type=Path, default=here/'verification_results.json')
    args = parser.parse_args()
    require(not args.output.exists(), 'Refusing to overwrite an existing result; choose a fresh --output path.')
    result = run(args.input)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ('status','named_checks_passed','arithmetic_control_words','seconds')},indent=2))


if __name__ == '__main__':
    main()
