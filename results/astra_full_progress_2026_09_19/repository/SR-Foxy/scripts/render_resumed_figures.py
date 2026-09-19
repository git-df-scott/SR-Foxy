#!/usr/bin/env python3
"""Render actual PD diagrams and the missing concordance arrow."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import snappy
from spherogram.links.orthogonal import OrthogonalLinkDiagram
import regina


def draw(ax,pd,colors=('#2466a2','#d18b18')):
    vertices,edges,crossings=OrthogonalLinkDiagram(snappy.Link(pd)).plink_data()
    v=np.array(vertices,dtype=float);next_edge={a:(i,b) for i,(a,b) in enumerate(edges)}
    edge_colors={};seen=set();component=0
    for a,b in edges:
        if a in seen:continue
        x=a
        while x not in seen:
            seen.add(x);i,y=next_edge[x];edge_colors[i]=colors[component%len(colors)];x=y
        component+=1
    for i,(a,b) in enumerate(edges):ax.plot(v[[a,b],0],v[[a,b],1],color=edge_colors[i],lw=2.4,solid_capstyle='round',zorder=1)
    # break_into_arrows actually emits (under, over, virtual, label);
    # plink_data's short docstring reverses the first two fields.
    for under,over,virtual,label in crossings:
        assert not virtual
        a,b=edges[over];c,d=edges[under]
        mat=np.column_stack((v[b]-v[a],-(v[d]-v[c])))
        t,s=np.linalg.solve(mat,v[c]-v[a]);assert 0<t<1 and 0<s<1
        pt=v[a]+t*(v[b]-v[a]);direction=(v[b]-v[a])/np.linalg.norm(v[b]-v[a]);ends=np.array([pt-3.2*direction,pt+3.2*direction])
        ax.plot(ends[:,0],ends[:,1],color='white',lw=7,zorder=2,solid_capstyle='butt')
        ax.plot(ends[:,0],ends[:,1],color=edge_colors[over],lw=2.4,zorder=3,solid_capstyle='butt')
    ax.set_aspect('equal');ax.invert_yaxis();ax.axis('off');ax.margins(.08)


def save(fig,name):
    out=Path('research/figures');out.mkdir(exist_ok=True)
    for ext in ['png','svg']:fig.savefig(out/(name+'.'+ext),dpi=180,facecolor='white',bbox_inches='tight')
    plt.close(fig)


def run():
    K0=json.loads(Path('data/knots/AbeTagami_K_0_K_-1__6_3.json').read_text())['pd_code_snappy_0indexed']
    K1=json.loads(Path('data/knots/AbeTagami_K_1.json').read_text())['pd_code_snappy_0indexed']
    J=json.loads(Path('results/coupled_small_targets.json').read_text())['candidates'][0]['endpoint_pd']
    fig=plt.figure(figsize=(11,7))
    for rect,pd,title in [([.03,.55,.36,.34],K0,'K₀ = 6₃'),([.03,.1,.36,.34],K1,'K₁: stored 19-crossing diagram'),([.58,.22,.39,.57],J,'J: new genus-four target')]:
        ax=fig.add_axes(rect);draw(ax,pd);ax.set_title(title,fontsize=12,pad=10)
    for start,end,color,style in [((.37,.68),(.59,.57),'#2466a2','-'),((.37,.30),(.59,.47),'#b34239','--')]:
        fig.add_artist(FancyArrowPatch(start,end,transform=fig.transFigure,arrowstyle='-|>',mutation_scale=15,color=color,linestyle=style,lw=2))
    fig.text(.41,.66,'Saved ribbon\nconcordance movie',fontsize=10,color='#2466a2')
    fig.text(.41,.23,'Missing movie:\nthe research target',fontsize=10,color='#b34239')
    fig.suptitle('A concrete target, with one essential arrow still missing',fontsize=17,y=.98)
    fig.text(.05,.015,'Unoriented knot diagrams. The dashed arrow has not been constructed. No counterexample is established.',fontsize=10,color='#444444')
    save(fig,'resumed_common_target')
    record=json.loads(Path('results/coupled_K0_double_return_jones_regina.json').read_text())['checks'][-1]
    assert record['nonsplit_by_Jones'];pd=record['pd']
    G=regina.Link.fromPD([[a+1 for a in c] for c in pd]);p=G.jones(regina.Algorithm.Treewidth)
    coeff=[(i,int(str(p[i]))) for i in range(p.minExp(),p.maxExp()+1)]
    H=regina.Link.fromPD([[a+1 for a in c] for c in pd]);naive=H.jones(regina.Algorithm.Naive)
    assert coeff==[(i,int(str(naive[i]))) for i in range(naive.minExp(),naive.maxExp()+1)]
    def evaluate(poly):return sum(c*pow(-2,e,101) for e,c in poly)%101
    actual=evaluate(coeff)
    # Work in Regina's x convention; x=-2 corresponds to q=2.
    product=(-(-2+pow(-2,-1,101)))%101
    for component in record['component_pd']:
        if not component:continue
        C=regina.Link.fromPD([[a+1 for a in c] for c in component]);P=C.jones()
        product=product*evaluate([(i,int(str(P[i]))) for i in range(P.minExp(),P.maxExp()+1)])%101
    assert actual!=product
    certificate={'record':'results/coupled_K0_double_return_jones_regina.json','first_id':record['first_id'],
        'q':2,'prime':101,'link_Jones_value':actual,'split_product_value':product,
        'Regina_treewidth_equals_naive':True,'Jones_x_coefficients':coeff}
    Path('results/coupled_nonsplit_two_algorithm_check.json').write_text(json.dumps(certificate,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(10,6));draw(ax,pd)
    ax.set_title('A verified nonsplit intermediate link with linking number zero',fontsize=15,pad=20)
    fig.text(.1,.03,f'Exact Jones test at q = 2 modulo 101: link = {actual}, split product = {product}. Unequal ⇒ nonsplit.',fontsize=11)
    save(fig,'resumed_nonsplit_intermediate')


if __name__=='__main__':run()
