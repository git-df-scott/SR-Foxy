
function verify(c) {
  const R = c.riley_polynomial_ascending.map(BigInt);
  const fail = msg => { throw new Error(msg); };
  const check = (ok,msg) => {if(!ok) fail(msg);};
  check(JSON.stringify(c.riley_polynomial_ascending)==='[1,1,2,4,5,3,1]', 'Unexpected defining polynomial');
  const coeff = (p,n,z) => p.get(n+','+z)||0n;
  const put = (p,n,z,v) => {const key=n+','+z; const w=(p.get(key)||0n)+v;if(w)p.set(key,w);else p.delete(key);};
  const add = (a,b) => {const p=new Map(a);for(const [k,v] of b){const [n,z]=k.split(',').map(Number);put(p,n,z,v);}return p;};
  const neg = a => new Map([...a].map(([k,v])=>[k,-v]));
  const sub = (a,b) => add(a,neg(b));
  const reduce = p => {
    for(;;){let changed=false;for(const [key,v] of p){
      const [n,z]=key.split(',').map(Number);
      if(z>=6){p.delete(key);for(let i=0;i<6;i++)put(p,n,z-6+i,-v*R[i]);changed=true;break;}
    }if(!changed) return p;}
  };
  const mul = (a,b) => {const p=new Map();for(const [ka,va]of a)for(const [kb,vb]of b){
    const [na,za]=ka.split(',').map(Number),[nb,zb]=kb.split(',').map(Number);
    put(p,na+nb,za+zb,va*vb);
  }return reduce(p);};
  const scalar = (v,n=0,z=0) => new Map(v?[[n+','+z,BigInt(v)]]:[]);
  const P = arr => new Map(arr.map((v,z)=>['0,'+z,BigInt(v)]).filter(([k,v])=>v!==0n));
  const zero = new Map(), one=scalar(1);
  const I=[one,zero,zero,one];
  const mm=(a,b)=>[add(mul(a[0],b[0]),mul(a[1],b[2])),add(mul(a[0],b[1]),mul(a[1],b[3])),add(mul(a[2],b[0]),mul(a[3],b[2])),add(mul(a[2],b[1]),mul(a[3],b[3]))];
  const inverse=a=>[a[3],neg(a[1]),neg(a[2]),a[0]];
  const eq=(a,b)=>sub(a,b).size===0;
  const meq=(a,b)=>a.every((p,i)=>eq(p,b[i]));
  const evaluate=(word,images)=>word.reduce((out,x)=>mm(out,x>0?images[x]:inverse(images[-x])),I);
  const det=a=>sub(mul(a[0],a[3]),mul(a[1],a[2]));
  const source=Object.fromEntries(Object.entries(c.source_matrices).map(([k,a])=>[k,a.map(P)]));
  for(const [k,a]of Object.entries(source))check(eq(det(a),one),'source determinant '+k);
  for(const w of c.source_relators)check(meq(evaluate(w,source),I),'source relator');
  const col=Object.fromEntries(Object.entries(c.boundary_arc_images).map(([k,w])=>[k,evaluate(w,source)]));
  const m=col[4]; check(meq(m,col[14]),'seam');
  const N=m.map((p,i)=>sub(p,I[i]));
  check(mm(N,N).every(p=>p.size===0),'seam not unipotent');
  const h=I.map((p,i)=>add(p,mul(scalar(1,1),N[i])));
  const lower=new Set(c.lower_arcs_zero_based);
  const cn=Object.fromEntries(Object.entries(col).map(([k,a])=>[Number(k)+1,lower.has(Number(k))?mm(mm(h,a),inverse(h)):a]));
  for(const [k,a]of Object.entries(cn))check(eq(det(a),one),'boundary determinant '+k);
  for(const [i,o,b,s]of c.boundary_relations)check(meq(evaluate([-(b+1)*s,i+1,(b+1)*s,-o-1],cn),I),'boundary relator');
  const axes=c.axis_boundary_words.map(w=>evaluate(w,cn));
  const tr=a=>add(a[0],a[3]);

  const trRows=a=>{const p=tr(a),rows=[];for(const [k,v]of p){let[n,z]=k.split(',').map(Number);while(rows.length<=n)rows.push([]);while(rows[n].length<=z)rows[n].push(0);rows[n][z]=Number(v);}return rows;};
  return axes.map(trRows);
}


import {readFileSync} from 'node:fs';
const c=JSON.parse(readFileSync(new URL('../astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json',import.meta.url),'utf8'));
const report=JSON.parse(readFileSync(new URL('./SHORT_RESULTS.json',import.meta.url),'utf8'));
for(const row of report.rows){
 const x=structuredClone(c);x.axis_boundary_words=row.axis_words;const tr=verify(x);
 for(let a=0;a<2;a++)for(let z=0;z<6;z++)if((tr[a][0]?.[z]||0)!==row.traces[a][z])throw Error('Trace mismatch');
}
console.log(JSON.stringify({status:'INDEPENDENT_TRACE_CHECK_PASSED',rows:report.rows.length,CE:false}));
