"""Convert an integral Fox boundary into explicit commutators of G' words.

All identities are finite free-word identities modulo the displayed relators.
The output describes a mapped surface, not an embedded surface or a clasper.
"""
from pathlib import Path
import json
import sympy as s

HERE = Path(__file__).parent
C = json.loads((HERE / 'short_integral.json').read_text())[1]
t = s.symbols('t')
MU = 3

def inv(w):
    return [-x for x in reversed(w)]

def reduce(w):
    stack = []
    for x in w:
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return stack

def power_mu(n):
    return ([MU] if n >= 0 else [-MU]) * abs(n)

terms = []
P = []
for ri, coefficient in enumerate(C['integral_Laurent_coefficients']):
    for monomial in s.Add.make_args(s.expand(s.sympify(coefficient))):
        coefficient, exponent = monomial.as_coeff_exponent(t)
        assert coefficient.is_Integer and exponent.is_Integer
        for _ in range(abs(int(coefficient))):
            sign = 1 if coefficient > 0 else -1
            rel = C['relators'][ri]
            if sign < 0:
                rel = inv(rel)
            term = power_mu(int(exponent)) + rel + power_mu(-int(exponent))
            terms.append({'relator': ri, 'sign': sign, 'deck_exponent': int(exponent)})
            P += term

# F(P)=F(delta). Consequently delta P^-1 has balanced Schreier letters.
# Each y_(i,k)=mu^k x_i mu^(-k-1) is in the exponent-zero subgroup.
dictionary = []
def schreier(word):
    height = 0
    result = []
    for x in word:
        k = height if x > 0 else height - 1
        if abs(x) != MU:
            pair = (abs(x), k)
            if pair not in dictionary:
                dictionary.append(pair)
            token = dictionary.index(pair) + 1
            result.append(token if x > 0 else -token)
        height += 1 if x > 0 else -1
    assert height == 0
    return reduce(result)

word = schreier(C['correction_word'] + inv(P))
balanced = word[:]
assert all(word.count(i) == word.count(-i) for i in range(1, len(dictionary)+1))
factors = []
conjugator = []
while word:
    # Extract an interleaved inverse pair. Each step removes four letters.
    pair = next(( (i,j,k,l)
        for i in range(len(word)) for k in range(i+2,len(word))
        if word[k] == -word[i]
        for j in range(i+1,k) for l in range(k+1,len(word))
        if word[l] == -word[j]), None)
    assert pair is not None
    i,j,k,l = pair
    prefix = word[:i]
    conjugator = reduce(conjugator + prefix)
    word = word[i:] + prefix
    j,k,l = j-i,k-i,l-i
    a,b = word[0],word[j]
    U,V,X,Y = word[1:j],word[j+1:k],word[k+1:l],word[l+1:]
    Z = X + V + U
    left = [a] + U + inv(Z)
    right = Z + [b] + V + U + inv(Z)
    residual = X + V + U + Y
    assert reduce(left+right+inv(left)+inv(right)+residual) == reduce(word)
    factors.append({'left': reduce(conjugator+left+inv(conjugator)),
                    'right': reduce(conjugator+right+inv(conjugator))})
    word = reduce(residual)

def expand(tokens):
    result = []
    for x in tokens:
        i, k = dictionary[abs(x)-1]
        w = power_mu(k) + [i] + power_mu(-k-1)
        result += w if x > 0 else inv(w)
    return reduce(result)

product = []
for f in factors:
    left, right = f['left'], f['right']
    product += left + right + inv(left) + inv(right)
    f['left_boundary_word'] = expand(left)
    f['right_boundary_word'] = expand(right)
assert reduce(product) == balanced
assert expand(product) == reduce(C['correction_word'] + inv(P))
for f in factors:
    for side in ('left_boundary_word', 'right_boundary_word'):
        assert sum(1 if x > 0 else -1 for x in f[side]) == 0

print(json.dumps({
    'scope': 'Explicit mapped surface only; embedded realization and response not certified',
    'meridian_generator': MU,
    'boundary_word': C['correction_word'],
    'relator_product_terms': terms,
    'relator_product_word': reduce(P),
    'schreier_generators': [{'id': n+1, 'generator': i, 'deck_exponent': k}
                           for n, (i,k) in enumerate(dictionary)],
    'balanced_schreier_word': balanced,
    'commutators': factors,
    'mapped_surface_genus_upper_bound': len(factors),
    'all_handle_loops_exponent_zero': True,
    'free_identity': 'product(commutators) = delta * inverse(relator_product)',
}, indent=2))
