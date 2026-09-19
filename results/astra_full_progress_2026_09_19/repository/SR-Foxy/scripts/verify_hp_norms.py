#!/usr/bin/env python3
"""Independent rational-arithmetic check of four HKL polynomial non-norms.

No SnapPy, Sage, polynomial factorizer, or numerical arithmetic is used.
Work in Q[z]/(z^2+z+1). A norm g(t) conjugate(g(t^-1)) has even
multiplicity at each root fixed by conjugate-reciprocal, in particular at
z and -z. Exact synthetic division finds odd multiplicities here.
This checks the final algebraic step, not the topology producing the polynomials.
"""
import argparse
import ast
from fractions import Fraction as F
import json
from pathlib import Path

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
Z = (F(0), F(1))


def add(a, b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0], -a[1])
def mul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def conj(a): return (a[0]-a[1], -a[1])


def parse(text):
    def ev(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return (F(node.value), F(0))
        if isinstance(node, ast.Name) and node.id == 'z': return Z
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return neg(ev(node.operand))
        if isinstance(node, ast.BinOp):
            a, b = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Add): return add(a,b)
            if isinstance(node.op, ast.Sub): return add(a,neg(b))
            if isinstance(node.op, ast.Mult): return mul(a,b)
            if isinstance(node.op, ast.Div):
                norm = mul(b,conj(b))
                assert norm[1] == 0 and norm[0] != 0
                c = mul(a,conj(b)); return (c[0]/norm[0],c[1]/norm[0])
        raise ValueError('Unsupported coefficient: '+text)
    return ev(ast.parse(text, mode='eval').body)


def multiplicity(coefficients, root):
    a, count = list(coefficients), 0
    while len(a)>1:
        b = [ZERO]*(len(a)-1); b[-1] = a[-1]
        for k in range(len(a)-2,0,-1):
            b[k-1] = add(a[k],mul(root,b[k]))
        if add(a[0],mul(root,b[0])) != ZERO: break
        a = b; count += 1
    return count


def verify(input_file, output):
    if Path(output).exists(): raise FileExistsError(output)
    d = json.loads(Path(input_file).read_text()); witnesses=[]
    for i, test in enumerate(d['norm_tests']):
        coeff = list(map(parse,test['coefficients_low_to_high']))
        for name, root in [('z',Z),('-z',neg(Z))]:
            assert mul(root,conj(root)) == ONE
            m = multiplicity(coeff,root)
            if m%2:
                witnesses.append({'polynomial':i+1, 'root':name, 'exact_multiplicity':m,
                                  'self_conjugate_reciprocal_root':True, 'cannot_be_a_norm':True})
                break
        else: raise AssertionError('No odd root multiplicity found')
    assert len(witnesses)==4
    result={'input':str(input_file),'field':'Q[z]/(z^2+z+1)', 'witnesses':witnesses,
            'arithmetic':'Python fractions.Fraction; exact synthetic division; no norm-test library',
            'scope':'Independent final algebra check only. Topological representation construction remains dependent on SnapPy.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('output')
    a=p.parse_args();verify(a.input,a.output)
