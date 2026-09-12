#!/usr/bin/env python3
"""Recompute/recheck Seifert reductions of the stored Abe--Tagami diagrams."""
import argparse
import json
from pathlib import Path
import sympy as s
import snappy
from audit_seifert_model import reduce_matrix


def run(output):
    result = {}
    for name in ['AbeTagami_K_0_K_-1__6_3','AbeTagami_K_1','AbeTagami_K_2']:
        d=json.loads(Path('data/knots/'+name+'.json').read_text())
        raw=snappy.Link(d['pd_code_snappy_0indexed']).seifert_matrix()
        original=s.Matrix(raw.tolist() if hasattr(raw,'tolist') else list(map(list,raw.rows())))
        V,steps=reduce_matrix(original)
        result[name]={'original_matrix':original.tolist(),'reduced_matrix':V.tolist(),'steps':steps}
    out=Path(output)
    if out.exists():
        old=json.loads(out.read_text())
        for name,d in result.items():
            assert old[name]['reduced_matrix']==json.loads(json.dumps(d['reduced_matrix'],default=int))
        print('Recomputed all three reduced matrices; existing data matched.')
    else:
        out.write_text(json.dumps(result,indent=2,default=int)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();run(a.output)
