#!/usr/bin/env python3
"""Fox characters, explicit Dehn/Goeritz bridge, and p=2 HKL polynomials.

The character pairing is y^T G z / q modulo q for integral lifts of
Goeritz-kernel vectors. Global linking-sign conventions do not affect
isotropy. All matrices and basis maps are saved. This is a computational
obstruction audit, not a slice certificate.
"""
import argparse
import json
from pathlib import Path
import string
import hashlib
import time
from sage.all import GF, ZZ, matrix, vector, CyclotomicField, LaurentPolynomialRing, MatrixSpace, FreeGroup
import snappy
from spherogram.links.links_base import CrossingStrand
from snappy.snap.slice_obs_HKL.basics import MatrixRepresentation, twisted_alexander_polynomial
from snappy.snap.slice_obs_HKL.poly_norm import poly_is_a_norm
from snappy.snap.nsagetools import MapToFreeAbelianization


def link_input(name):
    p = Path(name)
    if p.is_file():
        d = json.loads(p.read_text())
        return snappy.Link([tuple(c) for c in d.get('pd_code_snappy_0indexed', d.get('pd_code'))])
    if name == 'control_square_6_3':
        L = snappy.Link('6_3'); return L.connected_sum(L.mirror())
    return snappy.Link(name)


def bridge(L, q):
    assert ZZ(q).is_prime() and q % 2 == 1
    F = GF(q); n = len(L.crossings)
    pieces = L._pieces()
    arc = {tuple(cs): i for i, p in enumerate(pieces) for cs in p}
    rels = [list(map(int, r.Tietze())) for r in L.knot_group().relations()]
    fox = matrix(F, n + 1, n)
    for row, c in enumerate(L.crossings):
        fox[row, arc[(c, 0)]] += 1
        fox[row, arc[(c, 2)]] += 1
        fox[row, arc[(c, 1)]] -= 2
        assert arc[(c, 1)] == arc[(c, 3)]
    fox[n, 0] = 1  # quotient monochromatic colorings
    basis = fox.right_kernel().basis_matrix()
    faces = L.faces()
    face_of = {tuple(cs): i for i, face in enumerate(faces) for cs in face}
    G, graph = L.goeritz_matrix(return_graph=True)
    whites = graph.vertices(sort=True)
    blacks = sorted(set(range(len(faces))) - set(whites))
    # Each strand s separates the corners s-1 and s.
    equations = []
    colors = []
    for c in L.crossings:
        for s in range(4):
            row = vector(F, len(faces))
            row[face_of[(c, s)]] += 1
            row[face_of[(c, (s-1) % 4)]] += 1
            equations.append(row); colors.append(arc[(c, s)])
    row = vector(F, len(faces)); row[blacks[0]] = 1
    equations.append(row)
    D = matrix(F, equations)
    ys = []; regions = []
    for x in basis:
        r = D.solve_right(vector(F, [x[a] for a in colors] + [0]))
        assert D*r == vector(F, [x[a] for a in colors] + [0])
        y = vector(ZZ, [int(r[f]-r[whites[0]]) for f in whites[1:]])
        assert matrix(F, G)*vector(F, y) == 0
        ys.append(y); regions.append(list(map(int, r)))
    Y = matrix(ZZ, ys)
    assert matrix(F, Y).rank() == basis.nrows() == matrix(F, G).nullity()
    Bint = Y*G*Y.transpose()
    assert all(x % q == 0 for x in Bint.list())
    B = matrix(F, Bint / q)
    assert B.rank() == basis.nrows()
    # Verify the duality formula using the rational inverse pairing.
    duals = Y*G/q
    assert duals*G.inverse()*duals.transpose() == Bint/(q*q)
    return {'pd_code': L.PD_code(), 'q': q, 'fox_basis': [list(map(int, x)) for x in basis],
            'goeritz': [list(map(int, x)) for x in G.rows()],
            'goeritz_smith': list(map(int, G.elementary_divisors())),
            'white_faces': list(map(int, whites)), 'dehn_regions': regions,
            'goeritz_kernel_basis': [list(map(int, x)) for x in ys],
            'character_pairing': [list(map(int, x)) for x in B.rows()],
            'wirtinger_relators': rels}, basis, B


def reduce_word(word):
    out = []
    for a in word:
        if out and out[-1] == -a: out.pop()
        else: out.append(a)
    return out


def inverse(word): return [-x for x in reversed(word)]


