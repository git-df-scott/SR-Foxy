#!/usr/bin/env python3
"""Second-shading pairing and direct polynomial norm certificates.

No imports from hkl_fox_goeritz. Rebuilds Dehn colors by propagation,
Goeritz from crossing corners, and verifies the stored isotropic TAPs
by direct multiplication of their half-polynomials.
"""
import argparse, hashlib, json
from pathlib import Path
from sage.all import GF, ZZ, QQ, matrix, vector, CyclotomicField, LaurentPolynomialRing
import snappy


def pairing_for_shading(L, fox_basis, unshaded, q):
    faces=L.faces(); fmap={tuple(s):i for i,f in enumerate(faces) for s in f}
    pieces=L._pieces(); arc={tuple(s):i for i,p in enumerate(pieces) for s in p}
    regions=sorted(unshaded); pos={v:i for i,v in enumerate(regions)}
    G=matrix(ZZ,len(regions))
    for c in L.crossings:
        for s,sign in [(0,1),(1,-1)]:
            u,v=fmap[(c,s)],fmap[(c,s+2)]
            if u in unshaded:
                assert v in unshaded
                if u!=v:
                    i,j=pos[u],pos[v]
                    G[i,j]+=sign;G[j,i]+=sign;G[i,i]-=sign;G[j,j]-=sign
    G=G[1:,1:];ys=[]
    for fox in fox_basis:
        vals={regions[0]:0};pending=True
        while pending:
            pending=False
            for c in L.crossings:
                for s in range(4):
                    u,v=fmap[(c,s)],fmap[(c,(s-1)%4)];a=fox[arc[(c,s)]]
                    if u in vals and v not in vals:vals[v]=(a-vals[u])%q;pending=True
                    if v in vals and u not in vals:vals[u]=(a-vals[v])%q;pending=True
                    if u in vals and v in vals:assert (vals[u]+vals[v]-a)%q==0
        assert len(vals)==len(faces)
        y=vector(ZZ,[vals[r] for r in regions[1:]])
        assert all(a%q==0 for a in G*y);ys.append(y)
    Y=matrix(ZZ,ys);raw=Y*G*Y.transpose();assert all(a%q==0 for a in raw.list())
    return matrix(GF(q),raw/q),G


def run(inputs, output):
    out=Path(output)
    if out.exists():raise FileExistsError(out)
    records=[]
    for name in inputs:
        p=Path(name);d=json.loads(p.read_text());q=d['q'];L=snappy.Link(d['pd_code']);F=GF(q)
        # The saved white set fixes one shading. The complementary set is
        # constructed here without Spherogram's Goeritz routine.
        white=set(d['white_faces']);black=set(range(len(L.faces())))-white
        B0,G0=pairing_for_shading(L,d['fox_basis'],white,q)
        B1,G1=pairing_for_shading(L,d['fox_basis'],black,q)
        assert G0==matrix(ZZ,d['goeritz']);assert B0==matrix(F,d['character_pairing'])
        # With the recorded crossing-index convention, both checkerboards
        # give the same pairing in the fixed Fox-character coordinates.
        assert B1==B0
        tested=[];K=CyclotomicField(q,'z');z=K.gen();R=LaurentPolynomialRing(K,'t');t=R.gen()
        for row in d['results']:
            a=vector(F,row['line']);assert int(a*B0*a)==row['self_pairing_mod_q']
            assert (a*B1*a==0)==row['isotropic']
            if row['isotropic'] and 'coefficients' in row:
                poly=R({int(e):K([QQ(c) for c in cs]) for e,cs in row['coefficients']})
                # For the D01 and square controls the norm is literally a
                # square. Verify multiplication, then conjugate reciprocity.
                fac=poly.factor();assert all(e%2==0 for f,e in fac)
                h=R(1)
                for f,e in fac:h*=f**(e//2)
                assert h*h*fac.unit()==poly
                hbar=R({-int(e):c.conjugate() for e,c in h.dict().items()})
                ratio=poly/(h*hbar)
                ratio=R(ratio);assert len(ratio.dict())==1
                tested.append({'line':row['line'],'half_polynomial':str(h),'norm_unit':str(ratio),
                               'verified':poly==ratio*h*hbar})
        records.append({'input':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                        'opposite_shading_pairing':[list(map(int,r)) for r in B1.rows()],
                        'all_lines_same_isotropy':True,'norm_certificates':tested})
    out.write_text(json.dumps({'status':'OPPOSITE_CHECKERBOARD_AND_EXPLICIT_NORMS_VERIFIED',
        'records':records,'limitations':'The TAP determinant still uses SnapPy exact arithmetic; topology-to-presentation correspondence relies on the cited theorems.'},indent=2)+'\n')
    print([(r['input'],len(r['norm_certificates'])) for r in records])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('inputs',nargs='+');a=p.parse_args();run(a.inputs,a.output)
