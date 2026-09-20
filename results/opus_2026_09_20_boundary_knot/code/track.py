"""Build the stored 675-crossing surgery link, keep track of which spherogram
component is R / a / b', simplify, and reorder so cusp i == original component i.
Original indexing (from surgery_diagram.json): 0 = R, 1 = a, 2 = b'."""
import json, collections, snappy, spherogram, gaussbuild as GB
D='/home/user/SR-Foxy/results/astra_genus_one_2026_09_18/'

def load():
    dg=json.load(open(D+'surgery_diagram.json'))
    gw=[[list(c) for c in w] for w in dg['gauss_words']]
    under_comp={c['id']: c['under'][0] for c in dg['crossings']}
    over_comp={c['id']: c['over'][0] for c in dg['crossings']}
    return dg, gw, under_comp, over_comp

def comp_map(L, under_comp, over_comp):
    """Return list perm with perm[j] = original component index of L.link_components[j]."""
    perm=[]
    for j,comp in enumerate(L.link_components):
        votes=collections.Counter()
        for ep in comp:
            c=ep.crossing
            if c.label not in under_comp: continue
            if ep.strand_index==0: votes[under_comp[c.label]]+=1
            else: votes[over_comp[c.label]]+=1
        perm.append(votes.most_common(1)[0] if votes else (None,0))
    return perm

def reorder(L, order):
    """order: list of current component indices in the wanted new order."""
    starts=[L.link_components[i][0] for i in order]
    L._build_components(component_starts=starts)
    return L
