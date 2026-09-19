#!/usr/bin/env python3
"""Optional read-only comparison of transcribed fields with a local Git checkout.
No fetch, checkout, reset, branch creation, or file modification is performed.
Usage: python verify_against_checkout.py /path/to/SR-Foxy
This checker was prepared but not run against the user's Mac checkout.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess
P=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('repo',type=Path)
a=parser.parse_args();repo=a.repo.resolve()
if not repo.is_dir():raise SystemExit('Repository path is not a directory')
d=json.loads((P/'inputs_extended.json').read_text())
def git_file(path):
    raw=subprocess.check_output(['git','-C',str(repo),'show',d['source_commit']+':'+path],stderr=subprocess.PIPE)
    return json.loads(raw),hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
c,ch=git_file(d['certificate_path']);w,wh=git_file(d['original_delta_path'])
checks={
 'certificate_blob':ch==d['certificate_blob_sha1'],
 'original_correction_blob':wh==d['original_delta_blob_sha1'],
 'boundary_relations':c['boundary_relations']==d['boundary_relations'],
 'source_relators':c['source_relators']==d['source_relators'],
 'q0_generator_words':c['boundary_arc_images']==d['q0_images'],
 'matrix_propagation':c['propagation_steps']==d['source_matrix_propagation'],
 'original_boundary_delta':w['correction_boundary_word']==d['original_boundary_delta'],
 'original_source_delta':w['correction_source_word']==d['original_source_delta'],
 'axis1':w['original_axis1']==d['axis1'],
 'axis2':w['original_axis2']==d['axis2'],
 'seam':w['seam_meridian_boundary_generator']==d['seam_meridian']}
print(json.dumps({'status':'PASS' if all(checks.values()) else 'FAIL','source_commit':d['source_commit'],'checks':checks},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
