from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];g={};exec((ROOT/'results/chat_archive_2026_09_17/expanded/SR_Foxy_pass09_product_collar_2026_09_17/pass09_product_collar/diagram_core.py').read_text(),g)
A=g['adjacency_from_pd'](g['SCAFFOLD']);qb=g['quotient_R_wirtinger'](A)
D=g['add_zero_twist_band'](g['add_zero_twist_band'](A,g['BAND1']),g['BAND2']);q=g['quotient_R_wirtinger'](D);mp=g['map_final_R_arcs_to_scaffold'](qb,q)
for comp in (1,2):
 cur=min(q['components'][comp]);seen=set();rows=[]
 while cur not in seen:
  seen.add(cur);c,p=cur;word=[]
  if p in (0,2) and q['cmap'][c,1]==0:word=[(mp[q['arcs'][c,1]]+1)*q['signs'][c]]
  rows.append({'port':cur,'side':'upper' if c<27 else 'lower' if c<54 else 'band','word':word});cur=D[c][(p+2)%4]
 print(json.dumps({'comp':comp,'segments':rows}))
