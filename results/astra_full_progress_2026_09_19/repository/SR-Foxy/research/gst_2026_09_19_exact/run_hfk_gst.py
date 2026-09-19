import json,time,resource
from pathlib import Path
ROOT=Path(__file__).parent
resource.setrlimit(resource.RLIMIT_AS,(7*1024**3,7*1024**3))
import spherogram
K=spherogram.Link(json.load(open(ROOT/'gst48.json'))['pd']);a=time.time()
print('Starting GST48 HFK',flush=True)
r=K.knot_floer_homology()
r['ranks']=[{'A':a,'M':m,'rank':v} for (a,m),v in sorted(r['ranks'].items())]
r['elapsed_seconds']=time.time()-a
json.dump(r,open(ROOT/'gst48_hfk.json','w'),indent=2)
print(json.dumps(r),flush=True)
