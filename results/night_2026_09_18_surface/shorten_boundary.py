"""Deterministic, length-nonincreasing relator rewrites; no group search.

Retains every move as a certificate. Failure to shorten says nothing about
minimal length or whether the word is trivial.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
C=json.loads((ROOT/'results/astra_2026_09_17_collar_boundary_audit/CERTIFICATE.json').read_text())
W=json.loads((ROOT/'results/night_2026_09_18/word_correction.json').read_text())
inv=lambda w:tuple(-x for x in reversed(w))
key=lambda w:(len(w),tuple((abs(x),x<0) for x in w))
rules={}
for ri,rel in enumerate([[-sg*(b+1),i+1,sg*(b+1),-(o+1)] for i,o,b,sg,c in C['boundary_relations']]):
    for sign,w in [(1,tuple(rel)),(-1,inv(rel))]:
        for shift in range(len(w)):
            cyc=w[shift:]+w[:shift]
            for cut in range(1,len(w)):
                lhs,rhs=cyc[:cut],inv(cyc[cut:])
                if key(rhs)<key(lhs):
                    old=rules.get(lhs)
                    if old is None or key(rhs)<key(old[0]):
                        rules[lhs]=(rhs,ri,sign,shift,cut)
word=tuple(W['correction_boundary_word'])
steps=[]
for _ in range(10000):
    changed=False
    for i in range(len(word)):
        if i+1<len(word) and word[i]==-word[i+1]:
            new=word[:i]+word[i+2:]
            steps.append({'type':'free','at':i,'letters':list(word[i:i+2])})
            changed=True
            break
        for size in (3,2,1):
            lhs=word[i:i+size]
            if len(lhs)==size and lhs in rules:
                rhs,ri,sign,shift,cut=rules[lhs]
                new=word[:i]+rhs+word[i+size:]
                steps.append({'type':'relator','at':i,'from':list(lhs),'to':list(rhs),'relator':ri,'sign':sign,'rotation':shift,'cut':cut})
                changed=True
                break
        if changed:
            break
    if not changed:
        break
    assert key(new)<key(word)
    word=new
else:
    raise RuntimeError('deterministic rewrite step cap')
assert word
print(json.dumps({'scope':'Only a deterministic rewrite, not shortest-word or conjugacy search','initial_word':W['correction_boundary_word'],'final_word':word,'initial_length':len(W['correction_boundary_word']),'final_length':len(word),'steps':steps},indent=2))
