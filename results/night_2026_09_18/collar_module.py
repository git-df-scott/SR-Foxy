"""Compare the exact boundary module with the saved (not identified) q0 map.

No geometric disk collar or new band embedding is certified here.
"""
from pathlib import Path
import contextlib
import io
import json
import sympy as s

p = Path(__file__).with_name('axis_module.py')
ns = {'__file__': str(p)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(p.read_text(), str(p), 'exec'), ns)
red, mul, inv = (ns[k] for k in ('red', 'mul', 'inv'))
t, power = ns['t'], ns['power']
root = Path(__file__).resolve().parents[2]
C = json.loads((root/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())

def source_fox(w):
    row = [0]*9
    pref = 0
    for x in w:
        row[abs(x)-1] = red(row[abs(x)-1] + (1 if x>0 else -1)*power(pref if x>0 else pref-1))
        pref += 1 if x>0 else -1
    assert pref == 0
    return row[1:]

M = [source_fox(w) for w in C['source_relators']]
piv = []
for j in range(8):
    k = len(piv)
    a = next((i for i in range(k, len(M)) if M[i][j] != 0), None)
    if a is None:
        continue
    M[k], M[a] = M[a], M[k]
    u = inv(M[k][j])
    M[k] = [mul(v,u) for v in M[k]]
    for i in range(len(M)):
        if i != k:
            c = M[i][j]
            M[i] = [red(v-mul(c,w)) for v,w in zip(M[i],M[k])]
    piv.append(j)
free = [j for j in range(8) if j not in piv]
assert len(free) == 1
Z = [0]*8
Z[free[0]] = 1
for i,j in enumerate(piv):
    Z[j] = -M[i][free[0]]

def source_class(w):
    return red(sum(mul(a,b) for a,b in zip(source_fox(w), Z)))

assert all(source_class(w) == 0 for w in C['source_relators'])
images = {int(i)+1:w for i,w in C['boundary_arc_images'].items()}
def push(w):
    return [v for x in w for v in (images[x] if x>0 else [-v for v in images[-x][::-1]])]
assert all(source_class(push(w)) == 0 for w in ns['rel'])
native = [source_class(push(w)) for w in ns['oldwords']]
assert native[0] != 0
relative = [mul(v,inv(native[0])) for v in native]
assert all(red(a-b)==0 for a,b in zip(relative,[1,power(-1),-1,-power(-1)]))

g = ns['g']
g['BAND1']['arc_is_under'] = [False,True]
g['BAND2']['arc_is_under'] = [True,False]
D = g['add_zero_twist_band'](g['add_zero_twist_band'](ns['A'],g['BAND1']),g['BAND2'])
repair_words = ns['words'](D)
rows = []
for label, words in [('0000',ns['newwords']),('0110',repair_words)]:
    coords = [[red(v) for v in ns['Binv']*s.Matrix(ns['coords'](w))] for w in words]
    im = [mul(source_class(push(w)),inv(native[0])) for w in words]
    assert all(red(a+mul(b,relative[2])-v)==0 for (a,b),v in zip(coords,im))
    expected = [[1,-power(-1)],[power(-1),-1]] if label=='0000' else [[1,-1],[power(-1),-power(-1)]]
    assert all(red(a-b)==0 for row,target in zip(coords,expected) for a,b in zip(row,target))
    rows.append({'bits':label,'words':words,'boundary_coordinates':[[str(v) for v in row] for row in coords],'q0_images_relative_to_eU':[str(v) for v in im]})
d = ns['Delta']
H = s.diag(t**2/d,-t**2/d)
mixed = s.Matrix([[1,-1/t],[1/t,-1]])
star = lambda A: A.subs(t,1/t).T
response = s.Matrix([[0,t*(t**2-1)/d],[-t*(t**2-1)/d,0]])
assert all(s.cancel(v)==0 for v in mixed*H*star(mixed)-response)
repair = s.Matrix([[1,-1],[1/t,-1/t]])
assert all(s.cancel(v)==0 for v in repair*H*star(repair))
assert all(s.cancel(v)==0 for v in H-star(H))
r,a,b,c,e = s.symbols('r a b c e')
E=s.Matrix([[a,b],[c,e]])
assert s.expand((s.eye(2)+s.diag(r,-r)*E).det()-(1+r*(a-e)-r*r*E.det()))==0
print(json.dumps({'scope':'Exact module of saved q0 only; no geometric collar identified','source_module_dimension':len(free),'native_images_relative_to_eU':[str(v) for v in relative],'checks':'All source and mapped boundary Fox relations vanish; direct word images equal coordinate pushforward; Hermitian and both pairing matrix identities verified','axes':rows,'native_pairing_representative':[[str(v) for v in row] for row in H.tolist()],'saved_q_n_functional':'(a,b) -> a-t^n*b','saved_q_n_kernel':'span((t^n,1))','0110_line':'span((1,-1)); transverse to every saved q_n kernel','opposite_surgery_Laurent_response_factor':'1+r*(E11-E22)-r^2*det(E)'},indent=2))
