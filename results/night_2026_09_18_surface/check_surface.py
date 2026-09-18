"""Independent standard-library verification of the mapped-surface certificate.

No Fox derivatives, Laurent algebra, SymPy, or group-word oracle is needed.
"""
from pathlib import Path
import copy
import json

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
C = json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
W = json.loads((ROOT/'results/night_2026_09_18/word_correction.json').read_text())
RELS = [[-sg*(b+1), i+1, sg*(b+1), -(o+1)] for i,o,b,sg,c in C['boundary_relations']]

def inverse(word):
    return [-x for x in word[::-1]]

def free(word):
    result = []
    for x in word:
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return result

def check(short, surface):
    reached = {1}
    for _ in range(18):
        for r in RELS:
            assert len(r) == 4 and r[0] == -r[2] and r[1] > 0 and r[3] < 0
            if r[1] in reached or -r[3] in reached:
                reached.update((r[1],-r[3]))
    assert reached == set(range(1,19))  # Abelianization is exactly Z.
    assert short['initial_word'] == W['correction_boundary_word']
    word = short['initial_word'][:]
    for step in short['steps']:
        at = step['at']
        if step['type'] == 'free':
            assert word[at:at+2] == step['letters']
            assert word[at] == -word[at+1]
            word[at:at+2] = []
        else:
            rel = RELS[step['relator']]
            assert step['sign'] in (1,-1)
            if step['sign'] == -1:
                rel = inverse(rel)
            n = step['rotation']
            rel = rel[n:]+rel[:n]
            left,right = rel[:step['cut']],inverse(rel[step['cut']:])
            assert step['from'] == left and step['to'] == right
            assert word[at:at+len(left)] == left
            word[at:at+len(left)] = right
    assert word == short['final_word'] == surface['boundary_word']
    mu = surface['meridian_generator']
    assert 1 <= mu <= 18
    P = []
    for term in surface['relator_product_terms']:
        rel = RELS[term['relator']]
        assert term['sign'] in (-1,1)
        if term['sign'] == -1:
            rel = inverse(rel)
        k = term['deck_exponent']
        conjugator = ([mu] if k >= 0 else [-mu])*abs(k)
        P += conjugator + rel + inverse(conjugator)
    assert free(P) == surface['relator_product_word']
    product = []
    for factor in surface['commutators']:
        a,b = factor['left_boundary_word'],factor['right_boundary_word']
        for loop in (a,b):
            assert all(type(x) is int and 1 <= abs(x) <= 18 for x in loop)
            assert sum(1 if x > 0 else -1 for x in loop) == 0
        product += a+b+inverse(a)+inverse(b)
    # Direct free equality is stronger than reusing the producer's Schreier check.
    assert free(product+P) == free(word)
    assert len(surface['commutators']) == surface['mapped_surface_genus_upper_bound']

short = json.loads((HERE/'short_boundary.json').read_text())
surface = json.loads((HERE/'surface_certificate.json').read_text())
check(short,surface)
bad = copy.deepcopy(surface)
bad['commutators'][0]['left_boundary_word'].append(1)
try:
    check(short,bad)
except AssertionError:
    pass
else:
    raise AssertionError('altered handle loop accepted')
bad = copy.deepcopy(surface)
bad['relator_product_terms'][0]['sign'] *= -1
try:
    check(short,bad)
except AssertionError:
    pass
else:
    raise AssertionError('altered relator sign accepted')
print(json.dumps({'boundary_rewrite_steps_verified':len(short['steps']),
                  'boundary_word_length':len(short['final_word']),
                  'commutator_identity':'PASS: literal free reduction',
                  'handle_loops_in_exponent_zero_subgroup':2*len(surface['commutators']),
                  'mapped_genus_upper_bound':len(surface['commutators']),
                  'mutation_controls_rejected':2},indent=2))
