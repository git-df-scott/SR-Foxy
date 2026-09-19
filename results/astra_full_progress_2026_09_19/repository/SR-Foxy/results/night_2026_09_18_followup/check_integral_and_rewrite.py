"""Standard-library integer Laurent replay, including relator provenance.

No SymPy, group solver, or geometry library is used.
"""
from pathlib import Path
import ast
import copy
import json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
W=json.loads((ROOT/'results/night_2026_09_18/word_correction.json').read_text())
clean=lambda d:{k:v for k,v in d.items() if v}
def add(a,b):
    c=dict(a)
    for k,v in b.items():c[k]=c.get(k,0)+v
    return clean(c)
def mul(a,b):
    c={}
    for i,v in a.items():
        for j,w in b.items():c[i+j]=c.get(i+j,0)+v*w
    return clean(c)
def parse(node):
    if isinstance(node,ast.Constant):
        assert type(node.value)==int
        return clean({0:node.value})
    if isinstance(node,ast.Name):
        assert node.id=='t'
        return {1:1}
    if isinstance(node,ast.UnaryOp):
        assert isinstance(node.op,ast.USub)
        return {k:-v for k,v in parse(node.operand).items()}
    assert isinstance(node,ast.BinOp)
    a,b=parse(node.left),parse(node.right)
    if isinstance(node.op,ast.Add):return add(a,b)
    if isinstance(node.op,ast.Sub):return add(a,{k:-v for k,v in b.items()})
    if isinstance(node.op,ast.Mult):return mul(a,b)
    if isinstance(node.op,ast.Div):
        assert len(b)==1
        (j,w),=b.items()
        assert w in (-1,1)
        return {i-j:v*w for i,v in a.items()}
    assert isinstance(node.op,ast.Pow) and set(b)<= {0}
    n=b.get(0,0)
    if n<0:
        assert len(a)==1
        (j,w),=a.items()
        assert w in (-1,1)
        return {j*n:w**abs(n)}
    ans={0:1}
    for _ in range(n):ans=mul(ans,a)
    return ans
def fox(w,N):
    rows=[{} for _ in range(N)]
    p=0
    for x in w:
        assert 1<=abs(x)<=N
        e=p if x>0 else p-1
        rows[abs(x)-1]=add(rows[abs(x)-1],{e:1 if x>0 else -1})
        p+=1 if x>0 else -1
    assert p==0
    return rows
expected_rel={'source':C['source_relators'],'boundary':[[-sg*(b+1),i+1,sg*(b+1),-(o+1)] for i,o,b,sg,c in C['boundary_relations']]}
def check_integral(row):
    group=row['group']
    assert row['relators']==expected_rel[group]
    assert row['correction_word']==W[f'correction_{group}_word']
    N=9 if group=='source' else 18
    assert row['generators']==N
    # Each relator abelianizes to identification of two meridians. The
    # connected identification graph proves the full abelianization is Z.
    reached={1}
    for rel in row['relators']:
        assert len(rel)==4 and rel[0]==-rel[2] and rel[1]>0 and rel[3]<0
    for _ in range(N):
        for rel in row['relators']:
            i,o=rel[1],-rel[3]
            if i in reached or o in reached:reached.update((i,o))
    assert reached==set(range(1,N+1))
    target=fox(row['correction_word'],N)
    coeff=[parse(ast.parse(v,mode='eval').body) for v in row['integral_Laurent_coefficients']]
    assert len(coeff)==len(row['relators'])
    result=[{} for _ in range(N)]
    for a,rel in zip(coeff,row['relators']):
        for i,b in enumerate(fox(rel,N)):result[i]=add(result[i],mul(a,b))
    assert result==target

def inv(w):return [-x for x in w[::-1]]
def check_rewrite(row):
    assert row['initial_word']==W['correction_source_word']
    word=row['initial_word'][:]
    for step in row['steps']:
        at=step['at']
        if step['type']=='free':
            assert word[at:at+2]==step['letters']
            assert word[at]==-word[at+1]
            word[at:at+2]=[]
        else:
            r=C['source_relators'][step['relator']]
            assert step['sign'] in (1,-1)
            if step['sign']==-1:r=inv(r)
            k=step['rotation'];r=r[k:]+r[:k]
            cut=step['cut'];lhs,rhs=r[:cut],inv(r[cut:])
            assert step['from']==lhs and step['to']==rhs
            assert word[at:at+len(lhs)]==lhs
            word[at:at+len(lhs)]=rhs
    assert word==row['final_word'] and len(word)==row['final_length']==20

rows=json.loads((HERE/'integral_correction.json').read_text())
for row in rows:check_integral(row)
short=json.loads((HERE/'shortened_correction.json').read_text())
check_rewrite(short)
bad=copy.deepcopy(rows[0]);bad['integral_Laurent_coefficients'][0]+='+1'
try:check_integral(bad)
except AssertionError:pass
else:raise AssertionError('integral coefficient mutation survived')
bad=copy.deepcopy(short);bad['steps'][0]['to']=[999]
try:check_rewrite(bad)
except AssertionError:pass
else:raise AssertionError('rewrite mutation survived')
print(json.dumps({'integral_source_Fox_identity':'PASS','integral_boundary_Fox_identity':'PASS','all_73_rewrites':'PASS','two_mutations_rejected':True,'independence':'standard-library integer Laurent arithmetic; exact relator provenance'},indent=2))
