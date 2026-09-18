"""Check recipe against independently replayed commutators, not geometry."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'results/night_2026_09_18_surface/surface_certificate.json'
replay = subprocess.run([sys.executable, str(INPUT.with_name('check_surface.py'))],
                        check=True, capture_output=True, text=True)
source = json.loads(INPUT.read_text())

def free(word):
    stack = []
    for x in word:
        if stack and stack[-1] == -x:
            stack.pop()
        else:
            stack.append(x)
    return stack

def check(d):
    assert d['source_sha256'] == hashlib.sha256(INPUT.read_bytes()).hexdigest()
    assert d['boundary_correction'] == source['boundary_word']
    assert d['genus'] == len(source['commutators']) == 13
    assert len(d['handles']) == 26
    count = 0
    for j, c in enumerate(source['commutators']):
        for k, (label, key) in enumerate([('u', 'left_boundary_word'), ('v', 'right_boundary_word')]):
            h = d['handles'][2*j+k]
            assert h['handle'] == f'{label}{j+1}'
            assert h['target_boundary_word'] == c[key]
            assert sum(1 if x > 0 else -1 for x in c[key]) == 0
            current = []
            for x in h['left_insertion_sequence']:
                assert 1 <= abs(x) <= 9
                current = free([x] + current)
                count += 1
            assert current == free(c[key])
    assert count == d['disk_push_upper_bound'] == 614
    assert d['geometric_coordinates_certified'] is False

d = json.loads(Path(__file__).with_name('surface_recipe.json').read_text())
check(d)
bad = copy.deepcopy(d)
bad['handles'][18]['left_insertion_sequence'].reverse()
try:
    check(bad)
except AssertionError:
    pass
else:
    raise AssertionError('incorrect multiplication order survived')
print(json.dumps({'upstream_free_word_checker': json.loads(replay.stdout),
    'handle_instruction_replay': 'PASS', 'handles': 26, 'disk_push_upper_bound': 614,
    'wrong_multiplication_order_rejected': True,
    'scope': 'Algebraic inputs only; geometric proof is in research/42'}, indent=2))
