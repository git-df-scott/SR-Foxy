"""Bounded compact GST3 contraction; preserve prior resource-limit failure."""
from pathlib import Path
import json,time,hashlib
from compact_taylor import probe
p=Path(__file__).resolve().parent
d=p/'gst3_order8/double'
assert (p/'COMPACT_CONTROLS.json').exists()
target=d/'RESULT_COMPACT.json';assert not target.exists()
inp=json.loads((d/'INPUT.json').read_text())
lay=json.loads((d/'LAYOUT.json').read_text())
last={};start=time.monotonic()
def progress(r):
    last.update(r)
    (d/'PROGRESS_COMPACT.json').write_text(json.dumps(r,indent=2)+'\n')
try:
    result=probe(inp['pd'],lay['events'],inp['missing_unknots'],progress=progress)
    result['status']='complete'
except Exception as exc:
    result={'status':'inconclusive','error':repr(exc),'last_progress':last,'seconds':time.monotonic()-start}
result['input_sha256']=hashlib.sha256((d/'INPUT.json').read_bytes()).hexdigest()
target.write_text(json.dumps(result,indent=2)+'\n')
print(result,flush=True)
