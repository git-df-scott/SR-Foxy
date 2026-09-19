
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
  const expected=rows=>{const p=new Map();for(let n=0;n<rows.length;n++)for(let z=0;z<rows[n].length;z++)put(p,n,z,BigInt(rows[n][z]));return p;};
  check(eq(tr(axes[0]),expected(c.trace_eta1_coefficients_in_n)),'eta1 polynomial');
  check(eq(tr(axes[1]),expected(c.trace_eta2_coefficients_in_n)),'eta2 polynomial');
  const difference=sub(tr(axes[0]),tr(axes[1]));
  check(eq(difference,expected(c.trace_difference_coefficients_in_n)),'difference polynomial');
  check(coeff(difference,1,5)===-12n,'leading coefficient');
  check([...difference.keys()].every(k=>{const [n,z]=k.split(',').map(Number);return n>0 && z<6 && (z<5||n===1);}), 'nonvanishing support');
  const mod2rem=(a,b)=>{while(a && 31-Math.clz32(a)>=31-Math.clz32(b)) a^=b<<((31-Math.clz32(a))-(31-Math.clz32(b)));return a;};
  let bits=0;R.forEach((v,i)=>{if(v%2n)bits|=1<<i;});
  let divisors=0;for(let d=1;d<=3;d++)for(let v=1<<d;v<1<<(d+1);v++){check(mod2rem(bits,v)!==0,'reducible mod2');divisors++;}
  return {status:'INDEPENDENT_SYMBOLIC_CHECK_PASSED',arithmetic:'sparse bivariate integer polynomials modulo monic R(z), JavaScript BigInt',source_relators:c.source_relators.length,boundary_relations:c.boundary_relations.length,irreducibility_divisors:divisors,geometric_realization_verified:false,counterexample_found:false};
}

import {readFileSync} from 'node:fs';
const cert=JSON.parse(readFileSync(process.argv[2] || new URL('./CERTIFICATE.json',import.meta.url),'utf8'));
const result=verify(cert);
result.negative_controls=[];
for(const kind of ['axis','matrix','trace']) {
 const c=structuredClone(cert);
 if(kind==='axis')c.axis_boundary_words[0]=[];
 if(kind==='matrix')c.source_matrices['1'][0][0]+=1;
 if(kind==='trace')c.trace_difference_coefficients_in_n[1][0]+=1;
 let reason=null;try{verify(c);}catch(e){reason=e.message;}
 if(!reason)throw new Error('Negative control passed: '+kind);
 result.negative_controls.push({mutation:kind,rejected:true,reason});
}
console.log(JSON.stringify(result,null,2));