def simplify_presentation(n, rels):
    """Only generator-elimination Tietze moves; retained generators are original.

    Drop one redundant Wirtinger relator first. Every eliminated generator
    gets an explicit word, and all original relators are checked after all
    substitutions. This avoids untracked changes of character basis.
    """
    orig = [list(r) for r in rels]
    rels = [reduce_word(r) for r in rels[:-1]]
    words = {i: [i] for i in range(1, n+1)}
    alive = set(words); steps = []
    while True:
        opts = [(len(r), j, g) for j, r in enumerate(rels) for g in alive
                if sum(abs(x) == g for x in r) == 1]
        if not opts: break
        _, j, g = min(opts); r = rels[j]; k = next(i for i,x in enumerate(r) if abs(x)==g)
        tail = r[k+1:]+r[:k]
        replacement = inverse(tail) if r[k] > 0 else tail
        def sub(w):
            return reduce_word([a for x in w for a in (replacement if x==g else inverse(replacement) if x==-g else [x])])
        rels = [sub(r) for i,r in enumerate(rels) if i!=j]
        rels = [r for r in rels if r]
        words = {i:sub(w) for i,w in words.items()}; alive.remove(g)
        steps.append({'generator':g,'word':replacement})
    return sorted(alive), rels, words, steps


class Presentation:
    def __init__(self, gens, rels): self.gens=gens; self.rels=rels
    def generators(self): return self.gens
    def relators(self): return self.rels


def polynomial(record, coloring):
    n = len(coloring)
    alive, rels, words, steps = simplify_presentation(n, record['wirtinger_relators'])
    assert len(rels) == len(alive)-1
    letters = {g:string.ascii_lowercase[i] for i,g in enumerate(alive)}
    def encode(w): return ''.join(letters[abs(a)] if a>0 else letters[-a].upper() for a in w)
    relwords = [encode(r) for r in rels]
    gens = list(letters.values())
    K = CyclotomicField(record['q'], 'z'); z=K.gen()
    R=LaurentPolynomialRing(K, 't'); t=R.gen(); M=MatrixSpace(R,2)
    mats=[M([[0,t*z**(-int(coloring[g-1]))],[z**int(coloring[g-1]),0]]) for g in alive]
    alpha=MatrixRepresentation(gens,relwords,M,mats)
    alpha.epsilon=MapToFreeAbelianization(Presentation(gens,relwords))
    # Strong check: recover every original meridian matrix through the saved
    # substitutions, and check every original relator (including the omitted one).
    def subst(w): return reduce_word([a for x in w for a in (words[x] if x>0 else inverse(words[-x]))])
    for g in range(1,n+1):
        assert alpha(encode(words[g])) == M([[0,t*z**(-int(coloring[g-1]))],[z**int(coloring[g-1]),0]])
    assert all(alpha(encode(subst(r))) == 1 for r in record['wirtinger_relators'])
    p=twisted_alexander_polynomial(alpha,reduced=True)
    return {'polynomial':str(p),'coefficients':[[int(e),[str(v) for v in c.list()]] for e,c in p.dict().items()],
            'norm':bool(poly_is_a_norm(p)), 'simplified_generators':alive,
            'simplified_relators':rels,'eliminations':steps}


def run(name, output, q, compute):
    out=Path(output)
    if out.exists(): raise FileExistsError(out)
    start=time.monotonic(); L=link_input(name)
    rec, basis, B=bridge(L,q); rec['input']=name; rec['results']=[]; rec['complete']=False
    rec['snappy_version']=snappy.__version__
    rec['input_sha256']=hashlib.sha256(Path(name).read_bytes()).hexdigest() if Path(name).is_file() else None
    out.write_text(json.dumps(rec,indent=2)+'\n')
    d=basis.nrows()
    if d==1: lines=[(1,)]
    elif d==2: lines=[(1,a) for a in range(q)]+[(0,1)]
    else: raise ValueError('Only dimensions one or two implemented')
    for a in lines:
        av=vector(GF(q),a); pairing=int(av*B*av); x=av*basis
        row={'line':list(a),'self_pairing_mod_q':pairing,'isotropic':pairing==0,
             'fox_coloring':list(map(int,x))}
        if compute=='all' or compute=='isotropic' and pairing==0:
            ts=time.monotonic(); row.update(polynomial(rec,x)); row['seconds']=round(time.monotonic()-ts,3)
        rec['results'].append(row)
        out.write_text(json.dumps(rec,indent=2)+'\n')
        print({k:v for k,v in row.items() if k not in ('coefficients','eliminations','simplified_relators','fox_coloring')},flush=True)
    rec['complete']=True; rec['seconds']=round(time.monotonic()-start,3)
    out.write_text(json.dumps(rec,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('input');p.add_argument('output');p.add_argument('--q',type=int,default=13)
    p.add_argument('--compute',choices=['none','all','isotropic'],default='none');a=p.parse_args()
    run(a.input,a.output,a.q,a.compute)
