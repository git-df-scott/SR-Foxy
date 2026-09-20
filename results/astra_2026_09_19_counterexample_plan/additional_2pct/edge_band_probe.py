"""Keep literal attaching edges and every internal dual edge; finite simple paths only."""
from itertools import combinations,product
from pathlib import Path
from collections import Counter
import sys,json,time,random,inspect,hashlib
import networkx as nx
from spherogram import Link
from spherogram.links.bands.core import Band,simple_bands,normalize_crossing_labels,dual_graph_as_nx,add_one_band
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from whitehead_replay import alexander_rank_upper_bound,linking_number
P=Path(__file__).parent

def edge_bands(L,length,twists):
 normalize_crossing_labels(L);dual=dual_graph_as_nx(L,graph_class=nx.MultiGraph)
 faces={cs:F for A,B,info in dual.edges(data=True) for F,cs in info['interface'].items()}
 out={}
 for component in L.link_components:
  for a,b in combinations(component,2):
   for X,Y in product([a,a.opposite()],[b,b.opposite()]):
    F,G=faces[X],faces[Y];before,after=faces[X.opposite()],faces[Y.opposite()]
    paths={(F,)} if F==G else set(map(tuple,nx.all_simple_paths(dual,F,G,cutoff=length-2)))
    for path in paths:
     if not nx.is_simple_path(dual,(before,)+path+(after,)):continue
     internal=[[info['interface'][v] for info in dual[u][v].values()] for u,v in zip(path,path[1:])]
     for middle in product(*internal):
      cs=[X,*middle,Y.opposite()]
      spec=[(c.crossing.label,c.strand_index) for c in cs]
      parity=int((cs[0]==cs[0].oriented())==(cs[-1]==cs[-1].oriented()))
      for twist in range(-twists,twists+1):
       if twist%2!=parity:continue
       for bits in range(2**len(middle)):
        band=Band(spec,bits,twist)
        if not band.is_nonminimal(L):out[band.compressed_spec()]=band
 return out

def main():
 random.seed(20260919);start=time.monotonic();controls=[]
 length=int(sys.argv[1]) if len(sys.argv)>1 else 3; twists=int(sys.argv[2]) if len(sys.argv)>2 else 1
 tag=f"L{length}_T{twists}"
 for name in ['3_1','4_1','6_1','6_3']:
  L=Link(name);normalize_crossing_labels(L)
  old={b.compressed_spec() for b in simple_bands(L,max_twists=1,max_band_len=3)}
  new=edge_bands(L,3,1)
  assert old<=new.keys(),(name,old-new.keys())
  for b in new.values():assert len(add_one_band(L,b).link_components)==2
  controls.append({'knot':name,'old_distinct':len(old),'new_distinct':len(new),'old_included':True,'all_outputs_two_components':True})
 L=Link(json.loads((P/'gst48.json').read_text())['pd']);normalize_crossing_labels(L)
 old={b.compressed_spec() for b in simple_bands(L,max_twists=twists,max_band_len=length)};new=edge_bands(L,length,twists)
 assert old<=new.keys()
 specs=sorted(set(new)-old);counts=Counter();survivors=[]
 with (P/f'GST_NEW_EDGES_{tag}.jsonl').open('w') as f:
  for spec in specs:
   out=add_one_band(L,new[spec]);assert len(out.link_components)==2
   lk=linking_number(out);row={'band':spec,'linking':lk}
   if lk:row['status']='linking_exclusion'
   else:
    rank=alexander_rank_upper_bound(out);row['rank_upper_bound']=rank
    row['status']='rank_exclusion' if rank==0 else 'unexcluded'
    if rank:row['pd']=out.PD_code();survivors.append(row)
   counts[row['status']]+=1;f.write(json.dumps(row)+'\n')
 result={'controls':controls,'target':'literal GST48 PD, publisher-attributed GST identity','max_band_len':length,'max_twists':twists,'old_distinct':len(old),'edge_preserving_distinct':len(new),'additional_descriptors':len(specs),'counts':dict(counts),'survivors':survivors,'seconds':time.monotonic()-start,'upstream_simple_bands_sha256':hashlib.sha256(inspect.getsource(simple_bands).encode()).hexdigest(),'scope':'Finite generator experiment. Descriptors need not be distinct band isotopy classes. Passing necessities is not sliceness; no global nonribbon conclusion.'}
 (P/f'GST_EDGE_PROBE_{tag}.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='survivors'}),flush=True)
if __name__=='__main__':main()
