"""Replay saved L3/L4 exclusions and all 50 self-return movies, without search."""
import argparse,collections,hashlib,json,time
from pathlib import Path
import sympy as s
import spherogram
from spherogram.links.bands import core
from pd_algebra import fox_matrix,linking_numbers,structure,alexander,determinant,t
from prefix_certify import bareiss_det
from extended_prefix_search import detmod
from multivariable_prefix_certificate import multivariable_fox
from certify_trivial_L4 import apply
from analyze_L4_survivors import sig
ROOT=Path(__file__).parent

def read(name):return json.loads((ROOT/name).read_text())

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--level',type=int,choices=[3,4],default=4);parser.add_argument('--shards',type=int,default=4);parser.add_argument('--shard',type=int,default=0);a=parser.parse_args();assert 0<=a.shard<a.shards;start=time.time()
    source=read('gst48.json');pd=source['pd'];K=spherogram.Link(pd)
    assert hashlib.sha256((ROOT/'gst48.json').read_bytes()).hexdigest()==read('invariants.json')['source_sha256']
    # Known positive and negative algebra controls, including the mirror.
    for name,expected in [('3_1',3),('4_1',5),('6_1',9)]:
        C=spherogram.Link(name);p=[list(x) for x in C.PD_code()]
        assert determinant(p)==expected and determinant([list(x) for x in C.mirror().PD_code()])==expected
    try:structure([[0,1,2,3]])
    except ValueError:pass
    else:raise AssertionError('Malformed PD was accepted')
    fn='extended_prefix_L3_T1.json' if a.level==3 else 'extended_prefix_L4_T2.json';data=read(fn)
    specs=[b.compressed_spec() for b in core.simple_bands(K,max_twists=a.level-2,max_band_len=a.level)]
    assert specs==[r['band'] for r in data['records']] and len(set(specs))==len(specs)
    total=0;integer_spot_checks=0
    for i,r in enumerate(data['records']):
        if i%a.shards!=a.shard:continue
        L=K.add_band(r['band']);q=[list(x) for x in L.PD_code()]
        if r['status']=='excluded_nonzero_linking':
            lk=int(L.linking_number());assert lk==r['linking_number'] and lk!=0
            assert abs(linking_numbers(q).get((0,1),0))==abs(lk)
        elif r['status']=='excluded_nonzero_Fox_minor':
            A=fox_matrix(q,r['specialization'],require_knot=False);n=r['minor_size'];M=A[:n,:n].tolist()
            d=detmod(M,r['modulus']);assert d==r['determinant_mod_p'] and d
            if i%101==0:
                assert bareiss_det(M)%r['modulus']==d;integer_spot_checks+=1
        else:assert q==r['pd']
        total+=1
    checked_multi=0;checked_movies=0
    if a.level==3 and a.shard==0:
        tails=read('multivariable_prefix_certificates.json')['records']
        for r in tails:
            A,_=multivariable_fox(r['pd'],r['variables']);M=A.extract(r['rows'],r['columns']).tolist()
            assert [[int(z) for z in row] for row in M]==r['specialized_matrix']
            assert bareiss_det(M)==r['minor_determinant']!=0;checked_multi+=1
        assert {r['band'] for r in tails}=={r['band'] for r in data['records'] if r['status']=='inconclusive_specializations_zero'}
    elif a.level==4 and a.shard==0:
        tails=read('L4_followup.json')['records'];movies=read('L4_trivial_movies.json')['records'];trivial={r['band']:r for r in movies}
        assert {r['band'] for r in tails}=={r['band'] for r in data['records'] if r['status']=='inconclusive_specializations_zero'}
        for r in tails:
            if r['status']=='excluded_multivariable_minor':
                A,_=multivariable_fox(r['pd'],r['variables']);n=r['minor_size'];M=A[:n,:n].tolist()
                assert detmod(M,r['modulus'])==r['determinant_mod_p']!=0
                assert bareiss_det(M)%r['modulus']==r['determinant_mod_p'];checked_multi+=1
            else:
                mv=trivial[r['band']];q=r['pd'];assert q==mv['source_band_pd'];u=0
                for step in mv['movie']:
                    assert q==step['before']
                    spec=[tuple(z) for z in step['R3_triple']]
                    qq,uu,replayed=apply(q,spec)
                    # JSON conversion canonicalizes tuples without weakening the check.
                    assert json.loads(json.dumps(replayed))==step
                    q=qq;u+=uu
                assert u==1 and q==mv['result_pd'] and sig(q)==sig(pd);checked_movies+=1
        assert checked_movies==50 and checked_multi==12
    result={'level':a.level,'shard':a.shard,'shards':a.shards,'enumerated_records_replayed':total,'independent_integer_spot_checks':integer_spot_checks,'multivariable_certificates_replayed':checked_multi,'self_return_movies_replayed':checked_movies,'all_checks_passed':True,'elapsed_seconds':time.time()-start}
    (ROOT/f'replay_L{a.level}_shard{a.shard}_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
