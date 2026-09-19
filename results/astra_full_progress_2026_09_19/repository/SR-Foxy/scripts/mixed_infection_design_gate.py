"""Exact preliminary algebra; does not construct bands, annuli, or knots."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def inverse(word):
    return [-x for x in reversed(word)]


def winding(word):
    return sum({1: -3, 2: 2}[abs(x)] * (1 if x > 0 else -1) for x in word)


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def main():
    paths = ['data/knots/AbeTagami_marked_product_scaffold.json',
             'results/annulus_group_compact.json']
    scaffold, certificate = [json.loads((ROOT / p).read_text()) for p in paths]
    group = certificate['runs'][0]['simplified']
    require(group['generators'] == ['a', 'b'], 'Unexpected group basis')
    require(all(winding(r) == 0 for r in group['relator_letters']), 'Not a homomorphism')
    peripheral = group['peripheral_letters']
    mu, u, v = peripheral[0][0], peripheral[1][1], peripheral[2][1]
    require([winding(x) for x in [mu, u, v]] == [1, 0, 0], 'Unexpected winding')
    markings = scaffold['component_markings']
    linking = scaffold['linking_matrix']
    band_sums = [sum(linking[markings['R']][markings[x]] for x in pair)
                 for pair in scaffold['proposed_mixed_pairs']]
    require(band_sums == [0, 0], 'Unexpected marked-link winding')
    words = {}
    for label, left, right in [('original', u + v, v + u),
                               ('meridian_added', u + v + mu, v + mu + u)]:
        require(reduce_word(inverse(u) + left + u) == reduce_word(right),
                'Conjugacy identity failed')
        words[label] = {'left': left, 'right': right,
                        'windings': [winding(left), winding(right)],
                        'conjugacy_by_u_verified_in_free_group': True}
    delta0 = [1, -3, 5, -3, 1]
    delta_r = multiply(delta0, delta0)
    trefoil = [1, -1, 1]
    new_delta = multiply(delta_r, multiply(trefoil, trefoil))
    require(len(delta_r) - 1 == 8 and len(new_delta) - 1 == 12, 'Unexpected span')
    require(sum(delta_r) == sum(new_delta) == 1, 'Normalization failed')
    result = {
        'status': 'NO_NEW_KNOT_OR_DISK; CONDITIONAL_INFECTION_DESIGN_GATE',
        'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
        'oriented_mixed_band_sum_windings': band_sums,
        'proposed_words_only': words,
        'polynomial_coefficients_ascending': {'target_and_R': delta_r,
                                             'winding_one_trefoil_pair': new_delta},
        'alexander_spans': {'target_and_R': 8, 'winding_one_trefoil_pair': 12},
        'topological_hypotheses_not_verified': [
            'Embedded axes realizing proposed words and forming an unlink',
            'Smooth annulus disjoint from a slice disk',
            'Infection torus incompressible in final knot exterior',
            'Fibered solid-torus pattern and nonribbon output'],
        'interpretation': 'Zero winding excludes fibered output if an infection torus survives incompressibly. Adding meridians passes winding/conjugacy algebra but changes the fixed target polynomial for a trefoil companion pair.'
    }
    destination = ROOT / 'results/mixed_infection_design_gate.json'
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checks': 'passed', 'band_sum_windings': band_sums,
                      'alexander_spans': result['alexander_spans']}))


if __name__ == '__main__':
    main()
