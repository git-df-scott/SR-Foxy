#!/usr/bin/env python3
"""Replay the saved finite group-presentation proof, without the diagram code.

This verifies algebra only. The separate diagram generator and the geometric
product-collar interpretation remain distinct obligations.
"""
import argparse, copy, json
from pathlib import Path


def reduce_free(word):
    w=list(word);i=0
    while i+1<len(w):
        if w[i]+w[i+1]==0:del w[i:i+2];i=max(0,i-1)
        else:i+=1
    return tuple(w)
def backwards(w):return tuple(-x for x in reversed(w))
def conjugacy_key(w):
    w=reduce_free(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    if not w:return ()
    return min(v[i:]+v[:i] for v in (w,backwards(w)) for i in range(len(v)))
def substitute(word,images):
    out=[]
    for x in word:
        v=tuple(images.get(abs(x),(abs(x),)))
        out.extend(v if x>0 else backwards(v))
    return reduce_free(out)
def replay(w,trace,relations):
    w=reduce_free(w)
    for position,desc in trace:
        idx,sgn,shift,cut=desc
        r=tuple(relations[idx]);assert sgn in (-1,1)
        if sgn<0:r=backwards(r)
        r=r[shift:]+r[:shift]
        assert w[position:position+cut]==r[:cut]
        w=reduce_free(w[:position]+backwards(r[cut:])+w[position+cut:])
    return w


def check(d):
    relations=[tuple(w) for w in d['source_relators']]
    images={i:(i,) for i in range(1,10)}
    for e in d['tietze_eliminations']:
        x=e['generator'];r=tuple(e['relator']);v=tuple(e['image'])
        assert conjugacy_key(r) in {conjugacy_key(z) for z in relations}
        assert sum(abs(t)==x for t in r)==1 and all(abs(t)!=x for t in v)
        assert substitute(r,{x:v})==()
        relations=[substitute(z,{x:v}) for z in relations]
        images={i:substitute(z,{x:v}) for i,z in images.items()}
    assert images=={int(i):tuple(w) for i,w in d['source_generator_images'].items()}
    known={conjugacy_key(z) for z in relations}
    assert {conjugacy_key(z) for z in d['reduced_relators']}==known-{()}
    for step in d['derived_relators']:
        assert conjugacy_key(step['start']) in known
        assert all(conjugacy_key(z) in known for z in step['rules'])
        out=replay(step['start'],step['trace'],step['rules'])
        assert out==tuple(step['end_before_cyclic_reduction'])
        assert conjugacy_key(out)==conjugacy_key(step['new_relator'])
        known.add(conjugacy_key(step['new_relator']))
    assert all(conjugacy_key(z) in known for z in d['proof_rule_relators'])
    rs=d['proof_rule_relators']
    a=replay(d['eta1_word'],d['eta1_reduction'],rs)
    b=replay(d['eta2_word'],d['eta2_reduction'],rs)
    assert a==b==tuple(d['common_reduced_word'])
    assert not replay(tuple(d['eta1_word'])+backwards(d['eta2_word']),d['difference_reduction'],rs)
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path,nargs='?',default=Path(__file__).with_name('certificate.json'))
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    d=json.loads(args.certificate.read_text());assert check(d)
    tests=[]
    for name,edit in [('axis word',lambda x:x['eta1_word'].append(5)),('claimed common word',lambda x:x['common_reduced_word'].append(5)),('source generator image',lambda x:x['source_generator_images']['1'].append(5))]:
        mutant=copy.deepcopy(d);edit(mutant)
        try:check(mutant)
        except (AssertionError,IndexError):tests.append(name)
        else:raise AssertionError('Tampered certificate accepted: '+name)
    print(json.dumps({'independent_relator_replay':'PASS','tamper_tests_rejected':tests,'geometric_disk_identification':'NOT_VERIFIED_BY_THIS_CHECKER','counterexample':False},indent=2))
if __name__=='__main__':main()
