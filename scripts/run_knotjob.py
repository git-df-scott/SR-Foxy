#!/usr/bin/env python3
"""Run author-distributed KnotJob on saved PD input, one timed process per knot."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def run(java,jar,input_path,output_dir,timeout=120,profile='basic'):
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    profiles={'basic':['-s0','-s2','-s3','-sqo','-sqe','-scr','-sbls3'],
              'higher':['-sq2e','-sq2o0','-sq2o1','-sgr','-sbls15'],
              'sl3':['-sl0','-sl2','-sl3']}
    flags=profiles[profile]+['-nf']
    result={'status':'KNOTJOB_COMPUTATIONAL_CHECK','input':input_path,'flags':flags,
            'jar_sha256':hashlib.sha256(Path(jar).read_bytes()).hexdigest(),
            'java_version':subprocess.run([java,'-version'],capture_output=True,text=True,check=True).stderr,
            'source':'https://www.maths.dur.ac.uk/users/dirk.schuetz/knotjob.html',
            'timeout_per_knot_seconds':timeout,'profile':profile,'runs':[]}
    for line in Path(input_path).read_text().splitlines():
        name=line.split(' = ')[0]
        # Exclude the 41- and 47-crossing K2/D02 inputs from this bounded pass;
        # their input diagrams are preserved for the larger follow-up session.
        if name in ['AbeTagami_K_2','AbeTagami_D_0_2']:continue
        path=out/(name+'.txt');path.write_text(line+'\n')
        t0=time.monotonic();row={'name':name,'input':str(path)}
        command=[java,'-Xmx4g','-Djava.awt.headless=true','-jar',jar,str(path),*flags]
        try:
            p=subprocess.run(command,capture_output=True,text=True,timeout=timeout)
            text=p.stdout+p.stderr;row.update(exit_code=p.returncode,status='finished' if p.returncode==0 else 'error')
        except subprocess.TimeoutExpired as e:
            def decode(s):return s.decode(errors='replace') if isinstance(s,bytes) else (s or '')
            text=decode(e.stdout)+decode(e.stderr);row.update(status='inconclusive_timeout')
        log=out/(name+'.log');log.write_text(text)
        row.update(seconds=round(time.monotonic()-t0,3),log=str(log))
        result['runs'].append(row);(out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(row),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('java');p.add_argument('jar');p.add_argument('input');p.add_argument('output_dir')
    p.add_argument('--timeout',type=int,default=120);p.add_argument('--profile',choices=['basic','higher','sl3'],default='basic')
    a=p.parse_args();run(a.java,a.jar,a.input,a.output_dir,a.timeout,a.profile)
