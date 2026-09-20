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
    F,R,z=exact_context(q)
    assert z**q==F.one
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
        if not d[e]:del d[e]
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
        coeff=dense(f);k=next(i for i,c in enumerate(coeff) if c)
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
    coeffs=dense(delta); cs=[list(reversed(c.to_list())) for c in coeffs]
    return {'label':label,'q':q,'p':p,'scale':scale,'generators':gens,'relators':rels,'abelianization':eps,'cocycle':coc,'degree':delta.degree(),'coefficients_in_z_ascending':[[str(c) for c in row] for row in cs],'all_coefficients_integral':all(c.denominator==1 for row in cs for c in row),'seconds':time.monotonic()-start}

