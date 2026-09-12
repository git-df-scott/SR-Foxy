#!/usr/bin/env python3
"""Validate the resumed session's records and freeze a provenance manifest.

Run before committing: includes changed/untracked session files, plus explicit
unchanged mathematical inputs. Does not rerun expensive searches. A successful
integrity check is not a formal verification of the underlying topology.
"""
import argparse,datetime,gzip,hashlib,importlib.metadata,json,subprocess
from pathlib import Path


def read(name):return json.loads(Path(name).read_text())
def sha(name):return hashlib.sha256(Path(name).read_bytes()).hexdigest()


def run(output):
    out=Path(output)
    if out.exists():raise FileExistsError(out)
    archives=[]
    for path in sorted(Path('results').glob('coupled*.jsonl.gz')):
        counts={};header=last=None
        with gzip.open(path,'rt') as f:
            for line in f:
                row=json.loads(line);counts[row['type']]=counts.get(row['type'],0)+1
                if header is None:header=row
                last=row
        assert header['type']=='header' and last['type']=='summary'
        assert last['moves']==counts.get('move',0)
        assert last['first_bands']==counts.get('first',0)
        archives.append({'path':str(path),'sha256':sha(path),'counts':counts,'summary':last})
    assert sum(r['summary']['moves'] for r in archives)==33792
    audits=[read('results/'+name+'_audit.json') for name in ['coupled_K0_batch1','coupled_K1_batch1','coupled_K0_double_return','coupled_K1_double_return']]
    for d in audits:assert d['complete'] and sha(d['archive'])==d['sha256']
    assert sum(d['replayed_moves'] for d in audits)==32768
    assert sum(d['summary']['checked'] for d in audits)==2518
    assert sum(d['summary']['computed'] for d in audits)==2436
    assert sum(d['summary']['inconclusive'] for d in audits)==82
    assert sum(d['summary']['source_failures'] for d in audits)==0
    comparison=read('results/coupled_return_frontier_comparison.json')
    assert comparison['counts']==[267,1962] and not comparison['matches']
    for name,h in comparison['inputs_sha256'].items():assert sha(name)==h,name
    inv=read('results/involutive_structure_independent_check_v2.json')
    assert sha(inv['audit'])==inv['sha256'] and inv['full_iota_projection_cases_checked']==4096
    assert inv['mixed_gauges_checked']==256
    for d in read('results/fox_goeritz_independent_check.json')['records']:
        assert sha(d['input'])==d['sha256']
        assert d['all_lines_same_isotropy'] and all(r['verified'] for r in d['norm_certificates'])
    tap=read('results/fox_goeritz_D01_all.json')
    assert tap['complete'] and len(tap['results'])==14
    assert [r['line'] for r in tap['results'] if r['isotropic']]==[[1,3],[1,8]]
    assert all(r['norm'] for r in tap['results'] if r['isotropic'])
    torsion=read('results/torsion_order_final_check.json')
    assert {r['name']:r['torsion_order'] for r in torsion['knots']}=={'6_3':1,'6_1':1,'8_19':2,'K1':1,'J149':1,'18nh00000601':1,'K_B_0friend':1,'GST_knot':2}
    assert all(r['localized_homology_rank']==1 for r in torsion['knots'])
    for family in ['fast','sq2','sl3_v2']:
        d=read('results/resumed_knotjob_'+family+'/manifest.json');assert d['queue_complete']
    for family in ['higher','higher_direct']:
        d=read('results/resumed_hkl_'+family+'/manifest.json');assert d['complete']
        assert all(r['status']=='finished' and r['result']['result'] is None for r in d['jobs'])
    reverse=read('results/two_fission_J149.json');assert reverse['complete']
    assert any('K0' in r.get('numerical_source_matches',[]) for r in reverse['hits'])
    assert not any('K1' in r.get('numerical_source_matches',[]) for r in reverse['hits'])
    regression=Path('results/resumed_regression_tests.log').read_text()
    assert 'Ran 7 tests' in regression and '\nOK\n' in regression
    names=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'))
    names.update(subprocess.check_output(['git','diff','--name-only','HEAD','-z']).decode().split('\0'))
    names.update(['data/knots/AbeTagami_K_0_K_-1__6_3.json','data/knots/AbeTagami_K_1.json','data/knots/AbeTagami_D_0_1.json','results/chain_map_filter_wider.json'])
    files=[];compiled=parsed=0
    for name in sorted(names):
        p=Path(name)
        if not name or p==out or not p.is_file():continue
        if p.suffix=='.py':compile(p.read_text(),name,'exec');compiled+=1
        if p.suffix=='.json':read(name);parsed+=1
        files.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
    versions={n:importlib.metadata.version(n) for n in ['snappy','spherogram','regina','knot_floer_homology','passagemath-standard']}
    result={'status':'SESSION_RECORD_INTEGRITY_CHECK_PASSED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'base_commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
      'branch':subprocess.check_output(['git','branch','--show-current']).decode().strip(),
      'versions':versions,'compiled_python_files':compiled,'parsed_json_files':parsed,
      'archives':archives,'reverse_search_summary':{k:v for k,v in reverse.items() if not isinstance(v,list)},
      'files':files,'limitations':'Record integrity and computational checks; no smooth slice disk or counterexample certified.'}
    assert result['branch']=='main'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ('archives','files','reverse_search_summary')})
    print('files',len(files),'bytes',sum(r['bytes'] for r in files))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
