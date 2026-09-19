#!/usr/bin/env python3
"""Independent Fox construction using a triangulation-derived group presentation."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import snappy
import sympy
from colored_link_rank import fox_matrix, rank_minor, ribbon_control
from component_guided_bands import controls


def group_certificate(L,values=(2,3),prime=1009):
    G=L.exterior().fundamental_group();gens=G.generators();rels=G.relators();periph=G.peripheral_curves();n=len(gens)
    assert len(periph)==2 and all(len(g)==1 and g.islower() for g in gens)
    index={g:i for i,g in enumerate(gens)}
    def powers(word):
        v=[0]*n
        for c in word:v[index[c.lower()]]+=1 if c.islower() else -1
        return v
    mat=sympy.Matrix([powers(w) for w in rels]+[powers(mu) for mu,la in periph])
    rhs=sympy.zeros(len(rels)+2,2);rhs[-2,0]=1;rhs[-1,1]=1
    coords,parameters=mat.gauss_jordan_solve(rhs);assert parameters.rows==0
    assert all(x.q==1 for x in coords) and mat*coords==rhs
    exponents=[[int(coords[i,j]) for j in range(2)] for i in range(n)]
    ev=[pow(values[0],a,prime)*pow(values[1],b,prime)%prime for a,b in exponents]
    rows=[]
    for w in rels:
        row=[0]*n;pref=1
        for c in w:
            i=index[c.lower()]
            if c.islower():row[i]=(row[i]+pref)%prime;pref=pref*ev[i]%prime
            else:pref=pref*pow(ev[i],-1,prime)%prime;row[i]=(row[i]-pref)%prime
        assert pref==1 and sum(x*(v-1) for x,v in zip(row,ev))%prime==0
        rows.append(row)
    cert=rank_minor(rows,n,prime)
    # Recheck the advertised minor with SymPy integer arithmetic, independent
    # of the modular elimination used by rank_minor.
    minor=sympy.Matrix([[rows[i][j] for j in cert['minor_columns']] for i in cert['minor_rows']])
    assert int(minor.det())%prime==cert['minor_determinant_mod_prime']
    return dict(cert,generators=gens,relators=rels,meridians=[mu for mu,la in periph],
                generator_exponents=exponents,component_values=list(values),prime=prime)


def main():
    src=Path('results/normalized_component_neighborhoods.json');raw=src.read_bytes();D=json.loads(raw)
    first=Path('results/component_link_concordance_ranks.json');F=json.loads(first.read_text());assert F['complete']
    wanted={(r['index'],r['band']):r for r in F['rows']}
    rec={'status':'INDEPENDENT_GROUP_PRESENTATION_CHECK','source_sha256':hashlib.sha256(raw).hexdigest(),
         'first_certificate_sha256':hashlib.sha256(first.read_bytes()).hexdigest(),'controls':{},'rows':[],'counts':Counter(),'complete':False}
    for name,c in controls().items():
        pd=c['link_pd'];n=2*len(pd)
        if c['unlinked_unknots']:pd=pd+[[n,n+1,n+1,n]]
        C=group_certificate(snappy.Link(pd));assert C['maximal_minor_nonzero']==('Whitehead' in name);rec['controls'][name]=C
    L,meta=ribbon_control();C=group_certificate(L);assert not C['maximal_minor_nonzero'];rec['controls']['nonsplit_ribbon']=dict(C,provenance=meta)
    out=Path('results/component_link_concordance_independent.json')
    if out.exists():raise FileExistsError(out)
    def save():out.write_text(json.dumps(rec,separators=(',',':'))+'\n')
    for run in D['runs']:
        for c in run['matches']:
            L=snappy.Link(c['link_pd']);f=wanted[run['index'],c['band']]
            for x in f['checks']:
                rows,colors=fox_matrix(L,x['component_values'],x['prime']);M=sympy.Matrix([[rows[i][j] for j in x['minor_columns']] for i in x['minor_rows']])
                assert int(M.det(method='domain-ge'))%x['prime']==x['minor_determinant_mod_prime']
            witness=next(x for x in f['checks'] if x['maximal_minor_nonzero'])
            C=group_certificate(L,witness['component_values'],witness['prime'])
            assert C['maximal_minor_nonzero']
            rec['rows'].append(dict(C,index=run['index'],band=c['band']));rec['counts']['independently_obstructed']+=1
            if len(rec['rows'])%50==0:save();print(len(rec['rows']),flush=True)
    rec['complete']=True;save();print(json.dumps(rec['counts']),flush=True)


if __name__=='__main__':main()
