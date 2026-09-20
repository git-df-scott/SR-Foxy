import sys,json,snappy
from pathlib import Path
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'));from bounded_root_jet import probe
rows=[]
for name,pd,prod,expected in [('known_ribbon_L10n36',snappy.Link('L10n36').PD_code(),9,False),('square_pair_nonribbon',json.loads((p/'SQUARE_PAIR_NONRIBBON_CONTROL.json').read_text())['pd'],81,True),('provisional_n3',json.loads((p/'RECONSTRUCTED_n3.json').read_text())['pd'],81,False)]:
 a=probe(snappy.Link(pd),prod);assert a['ribbon_obstructed_mod_32']==expected;a['name']=name;rows.append(a);print(name,a['quotient_at_i_mod_32'],a['ribbon_obstructed_mod_32'],a['max_retained_states'],flush=True)
(p/'ROOT_JET_CONTROLS.json').write_text(json.dumps(rows,indent=2)+'\n')
