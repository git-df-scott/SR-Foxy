"""Finite handle instructions for research/42; not a geometric PD certificate."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'results/night_2026_09_18_surface/surface_certificate.json'
source = json.loads(INPUT.read_text())
handles = []
for j, c in enumerate(source['commutators'], 1):
    for label, key in [('u', 'left_boundary_word'), ('v', 'right_boundary_word')]:
        word = c[key]
        assert sum(1 if x > 0 else -1 for x in word) == 0
        handles.append({'handle': f'{label}{j}', 'target_boundary_word': word,
                        'left_insertion_sequence': word[::-1]})
print(json.dumps({
    'scope': 'Finite algebraic instructions for the geometric proof in research/42; no marked diagram',
    'source_path': str(INPUT.relative_to(ROOT)),
    'source_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    'genus': len(source['commutators']),
    'boundary_correction': source['boundary_word'],
    'initial_handle_words': 'all trivial; old zero-framed boundary collar fixed',
    'based_boundary_convention': 'b_prime = [u1,v1] ... [ug,vg] b',
    'disk_push_rule': 'left-multiply the selected handle by the signed based Wirtinger meridian',
    'handles': handles,
    'disk_push_upper_bound': sum(len(h['left_insertion_sequence']) for h in handles),
    'geometric_coordinates_certified': False,
}, indent=2))
