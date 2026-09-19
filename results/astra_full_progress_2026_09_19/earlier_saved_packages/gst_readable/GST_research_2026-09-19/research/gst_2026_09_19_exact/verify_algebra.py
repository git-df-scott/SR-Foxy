"""Exact algebra certificates, including the reciprocal-prime decomposition.
The statement about precisely two rational Blanchfield metabolizers is proved
in the report; polynomial computations alone are not ribbon obstructions.
"""
import json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from pd_algebra import t,alexander,determinant
ROOT=Path(__file__).parent

def main():
    pd=json.loads((ROOT/'gst48.json').read_text())['pd']
    f=t**8-2*t**7+t**6+t**5-2*t**4+t**3-1
    g=t**8-t**5+2*t**4-t**3-t**2+2*t-1
    A=3*t**7+t**6+t**5+16*t**3-4*t**2-24*t-32
    B=-3*t**7+5*t**6-2*t**5-5*t**4-t**3+19*t**2+2*t-11
    assert s.expand(g+t**8*f.subs(t,1/t))==0
    assert s.expand(A*f+B*g)==43
    assert s.Poly(f,t,modulus=2).is_irreducible and s.Poly(g,t,modulus=2).is_irreducible
    D=alexander(pd);assert s.expand(D+f*g)==0 and determinant(pd)==1
    assert D.subs(t,1)==D.subs(t,-1)==1
    result=int(s.resultant(f,g,t));assert result==1849
    h=s.gcd(s.Poly(f,t,modulus=43),s.Poly(g,t,modulus=43));assert h.as_expr()==t**2-4*t+1 and h.is_irreducible
    Syl=s.Matrix([[s.expand(t**k*p).coeff(t,j) for j in range(16)] for p in [f,g] for k in range(8)])
    SN=smith_normal_form(Syl,domain=s.ZZ);sn=[abs(int(SN[i,i])) for i in range(16)];assert sn==[1]*14+[43,43]
    cover_result=int(s.resultant(D,t**11-1,t));assert abs(cover_result)==43**4
    ans={'f':str(f),'g':str(g),'D':str(D),'Delta_symmetric':str(s.expand(D/t**8)),'reciprocal_relation':'g(t) = -t^8 f(t^-1)',
         'f_irreducible_mod_2':True,'g_irreducible_mod_2':True,'resultant':result,'bezout_A':str(A),'bezout_B':str(B),'bezout_value':43,
         'sylvester_integer_smith_diagonal':sn,'gcd_mod_43':str(h.as_expr()),'gcd_mod_43_irreducible':True,
         'abs_resultant_D_t11_minus1':abs(cover_result),'rational_Blanchfield_metabolizer_count':2,
         'scope':'Exact algebra. The two choices are rational module metabolizers, not all slice disks or all embedded derivatives. No non-ribbon obstruction follows.'}
    (ROOT/'algebra_certificates.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
if __name__=='__main__':main()
