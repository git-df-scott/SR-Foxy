#!/usr/bin/env python3
"""Try to connect a retained common-upper-bound target back to K1.

One splitting saddle then a death of a detected split unknot. A nominated
endpoint match is not a proof until its simplification and identification
are independently verified. No hit implies no nonconcordance statement.
"""
import argparse
import json
from pathlib import Path
import time
import subprocess
import sys
import snappy
from spherogram.links.bands.core import banded_links, normalize_crossing_labels
from fusion_successors import diagram_signature


def run(targets, output, count=3, moves=5000, seconds=30,include_fibered=False,length=6):
    if Path(output).exists():raise FileExistsError(output)
    entries=json.loads(Path(targets).read_text())['candidates']
    selected=[];seen=set()
    for r in entries:
        if r['hfk_check']['fibered'] and not include_fibered:continue
        key=r.get('numerical_isometry_signature') or r['diagram_signature']
        if key not in seen:selected.append(r);seen.add(key)
        if len(selected)>=count:break
    card=json.loads(Path('data/knots/AbeTagami_K_1.json').read_text())
    K=snappy.Link(card['pd_code_snappy_0indexed']);kh=K.knot_floer_homology()['ranks']
    target_sig=K.exterior().isometry_signature(of_link=True,ignore_orientation=False)
    result={'status':'BOUNDED_ENDPOINT_NOMINATION_ONLY','input_targets':targets,
            'length':length,'twists':2,'path':'shortest','simplification':'basic','include_fibered':include_fibered,
            'max_moves_per_target':moves,'seconds_per_target':seconds,'runs':[]}
    for r in selected:
        J=snappy.Link(r['endpoint_pd']);normalize_crossing_labels(J)
        n=deaths=hfk_passes=0;hits=[];unknown=[];numerical_unknown=[];t0=time.monotonic();stop='enumeration_finished';cache=set()
        for L,band in banded_links(J,2,length,'shortest'):
            n+=1;raw=L.PD_code();L.simplify('basic')
            if L.unlinked_unknot_components==1 and len(L.link_components)==1:
                deaths+=1;L.unlinked_unknot_components=0
                sig=diagram_signature(L.PD_code())
                if sig not in cache:
                    cache.add(sig)
                    try:
                        w=subprocess.run([sys.executable,str(Path(__file__).with_name('hfk_worker.py'))],input=json.dumps(L.PD_code()),capture_output=True,text=True,timeout=3,check=True)
                        h={(a,m):v for a,m,v in json.loads(w.stdout)['ranks']}
                    except Exception as e:
                        unknown.append({'band':band,'pd':L.PD_code(),'error':type(e).__name__+': '+str(e)})
                        h=None
                    if h==kh:
                        hfk_passes+=1
                        try:match=L.exterior().isometry_signature(of_link=True,ignore_orientation=False)==target_sig
                        except Exception as e:
                            numerical_unknown.append({'band':band,'pd':L.PD_code(),'error':type(e).__name__+': '+str(e)})
                            match=False
                        if match:hits.append({'start_pd':J.PD_code(),'band':band,'raw_split_pd':raw,'endpoint_pd':L.PD_code(),'certified':False})
            if n>=moves or time.monotonic()-t0>=seconds:
                stop='move_cap' if n>=moves else 'time_cap';break
        row={'source_index':r['index'],'crossings':r['crossings'],'bands_tested':n,
             'detected_split_unknot_deaths':deaths,'unique_predecessor_diagrams':len(cache),
             'K1_HFK_matches':hfk_passes,'numerical_hits':hits,'inconclusive_HFK':unknown,'inconclusive_identifications':numerical_unknown,'stop':stop,
             'seconds':round(time.monotonic()-t0,3)}
        result['runs'].append(row);Path(output).write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps(row,default=str),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('targets');p.add_argument('output');p.add_argument('--count',type=int,default=3)
    p.add_argument('--moves',type=int,default=5000);p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--include-fibered',action='store_true');p.add_argument('--length',type=int,default=6)
    a=p.parse_args();run(a.targets,a.output,a.count,a.moves,a.seconds,a.include_fibered,a.length)
