#!/usr/bin/env node
// Independent replay: no Python imports, no search, no topology libraries.
// This uses repeated adjacent cancellation rather than the producer's stack.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
let checks=0;
function requireThat(condition,message){checks++;if(!condition)throw new Error(message);}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function inverse(w){return [...w].reverse().map(x=>-x);}
function reduce(w){
  let v=[...w];
  for(const x of v)requireThat(Number.isSafeInteger(x)&&x!==0,'Invalid letter');
  for(let i=0;i+1<v.length;){if(v[i]===-v[i+1]){v.splice(i,2);i=Math.max(0,i-1);}else i++;}
  return v;
}
function cat(...ws){return reduce(ws.flat());}
function conjugacyCore(w){let v=reduce(w);while(v.length>1&&v[0]===-v.at(-1))v=v.slice(1,-1);return v;}
function replace(w,gen,rhs){return reduce(w.flatMap(x=>Math.abs(x)===gen?(x>0?rhs:inverse(rhs)):[x]));}
function power(x,n){return Array(Math.abs(n)).fill(n>=0?x:-x);}
function relators(d){return d.boundary_relations.map(([i,o,b,s,c])=>[-s*(b+1),i+1,s*(b+1),-o-1]);}
function checkCertificate(c,d,raw){
  requireThat(c.input_sha256===crypto.createHash('sha256').update(raw).digest('hex'),'Input hash mismatch');
  requireThat(c.source_commit===d.source_commit,'Commit mismatch');
  const rs=relators(d);
  requireThat(same(rs,c.original_boundary_relators),'Relator provenance');
  requireThat(same(c.relators_used_indices,[1,2,3,4,5,6,7,8]),'Unexpected relator subset');
  let live=rs.slice(1,9).map(conjugacyCore);
  const images={};for(let k=1;k<=9;k++)images[k]=[k];
  for(const step of c.tietze_steps){
    const j=live.findIndex(w=>same(w,step.defining_relator));
    requireThat(j>=0,'Defining relator missing');
    const g=step.generator;
    requireThat(step.defining_relator.filter(x=>Math.abs(x)===g).length===1,'Generator not unique');
    requireThat(!step.replacement.some(x=>Math.abs(x)===g),'Circular Tietze replacement');
    requireThat(replace(step.defining_relator,g,step.replacement).length===0,'Invalid Tietze equation');
    live=live.filter((_,k)=>k!==j).map(w=>conjugacyCore(replace(w,g,step.replacement))).filter(w=>w.length);
    for(const k of Object.keys(images))images[k]=replace(images[k],g,step.replacement);
  }
  requireThat(live.length===1&&same(live[0],c.remaining_relator),'Remaining relator mismatch');
  requireThat(same(images,c.tietze_images),'Tietze generator maps mismatch');
  function translate(w){return reduce(w.flatMap(x=>x>0?images[x]:inverse(images[-x])));}
  const offset=c.schreier_offset;
  const mu=c.schreier_meridian,other=c.schreier_other_generator;
  requireThat(mu===3&&other===5&&offset===20,'Unexpected Schreier conventions');
  function expandY(w){return cat(...w.map(x=>{
    const k=Math.abs(x)-offset;
    const v=cat(power(mu,k),[other],power(mu,-k-1));
    return x>0?v:inverse(v);
  }));}
  function schreier(w){
    let k=0,out=[];
    for(const x of w){
      requireThat(Math.abs(x)===mu||Math.abs(x)===other,'Unknown two-generator letter');
      if(Math.abs(x)===other)out.push(x>0?k+offset:-(k-1+offset));
      k+=Math.sign(x);
    }
    requireThat(k===0,'Nonzero exponent');
    const result=reduce(out);
    requireThat(same(expandY(result),reduce(w)),'Schreier free expansion failed');
    return result;
  }
  const r=schreier(c.remaining_relator);
  requireThat(same(r,c.schreier_relator),'Schreier relator mismatch');
  requireThat(same(c.basis_levels,[-1,2]),'Basis changed');
  const rules=new Map(c.finite_schreier_rules.map(x=>[x.level,x]));
  requireThat(rules.size===c.finite_schreier_rules.length,'Duplicate level');
  for(const [level,rule] of rules){
    const shifted=r.map(x=>Math.sign(x)*(Math.abs(x)+rule.relator_shift));
    requireThat(same(shifted,rule.shifted_relator),'Shifted relator mismatch');
    requireThat(shifted.filter(x=>Math.abs(x)===level+offset).length===1,'Nonunique Schreier elimination');
    requireThat(!rule.replacement.some(x=>Math.abs(x)===level+offset),'Self-dependent Schreier rule');
    requireThat(replace(shifted,level+offset,rule.replacement).length===0,'Invalid Schreier equation');
    // Literal check of the shift as conjugation by a meridian power.
    requireThat(same(expandY(shifted),cat(power(mu,rule.relator_shift),expandY(r),power(mu,-rule.relator_shift))),'Shift is not a meridional conjugation');
  }
  const memo=new Map([[-1,[1]],[0,[2]],[1,[3]],[2,[4]]]),active=new Set();
  function evaluateLevel(k){
    if(memo.has(k))return memo.get(k);
    requireThat(!active.has(k),'Cyclic elimination dependency');active.add(k);
    const rule=rules.get(k);requireThat(!!rule,'Missing Schreier rule');
    const answer=reduce(rule.replacement.flatMap(x=>x>0?evaluateLevel(Math.abs(x)-offset):inverse(evaluateLevel(Math.abs(x)-offset))));
    requireThat(same(answer,rule.basis_image),'Wrong basis image');
    active.delete(k);memo.set(k,answer);return answer;
  }
  function toBasis(w){return reduce(w.flatMap(x=>x>0?evaluateLevel(Math.abs(x)-offset):inverse(evaluateLevel(Math.abs(x)-offset))));}
  requireThat(same(c.words.original_delta.boundary_word,d.original_boundary_delta),'Original correction changed');
  requireThat(same(c.words.short_delta.boundary_word,d.boundary_delta_short),'Short correction changed');
  for(const [name,w] of Object.entries(c.words)){
    const tw=translate(w.boundary_word);
    requireThat(same(tw,w.two_generator_word),name+': Tietze translation');
    const sw=schreier(tw);requireThat(same(sw,w.schreier_word),name+': Schreier translation');
    requireThat(same(toBasis(sw),w.basis_word),name+': basis translation');
  }
  const f=c.words.A.basis_word,g=c.words.B.basis_word;
  const product=cat(f,g,inverse(f),inverse(g));
  requireThat(same(product,c.words.original_delta.basis_word),'Original correction is not the commutator');
  requireThat(same(product,c.words.short_delta.basis_word),'Short correction is not the commutator');
  requireThat(same(product,c.commutator_expansion_basis),'Recorded expansion differs');
  for(const key of ['A','B'])requireThat(c.words[key].boundary_word.reduce((s,x)=>s+Math.sign(x),0)===0,key+': exponent not zero');
  return {tietze_steps:c.tietze_steps.length,finite_schreier_rules:rules.size,original_length:d.original_boundary_delta.length,handle_lengths:[c.words.A.boundary_word.length,c.words.B.boundary_word.length],identity:true};
}
function finiteCheck(w,d,c){
  const rs=relators(d),I=[1n,0n,0n,1n];
  const answers=[];
  for(const witness of w.witnesses){
    const p=BigInt(witness.prime);const mod=x=>((x%p)+p)%p;
    const times=(a,b)=>[mod(a[0]*b[0]+a[1]*b[2]),mod(a[0]*b[1]+a[1]*b[3]),mod(a[2]*b[0]+a[3]*b[2]),mod(a[2]*b[1]+a[3]*b[3])];
    const invert=a=>[a[3],mod(-a[1]),mod(-a[2]),a[0]];
    const eq=(a,b)=>a.every((x,i)=>x===b[i]);
    const ims=Object.fromEntries(Object.entries(witness.boundary_images).map(([k,a])=>[k,a.map(BigInt)]));
    requireThat(Object.keys(ims).length===18,'Missing generator image');
    for(const a of Object.values(ims))requireThat(mod(a[0]*a[3]-a[1]*a[2])===1n,'Non-SL2 generator');
    const value=word=>word.reduce((a,x)=>times(a,x>0?ims[x]:invert(ims[-x])),I);
    for(const r of rs)requireThat(eq(value(r),I),'Finite boundary relator failure');
    const delta=value(d.original_boundary_delta),A=value(c.words.A.boundary_word),B=value(c.words.B.boundary_word);
    requireThat(eq(delta,value(d.boundary_delta_short)),'Finite delta mismatch');
    requireThat(eq(delta,times(times(times(A,B),invert(A)),invert(B))),'Finite commutator mismatch');
    requireThat(!eq(delta,I),'Trivial finite witness');
    requireThat(eq(delta,witness.delta.map(BigInt)),'Incorrect displayed finite value');
    answers.push({prime:witness.prime,z:witness.z,delta:witness.delta,nontrivial:true});
  }
  return answers;
}
const c=JSON.parse(fs.readFileSync(path.join(here,'CERTIFICATE.json'),'utf8'));
const raw=fs.readFileSync(path.join(here,'inputs_extended.json'));
const d=JSON.parse(raw);
const w=JSON.parse(fs.readFileSync(path.join(here,'finite_witness.json'),'utf8'));
const original=checkCertificate(c,d,raw),finite=finiteCheck(w,d,c);
const q0=Object.fromEntries(Object.entries(d.q0_images).map(([k,v])=>[Number(k)+1,v]));
const qword=word=>cat(...word.map(x=>x>0?q0[x]:inverse(q0[-x])));
const muword=q0[d.seam_meridian];
const qleft=qword(cat(d.original_boundary_delta,d.axis2));
const qright=cat(inverse(muword),qword(d.axis1),muword);
requireThat(same(qleft,qright),'Saved q0 free identity failed');
const mutations=[];
for(const [name,change] of [
 ['A sign',x=>x.words.A.boundary_word[0]*=-1],
 ['B sign',x=>x.words.B.boundary_word[0]*=-1],
 ['Tietze replacement',x=>x.tietze_steps[0].replacement[0]*=-1],
 ['Schreier replacement',x=>x.finite_schreier_rules[0].replacement[0]*=-1],
 ['Claimed commutator',x=>x.commutator_expansion_basis[0]*=-1],
 ['Original correction',x=>x.words.original_delta.boundary_word[0]*=-1],
]){
 const z=structuredClone(c);change(z);let rejected=false,message='';
 try{checkCertificate(z,d,raw);}catch(e){rejected=true;message=e.message;}
 requireThat(rejected,'Mutation escaped: '+name);mutations.push({name,rejected,message});
}
for(const [name,change] of [
 ['Finite generator image',x=>x.witnesses[0].boundary_images['1'][0]+=1],
 ['Finite displayed delta',x=>x.witnesses[0].delta[0]+=1]
]){
 const z=structuredClone(w);change(z);let rejected=false,message='';
 try{finiteCheck(z,d,c);}catch(e){rejected=true;message=e.message;}
 requireThat(rejected,'Finite mutation escaped: '+name);mutations.push({name,rejected,message});
}
// Separate elementary controls for the free-word and matrix checks.
requireThat(same(cat([1,2],[-2,-1]),[]),'Cancellation control');
requireThat(same(cat([1,2,-1,-2]),[1,2,-1,-2]),'Nontrivial commutator control');
requireThat(!same(cat([1,2,-1,-2]),cat([2,1,-2,-1])),'Commutator sign control');
// Every abelianized relation is just x_i=x_o; connectivity proves G_ab=Z.
const reached=new Set([1]);let changed=true;
while(changed){changed=false;for(const [i,o] of d.boundary_relations){if(reached.has(i+1)||reached.has(o+1)){const n=reached.size;reached.add(i+1);reached.add(o+1);changed||=reached.size!==n;}}}
requireThat(reached.size===18,'Abelianization graph disconnected');
console.log(JSON.stringify({status:'PASS',implementation:'Independent JavaScript; free cancellation and BigInt finite matrices',identity:original,finite_nontriviality:finite,corrupt_certificates_rejected:mutations,abelianization:'Z',saved_q0_identity_by_free_reduction:true,geometric_q0_identified:false,commutator_length_in_G_prime:1,checks_including_letter_validation:checks,CE:false},null,2));
