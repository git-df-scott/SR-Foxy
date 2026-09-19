"""One geometrically specified ribbon stabilizer and one exact split prefix.

No partner sweep, invariants, random simplification, or band search. The
remaining ribbon certificate for D01#J is UNKNOWN. See STABILIZER.md.
"""
import hashlib
import json
from pathlib import Path
import resource
import spherogram
from spherogram import Link

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def pd(card): return card.get('pd_code') or card['pd_code_snappy_0indexed']

def diagram(link):
    return {'pd_code':link.PD_code(),'crossings':len(link.crossings),
            'components':len(link.link_components),'writhe':link.writhe(),
            'tagged_adjacency':[{'crossing':c.label,'sign':c.sign,
                 'neighbors':[[d.label,p] for d,p in c.adjacent]} for c in link.crossings]}

def main():
    resource.setrlimit(resource.RLIMIT_CPU,(30,35))
    out=HERE/'stabilizer.json'
    if out.exists(): raise FileExistsError(out)
    files=[ROOT/'data/knots/AbeTagami_K_0_K_-1__6_3.json',
           ROOT/'data/knots/AbeTagami_D_0_1.json']
    K,D=[Link(pd(json.loads(p.read_text()))) for p in files]
    alpha=K.braid_word()
    assert alpha==[1,-2,1,-2,-2,1]
    n=max(map(abs,alpha))+1
    # Braids on two n-strand blocks sharing one strand give connected sum.
    beta=alpha+[-(1 if x>0 else -1)*(abs(x)+n-1) for x in alpha]
    R=Link(braid_closure=beta)
    assert len(R.link_components)==1 and R.writhe()==sum(1 if x>0 else -1 for x in beta)==0
    doubled=[]; blocks=[]
    for i,x in enumerate(beta):
        j=abs(x); sign=1 if x>0 else -1
        block=[2*j,2*j-1,2*j+1,2*j]
        if sign<0: block=[-v for v in reversed(block)]
        blocks.append({'source_crossing':i,'source_generator':x,'cable_start':len(doubled),'block':block})
        doubled+=block
    # Independently read each component's braid after forgetting the other.
    colors=[0,1]*(2*n-1); component_words=[[],[]]; mixed_signed=0
    for x in doubled:
        j=abs(x); a,b=colors[j-1:j+1]
        if a==b:
            within=sum(v==a for v in colors[:j])
            component_words[a].append((1 if x>0 else -1)*within)
        else: mixed_signed+=1 if x>0 else -1
        colors[j-1],colors[j]=colors[j],colors[j-1]
    assert colors==[0,1]*(2*n-1)
    assert component_words==[beta,beta]
    assert mixed_signed==0  # preferred-zero parallel framing, not a split-link assertion
    cable_word=doubled+[1]
    J=Link(braid_closure=cable_word)
    P=Link(braid_closure=doubled)
    assert len(J.link_components)==1 and len(P.link_components)==2
    assert len(J.crossings)==49 and len(P.crossings)==48
    for i,c in enumerate(J.crossings): c.label=i
    for i,c in enumerate(D.crossings): c.label=i
    S=D.connected_sum(J)
    assert len(S.crossings)==74 and len(S.link_components)==1
    T=S.copy()
    cap=next(c for c in T.crossings if c.label==(48,2))
    incoming={p for p in range(4) if cap.is_incoming(p)}
    options=[[(0,1),(2,3)],[(0,3),(1,2)]]
    valid=[pairs for pairs in options if all((a in incoming)!=(b in incoming) for a,b in pairs)]
    assert len(valid)==1
    pairs=valid[0]
    attachments=[]
    for a,b in pairs:
        x,i=cap.adjacent[a];y,j=cap.adjacent[b]
        assert x is not cap and y is not cap
        attachments.append({'removed_ports':[a,b],'join':[[x.label,i],[y.label,j]]})
        x[i]=y[j]
    T=Link([c for c in T.crossings if c is not cap])
    assert T.is_planar() and len(T.link_components)==2 and len(T.crossings)==73
    # The connected-sum cut was in cable crossing 0, disjoint from crossing 48.
    # Smoothing therefore leaves D tied into exactly one of the two R copies.
    sizes=[]
    for ci in range(2):
        sub=T.sublink([ci]); sizes.append(len(sub.crossings))
    assert sorted(sizes)==[12,37]
    report={'scope':'One ribbon stabilizer J and one obstructed ribbon-prefix attempt on D01#J; no certificate for D01#J',
            'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
            'spherogram_version':spherogram.__version__,
            'K0_braid':alpha,'R_braid':beta,'R':diagram(R),
            'doubling_blocks':blocks,'zero_parallel_braid':doubled,
            'component_braid_projection':component_words,'parallel_linking_number':mixed_signed//2,
            'J_braid':cable_word,'J':diagram(J),'D01_connected_sum_J':diagram(S),
            'prefix':{'operation':'Oriented saddle smoothing the specified final cable crossing',
                      'crossing_tag':[48,2],'incoming_ports':sorted(incoming),'attachments':attachments,
                      'result':diagram(T),'isolated_component_crossing_counts':sizes,
                      'identified_component_types':['R','D01#R'],
                      'component_identification_reason':'Deleting the final sigma1 leaves two preferred-zero parallel R copies; the connected-sum insertion is disjoint from the deleted crossing.'},
            'ribbon_J':'Two disjoint zero-framed parallel copies of the explicit product ribbon disk joined by one positive half-twisted boundary band; chi=1, no maxima.',
            'ribbon_D01_sum_J':'UNKNOWN',
            'prefix_failure':'A ribbon disk starting with this split saddle would give separate ribbon disks for both output components; D01#R is nonribbon by the already certified prime-fibered irreducible-Delta pairing argument.',
            'limits':'30 CPU seconds; one fixed 74-crossing diagram; no invariant computation or search'}
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'J_crossings':49,'sum_crossings':74,'split_link_crossings':73,
                      'output_component_crossings':sizes,'J_ribbon':'geometric construction',
                      'D01_sum_J_ribbon':'UNKNOWN','prefix':'specified cable-splitting saddle'}))

if __name__=='__main__': main()
