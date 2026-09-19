#!/usr/bin/env python3
"""Isolate each KnotJob invariant so slow jobs cannot hide completed values."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def run(java,jar,input_path,output,names,flags,timeout=180):
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    lines={line.split(' = ')[0]:line for line in Path(input_path).read_text().splitlines() if line.strip()}
    unknown=set(names)-lines.keys()
    if unknown:raise ValueError('Missing names: '+str(unknown))
    result={'status':'SCOPED_INVARIANT_CALCULATIONS','input':input_path,
            'input_sha256':hashlib.sha256(Path(input_path).read_bytes()).hexdigest(),
            'jar_sha256':hashlib.sha256(Path(jar).read_bytes()).hexdigest(),
            'java_version':subprocess.run([java,'-version'],capture_output=True,text=True,check=True).stderr,
            'names':names,'flags':flags,'timeout_seconds':timeout,'heap_limit':'2g','runs':[]}
    for name in names:
        path=out/(name+'.txt');path.write_text(lines[name]+'\n')
        for flag in flags:
            if not flag.startswith('-s'):raise ValueError('Only documented invariant flags allowed')
            t0=time.monotonic();row={'name':name,'flag':flag}
            cmd=[java,'-Xmx2g','-Djava.awt.headless=true','-jar',jar,str(path),flag,'-nf']
            try:
                p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
                text=p.stdout+p.stderr;row.update(status='finished' if p.returncode==0 else 'error',exit_code=p.returncode)
            except subprocess.TimeoutExpired as e:
                def dec(s):return s.decode(errors='replace') if isinstance(s,bytes) else (s or '')
                text=dec(e.stdout)+dec(e.stderr);row['status']='inconclusive_timeout'
            log=out/(name+'_'+flag.lstrip('-')+'.log');log.write_text(text)
            row.update(log=str(log),seconds=round(time.monotonic()-t0,3))
            # Finished is only process status. Preserve the actual printed values
            # separately so a missing/aborted numerical answer cannot become zero.
            row['printed_values']=[line for line in text.splitlines() if ' : ' in line]
            result['runs'].append(row)
            (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(row),flush=True)
    result['queue_complete']=True;(out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('java');p.add_argument('jar');p.add_argument('input');p.add_argument('output')
    p.add_argument('--names',nargs='+',required=True);p.add_argument('--flag',action='append',required=True)
    p.add_argument('--timeout',type=int,default=180);a=p.parse_args();run(a.java,a.jar,a.input,a.output,a.names,a.flag,a.timeout)
