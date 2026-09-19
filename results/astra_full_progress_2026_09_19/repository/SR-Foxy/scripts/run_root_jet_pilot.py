#!/usr/bin/env python3
"""Serial root-jet cable pilot; time/memory failures remain unknown."""
import hashlib,json,os
from pathlib import Path
import subprocess,sys,time
import snappy
from cable import cable_braid


def run(directory):
    out=Path(directory);out.mkdir(parents=True,exist_ok=False)
    card=Path('data/knots/18nh00000601.json')
    K=snappy.Link(json.loads(card.read_text())['pd_code_snappy_0indexed'])
    rec={'input_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),
         'jet_script_sha256':hashlib.sha256(Path('scripts/jones_root_jet.py').read_bytes()).hexdigest(),
         'scope':'Necessary Eisermann conditions mod 32 only. Zero residue is inconclusive. No verified counterexample.',
         'runs':[],'complete':False}
    for name,knot,p,det in [('trefoil_3parallel',snappy.Link('3_1'),3,-3),
                            ('ribbon61_3parallel',snappy.Link('6_1'),3,9),
                            ('KDG_2parallel',K,2,25),('KDG_3parallel',K,3,25)]:
        bw=knot.braid_word();w=sum(1 if a>0 else -1 for a in bw)
        cw,ns=cable_braid(bw,max(abs(a) for a in bw)+1,p,0,w)
        link=snappy.Link(braid_closure=cw);link.simplify('basic')
        assert len(link.link_components)==p and link.is_planar()
        linking=[[int(x) for x in r] for r in link.linking_matrix()]
        assert all(x==0 for r in linking for x in r)
        payload={'pd':link.PD_code(),'expected_product':det**p}
        inputfile=out/(name+'.input.json');inputfile.write_text(json.dumps(payload)+'\n')
        row={'name':name,'p':p,'crossings':len(link.crossings),'braid_writhe':w,
             'linking_matrix':linking,'status':'UNKNOWN','timeout_seconds':45,'rss_limit_mib':1024}
        start=time.monotonic();reason=None
        with inputfile.open() as inp, (out/(name+'.output.json')).open('w') as stdout, (out/(name+'.stderr.log')).open('w') as stderr:
            process=subprocess.Popen([sys.executable,'scripts/jones_root_jet.py'],stdin=inp,stdout=stdout,stderr=stderr)
            while process.poll() is None:
                rss=subprocess.run(['ps','-o','rss=','-p',str(process.pid)],capture_output=True,text=True).stdout.strip()
                if time.monotonic()-start>45 or int(rss or 0)>1024*1024:
                    reason='TIME_OR_MEMORY_LIMIT_UNKNOWN';process.kill();process.wait();break
                time.sleep(.5)
        row.update(seconds=round(time.monotonic()-start,3),exit_code=process.returncode)
        if reason:row['status']=reason
        elif process.returncode:row['status']='ERROR_UNKNOWN'
        else:
            row['result']=json.loads((out/(name+'.output.json')).read_text());row['status']='COMPUTED'
        rec['runs'].append(row);(out/'manifest.json').write_text(json.dumps(rec,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if name=='ribbon61_3parallel' and (row['status']!='COMPUTED' or row['result']['ribbon_obstructed_mod_32']):
            rec['blocked_by_control']=True;break
        if name.startswith('KDG') and row.get('result',{}).get('ribbon_obstructed_mod_32'):
            rec['candidate_requires_independent_verification']=True;break
    rec['complete']=True;(out/'manifest.json').write_text(json.dumps(rec,indent=2)+'\n')


if __name__=='__main__':run(sys.argv[1])
