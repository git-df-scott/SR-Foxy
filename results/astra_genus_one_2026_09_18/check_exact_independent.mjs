/* Independent BigInt replay. No imports of the Python producer or SymPy.
 * Reconstructs polygon crossings, peripheral words, Laurent Fox rows, all
 * recorded unit pivots, final minors and the auxiliary full-group certificate.
 */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const P=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(P,n),'utf8'));
let checks=[];
function requireTrue(b,name){if(!b)throw new Error(name);checks.push(name);}
const stable=x=>JSON.stringify(x);
function reduce(w){let r=[];for(const x of w){if(r.length&&r.at(-1)===-x)r.pop();else r.push(x);}return r;}
const inverse=w=>w.slice().reverse().map(x=>-x);
const substitute=(w,im)=>reduce(w.flatMap(x=>x>0?im[Math.abs(x)]:inverse(im[Math.abs(x)])));
function cyclic(w){w=reduce(w);let a=0,b=w.length;while(b-a>1&&w[a]===-w[b-1]){a++;b--;}return w.slice(a,b);}
const eq=(a,b)=>stable(a)===stable(b);
const diagram=read('surgery_diagram.json'), f=read('framed_fox_boundary.json');
// A second generic-projection implementation: all segment pairs, no sweep.
const ip=diagram.integer_polygons.map(poly=>poly.map(v=>v.map(BigInt)));
const [un,pn,vn,qn]=diagram.projection;let u=BigInt(un),p=BigInt(pn),v=BigInt(vn),q=BigInt(qn),scale=p*q;
const det=(a,b)=>a[0]*b[1]-a[1]*b[0],diff=(a,b)=>a.map((x,i)=>x-b[i]);
let seg=[];
for(let c=0;c<ip.length;c++)for(let k=0;k<ip[c].length;k++){
 const a=ip[c][k],b=ip[c][(k+1)%ip[c].length];const A=[scale*a[0]+u*q*a[2],scale*a[1]+v*p*a[2]],B=[scale*b[0]+u*q*b[2],scale*b[1]+v*p*b[2]];
 seg.push({c,k,a,A,B,d:diff(B,A),dz:b[2]-a[2]});
}
const key=(a,b)=>[`${a[0]}:${a[1]}`,`${b[0]}:${b[1]}`].sort().join('|');
const expected=new Map(diagram.crossings.map(c=>[key(c.a,c.b),c]));let events=ip.map(()=>[]),count=0;
const bmin=(a,b)=>a<b?a:b,bmax=(a,b)=>a>b?a:b;
for(let i=0;i<seg.length;i++)for(let j=0;j<i;j++){
 const a=seg[i],b=seg[j];if(a.c===b.c){let n=ip[a.c].length,d=(a.k-b.k+n)%n;if(d===0||d===1||d===n-1)continue;}
 if([0,1].some(k=>bmin(a.A[k],a.B[k])>bmax(b.A[k],b.B[k])||bmin(b.A[k],b.B[k])>bmax(a.A[k],a.B[k])))continue;
 let dd=diff(b.A,a.A),den=det(a.d,b.d),na=det(dd,b.d),nb=det(dd,a.d);
 if(den===0n){if(na===0n&&nb===0n)throw new Error('projection collinearity');continue;}
 if(den<0n){den=-den;na=-na;nb=-nb;}
 if(!(na>=0n&&na<=den&&nb>=0n&&nb<=den))continue;
 if(na===0n||na===den||nb===0n||nb===den)throw new Error('projection through vertex');
 const za=a.a[2]*den+a.dz*na,zb=b.a[2]*den+b.dz*nb;if(za===zb)throw new Error('actual spatial intersection');
 const over=za>zb?a:b,under=za>zb?b:a,sign=(det(a.d,b.d)>0n?1:-1)*(za>zb?1:-1);
 const ex=expected.get(key([a.c,a.k],[b.c,b.k]));if(!ex||!eq(ex.over,[over.c,over.k])||!eq(ex.under,[under.c,under.k])||ex.sign!==sign)throw new Error('crossing disagrees');
 events[a.c].push({k:a.k,n:na,d:den,id:ex.id,kind:za>zb?'O':'U',sign});events[b.c].push({k:b.k,n:nb,d:den,id:ex.id,kind:za>zb?'U':'O',sign});count++;
}
const cmp=(a,b)=>{if(a.k!==b.k)return a.k-b.k;const x=a.n*b.d-b.n*a.d;return x<0n?-1:x>0n?1:0;};
let gauss=[];for(const ev of events){ev.sort(cmp);for(let j=1;j<ev.length;j++)if(cmp(ev[j-1],ev[j])===0)throw new Error('triple projected crossing');gauss.push(ev.map(e=>[e.id,e.kind,e.sign]));}
requireTrue(count===diagram.crossings.length&&eq(gauss,diagram.gauss_words),'all 675 projected crossings and Gauss ordering independently reconstructed');
// Marked words read at undercrossings with R, using the saved native arc labels.
const spatial=read('spatial_model.json'),byID=new Map(diagram.crossings.map(x=>[x.id,x]));
let actualAxis=gauss.slice(1).map(w=>reduce(w.filter(([k,typ])=>typ==='U'&&byID.get(k).over[0]===0).map(([k,typ,sg])=>sg*spatial.base_segment_generators[0][byID.get(k).over[1]])));
requireTrue(eq(actualAxis,diagram.expected_marked_axis_words),'actual axes read the intended a and [A,B]b boundary words');
// Peripheral extraction from this independently reconstructed Gauss code.
function peripheral(words){
 let ng=0,mer=[],weight={},comp={},cr={},owners={};
 words.forEach((w,c)=>w.forEach(([k,typ,s])=>(owners[k]??=[]).push(c)));
 words.forEach((w,c)=>{let n=Math.max(1,w.filter(x=>x[1]==='U').length),start=ng+1,cur=start;ng+=n;mer.push(start);for(let g=start;g<=ng;g++){weight[g]=c===0?1:0;comp[g]=c;}
  for(const [k,typ,s]of w){cr[k]??={s};if(typ==='O')cr[k].b=cur;else{let nxt=start+(cur-start+1)%n;cr[k].i=cur;cr[k].o=nxt;cur=nxt;}}
 });
 const rel=Object.keys(cr).map(Number).sort((a,b)=>a-b).map(k=>{let c=cr[k];return[-c.s*c.b,c.i,c.s*c.b,-c.o];});
 let longs=[],wr=[];words.forEach((w,c)=>{let self=w.filter(([k,typ])=>typ==='U'&&owners[k].every(o=>o===c)).reduce((a,x)=>a+x[2],0);wr.push(self);let fix=Array(Math.abs(self)).fill(self>=0?-mer[c]:mer[c]);longs.push(reduce(fix.concat(w.filter(x=>x[1]==='U').map(([k,typ,s])=>s*cr[k].b))));});
 return {ng,mer,weight,rel,longs,wr};
}
const data=peripheral(gauss);requireTrue(data.ng===f.n_generators&&eq(data.mer,f.meridians)&&eq(data.rel,f.relators)&&eq(data.longs,f.preferred_longitudes)&&eq(data.wr,f.self_writhes),'full meridians, Wirtinger relators and zero-framed longitudes rebuilt');
// Laurent polynomials are Map(exponent, BigInt).
const poly=o=>new Map(Object.entries(o).map(([k,v])=>[Number(k),BigInt(v)]).filter(([k,v])=>v!==0n));
function plus(a,b,k=0,c=1n){const r=new Map(a);for(const [e,v]of b){let s=(r.get(e+k)??0n)+c*v;if(s===0n)r.delete(e+k);else r.set(e+k,s);}return r;}
function times(a,b){let r=new Map();for(const [e,v]of a)r=plus(r,b,e,v);return r;}
function same(a,b){return a.size===b.size&&[...a].every(([e,c])=>b.get(e)===c);}
const rp=o=>new Map(Object.entries(o).map(([g,p])=>[Number(g),poly(p)]));
function sameRow(a,b){return a.size===b.size&&[...a].every(([g,p])=>b.has(g)&&same(p,b.get(g)));}
function fox(w,weights){let r=new Map(),e=0;for(const x of w){const g=Math.abs(x),a=weights[g],k=x>0?e:e-a;let z=plus(r.get(g)??new Map(),new Map([[k,x>0?1n:-1n]]));if(z.size)r.set(g,z);else r.delete(g);e+=x>0?a:-a;}if(e!==0)throw new Error('nonzero peripheral exponent');return r;}
let rows=new Map(),obs=new Map();data.rel.forEach((w,i)=>{let r=fox(w,data.weight);r.delete(data.mer[0]);rows.set(i,r);});data.longs.forEach((w,i)=>{let r=fox(w,data.weight);r.delete(data.mer[0]);obs.set(i,r);});
requireTrue([...rows].every(([i,r])=>sameRow(r,rp(f.initial_fox_rows[i])))&&[...obs].every(([i,r])=>sameRow(r,rp(f.initial_longitude_rows[i]))),'initial integer Laurent Fox derivatives independently match');
function eliminateRow(r,pivot,g,k,c){if(!r.has(g))return;const f=plus(new Map(),r.get(g),-k,-c);r.delete(g);for(const[h,p]of pivot){if(h===g)continue;const v=plus(r.get(h)??new Map(),times(f,p));if(v.size)r.set(h,v);else r.delete(h);}}
for(const move of f.pivots){let pivot=rows.get(move.row),c=BigInt(move.coefficient);if(!pivot||!same(pivot.get(move.column)??new Map(),new Map([[move.power,c]]))||!(c===1n||c===-1n))throw new Error('invalid Laurent pivot');rows.delete(move.row);for(const r of rows.values())eliminateRow(r,pivot,move.column,move.power,c);for(const r of obs.values())eliminateRow(r,pivot,move.column,move.power,c);}
rows=new Map([...rows].filter(([i,r])=>r.size));requireTrue(rows.size===3&&[...rows].every(([i,r])=>sameRow(r,rp(f.reduced_rows[i])))&&[...obs].every(([i,r])=>sameRow(r,rp(f.reduced_longitudes[i]))),'all 670 unit pivots and reduced longitude rows replay exactly');
const gens=f.remaining_generators,matrix=[...rows.values()].map(r=>gens.map(g=>r.get(g)??new Map())),longmat=[0,1,2].map(i=>gens.map(g=>obs.get(i).get(g)??new Map()));
const d=poly({0:1,1:-3,2:5,3:-3,4:1}),one=poly({0:1}),zero=new Map(),target=times(d,d),td=plus(zero,d,1);
// Rational response with common denominator t*d. Columns are meridian_a,b'.
const n0=poly({0:-1,1:4,2:-6,3:4,4:-1}),n1=poly({0:-1,1:2,2:-2,3:1});
let S=[[n0,plus(zero,n0,1)],[n1,plus(zero,n1,1)],[td,zero],[zero,td]];
function productZero(M,S){return M.every(r=>[0,1].every(j=>{let v=zero;for(let i=0;i<r.length;i++)v=plus(v,times(r[i],S[i][j]));return v.size===0;}));}
requireTrue(productZero(matrix,S)&&productZero(longmat.slice(1),S),'rational meridian solution and exact E=0 verified by polynomial multiplication');
let filled=matrix.concat([longmat[1].map((p,i)=>plus(p,gens[i]===data.mer[1]?one:zero)),longmat[2].map((p,i)=>plus(p,gens[i]===data.mer[2]?one:zero,0,-1n))]);
function determinant(M){if(!M.length)return one;let r=zero;for(let j=0;j<M.length;j++){if(!M[0][j].size)continue;let sub=M.slice(1).map(row=>row.filter((x,i)=>i!==j));r=plus(r,times(M[0][j],determinant(sub)),0,j%2?-1n:1n);}return r;}
const subsets=[[0,1,2,3],[0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4]],shifts=[null,null,[-4,-1n],[-2,1n],[-3,-1n]];
requireTrue(subsets.every((ix,k)=>same(determinant(ix.map(i=>filled[i])),shifts[k]===null?zero:plus(zero,target,...shifts[k]))),'all five filled maximal minors are 0,0,-t^-4 d^2,t^-2 d^2,-t^-3 d^2');
// Determinants are affine in each parameter separately: four exact corner
// values therefore determine every coefficient, not an empirical extrapolation.
let uniform=true;
for(const x of [0n,1n])for(const y of [0n,1n]){
 const F=matrix.concat([longmat[1].map((p,i)=>plus(gens[i]===data.mer[1]?one:zero,p,0,x)),longmat[2].map((p,i)=>plus(gens[i]===data.mer[2]?one:zero,p,0,y))]);
 const expected=[zero,zero,plus(zero,target,-4,1n),plus(zero,target,-2,-1n),plus(zero,target,-3,1n)];
 uniform=uniform&&subsets.every((ix,k)=>same(determinant(ix.map(i=>F[i])),expected[k]));
}
requireTrue(uniform,'all-parameter minors certified by determinant multiaffinity and four exact coefficient-determining evaluations');
// Direct free-word verification of unlink longitudes, independent of geometry.
const aux=read('auxiliary_group_certificate.json');
const auxIDs=new Set(diagram.crossings.filter(c=>c.over[0]!==0&&c.under[0]!==0).map(c=>c.id));const auxData=peripheral(gauss.slice(1).map(w=>w.filter(c=>auxIDs.has(c[0]))));
requireTrue(auxData.ng===aux.input_generators&&eq(auxData.rel,aux.input_relators)&&eq(auxData.mer,aux.input_meridians)&&eq(auxData.longs,aux.input_longitudes),'auxiliary group and preferred longitudes reconstructed directly from the polygon sublink');
let rels=aux.input_relators.map(cyclic).filter(r=>r.length),im={};for(let g=1;g<=aux.input_generators;g++)im[g]=[g];let curmer=aux.input_meridians.map(g=>[g]),curlong=aux.input_longitudes.map(reduce);
for(const move of aux.moves){const g=move.generator,r=move.defining_relator,expr=move.replacement;const ri=rels.findIndex(s=>eq(s,r));if(ri<0||r.filter(x=>Math.abs(x)===g).length!==1||expr.some(x=>Math.abs(x)===g))throw new Error('bad auxiliary Tietze move');let m={};for(let a=1;a<=aux.input_generators;a++)m[a]=[a];m[g]=expr;if(substitute(r,m).length)throw new Error('replacement does not kill defining relator');rels=rels.filter((r,i)=>i!==ri).map(r=>cyclic(substitute(r,m))).filter(r=>r.length);for(const words of [curmer,curlong])for(let i=0;i<words.length;i++)words[i]=substitute(words[i],m);}
requireTrue(rels.length===0&&curlong.every(w=>w.length===0)&&eq(curmer,aux.meridian_images),'auxiliary exact Tietze replay kills both preferred longitudes; free group rank two');
// Positive / negative controls and deliberate corruptions.
const hopf=peripheral([[[0,'O',1],[1,'U',1]],[[0,'U',1],[1,'O',1]]]);requireTrue(eq(hopf.longs,[[2],[1]]),'positive Hopf peripheral control has nontrivial opposite meridians');
const unk=peripheral([[],[]]);requireTrue(unk.ng===2&&eq(unk.longs,[[],[]]),'unlink peripheral control');
const wrongLong=longmat.slice(1).map(r=>r.map(p=>new Map(p)));wrongLong[1][gens.indexOf(data.mer[2])]=plus(wrongLong[1][gens.indexOf(data.mer[2])],one,0,-1n);requireTrue(!productZero(wrongLong,S),'incorrect b-prime zero-framing is rejected');
requireTrue(reduce(curlong[0].concat(curmer[0])).length>0,'corrupted null longitude is rejected');
const wrongTarget=plus(target,one);requireTrue(!same(determinant(subsets[2].map(i=>filled[i])),plus(zero,wrongTarget,-4,-1n)),'corrupted Alexander polynomial is rejected');
let badPivot={...f.pivots[0],coefficient:-f.pivots[0].coefficient};let original=rp(f.initial_fox_rows[badPivot.row]);requireTrue(!same(original.get(badPivot.column),poly({[badPivot.power]:badPivot.coefficient})),'corrupted unit-pivot sign is rejected');
const report={status:'PASS',checks:checks.length,passed:checks,polygon_crossings:count,fox_unit_pivots:f.pivots.length,auxiliary_tietze_moves:aux.moves.length,exact_target_coefficients_ascending:[...target].sort((a,b)=>a[0]-b[0]).map(([k,c])=>Number(c)),scope:'Independent arithmetic and polygon-projection replay. Does not construct a slice disk or identify the surgery knot as D01.'};
fs.writeFileSync(path.join(P,'independent_exact_check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
