#!/usr/bin/env python3
"""Manual audit: re-verify every knot data card in the repo from its PD code alone.
Nothing is trusted from an agent report; every number below is recomputed here."""
import json, glob, sys, snappy, sympy as sp
t = sp.symbols('t')
rows = []
for f in sorted(glob.glob('data/knots/*.json')):
    d = json.load(open(f))
    pd = d.get('pd_code_snappy_0indexed') or d.get('pd_code')
    name = d.get('name', f)
    if not pd or not isinstance(pd, list) or not pd or not isinstance(pd[0], (list, tuple)):
        rows.append((name, 'NO PD', '', '', '', '', '')); continue
    try:
        K = snappy.Link([tuple(c) for c in pd])
    except Exception as e:
        rows.append((name, f'PD INVALID: {e}', '', '', '', '', '')); continue
    n = len(K.crossings); comps = len(K.link_components)
    try:
        h = K.knot_floer_homology() if n <= 60 else None
    except Exception:
        h = None
    g = h['seifert_genus'] if h else '?'
    fib = h['fibered'] if h else '?'
    tau = h['tau'] if h else '?'
    try:
        E = K.exterior(); E.simplify(); vol = round(E.volume(), 6); sol = E.solution_type()[:9]
    except Exception:
        vol, sol = '?', '?'
    rows.append((name, n, comps, g, fib, tau, f'{vol} {sol}'))
w = max(len(str(r[0])) for r in rows)
print(f'{"knot".ljust(w)}  cr  comp  genus  fib   tau  volume')
for r in rows:
    print(f'{str(r[0]).ljust(w)}  {r[1]}  {r[2]}  {r[3]}  {r[4]}  {r[5]}  {r[6]}')
