from pathlib import Path
import json, shutil, hashlib
P=Path(__file__).parent; Q=P/'publication';Q.mkdir(exist_ok=False)
for f in ['frontier_jet.cpp','geometry.py','validation.json']:
 shutil.copy2(P/f,Q/f)
source=json.loads((P/'source_pd.json').read_text())
from geometry import sublink
names=['ribbon61_1','ribbon61_3','ribbon61_4','KDG_1','KDG_4','KDG_4_reverse']
inputs={name:json.loads((P/(name+'.json')).read_text()) for name in names}
cert={
 'status':'EXACT_FOUR_PARALLEL_PASS_NO_COUNTEREXAMPLE',
 'base_commit':'b71a29f3193bd725d41274e52efd3c6bdaa52b04',
 'created_utc':'2026-09-17T04:23:26Z',
 'source_KDG_PD':source['KDG'],
 'source_ribbon61_PD':sublink(source['ribbon61_3_saved'],{0}),
 'source_ribbon61_description':'One component extracted from the previously saved 84-crossing three-parallel input; the original complete input was reproduced byte-for-byte with git blob SHA 00135706508cf045df4fb19f5a6f6186df156a9a.',
 'orders':{name:obj['order'] for name,obj in inputs.items()},
 'runs':{f.name:json.loads(f.read_text()) for f in P.glob('*.json') if '.exact.' in f.name or '.mod32.' in f.name},
 'target':{'crossings':288,'components':4,'zero_framed':True,'exact_quotient':106081,'normalized_Jones_nullity':3,'expected_product':390625,'difference':-284544,'difference_divided_by_32':-8892,'ribbon_obstruction':False},
 'limitations':['No SnapPy, Spherogram or Regina was available: this uses a new standalone PD/grid/frontier implementation, not the prepared runner.','The knot identity and standard-B4 disk are upstream dependencies, not independently re-proved here.','No independent full polynomial for the 288-crossing target.','A first unbounded-integer attempt was interrupted with no value; it is preserved as UNKNOWN.','Checked 128-bit integer operations throw on overflow; the successful run did not overflow.','Passing these two tests does not prove ribbonness or universal satellite-test automaticity.'],
 'next_action':'Audit how the exact fourth-parallel jet affects the existing degree-four satellite transfer gate before investing in additional degree-four patterns or a larger cable.',
}
(Q/'certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
print('certificate bytes',(Q/'certificate.json').stat().st_size)
