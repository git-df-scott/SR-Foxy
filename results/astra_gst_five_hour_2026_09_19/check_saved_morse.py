from pathlib import Path
import json,regina
from spherogram.links.exhaust import MorseEncoding
p=Path(__file__).parent;d=p/'suzuki_mixed/GST3_c0';r=json.loads((d/'TAYLOR_INTEGER_SEEDED_RESULT.json').read_text());pd=json.loads((d/'TAYLOR_INPUT_PD.json').read_text());L=MorseEncoding(r['morse_events']).link();A=regina.Link.fromPD([[v+1 for v in row] for row in pd]);B=regina.Link.fromPD([[v+1 for v in row] for row in L.PD_code()]);sa=A.sig(False,True,True);sb=B.sig(False,True,True);assert sa==sb
(d/'MORSE_DIAGRAM_CHECK.json').write_text(json.dumps({'input_pd':pd,'reconstructed_pd':L.PD_code(),'same_diagram_signature_up_to_rotation_reversal_and_component_permutation':True,'signature':sa,'mirror_allowed':False},indent=2)+'\n');print('Saved Morse events reproduce the input diagram signature; no reflection allowed.')
