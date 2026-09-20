from pathlib import Path
import sys,json,random,snappy,sympy as S,regina,time
p=Path(__file__).parent;sys.path.insert(0,str(p.resolve().parents[1]/'scripts'))
from variable_parallel import parallel
from suzuki_root_minus_one import Jet,probe
name=sys.argv[1];a,b=map(int,sys.argv[2:4]);precision=a+b-1;assert 1<=precision<=5
out=p/'suzuki33'/name/f'{a}{b}';out.mkdir(parents=True,exist_ok=True)
if (out/'RESULT.json').exists():raise FileExistsError('Preserve completed term')
if name.startswith('GST'):word=json.loads((p/f'suzuki_mixed/{name}_c0/INPUT.json').read_text())['full_cable']['input_braid']
else:word=snappy.Link(name).braid_word()
L,meta=parallel(word,[a,b]);random.seed(20260920);L.simplify('global');visible=len(L.link_components);missing=a+b-visible;meta.update(simplified_pd=L.PD_code(),unlinked_components=missing);(out/'INPUT.json').write_text(json.dumps(meta,indent=2)+'\n');Jet.order=precision;v=Jet([10,1]);delta=v+v**-1;start=time.monotonic()
if not L.crossings:value=delta**(a+b);r={'coefficients_mod101':list(value.d),'crossings':0}
else:
 L.unlinked_unknot_components=0;r=probe(L,precision);value=Jet(r['coefficients_mod101'])*delta**missing;r['coefficients_mod101']=list(value.d)
r.update(label=name,a=a,b=b,precision=precision,seconds=time.monotonic()-start)
if L.crossings and len(L.crossings)<=40:
 R=regina.Link.fromPD([[x+1 for x in row] for row in L.PD_code()]);J=R.jones(regina.Algorithm.Treewidth);expected=delta**(missing+1)*sum((int(str(J[i]))*(-1 if i%2 else 1)*v**i for i in range(J.minExp(),J.maxExp()+1)),Jet(0));assert expected==value,'Independent full Jones mismatch';r['independent_full_regina_agrees']=True
(out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='morse_events'},flush=True)
