"""Independent standard-library proof replay. No SymPy, Groebner, or imports
from producer scripts. Parse the six recorded polynomials as rational maps.
"""
import ast,json
from fractions import Fraction as Q
from pathlib import Path

def plus(a,b):
 c=dict(a)
 for m,v in b.items():c[m]=c.get(m,Q(0))+v
 return {m:v for m,v in c.items() if v}
def times(a,b):
 c={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():
   m=(i+k,j+l);c[m]=c.get(m,Q(0))+v*w
 return {m:v for m,v in c.items() if v}
def parse(s):
 def walk(x):
  if isinstance(x,ast.Constant) and isinstance(x.value,int):return {(0,0):Q(x.value)} if x.value else {}
  if isinstance(x,ast.Name) and x.id in ('n','l'):return {(1,0) if x.id=='n' else (0,1):Q(1)}
  if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub):return {m:-v for m,v in walk(x.operand).items()}
  if isinstance(x,ast.BinOp):
   a,b=walk(x.left),walk(x.right)
   if isinstance(x.op,ast.Add):return plus(a,b)
   if isinstance(x.op,ast.Sub):return plus(a,{m:-v for m,v in b.items()})
   if isinstance(x.op,ast.Mult):return times(a,b)
   if isinstance(x.op,ast.Div) and set(b)=={(0,0)}:return {m:v/b[(0,0)] for m,v in a.items()}
   if isinstance(x.op,ast.Pow) and set(b)=={(0,0)}:
    q=b[(0,0)];assert q.denominator==1 and 0<=q<=10
    c={(0,0):Q(1)}
    for _ in range(int(q)):c=times(c,a)
    return c
  raise ValueError(ast.dump(x))
 return walk(ast.parse(s,mode='eval').body)
def total(fs,ms):
 out={}
 for f,m in zip(fs,ms):out=plus(out,times(f,m))
 return out
p=Path(__file__).with_name('winding_collar.json');d=json.loads(p.read_text())
fs=[parse(v) for v in d['coefficients_ascending_z']];ms=[parse(v) for v in d['bezout_multipliers']]
assert len(fs)==len(ms)==6
assert total(fs,ms)=={(0,0):Q(1)}
# The proof must reject changes to either an equation or a multiplier.
bad=list(fs);bad[0]=plus(bad[0],{(0,0):Q(1)});assert total(bad,ms)!={(0,0):Q(1)}
bad=list(ms);bad[0]={};assert total(fs,bad)!={(0,0):Q(1)}
print(json.dumps({'bezout_identity_verified':True,'mutation_rejections':2,'scope':'Saved trace-coefficient inconsistency, not a geometric collar certificate'}))
