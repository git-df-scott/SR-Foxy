import json,time
from pathlib import Path
import regina
from spherogram import Link
P=Path(__file__).parent;start=time.monotonic()
V=json.loads((P/'GST_SEIFERT_MATRIX.json').read_text());pd=json.loads((P/'gst48.json').read_text())['pd']
fresh=[list(r) for r in Link(pd).seifert_matrix()]
assert fresh==V
j=json.loads((P/'GST_COVER11_PADIC.json').read_text());M=regina.MatrixInt(j['presentation_matrix'])
regina.smithNormalForm(M)
diag=[int(str(M.entry(i,i))) for i in range(M.rows())];factors=[x for x in diag if x!=1]
assert factors==j['nonunit_invariant_factors']==[1849,1849]
out={'status':'PASS','fresh_seifert_matrix_equal':True,'method':'Regina exact integer Smith normal form, independent of p-adic elimination','smith_diagonal':diag,'seconds':time.monotonic()-start}
(P/'GST_COVER11_REGINA_CHECK.json').write_text(json.dumps(out,indent=2));print(out)
