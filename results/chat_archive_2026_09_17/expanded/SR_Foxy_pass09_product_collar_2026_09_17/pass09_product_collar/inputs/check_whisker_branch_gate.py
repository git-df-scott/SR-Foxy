#!/usr/bin/env python3
"""Finite-quotient branch gate for the explicit crossed-axis bands.

Purpose
-------
The exact product-disk based whiskers for the lower copy are not recorded in
AbeTagami_marked_product_scaffold.json.  This checker therefore does NOT guess
those whiskers.  Instead it enumerates every SL(2,F5) Wirtinger colouring of
the doubled boundary knot R compatible with the known meridian image, then
filters to colourings whose four original marked circles have the same
witness-type trace data (1,4) on both ends.  It asks how the two explicit
band-summed axes eta1,eta2 behave in each compatible branch.

A branch that gives different traces (or orders) for eta1,eta2 proves those
axes are not conjugate up to inversion in that finite quotient.  A branch on
which they are conjugate does NOT prove conjugacy in the knot group.

This is a necessary-group-gate audit, not an annulus or slice-disk certificate.
"""
from collections import defaultdict, Counter
import json

MOD=5
SOURCE_COMMIT='0439e8fa002f2c107fa699df6e57e5a313ffd23a'
SOURCE_SCAFFOLD='data/knots/AbeTagami_marked_product_scaffold.json'
BAND1={
    'along_top': [(15,2),(16,2),(2,2),(41,0)],
    'arc_is_under': [False,False], 'twist':0,
    'compressed_spec':'a40a423e_0_0',
}
BAND2={
    'along_top': [(13,2),(27,0),(32,2),(52,0)],
    'arc_is_under': [False,False], 'twist':0,
    'compressed_spec':'d0826c36_0_0',
}

SCAFFOLD=[
[31,22,32,23],[19,66,20,67],[1,18,2,19],[0,8,1,7],[6,0,7,67],[30,4,31,3],
[29,85,30,84],[28,68,29,75],[27,10,28,11],[81,27,82,26],[72,26,73,25],[13,24,14,25],
[2,24,3,23],[86,21,87,22],[20,87,21,76],[69,16,70,17],[78,17,79,18],[15,70,16,71],
[14,79,15,80],[73,12,74,13],[82,11,83,12],[68,10,69,9],[77,9,78,8],[5,77,6,76],
[85,5,86,4],[83,75,84,74],[71,81,72,80],[41,33,42,32],[65,45,66,44],[45,63,46,62],
[56,63,57,64],[64,57,65,58],[60,33,61,34],[103,35,104,34],[94,36,95,35],[53,37,54,36],
[37,101,38,100],[38,92,39,91],[39,51,40,50],[40,61,41,62],[42,105,43,106],[106,43,107,44],
[47,88,48,89],[46,97,47,98],[89,48,90,49],[98,49,99,50],[51,92,52,93],[52,101,53,102],
[54,88,55,95],[55,97,56,96],[107,59,96,58],[59,105,60,104],[93,102,94,103],[99,90,100,91]
]

# Known meridian image from the independently checked source representation.
MERIDIAN=(4,1,2,2)
I=(1,0,0,1)

def mm(A,B):
    a,b,c,d=A; e,f,g,h=B
    return ((a*e+b*g)%MOD,(a*f+b*h)%MOD,(c*e+d*g)%MOD,(c*f+d*h)%MOD)

def inv(A):
    a,b,c,d=A
    return (d%MOD,(-b)%MOD,(-c)%MOD,a%MOD)

def mpow(A,n):
    if n<0:return mpow(inv(A),-n)
    r=I
    while n:
        if n&1:r=mm(r,A)
        A=mm(A,A);n//=2
    return r

def tr(A):return (A[0]+A[3])%MOD

def order(A):
    r=I
    for k in range(1,121):
        r=mm(r,A)
        if r==I:return k
    raise RuntimeError('order exceeds SL2(F5)')

def sl2():
    out=[]
    for a in range(MOD):
      for b in range(MOD):
       for c in range(MOD):
        for d in range(MOD):
         if (a*d-b*c)%MOD==1:out.append((a,b,c,d))
    assert len(out)==120
    return out
G=sl2()

def conjugate(A,B):
    # In SL(2), inverse has same trace; still enumerate to distinguish edge cases.
    Binv=inv(B)
    for X in G:
        Y=mm(mm(inv(X),A),X)
        if Y==B or Y==Binv:return True
    return False

def adjacency_from_pd(pd):
    occ=defaultdict(list)
    for c,row in enumerate(pd):
        assert len(row)==4
        for p,e in enumerate(row):occ[e].append((c,p))
    assert all(len(v)==2 for v in occ.values())
    adj={c:[None]*4 for c in range(len(pd))}
    for a,b in occ.values():
        adj[a[0]][a[1]]=b;adj[b[0]][b[1]]=a
    return adj

