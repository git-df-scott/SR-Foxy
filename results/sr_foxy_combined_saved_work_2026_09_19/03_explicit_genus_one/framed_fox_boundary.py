#!/usr/bin/env python3
"""Exact framed peripheral/Fox data of the saved polygonal surgery link.
Only integer Laurent-unit pivots are used before a small rational solve.
No isometry tests or numerical knot-invariant values enter the answer.
"""
import json,time,hashlib,signal,sys
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent

def red(w):
 ans=[]
 for x in w:
  if ans and ans[-1]==-x:ans.pop()
  else:ans.append(x)
 return ans

def build(words):
 cross={};N=0;mers=[];weights={};comps={};under_words=[];selfwr=[]
 # All component indices are fixed: R=0, a=1, b'=2.
 owners={k:[] for w in words for k,typ,s in w}
 for ci,w in enumerate(words):
  for k,typ,s in w:owners[k].append(ci)
 for ci,w in enumerate(words):
  n=sum(typ=='U' for k,typ,s in w);n=max(n,1);start=N+1;N+=n;cur=start;mers.append(start)
  for g in range(start,N+1):weights[g]=int(ci==0);comps[g]=ci
  for k,typ,s in w:
   cross.setdefault(k,{'sign':s})
   if cross[k]['sign']!=s:raise ValueError('inconsistent crossing sign')
   if typ=='O':cross[k]['over']=cur
   else:
    nxt=start+(cur-start+1)%n;cross[k]['in']=cur;cross[k]['out']=nxt;cur=nxt
 rels=[]
 for k,c in sorted(cross.items()):
  b=c['over'];s=c['sign'];rels.append([-s*b,c['in'],s*b,-c['out']])
 longs=[];linking=[]
 for ci,w in enumerate(words):
  wr=sum(s for k,typ,s in w if typ=='U' and owners[k]==[ci,ci]);selfwr.append(wr)
  transport=[s*cross[k]['over'] for k,typ,s in w if typ=='U']
  longitude=red(([-mers[ci]]*wr if wr>=0 else [mers[ci]]*(-wr))+transport);longs.append(longitude)
  lk=[0]*len(words)
  for k,typ,s in w:
   if typ=='U':lk[comps[cross[k]['over']]]+=s
  lk[ci]-=wr;linking.append(lk)
 return {'n_generators':N,'meridians':mers,'weights':weights,'generator_component':comps,'relators':rels,'preferred_longitudes':longs,'self_writhes':selfwr,'linking_matrix':linking}

def fox(w,weights):
 row={};power=0
 for x in w:
  g=abs(x);e=weights[g];p=power if x>0 else power-e
  c=row.setdefault(g,{});c[p]=c.get(p,0)+(1 if x>0 else -1)
  if not c[p]:del c[p]
  if not c:del row[g]
  power+=e if x>0 else -e
 if power:raise ValueError(f'nonzero exponent {power}')
 return row

def addpoly(a,b,shift=0,factor=1):
 c=a.copy()
 for k,v in b.items():
  c[k+shift]=c.get(k+shift,0)+factor*v
  if not c[k+shift]:del c[k+shift]
 return c

def multpoly(a,b):
 c={}
 for k,v in a.items():c=addpoly(c,b,k,v)
 return c

def row_elim(row,pivot,g,power,coeff):
 f=row.pop(g,None)
 if f is None:return
 # row <- row - (f / (coeff*t^power))*pivot; coeff = +/-1
 f={k-power:-v*coeff for k,v in f.items()}
 for h,p in pivot.items():
  if h==g:continue
  c=addpoly(row.get(h,{}),multpoly(f,p))
  if c:row[h]=c
  else:row.pop(h,None)

def serrow(r):return {str(g):{str(k):v for k,v in sorted(p.items())} for g,p in sorted(r.items())}
def serrows(rows):return {str(i):serrow(r) for i,r in sorted(rows.items())}

