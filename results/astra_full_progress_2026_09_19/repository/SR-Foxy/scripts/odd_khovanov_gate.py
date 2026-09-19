#!/usr/bin/env python3
"""Rational odd Kh necessary test; Migdail--Wehrli 2607.04018v1 Thm 8.
KnotJob returns reduced odd Kh. Reconstruct unreduced using Remark 21.
Never infer an integral or odd-prime obstruction from this theorem.
"""
from collections import Counter
import hashlib,json,subprocess,time
from pathlib import Path
from khovanov_upper_filter import parse_poincare,euler_check,deficits
import snappy

ROOT=Path(__file__).resolve().parents[1]
JAVA=ROOT.parent/'java-runtime/jdk-25.0.4.1+1-jre/Contents/Home/bin/java'
JAR=ROOT.parent/'knotjob-runtime/KnotJob/KnotJob.jar'
OUT=ROOT/'results/odd_khovanov_Q'

def parse_odd(text):
    old='Odd rational Khovanov Homology : '
    assert sum(s.startswith(old) for s in text.splitlines())==1
    return parse_poincare(text.replace(old,'Rational unreduced Khovanov Homology : '),1)

def unreduced(reduced):
    ranks=Counter()
    for (i,j),n in reduced.items():
        ranks[i,j-1]+=n;ranks[i,j+1]+=n
    return ranks

def run():
    OUT.mkdir(exist_ok=False);inputs=[];hashes={}
    for name,card in [('K0','AbeTagami_K_0_K_-1__6_3'),('K1','AbeTagami_K_1')]:
        p=ROOT/('data/knots/'+card+'.json');hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
        inputs.append((name,json.loads(p.read_text())['pd_code_snappy_0indexed']))
    inputs += [(n,snappy.Link(k).PD_code()) for n,k in [('trefoil','3_1'),('ribbon_6_1','6_1')]]
    p=ROOT/'results/nonfibered_kh_survivors.json';hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    inputs += [('J'+str(r['index']),r['endpoint_pd']) for r in json.loads(p.read_text())['candidates']]
    p=ROOT/'results/fission_ancestry_Kh/manifest.json';hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    inputs += [(r['name'],r['pd']) for r in json.loads(p.read_text())['runs'] if r['name'] in ['C2','C4']]
    rec={'source':'https://arxiv.org/html/2607.04018v1','source_status':'preprint; Theorem 8 and Remark 21',
         'coefficients':'Q','computed_flavor':'reduced odd','compared_flavor':'unreduced odd',
         'status':'NECESSARY_CONDITION_ONLY','input_hashes':hashes,'jar_sha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),
         'timeout_per_job_seconds':60,'runs':[],'complete':False}
    def save():(OUT/'manifest.json').write_text(json.dumps(rec,indent=2)+'\n')
    ranks_by_name={};save()
    for name,pd in inputs:
        file=OUT/(name+'.txt');file.write_text(name+' = PD['+','.join('X['+','.join(str(a+1) for a in c)+']' for c in pd)+']\n')
        row={'name':name,'pd':pd};start=time.monotonic()
        try:
            job=subprocess.run([str(JAVA),'-Xmx2g','-Djava.awt.headless=true','-jar',str(JAR),str(file),'-ko1','-nf'],capture_output=True,text=True,timeout=60,check=True)
            (OUT/(name+'.log')).write_text(job.stdout+job.stderr)
            red=parse_odd(job.stdout);unred=unreduced(red);ranks_by_name[name]=unred
            row.update(reduced_ranks=[[i,j,n] for (i,j),n in sorted(red.items())],unreduced_ranks=[[i,j,n] for (i,j),n in sorted(unred.items())],reduced_total=sum(red.values()),unreduced_total=sum(unred.values()),euler=euler_check(pd,unred))
            assert row['euler']['passed'],'Jones/Euler mismatch'
            if name.startswith('J'):
                row['K0_deficits']=deficits(ranks_by_name['K0'],unred);assert not row['K0_deficits'],'Known ribbon movie failed'
            if name.startswith(('J','C')):
                row['K1_deficits']=deficits(ranks_by_name['K1'],unred)
                row['K1_ribbon_predecessor_obstructed']=bool(row['K1_deficits'])
            row['status']='computed_euler_checked'
        except Exception as e:
            row.update(status='FAILED_OR_UNKNOWN',error=repr(e));rec['runs'].append(row);save();raise
        row['seconds']=round(time.monotonic()-start,3);rec['runs'].append(row);save()
        print(json.dumps({k:row[k] for k in ['name','reduced_total','unreduced_total','K1_deficits','seconds'] if k in row}),flush=True)
    rec['complete']=True;save()
if __name__=='__main__':run()