def components(adj):
    nodes={(c,p) for c in adj for p in range(4)};seen=set();ans=[]
    for start in sorted(nodes):
        if start in seen:continue
        cc=set();stack=[start]
        while stack:
            x=stack.pop()
            if x in cc:continue
            cc.add(x);seen.add(x)
            c,p=x
            for y in (adj[c][p],(c,(p+2)%4)):
                if y not in cc:stack.append(y)
        ans.append(cc)
    return ans

def component_map(adj):
    cs=components(adj);where={}
    for i,cc in enumerate(cs):
        for x in cc:where[x]=i
    return cs,where

def connect(adj,a,b):adj[a[0]][a[1]]=b;adj[b[0]][b[1]]=a

def add_zero_twist_band(adj,band):
    A={c:list(v) for c,v in adj.items()};along=list(band['along_top']);bits=band['arc_is_under']
    X,Z=along[0],along[-1];Y,W=A[X[0]][X[1]],A[Z[0]][Z[1]];mids=along[1:-1];opps=[A[c][p] for c,p in mids]
    nxt=max(A)+1;Bs=list(range(nxt,nxt+len(mids)));Cs=list(range(nxt+len(mids),nxt+2*len(mids)))
    for c in Bs+Cs:A[c]=[None]*4
    for i,((ac,ap),(dc,dp)) in enumerate(zip(mids,opps)):
        B,C=Bs[i],Cs[i]
        if bits[i]:connect(A,(ac,ap),(B,2));connect(A,(dc,dp),(C,0));connect(A,(B,0),(C,2))
        else:connect(A,(ac,ap),(B,3));connect(A,(dc,dp),(C,1));connect(A,(B,1),(C,3))
    upper,lower=X,Y
    for i,bit in enumerate(bits):
        B,C=Bs[i],Cs[i]
        if bit:
            connect(A,upper,(B,3));connect(A,lower,(C,3));upper,lower=(B,1),(C,1)
        else:
            connect(A,upper,(B,0));connect(A,lower,(C,0));upper,lower=(B,2),(C,2)
    connect(A,upper,Z);connect(A,lower,W)
    return A

def crossing_sign_and_incoming(adj,c,comp_ports):
    # Follow an oriented component and record which ports are entry ports.
    pass

def oriented_component_data(adj):
    """Return component index, incoming ports and crossing signs.

    We orient each component by choosing its lexicographically first port and
    following across then along the diagram. Reversing a whole component does
    not change crossing signs; loop words may invert/conjugate, which is allowed
    by the conjugacy-up-to-inversion gate.
    """
    cs=components(adj); cmap={};incoming=set()
    for ci,cc in enumerate(cs):
        for x in cc:cmap[x]=ci
        start=min(cc);cur=start
        while cur not in incoming:
            incoming.add(cur)
            c,p=cur
            out=(c,(p+2)%4)
            cur=adj[out[0]][out[1]]
    signs={}
    for c in adj:
        inc={p for p in range(4) if (c,p) in incoming}
        if inc in ({0,3},{1,2}):s=1
        elif inc in ({0,1},{2,3}):s=-1
        else:raise RuntimeError(('bad incoming set',c,inc))
        signs[c]=s
    return cs,cmap,incoming,signs

def quotient_R_wirtinger(adj,Rcomp=0):
    """Build Wirtinger arcs/relations of R after killing all other meridians."""
    cs,cmap,incoming,signs=oriented_component_data(adj)
    # Union R ports along diagram edges and through mixed crossings. At R-R
    # crossings, over-strand ports are same Wirtinger arc; understrand is cut.
    parent={x:x for x in cs[Rcomp]}
    def find(x):
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[a]=b
    for x in list(parent):
        y=adj[x[0]][x[1]]
        if y in parent:union(x,y)
    relations=[]
    for c in adj:
        comps={cmap[(c,p)] for p in range(4)}
        if Rcomp not in comps:continue
        if comps=={Rcomp}:
            # ports 1,3 are over in this PD convention; union them.
            union((c,1),(c,3))
        else:
            # At mixed crossings, R just passes through; killing auxiliary
            # meridian removes any Wirtinger conjugation.
            rports=[p for p in range(4) if cmap[(c,p)]==Rcomp]
            assert len(rports)==2 and abs(rports[0]-rports[1])==2
            union((c,rports[0]),(c,rports[1]))
    roots=sorted({find(x) for x in parent})
    rid={r:i for i,r in enumerate(roots)}
    arc={x:rid[find(x)] for x in parent}
    for c in adj:
        if all(cmap[(c,p)]==Rcomp for p in range(4)):
            s=signs[c]
            over=arc[(c,1)]
            # Identify incoming and outgoing under ports from orientation.
            und=[0,2]; ui=next(p for p in und if (c,p) in incoming);uo=(ui+2)%4
            relations.append((arc[(c,ui)],arc[(c,uo)],over,s,c))
    return {'arcs':arc,'relations':relations,'cmap':cmap,'incoming':incoming,'signs':signs,'components':cs}

