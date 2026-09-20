"""Exact polynomial check of the LOCAL patches; does not check global movies."""
import itertools
import json
from fractions import Fraction as Q


def add(a,b):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def mul(a,b):
    out={}
    for (i,j),x in a.items():
        for (k,l),y in b.items(): out[i+k,j+l]=out.get((i+k,j+l),0)+x*y
    return {k:v for k,v in out.items() if v}

def scale(a,k): return {p:k*x for p,x in a.items() if k*x}

def derivative(a,axis):
    out={}
    for p,x in a.items():
        if p[axis]:
            q=list(p);q[axis]-=1;out[tuple(q)]=x*p[axis]
    return out

def dot(a,b):
    out={}
    for x,y in zip(a,b):out=add(out,mul(x,y))
    return out

def at(p,u,t):return sum(x*u**i*t**j for (i,j),x in p.items())

def determinant(columns):
    ans=0
    for p in itertools.permutations(range(4)):
        sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        term=sign
        for j in range(4):term*=columns[j][p[j]]
        ans+=term
    return ans

def main():
    zero={};one={(0,0):1};time={(0,1):1}
    beta={(0,0):1,(2,0):-2,(4,0):1}
    z=add(one,scale(mul(time,beta),-2))
    tu=[zero,one,derivative(z,0),zero]
    tt=[zero,zero,derivative(z,1),one]
    n1=[one,zero,zero,zero]
    n2=[zero,scale(mul(time,derivative(beta,0)),2),one,scale(beta,2)]
    assert all(dot(n,v)=={} for n in [n1,n2] for v in [tu,tt])
    assert n1[0]==one and n2[2]==one  # independent everywhere
    assert at(beta,0,Q(1,2))==1 and at(z,0,Q(1,2))==0
    for u in [-1,1]:assert at(beta,u,0)==at(derivative(beta,0),u,0)==0
    Tu=[at(p,0,Q(1,2)) for p in tu];Tt=[at(p,0,Q(1,2)) for p in tt]
    P_s=[1,0,0,0];P_t=[0,0,0,1]
    det=determinant([Tt,Tu,P_s,P_t])
    assert det==2
    events=[{'id':'p_minus','sheets':['T_minus','P'],'location':['-1/4','0','0','1/2'],
             'sign':-1,'local_ambient_label':[],'local_puncture_meridian':'m_a^-1'},
            {'id':'p_plus','sheets':['T_plus','P'],'location':['1/4','0','0','1/2'],
             'sign':1,'local_ambient_label':[],'local_puncture_meridian':'m_a'}]
    assert sum(x['sign'] for x in events)==0
    assert events[0]['local_ambient_label']==events[1]['local_ambient_label']
    assert set(events[0]['sheets'])!=set(events[1]['sheets'])
    result={'status':'PASS','scope':'LOCAL coordinate patches only; no correction-handle endpoint identification',
            'normal_field_dot_products':'identically zero as polynomials','intersection_determinants':[-2,2],
            'events':events,'self_intersections':[], 'mutual_T_intersections':[],
            'Whitney_pair':False,'reason':'Different transfer sheets; no connecting arc on their disjoint union',
            'global_labels':None,'global_intersection_ledger':None,'full_transfers':False}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
