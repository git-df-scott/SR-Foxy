#!/usr/bin/env python3
"""Apply the ribbon Kh injection to the distinguished fission-tree component."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
from fusion_successors import diagram_signature
from khovanov_upper_filter import parse_poincare, euler_check, deficits


def run(a):
    out=Path(a.output);out.mkdir(exist_ok=False)
    raw=Path(a.input).read_bytes();d=json.loads(raw);assert d['complete']
    prior_raw=Path(a.prior).read_bytes();prior=json.loads(prior_raw)
    assert hashlib.sha256(Path(a.jar).read_bytes()).hexdigest()==prior['jar_sha256']
    old={diagram_signature(r['pd']):r for r in prior['runs'] if r['status']=='computed_and_euler_checked'}
    lower=next(r for r in prior['runs'] if r['name']=='K1');ranks={(i,j):n for i,j,n in lower['ranks']}
    assert euler_check(lower['pd'],ranks)['passed']
    keys=sorted({r['component_keys'][x['target_component']] for r in d['rows'] for x in r['sources']['K1'] if x['passes_necessary_any_number_of_fissions']})
    rec={'status':'COMPONENT_KH_NECESSARY_FILTER', 'parameters':vars(a),
         'input_sha256':hashlib.sha256(raw).hexdigest(),'prior_sha256':hashlib.sha256(prior_raw).hexdigest(),
         'jar_sha256':prior['jar_sha256'],'runs':[],'complete':False}
    def save():(out/'manifest.json').write_text(json.dumps(rec,indent=2)+'\n')
    lookup={}
    for number,key in enumerate(keys):
        pd=d['components'][key]['pd'];row={'key':key,'pd':pd,'name':'C'+str(number)};t=time.monotonic()
        try:
            if key in old:
                r=old[key];rawlog=(Path(a.prior).parent/(r['name']+'.log')).read_text();row['reused_log']=r['name']+'.log'
                kh=parse_poincare(rawlog);assert sorted([[i,j,n] for (i,j),n in kh.items()])==r['ranks']
            else:
                inp=out/(row['name']+'.txt');inp.write_text(row['name']+' = PD['+','.join('X['+','.join(str(k+1) for k in c)+']' for c in pd)+']\n')
                job=subprocess.run([a.java,'-Xmx2g','-Djava.awt.headless=true','-jar',a.jar,str(inp),'-ku2','-nf'],capture_output=True,text=True,timeout=60,check=True)
                rawlog=job.stdout+job.stderr;kh=parse_poincare(job.stdout)
            (out/(row['name']+'.log')).write_text(rawlog)
            row['ranks']=[[i,j,n] for (i,j),n in sorted(kh.items())];row['euler']=euler_check(pd,kh);assert row['euler']['passed']
            row['K1_deficits']=deficits(ranks,kh);row['status']='checked';row['K1_obstructed']=bool(row['K1_deficits'])
        except (ValueError,AssertionError):
            rec['status']='VALIDATION_FAILURE';rec['runs'].append(row);save();raise
        except Exception as e:row['status']='unknown';row['error']=type(e).__name__+': '+str(e)
        row['seconds']=round(time.monotonic()-t,3);lookup[key]=row;rec['runs'].append(row);save()
        print(json.dumps({k:v for k,v in row.items() if k not in ['pd','ranks','euler','key']}),flush=True)
    rec['retained_first_bands']=[];rec['excluded_first_bands']=[]
    for r in d['rows']:
        alive=[x for x in r['sources']['K1'] if x['passes_necessary_any_number_of_fissions']]
        if not alive:continue
        possible=any(not lookup[r['component_keys'][x['target_component']]].get('K1_obstructed',False) for x in alive)
        rec['retained_first_bands' if possible else 'excluded_first_bands'].append(r['first_band'])
    rec['complete']=True;save()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ['java','jar','input','prior','output']:p.add_argument(arg)
    run(p.parse_args())