def solve_colourings(q):
    n=1+max(q['arcs'].values());rels=q['relations']
    # Constraint propagation over 120^n is impossible; use DFS relation closure.
    # The diagrams have 18 arcs and a cyclic Wirtinger presentation, so fixing
    # one meridian and branching only when no relation has two known variables
    # is tiny.
    byarc=defaultdict(list)
    for rel in rels:
        for a in rel[:3]:byarc[a].append(rel)
    solutions=[]
    def rel_check(rel,vals):
        i,o,b,s,_=rel
        known=[x in vals for x in (i,o,b)]
        if sum(known)<2:return None
        if i in vals and b in vals:
            rhs=mm(mm(mpow(vals[b],-s),vals[i]),mpow(vals[b],s))
            if o in vals:return vals[o]==rhs
            return ('set',o,rhs)
        if o in vals and b in vals:
            # i=b^s o b^-s
            rhs=mm(mm(mpow(vals[b],s),vals[o]),mpow(vals[b],-s))
            if i in vals:return vals[i]==rhs
            return ('set',i,rhs)
        if i in vals and o in vals:
            # Cannot solve b uniquely; only validate when b known.
            return None
    def propagate(vals):
        changed=True
        while changed:
            changed=False
            for rel in rels:
                z=rel_check(rel,vals)
                if z is False:return False
                if isinstance(z,tuple):
                    _,a,v=z
                    if a in vals and vals[a]!=v:return False
                    if a not in vals:vals[a]=v;changed=True
        for rel in rels:
            i,o,b,s,_=rel
            if i in vals and o in vals and b in vals:
                rhs=mm(mm(mpow(vals[b],-s),vals[i]),mpow(vals[b],s))
                if vals[o]!=rhs:return False
        return True
    def dfs(vals):
        vals=dict(vals)
        if not propagate(vals):return
        if len(vals)==n:
            solutions.append(tuple(vals[i] for i in range(n)));return
        # Prefer an unassigned arc appearing with two assigned neighbors.
        best=None;score=-1
        for a in range(n):
            if a in vals:continue
            sc=sum(sum(x in vals for x in rel[:3]) for rel in byarc[a])
            if sc>score:best,score=a,sc
        # All meridians of a knot representation are conjugate; restrict branch
        # values to the conjugacy class of the fixed meridian.
        cls=[]
        for X in G:
            v=mm(mm(inv(X),MERIDIAN),X)
            if v not in cls:cls.append(v)
        for v in cls:dfs({**vals,best:v})
    dfs({0:MERIDIAN})
    # remove duplicates from alternative propagation paths (normally none)
    uniq=list(dict.fromkeys(solutions))
    return uniq

def loop_value(adj,q,colouring,comp):
    """Evaluate a non-R component after killing its own meridian.

    Traverse the chosen orientation. Every time the loop passes UNDER R, append
    the R over-meridian to the blackboard longitude with exponent equal to the
    crossing sign. Mixed crossings where the loop is over R contribute nothing.
    The result is defined up to conjugacy and inversion for our purposes.
    """
    cmap=q['cmap'];incoming=q['incoming'];signs=q['signs'];arc=q['arcs']
    cc=q['components'][comp];start=min(cc);cur=start;value=I;seen=set()
    while cur not in seen:
        seen.add(cur);c,p=cur
        if cmap[(c,p)]!=comp:raise RuntimeError('component traversal escaped')
        # If this component occupies under ports 0/2 and R occupies over 1/3.
        if p in (0,2) and cmap[(c,1)]==0 and cmap[(c,3)]==0:
            # contribution once per crossing: only at incoming under port
            if (c,p) in incoming:
                value=mm(value,mpow(colouring[arc[(c,1)]],signs[c]))
        out=(c,(p+2)%4);cur=adj[out[0]][out[1]]
    return value

def map_final_R_arcs_to_scaffold(q0,qf):
    """Map final R Wirtinger arcs to scaffold arcs using inherited ports."""
    mp={}
    for (c,p),af in qf['arcs'].items():
        if c < len(SCAFFOLD) and (c,p) in q0['arcs']:
            a0=q0['arcs'][(c,p)]
            if af in mp and mp[af]!=a0:raise RuntimeError('R arc map inconsistent')
            mp[af]=a0
    assert len(mp)==1+max(qf['arcs'].values())
    return mp

