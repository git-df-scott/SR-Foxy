"""Standard-library replay of the saved correction's exact free-group identity.

The module-zero assertion is checked separately by the SymPy producer.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
W=json.loads(Path(__file__).with_name('word_correction.json').read_text())
images={int(i)+1:w for i,w in C['boundary_arc_images'].items()}

def inv(w):
    return [-x for x in reversed(w)]

def evaluate(w):
    out=[]
    for letter in w:
        segment=images[letter] if letter>0 else inv(images[-letter])
        for x in segment:
            if out and out[-1]==-x:
                out.pop()
            else:
                out.append(x)
    return out

a=W['original_axis1']
b=W['corrected_axis2']
m=W['seam_meridian_boundary_generator']
# b equals m^-1 a m after applying the saved q0.
relation=[-m]+a+[m]+inv(b)
assert evaluate(relation)==[]
# Replay the correction itself against the original second axis.
assert evaluate(W['correction_boundary_word'])==W['correction_source_word']
assert evaluate(W['correction_boundary_word']+W['original_axis2'])==evaluate(b)
# Dropping a letter or reversing the conjugator must fail for these data.
assert evaluate([-m]+a+[m]+inv(b[1:]))!=[]
assert evaluate([m]+a+[-m]+inv(b))!=[]
print(json.dumps({'free_group_identity':'PASS','correction_replay':'PASS','two_mutation_rejections':'PASS','module_or_geometry_checked_by_this_script':False},indent=2))
