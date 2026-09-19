#!/usr/bin/env python3
"""Exact-data research figures; drawn knot crossings come from Spherogram PDs."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import snappy
from spherogram.links.orthogonal import OrthogonalLinkDiagram


def knot_panel(ax, pd, color):
    vertices, arrows, crossings = OrthogonalLinkDiagram(snappy.Link(pd)).plink_data()
    for a,b in arrows:
        ax.plot([vertices[a][0],vertices[b][0]], [vertices[a][1],vertices[b][1]],color=color,lw=2.7,solid_capstyle='round')
    # break_into_arrows gives (UNDER, OVER), despite the plink_data docstring.
    for under,over,_,label in crossings:
        u,v=[vertices[i] for i in arrows[under]]
        a,b=[vertices[i] for i in arrows[over]]
        if u[0]==v[0]: x,y=u[0],a[1]
        else: x,y=a[0],u[1]
        assert min(u[0],v[0])<=x<=max(u[0],v[0]) and min(u[1],v[1])<=y<=max(u[1],v[1])
        assert min(a[0],b[0])<=x<=max(a[0],b[0]) and min(a[1],b[1])<=y<=max(a[1],b[1])
        dx,dy=(2.4,0) if a[1]==b[1] else (0,2.4)
        ax.plot([x-dx,x+dx],[y-dy,y+dy],color='white',lw=7,solid_capstyle='butt')
        ax.plot([x-dx,x+dx],[y-dy,y+dy],color=color,lw=2.7,solid_capstyle='butt')
    ax.set_aspect('equal'); ax.invert_yaxis(); ax.axis('off'); ax.margins(.10)
    return len(crossings)


def render(output):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    d=json.loads(Path('results/fusion_HFK_filter_all.json').read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig,axes=plt.subplots(1,3,figsize=(12,5.8),sharex=True,sharey=True)
    datasets=d['source_ranks']+[d['required_ranks']]
    titles=['K₀: 13 generators','K₁: 13 generators','Any common successor: at least 21']
    for ax,rows,title,col in zip(axes,datasets,titles,['#24647d','#ab5730','#633f87']):
        for a,m,n in rows:
            ax.scatter(a,m,s=250+n*65,c=col,zorder=3)
            ax.text(a,m,str(n),ha='center',va='center',color='white',weight='bold',zorder=4)
        ax.set_title(title,pad=14,fontsize=11,weight='bold');ax.set_xlabel('Alexander grading A')
        ax.set_xticks(range(-2,3));ax.set_yticks(range(-4,3));ax.set_xlim(-2.6,2.6);ax.set_ylim(-4.6,2.6)
        ax.grid(color='#e1e5e8',lw=.7);ax.spines[['top','right']].set_visible(False)
    axes[0].set_ylabel('Maslov grading M')
    fig.suptitle('A target must have room for both knots',fontsize=19,weight='bold',y=.98)
    fig.text(.5,.055,'Numbers are exact ranks over F₂. Each required rank is the larger of the two source ranks.\nZemke, Theorem 1.2: ribbon concordance induces a grading-preserving injection. Passing is necessary, not sufficient.',ha='center',fontsize=10,color='#404850')
    fig.subplots_adjust(top=.83,bottom=.23,wspace=.20)
    for ext in ['png','svg']:fig.savefig(out/f'common-successor-filter.{ext}',dpi=180,facecolor='white')
    plt.close(fig)
    w=json.loads(Path('results/fusion_AT0_hyperbolic_display_witness.json').read_text())
    # Witness file can contain the raw witness directly or under 'witness'.
    w=w.get('witness',w)
    source=json.loads(Path('data/knots/AbeTagami_K_0_K_-1__6_3.json').read_text())['pd_code_snappy_0indexed']
    fig,axes=plt.subplots(1,3,figsize=(13,5.5))
    pds=[source,w['birth_pd'],w['endpoint_pd']]
    labels=['Start: K₀ = 6₃','Birth an unknot; overlap by isotopy','Fuse by a band: a new successor']
    counts=[]
    for ax,pd,label in zip(axes,pds,labels):
        counts.append(knot_panel(ax,pd,'#24647d'));ax.set_title(label,fontsize=11,weight='bold',pad=18)
    fig.suptitle('An actual move from the search',fontsize=19,weight='bold',y=.99)
    fig.text(.5,.04,'This 12-crossing endpoint is a valid one-sided search witness, but fails the common-successor Floer test.\nPanels show stored diagrams; the band and simplification replay data are saved separately. This is not a counterexample.',ha='center',fontsize=10,color='#404850')
    fig.subplots_adjust(top=.80,bottom=.19,wspace=.18)
    for ext in ['png','svg']:fig.savefig(out/f'fusion-example.{ext}',dpi=180,facecolor='white')
    print('Rendered crossing counts:',counts)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();render(a.output)