def main():
 raw=(P/'surgery_diagram.json').read_bytes();d=json.loads(raw);out=build(d['gauss_words']);weights=out['weights'];reference=out['meridians'][0]
 rows={i:fox(w,weights) for i,w in enumerate(out['relators'])};observers={i:fox(w,weights) for i,w in enumerate(out['preferred_longitudes'])}
 for r in list(rows.values())+list(observers.values()):r.pop(reference,None)
 out['diagram_sha256']=hashlib.sha256(raw).hexdigest();out['reference_column_removed']=reference;out['initial_fox_rows']=serrows(rows);out['initial_longitude_rows']=serrows(observers)
 keep=set(out['meridians'][1:]);log=[];t0=time.monotonic()
 while True:
  counts=Counter(g for r in rows.values() for g in r);choices=[]
  for ri,r in rows.items():
   for g,p in r.items():
    if g in keep or len(p)!=1:continue
    power,coeff=next(iter(p.items()))
    if coeff not in (-1,1):continue
    score=(len(r)-1)*(counts[g]-1)
    choices.append((score,sum(map(len,r.values())),len(r),g,ri,power,coeff))
  if not choices:break
  _,_,_,g,ri,power,coeff=min(choices);pivot=rows.pop(ri)
  log.append({'row':ri,'column':g,'power':power,'coefficient':coeff})
  for row in rows.values():row_elim(row,pivot,g,power,coeff)
  for row in observers.values():row_elim(row,pivot,g,power,coeff)
  if len(log)%100==0:print('pivots',len(log),'rows',len(rows),'entries',sum(map(len,rows.values())),'seconds',round(time.monotonic()-t0,3),flush=True)
  if time.monotonic()-t0>120:raise TimeoutError('120 second exact pivot cap')
 rows={i:r for i,r in rows.items() if r};gs=sorted({g for r in rows.values() for g in r}|{g for r in observers.values() for g in r}|keep)
 out['pivots']=log;out['reduced_rows']=serrows(rows);out['reduced_longitudes']=serrows(observers);out['remaining_generators']=gs
 out['pivot_seconds']=time.monotonic()-t0;print('reduced',len(rows),len(gs),'gens',gs,flush=True)
 # Small exact solve over the rational function field.
 import sympy as sp
 t=sp.Symbol('t')
 def expr(p):return sum(v*t**k for k,v in p.items())
 def matrix(rows):return sp.Matrix([[expr(r.get(g,{})) for g in gs] for r in rows])
 M=matrix(list(rows.values()));Lg=matrix([observers[i] for i in range(3)])
 out['small_fox_matrix']=[[str(x) for x in row] for row in M.tolist()];out['small_longitude_matrix']=[[str(x) for x in row] for row in Lg.tolist()]
 unknown=[g for g in gs if g not in keep];uix=[gs.index(g) for g in unknown];kix=[gs.index(g) for g in out['meridians'][1:]]
 MU=M[:,uix];MK=M[:,kix];solution=MU.gauss_jordan_solve(-MK)[0]
 if any(x.free_symbols-{t} for x in solution):raise ValueError('free rational variables beyond axes')
 S=sp.zeros(len(gs),2)
 for i,g in enumerate(unknown):
  for j in range(2):S[gs.index(g),j]=sp.cancel(solution[i,j])
 for j,g in enumerate(out['meridians'][1:]):S[gs.index(g),j]=1
 if any(sp.cancel(x)!=0 for x in M*S):raise ValueError('response does not satisfy every relator')
 E=(Lg[1:,:]*S).applyfunc(sp.cancel)
 out['meridian_response']=[[str(x) for x in row] for row in S.tolist()];out['exact_axis_longitude_response']=[[str(x) for x in row] for row in E.tolist()]
 out['E_zero']=E==sp.zeros(2);out['surgery_response_determinant']=str(sp.cancel((sp.eye(2)+sp.diag(1,-1)*E).det()))
 # Full filled presentation: retain unit pivots then add two preferred surgery rows.
 filling=M.col_join(sp.Matrix([[int(g==out['meridians'][1])+Lg[1,i] for i,g in enumerate(gs)],[-int(g==out['meridians'][2])+Lg[2,i] for i,g in enumerate(gs)]]))
 from sympy.matrices.normalforms import smith_normal_form
 clearing=[]
 for row in filling.tolist():
  terms=[int(z.as_powers_dict().get(t,0)) for x in row for z in sp.Add.make_args(sp.expand(x)) if z!=0];lo=min(terms) if terms else 0
  clearing.append([sp.expand(x*t**(-lo)) for x in row])
 smith=smith_normal_form(sp.Matrix(clearing),domain=sp.QQ.poly_ring(t));diag=[sp.expand(smith[i,i]) for i in range(min(smith.shape))]
 order=sp.Poly(sp.prod(diag),t)
 while order.degree()>0 and order.nth(0)==0:order=sp.Poly(order.as_expr()/t,t)
 order=order.monic();out['filled_smith_diagonal']=[str(x) for x in diag];out['filled_alexander_order_monic']=str(order.as_expr());out['filled_alexander_coefficients_ascending']=[str(order.nth(i)) for i in range(order.degree()+1)]
 target=(t**4-3*t**3+5*t**2-3*t+1)**2;out['target_alexander_match']=sp.expand(order.as_expr()-target)==0
 out['elapsed_seconds']=time.monotonic()-t0;out['status']='EXACT_FRAMED_FOX_CALCULATION_COMPLETE_FOR_SAVED_POLYGON';out['limitations']=['Identical Alexander polynomial is not a knot identification.','No embedded modifying annulus, smooth slice disk, or nonribbon proof for the surgery output.','An S3 ambient identification still requires a certificate that the auxiliary sublink is an unlink.']
 (P/'framed_fox_boundary.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['linking_matrix','self_writhes','E_zero','exact_axis_longitude_response','filled_alexander_order_monic','target_alexander_match','elapsed_seconds']},indent=2),flush=True)
if __name__=='__main__':main()
