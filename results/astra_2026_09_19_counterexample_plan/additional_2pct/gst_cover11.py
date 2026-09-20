"""Integral cyclic-cover homology from a pinned Seifert matrix, not a ribbon test."""
from pathlib import Path
import json,time,math
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
P=Path(__file__).parent

def cover_matrix(V,n):
 F=V.T-V
 assert abs(F.det(method='domain-ge'))==1
 G=F.inv()*V.T
 assert all(v.q==1 for v in G)
 return G**n-(G-s.eye(V.rows))**n

def smith(M):
 D=smith_normal_form(M,domain=s.ZZ)
 return [abs(int(D[i,i])) for i in range(D.rows)]

def main():
 start=time.monotonic()
 V4=s.Matrix([[1,0],[-1,-1]])
 expected={2:[5],3:[4,4],4:[3,15],5:[11,11],6:[8,40],7:[29,29],8:[21,105],9:[76,76]}
 controls=[]
 for n,ex in expected.items():
  got=[a for a in smith(cover_matrix(V4,n)) if a!=1];assert got==ex
  controls.append({'knot':'figure-eight','n':n,'nonunit_smith':got})
 V=s.Matrix(json.loads((P/'GST_SEIFERT_MATRIX.json').read_text()))
 print('controls PASS; matrix',V.shape,flush=True)
 R=cover_matrix(V,11);print('integer presentation formed',time.monotonic()-start,flush=True)
 diag=smith(R);nonunits=[a for a in diag if a!=1]
 assert math.prod(diag)==43**4
 out={'status':'PASS','matrix_source':'841d445:research/gst_2026_09_19_exact/spherogram_seifert_matrix.json','source_dimension':V.rows,'n':11,'smith_diagonal':diag,'nonunit_smith':nonunits,'homology_order':math.prod(diag),'presentation_matrix':[[int(a) for a in row] for row in R.tolist()],'controls':controls,'seconds':time.monotonic()-start,'scope':'Integral H1 of 11-fold branched cover of literal GST48, conditional on saved Seifert-matrix identification. Not a linking-form, disk-kernel or nonribbon certificate.'}
 (P/'GST_COVER11_HOMOLOGY.json').write_text(json.dumps(out,indent=2))
 print('H1 invariant factors',nonunits,'seconds',time.monotonic()-start,flush=True)
if __name__=='__main__':main()
