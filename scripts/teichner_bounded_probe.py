#!/usr/bin/env python3
"""Bounded, checkpointed Teichner sum probe, with separate partner verification."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path

def worker(a):
    import snappy
    import snappy.sage_helper as sh
    assert sh._within_sage
    import spherogram.links.bands.search as search
    from teichner_certify import certificate_status  # installs conservative split-link filter
    from colored_link_rank import check
    # Native multivariate Fox-Milnor minors segfaulted on this runtime.
    # Use only a necessary generic-rank condition; deficient evaluations
    # are retained, never labeled slice. No environment/library files change.
    def conservative_filter(L):
        m=len(L.link_components)+L.unlinked_unknot_components
        if not search.linking_nums_all_zero(L):return False
        for values,prime in [([2]*m,101),([3]*m,103)]:
            c=check(L,values,prime)
            if c['specialized_H1_dimension']<m-1:return False
        return True
    search.could_be_strongly_slice=conservative_filter
    source=Path('data/knots/AbeTagami_D_0_1.json');raw=source.read_bytes();D=json.loads(raw)
    K=snappy.Link(D.get('pd_code_snappy_0indexed') or D['pd_code']);J=snappy.Link(a.partner)
    out=Path(a.output);assert not out.exists()
    rec={'status':'RUNNING','complete':False,'partner':a.partner,'source_sha256':hashlib.sha256(raw).hexdigest(),'parameters':vars(a),'bands_generated':0,'certified_slice':False,'limitations':'Timeout or a negative bounded search gives no nonsliceness conclusion. Certificates replayed with the same library.'}
    rec['filter']='Zero linking and specialized Alexander H1 dimension upper bound; no native Fox-Milnor minors. Retained links are unknown.'
    def save():out.write_text(json.dumps(rec,indent=2,default=str)+'\n')
    save();p=search.ribbon_concordant_links(J,max_bands=1,max_twists=2,max_band_len=6,certify=True)
    assert certificate_status(J,p),'Partner ribbonness not verified'
    rec.update(partner_ribbon_verified=True,partner_certificate=p['unknot'],partner_pd=J.PD_code());save()
    S=K.connected_sum(J);S.simplify('global');rec.update(sum_pd=S.PD_code(),sum_crossings=len(S.crossings));save()
    original=search.banded_links
    def observed(*args,**kw):
        for L,spec in original(*args,**kw):
            rec['bands_generated']+=1
            if rec['bands_generated']%100==0:save()
            yield L,spec
    search.banded_links=observed
    result=search.ribbon_concordant_links(S,max_bands=a.bands,max_twists=2,max_band_len=a.length,certify=True)
    rec['surviving_final_links']=len(result);rec['frontier_certificates']=[v for k,v in result.items() if k!='unknot']
    if 'unknot' in result:
        rec['sum_certificate']=result['unknot'];rec['sum_ribbon_verified']=certificate_status(S,result)
        rec['certified_slice']=bool(rec['sum_ribbon_verified'] and rec['partner_ribbon_verified'])
    rec.update(status='CERTIFICATE_FOUND' if rec['certified_slice'] else 'BOUNDED_SEARCH_NO_CERTIFICATE',complete=True);save()

def main(a):
    if a.worker:return worker(a)
    out=Path(a.output);assert not out.exists();start=time.monotonic()
    with out.with_suffix('.log').open('w') as log:
        p=subprocess.Popen([sys.executable,__file__,a.partner,a.output,'--bands',str(a.bands),'--length',str(a.length),'--worker'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:code=p.wait(timeout=a.seconds)
        except subprocess.TimeoutExpired:
            import signal
            os.killpg(p.pid,signal.SIGTERM);p.wait(timeout=10);code=None
    rec=json.loads(out.read_text()) if out.exists() else {'certified_slice':False,'complete':False}
    rec['elapsed_seconds']=round(time.monotonic()-start,3);rec['exit_code']=code;rec['wall_time_limit_seconds']=a.seconds
    if code is None:rec.update(status='TIMEOUT_UNKNOWN',complete=False)
    elif code!=0:rec.update(status='WORKER_FAILURE_UNKNOWN',complete=False)
    out.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps({k:v for k,v in rec.items() if k in ['status','partner','bands_generated','certified_slice','elapsed_seconds']}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('partner');p.add_argument('output');p.add_argument('--bands',type=int,default=2);p.add_argument('--length',type=int,default=6);p.add_argument('--seconds',type=int,default=180);p.add_argument('--worker',action='store_true');main(p.parse_args())
