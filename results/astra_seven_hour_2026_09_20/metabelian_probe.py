"""Finite-field metabelian twisted-Alexander screen, scalar deck eigenspaces.

Independent Wada Fox implementation. Passes are inconclusive; any failure
requires a characteristic-zero or justified good-reduction proof audit.
"""
from pathlib import Path
import json,math,time,signal
import sympy as S
import snappy
from flint import fq_default_ctx,fq_default_poly_ctx
pdir=Path(__file__).resolve().parent

def kernel(A,q):
    A=[[int(x)%q for x in row] for row in A];n=len(A[0]);piv=[];r=0
    for j in range(n):
        h=next((h for h in range(r,len(A)) if A[h][j]),None)
        if h is None:continue
        A[r],A[h]=A[h],A[r];a=pow(A[r][j],-1,q);A[r]=[x*a%q for x in A[r]]
        for h in range(len(A)):
            if h!=r:
                a=A[h][j];A[h]=[(x-a*y)%q for x,y in zip(A[h],A[r])]
        piv.append(j);r+=1
    ans=[]
    for j in range(n):
        if j in piv:continue
        v=[0]*n;v[j]=1
        for i,k in enumerate(piv):v[k]=-A[i][j]%q
        ans.append(v)
    return ans

def probe(label,M,p,q,a,ell,scale=1):
    start=time.monotonic();G=M.fundamental_group();gens=G.generators();rels=G.relators();ng=len(gens)
    assert len(rels)==ng-1 and pow(a,p,q)==1 and a!=1 and ell%q==q-1
    index={g:i for i,g in enumerate(gens)}
    E=S.Matrix([[r.count(g)-r.count(g.upper()) for g in gens] for r in rels]);ns=E.nullspace();assert len(ns)==1
    v=ns[0];den=S.ilcm(*[z.q for z in v]);eps=[int(z*den) for z in v];div=math.gcd(*eps);eps=[e//div for e in eps]
    rows=[]
    for rel in rels:
        row=[0]*ng;pre=0
        for c in rel:
            j=index[c.lower()];e=eps[j]
            if c.islower():row[j]=(row[j]+pow(a,pre,q))%q;pre+=e
            else:pre-=e;row[j]=(row[j]-pow(a,pre,q))%q
        assert pre==0;rows.append(row)
    B=[(pow(a,e,q)-1)%q for e in eps];assert any(B)
    k=next(i for i,x in enumerate(B) if x)
    zs=kernel(rows,q);coc=next(z for z in zs if any((z[i]-z[k]*pow(B[k],-1,q)*B[i])%q for i in range(ng)))
    assert len(zs)==2,'Only multiplicity-one eigenspaces implemented'
    assert scale%q; coc=[scale*x%q for x in coc]
    F=fq_default_ctx(ell,2,'u');R=fq_default_poly_ctx(F);z=next((F.gen()+i)**((ell*ell-1)//q) for i in range(ell) if (F.gen()+i)**((ell*ell-1)//q)!=1)
    assert z**q==1 and z**ell==z**-1
    zp=[z**i for i in range(q)];ident=[(i,0,0) for i in range(p)]
    def mm(A,B):
        return [(A[r][0],e+A[r][1],(c+A[r][2])%q) for r,e,c in B]
    images={}
    for i,g in enumerate(gens):
        U=[]
        for j in range(p):
            e,l=divmod(eps[i]+j,p);U.append((l,e,pow(a,-l,q)*coc[i]%q))
        images[g]=U;V=[None]*p
        for j,(r,e,c) in enumerate(U):V[r]=(j,-e,-c%q)
        images[g.upper()]=V;assert mm(U,V)==ident
    def acc(d,e,c):
        d[e]=d.get(e,F(0))+c
        if d[e]==0:del d[e]
    Fox=[[{} for _ in range(ng*p)] for _ in range((ng-1)*p)]
    for ri,rel in enumerate(rels):
        pre=ident
        for c in rel:
            gi=index[c.lower()]
            if c.isupper():pre=mm(pre,images[c])
            for j,(r,e,kz) in enumerate(pre):acc(Fox[ri*p+r][gi*p+j],e,zp[kz] if c.islower() else -zp[kz])
            if c.islower():pre=mm(pre,images[c])
        assert pre==ident,'Representation relator failed'
    # Check every entry of Fox*(rho(g)-I)=0, independently of determinant.
    for row in Fox:
        boundary=[{} for _ in range(p)]
        for gi,g in enumerate(gens):
            for j,(r,e,kz) in enumerate(images[g]):
                for f,c in row[gi*p+r].items():acc(boundary[j],e+f,zp[kz]*c)
                for f,c in row[gi*p+j].items():acc(boundary[j],f,-c)
        assert not any(boundary),('Fox chain identity failed',boundary,eps,coc,rels)
    delete=next(i for i,e in enumerate(eps) if e)
    num=[[d for j,d in enumerate(row) if j//p!=delete] for row in Fox]
    den=[[{} for _ in range(p)] for _ in range(p)]
    for j,(r,e,kz) in enumerate(images[gens[delete]]):acc(den[r][j],e,zp[kz])
    for j in range(p):acc(den[j][j],0,-F(1))
    def normalize(f):
        assert f
        coeff=f.coeffs();k=next(i for i,c in enumerate(coeff) if c!=0)
        return R(coeff[k:])
    def determinant(L):
        A=[]
        for row in L:
            shift=min([e for d in row for e in d] or [0]);A.append([R([d.get(e,F(0)) for e in range(shift,max(d,default=shift)+1)]) for d in row])
        n=len(A);prev=R(1);sign=1
        for k in range(n-1):
            h=next((i for i in range(k,n) if A[i][k]),None)
            if h is None:return R(0)
            if h!=k:A[k],A[h]=A[h],A[k];sign=-sign
            pivot=A[k][k]
            for i in range(k+1,n):
                for j in range(k+1,n):
                    t=A[i][j]*pivot-A[i][k]*A[k][j];quo,rem=divmod(t,prev);assert not rem,'Bareiss division';A[i][j]=quo
                A[i][k]=R(0)
            prev=pivot
        return normalize(sign*A[-1][-1])
    numerator=determinant(num);denominator=determinant(den)
    delta,rem=divmod(numerator,denominator);assert not rem,'Torsion polynomial division'
    delta=normalize(delta);delta,rem=divmod(delta,R([-1,1]));assert not rem,'Reduced t-1 division'
    delta=delta.monic()
    def bar(f):return R([c**ell for c in reversed(f.coeffs())]).monic()
    assert bar(delta)==delta,'Reciprocal-conjugate symmetry failed'
    factors=list(delta.factor()[1]);bad=[]
    for f,m in factors:
        fbar=bar(f);matched=next((n for h,n in factors if h==fbar),0)
        if (f==fbar and m%2) or matched!=m:bad.append({'factor':str(f),'multiplicity':m,'conjugate_multiplicity':matched})
    # A synthetic norm and single self-dual factor exercise both outcomes.
    h=R([z,1,z**2]);norm=h*bar(h)
    for f,m in norm.factor()[1]:
        if f.monic()==bar(f):assert m%2==0
    assert bar(R([-1,1]))==R([-1,1])
    return {'label':label,'character_scale':scale,'cover_degree':p,'character_prime':q,'deck_eigenvalue':a,'reduction_prime':ell,'field':str(F),'root':str(z),'generators':gens,'relators':rels,'abelianization':eps,'cocycle':coc,'cocycle_dimension':len(zs),'reduced_twisted_polynomial':str(delta),'degree':delta.degree(),'factors':[(str(f),m) for f,m in factors],'not_norm_mod_reduction':bool(bad),'bad_factors':bad,'representation_and_Fox_checks':True,'seconds':time.monotonic()-start,'scope':'Finite-field screen only; a non-norm requires a good-reduction/characteristic-zero audit before declaring nonsliceness.'}

if __name__=='__main__':
    import sys
    out=pdir/'metabelian';out.mkdir(exist_ok=True)
    label=sys.argv[1]
    if label=='control':M=snappy.Manifold('K12n813');p,q,ell=3,7,13;eigen=(2,4)
    elif label=='10_17':
        d=json.loads((pdir.parents[1]/'data/knots/10_17_2_1-cable.json').read_text());M=snappy.Link(d.get('pd_code_snappy_0indexed') or d['pd_code']).exterior();p,q,ell=4,41,163;eigen=(9,32)
    else:raise ValueError(label)
    for a in eigen:
        path=out/f'{label}_{p}_{q}_{a}_v2.json';assert not path.exists()
        def timeout(*_):raise TimeoutError('240_SECOND_LIMIT_INCONCLUSIVE')
        signal.signal(signal.SIGALRM,timeout);signal.alarm(240)
        try:r=probe(label,M,p,q,a,ell)
        except Exception as exc:r={'status':'failed','error':repr(exc),'label':label,'p':p,'q':q,'a':a}
        finally:signal.alarm(0)
        path.write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