def main():
    a0=adjacency_from_pd(SCAFFOLD)
    once=add_zero_twist_band(a0,BAND1)
    final=add_zero_twist_band(once,BAND2)
    q0=quotient_R_wirtinger(a0,0);qf=quotient_R_wirtinger(final,0)
    assert len(q0['relations'])==18 and len(qf['relations'])==18
    assert len(set(q0['arcs'].values()))==18 and len(set(qf['arcs'].values()))==18
    sols=solve_colourings(q0)
    assert len(sols)==49, len(sols)
    # Scaffold BFS names are exactly the ones recorded in pass06.
    names={0:'R',1:'c2_upper',2:'c1_upper',3:'c2_lower',4:'c1_lower'}
    traces=Counter(); witness=[]
    for sol in sols:
        vals={names[i]:loop_value(a0,q0,sol,i) for i in range(1,5)}
        tq=(tr(vals['c1_upper']),tr(vals['c2_upper']),tr(vals['c1_lower']),tr(vals['c2_lower']))
        traces[tq]+=1
        if tq==(1,4,1,4):witness.append((sol,vals))
    assert traces==Counter({(1,4,1,4):36,(1,4,2,2):6,(2,2,1,4):6,(2,2,2,2):1}), traces
    fmap=map_final_R_arcs_to_scaffold(q0,qf)
    outcome=Counter();examples={}
    for sol,oldvals in witness:
        fsol=tuple(sol[fmap[i]] for i in range(len(fmap)))
        eta1=loop_value(final,qf,fsol,1);eta2=loop_value(final,qf,fsol,2)
        key=(tr(eta1),tr(eta2),order(eta1),order(eta2),conjugate(eta1,eta2))
        outcome[key]+=1;examples.setdefault(key,{'eta1':eta1,'eta2':eta2})
    expected=Counter({
      (2,2,5,5,True):6,
      (4,4,3,3,True):6,
      (0,2,4,5,False):6,
      (2,0,5,4,False):6,
      (4,0,3,4,False):6,
      (0,3,4,2,False):6,
    })
    assert outcome==expected,(outcome,expected)
    separated=sum(n for k,n in outcome.items() if not k[-1]);surviving=sum(n for k,n in outcome.items() if k[-1])
    assert separated==24 and surviving==12
    # Positive control: original corresponding axes have compatible conjugacy
    # up to inversion in every witness/witness branch.
    for _,vals in witness:
        assert conjugate(vals['c1_upper'],vals['c1_lower'])
        assert conjugate(vals['c2_upper'],vals['c2_lower'])
    result={
      'status':'BRANCH_GATE_PARTIAL_24_OF_36_SEPARATED_NO_COUNTEREXAMPLE',
      'source_commit':SOURCE_COMMIT,
      'bands':[BAND1['compressed_spec'],BAND2['compressed_spec']],
      'sl2_f5_order':len(G),
      'fixed_meridian':MERIDIAN,
      'R_wirtinger_arcs':18,
      'all_colourings_with_fixed_meridian':len(sols),
      'end_trace_distribution':[{ 'traces':list(k),'count':v} for k,v in sorted(traces.items())],
      'witness_witness_branches':len(witness),
      'eta_outcomes':[
        {'eta1_trace':k[0],'eta2_trace':k[1],'eta1_order':k[2],'eta2_order':k[3],
         'conjugate_up_to_inversion':k[4],'count':v,
         'example_eta1':list(examples[k]['eta1']),'example_eta2':list(examples[k]['eta2'])}
        for k,v in sorted(outcome.items())
      ],
      'branches_separated_by_F5':separated,
      'branches_surviving_F5':surviving,
      'positive_control':'Every witness/witness branch makes each corresponding original upper/lower axis pair conjugate up to inversion in SL(2,F5).',
      'interpretation':'Unbased end-circle data do not select the actual product-disk based-whisker branch. Four of six relative branch types are killed; two survive. The scaffold must be upgraded with a based lower-to-upper whisker map before this finite quotient can decide the explicit band pair.',
      'counterexample':False,
    }
    print('PASS SL(2,F5) has 120 elements')
    print('PASS 49 fixed-meridian colourings = 7 x 7 end-factor count')
    print('PASS 36 witness/witness branches with end traces (1,4,1,4)')
    print('PASS all corresponding original axis pairs conjugate up to inversion')
    print('PASS eta branch gate: 24 separated, 12 survive')
    print(json.dumps(result,indent=2,sort_keys=True))
    return result

if __name__=='__main__':main()
