#!/usr/bin/env python3
"""Herald-Kirk-Livingston / Casson-Gordon slice obstruction (Dunfield-Gong implementation in SnapPy 3.3, Sage only).
Usage: python3 hkl_obstruction.py <knot.json> <out.json>
A nonzero result proves the knot is not topologically slice (hence not smoothly slice)."""
import json, sys, time, snappy
import snappy.sage_helper as sh; assert sh._within_sage
d=json.load(open(sys.argv[1])); pd=d.get('pd_code_snappy_0indexed') or d['pd_code']
M=snappy.Link([tuple(c) for c in pd]).exterior()
t=time.time()
spec=[(10,[0,20]),(20,[0,10])]
try:
    res=M.slice_obstruction_HKL(spec, method='basic', verbose=False)
except Exception as e:
    res=f'error: {e}'
out={'knot':d['name'],'spec':spec,'method':'basic','result':str(res),'seconds':round(time.time()-t,1),'meaning':'None = no obstruction found in this spec; (p,q) = NOT topologically slice'}
json.dump(out,open(sys.argv[2],'w'),indent=1); print(out)
