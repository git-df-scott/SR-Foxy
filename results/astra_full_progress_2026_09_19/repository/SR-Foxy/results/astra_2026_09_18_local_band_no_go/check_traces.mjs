
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

function normWitness() {
 const R=[1n,1n,2n,4n,5n,3n,1n];
 const d=[-572n,-268n,-804n,-1816n,-1652n,-336n];
 const rem=p=>{p=p.slice();for(let i=p.length-1;i>=6;i--){const v=p[i]||0n;for(let j=0;j<6;j++)p[i-6+j]=(p[i-6+j]||0n)-v*R[j];p[i]=0n;}return Array.from({length:6},(_,i)=>p[i]||0n);};
 const columns=Array.from({length:6},(_,j)=>rem([...Array(j).fill(0n),...d]));
 const a=Array.from({length:6},(_,i)=>columns.map(c=>c[i]));let prev=1n,sign=1n;
 for(let k=0;k<5;k++){if(a[k][k]===0n){let j=k+1;while(j<6&&a[j][k]===0n)j++;if(j===6)throw Error("Singular norm");[a[k],a[j]]=[a[j],a[k]];sign=-sign;}
 const pivot=a[k][k];
 for(let i=k+1;i<6;i++)for(let j=k+1;j<6;j++){const v=a[i][j]*pivot-a[i][k]*a[k][j];if(v%prev!==0n)throw Error("Nonexact division");a[i][j]=v/prev;}
 for(let i=k+1;i<6;i++)a[i][k]=0n;prev=pivot;}
 const norm=sign*a[5][5];
 let lo=0n,hi=norm+1n;while(hi-lo>1n){let mid=(lo+hi)/2n;if(mid*mid<=norm)lo=mid;else hi=mid;}
 if(norm!==199282855936n||lo*lo===norm)throw Error("Norm witness failed");
 return {norm:norm.toString(),sqrt_floor:lo.toString(),lower_square:(lo*lo).toString(),upper_square:(hi*hi).toString(),square:false};
}

import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const raw=readFileSync(new URL('../astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json',import.meta.url));
const digest=createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
if(digest!=='86bb4e5ec1ae5a1762f4ce724279c7c5a509fed6')throw Error('Pinned certificate changed');
const cert=JSON.parse(raw),rows=JSON.parse(readFileSync(new URL('./SCAN.json',import.meta.url),'utf8'));
if(rows.length!==16)throw Error('Incomplete variant set');
for(const row of rows) {
 const c=structuredClone(cert);c.axis_boundary_words=row.axis_words;
 const tr=verify(c);
 const diff=Array.from({length:Math.max(...tr.map(x=>x.length))},(_,i)=>Array.from({length:6},(_,j)=>(tr[0][i]?.[j]||0)-(tr[1][i]?.[j]||0)));
 if(JSON.stringify(diff)!==JSON.stringify(row.trace_difference))throw Error('Trace mismatch '+row.bits);
}
console.log(JSON.stringify({status:'ALL_16_TRACE_POLYNOMIALS_VERIFIED',centralizer_norm:normWitness()},null,2));
