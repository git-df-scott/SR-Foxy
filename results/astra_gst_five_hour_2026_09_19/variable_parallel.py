"""Componentwise zero-framed braid parallels, multiplicities0..3."""
import snappy
from selective_cable import data

def parallel(word,mults):
 n,cycles,colors=data(word);assert len(mults)==len(cycles)
 widths={s:mults[colors[s]] for s in range(n)};pos=list(range(n));wr=[0]*len(cycles);out=[]
 for g in word:
  i=abs(g)-1;sgn=1 if g>0 else -1;a,b=pos[i:i+2];p,q=widths[a],widths[b];base=sum(widths[s] for s in pos[:i])
  for u in range(p):
   for z in range(q):out.append(sgn*(base+p-u+z))
  if colors[a]==colors[b]:wr[colors[a]]+=sgn
  pos[i],pos[i+1]=b,a
 for ci,cycle in enumerate(cycles):
  p=mults[ci];base=sum(widths[s] for s in range(min(cycle)));sgn=-1 if wr[ci]>0 else 1
  for _ in range(p*abs(wr[ci])):
   for a in range(p-1):out.append(sgn*(base+a+1))
 ns=sum(widths.values());assert ns>=2
 if not out or max(map(abs,out))<ns-1:out.extend([ns-1,-(ns-1)])
 L=snappy.Link(braid_closure=out);assert len(L.link_components)+L.unlinked_unknot_components==sum(mults)
 assert not any(x for r in L.linking_matrix() for x in r)
 return L,{'input_braid':word,'cycles':cycles,'multiplicities':mults,'self_writhes':wr,'output_braid':out,'raw_pd':L.PD_code(),'linking_matrix':L.linking_matrix()}
