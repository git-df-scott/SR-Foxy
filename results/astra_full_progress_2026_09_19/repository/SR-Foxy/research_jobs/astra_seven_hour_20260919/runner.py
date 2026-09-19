#!/usr/bin/env python3
"""Checkpointed, bounded Slice--Ribbon movie search. Nominations are NOT proofs.

No network calls, remote writes, or automatic retries. Elementary moves and
parent chains are stored in SQLite. Interruptions are not mathematical negatives.
Two modes: common-upper birth/fusion movies and stabilized ribbon-disk movies.
"""
from __future__ import annotations
import argparse, contextlib, hashlib, importlib.metadata, json, math, os
from pathlib import Path
import random, signal, sqlite3, sys, time, traceback, zlib
from collections import Counter
import networkx as nx
import regina
from spherogram import Link, Crossing
from spherogram.links import simplify
from spherogram.links.bands.core import Band, add_one_band, normalize_crossing_labels, min_len_bands
from spherogram.links.simplify import dual_graph_as_nx

HERE = Path(__file__).resolve().parent
class ControlFailure(RuntimeError): pass
class ComputationTimeout(TimeoutError): pass

def require(condition, message):
    if not condition: raise ControlFailure(message)

def compact(value): return json.dumps(value, sort_keys=True, separators=(',', ':'))
def pack(value): return zlib.compress(compact(value).encode(), 6)
def unpack(value): return json.loads(zlib.decompress(value))
def utc(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2, sort_keys=True); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    temp.replace(path)

def pd(link): return [list(row) for row in link.PD_code()]
def normal(link):
    normalize_crossing_labels(link)
    return link

def load(state):
    link = Link(state['pd']); link.unlinked_unknot_components = int(state.get('circles', 0))
    return normal(link)

def state(link): return {'pd': pd(link), 'circles': int(link.unlinked_unknot_components)}
def total_components(link): return len(link.link_components) + link.unlinked_unknot_components

def regina_link(link):
    # PD_code supplies oriented PD, unlike arbitrary raw dart rows.
    return regina.Link.fromPD([[v+1 for v in row] for row in link.PD_code()]) if link.crossings else regina.Link(0)

def signature(link):
    return regina_link(link).sig(False, True, True) + ':' + str(link.unlinked_unknot_components)

def rebuild(link):
    circles = link.unlinked_unknot_components
    link._rebuild(True)
    link.unlinked_unknot_components = circles
    normal(link)

def reduce_movie(link, rng, trials=32):
    """Use only recorded elementary RI/RII/RIII moves, never numerical matching."""
    journal=[]; failures=0
    while True:
        changed=False
        for index, crossing in enumerate(list(link.crossings)):
            eliminated,_ = simplify.reidemeister_I_and_II(link, crossing)
            if eliminated:
                journal.append({'move':'RI_II','at':index,'removed':len(eliminated)})
                rebuild(link); changed=True; failures=0; break
        if changed: continue
        if not link.crossings or failures>=trials: break
        faces=simplify.possible_type_III_moves(link)
        if not faces: break
        face=rng.choice(faces)
        journal.append({'move':'RIII','face':[[int(x.crossing.label),int(x.strand_index)] for x in face]})
        simplify.reidemeister_III(link,face); rebuild(link); failures+=1
    require(link.is_planar(), 'Reduction produced a nonplanar diagram')
    return journal

def replay_reduction(link,journal):
    for entry in journal:
        normal(link)
        if entry['move']=='RI_II':
            require(0<=entry['at']<len(link.crossings),'Invalid RI/II index')
            eliminated,_=simplify.reidemeister_I_and_II(link,link.crossings[entry['at']])
            require(len(eliminated)==entry['removed'] and bool(eliminated),'RI/II replay mismatch')
        elif entry['move']=='RIII':
            options=simplify.possible_type_III_moves(link)
            face=next((f for f in options if [[int(x.crossing.label),int(x.strand_index)] for x in f]==entry['face']),None)
            require(face is not None,'Invalid RIII face')
            simplify.reidemeister_III(link,face)
        else: raise ControlFailure('Unknown reduction move')
        rebuild(link)
    return link

def birth(link, anchor, under=False):
    """Add a split unknot with two cancellable crossings near one edge.
    The inverse RII cancellation is a mandatory control, not a guessed unlink.
    """
    out=link.copy(); normal(out)
    c,p=anchor; X=out.crossings[c]; Y,q=X.adjacent[p]
    U,V=Crossing(len(out.crossings)),Crossing(len(out.crossings)+1)
    shift=1 if under else 0
    X[p]=U[shift]; U[(shift+2)%4]=V[shift]; V[(shift+2)%4]=Y[q]
    U[(shift+1)%4]=V[(shift+1)%4]; U[(shift+3)%4]=V[(shift+3)%4]
    out.crossings.extend([U,V]); out._rebuild(); normal(out)
    require(out.is_planar() and total_components(out)==total_components(link)+1,'Birth topology control failed')
    return out

def sampled_band(link,rng,mode,max_crossed,max_twists):
    """Sample a simple augmented face path, retaining selected dual edges.
    Sampling is NOT a complete enumeration of this parameter box.
    """
    dual=dual_graph_as_nx(link,graph_class=nx.MultiGraph)
    mapping={}
    for f,g,info in dual.edges(data=True):
        for h,cs in info['interface'].items(): mapping[cs]=h
    all_cs=[cs for comp in link.link_components for cs in comp]
    cmap={}
    for i,comp in enumerate(link.link_components):
        for cs in comp:
            cmap[(cs.crossing,cs.strand_index)]=i
            cmap[(cs.crossing,(cs.strand_index+2)%4)]=i
    def ci(cs): return cmap[(cs.crossing,cs.strand_index)]
    for _ in range(64):
        cs=rng.choice(all_cs); X=cs if rng.getrandbits(1) else cs.opposite()
        if X not in mapping or X.opposite() not in mapping: continue
        F=mapping[X]; P0=mapping[X.opposite()]
        if F==P0: continue
        visited={F}; interior=[]; goal=rng.randrange(max_crossed+1)
        valid=True
        for __ in range(goal):
            options=[(g,info) for g,edges in dual[F].items() if g not in visited and g!=P0 for info in edges.values()]
            if not options: valid=False; break
            F,info=rng.choice(options); interior.append(info['interface'][F]); visited.add(F)
        if not valid: continue
        ends=[]
        for P1,edges in dual[F].items():
            if P1 in visited or P1==P0: continue
            for info in edges.values():
                Z=info['interface'][P1]
                if (ci(X)==ci(Z)) != (mode=='fission'): continue
                ends.append(Z)
        if not ends: continue
        Z=rng.choice(ends)
        parity=int((X==X.oriented())==(Z==Z.oriented()))
        twists=[t for t in range(-max_twists,max_twists+1) if t%2==parity]
        desc=[(int(c.crossing.label),int(c.strand_index)) for c in [X]+interior+[Z]]
        band=Band(desc,rng.randrange(1<<len(interior)),rng.choice(twists))
        if not band.is_nonminimal(link): return band
    return None

def determinant(link):
    """Absolute integral Fox-coloring cofactor at t=-1, computed by Bareiss."""
    if not link.crossings: return 1
    require(len(link.link_components)==1,'Determinant routine expects a knot')
    ports=[(c,p) for c in link.crossings for p in range(4)]; parent={x:x for x in ports}
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def join(x,y):
        x,y=find(x),find(y)
        if x!=y: parent[y]=x
    for c,p in ports: join((c,p),c.adjacent[p])
    for c in link.crossings: join((c,1),(c,3))
    roots=list(dict.fromkeys(find(x) for x in ports)); ids={x:i for i,x in enumerate(roots)}
    n=len(roots); rows=[]
    for c in link.crossings:
        row=[0]*n
        row[ids[find((c,1))]]+=2
        row[ids[find((c,0))]]-=1; row[ids[find((c,2))]]-=1; rows.append(row)
    require(len(rows)==n,'Unexpected Fox cofactor dimensions')
    A=[row[:-1] for row in rows[:-1]]; n-=1
    if n==0:return 1
    sign=1; denom=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k]; sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=A[i][j]*p-A[i][k]*A[k][j]
                require(v%denom==0,'Nonintegral Bareiss division')
                A[i][j]=v//denom
        for i in range(k+1,n):A[i][k]=0
        denom=p
    return abs(sign*A[-1][-1])

def possible_slice_components(link):
    if any(x for row in link.linking_matrix() for x in row):return False,'NONZERO_LINKING'
    for i in range(len(link.link_components)):
        d=determinant(link.sublink(i))
        if math.isqrt(d)**2!=d:return False,'NONSQUARE_COMPONENT_DETERMINANT'
    return True,'PASSED_NECESSARY_FILTERS_ONLY'

def inputs():
    obj=json.loads((HERE/'INPUTS.json').read_text())
    K0=normal(Link('6_3')); K1=normal(Link(obj['K1']))
    W0=normal(Link(obj['wild_pair'][0])); W1=normal(Link(obj['wild_pair'][1]))
    D=normal(Link(obj['D01'])); WD=normal(W0.connected_sum(W1.mirror()))
    return {'AT':(K0,K1),'wild17':(W0,W1)}, {'D01':D,'wild17':WD}

def verify_step(before,entry,after):
    L=load(before)
    if entry.get('pre_reduction'):replay_reduction(L,entry['pre_reduction'])
    if entry['kind']=='birth_fusion':
        L=birth(L,entry['anchor'],entry['under'])
        require(state(L)==entry['born'],'Birth replay mismatch')
    require(state(L)==entry['before_band'],'Band input mismatch')
    b=Band(entry['band']); n=total_components(L)
    from spherogram.links.links_base import CrossingStrand
    X,Z=[CrossingStrand(L.crossings[c],p) for c,p in (b.cs_along_top[0],b.cs_along_top[-1])]
    require(b.num_twist%2==int((X==X.oriented())==(Z==Z.oriented())),'Band parity mismatch')
    L=add_one_band(L,b); normal(L)
    delta=1 if entry['kind']=='fission' else -1
    require(total_components(L)==n+delta,'Saddle component count failed')
    require(state(L)==entry['after_band'],'Band output mismatch')
    replay_reduction(L,entry['reduction'])
    require(L.unlinked_unknot_components==entry['deaths'],'Death count mismatch')
    L.unlinked_unknot_components=0
    require(state(L)==after,'Movie endpoint mismatch')
    return True

@contextlib.contextmanager
def time_limit(seconds):
    def alarm(*_):raise ComputationTimeout('Per-operation time bound exceeded')
    old=signal.signal(signal.SIGALRM,alarm); signal.setitimer(signal.ITIMER_REAL,seconds)
    try:yield
    finally:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)

def controls(out):
    started=time.monotonic(); result={'status':'CONTROL_FAILURE','checks':[],'at':utc()}
    def ok(s):result['checks'].append(s)
    try:
        versions={n:importlib.metadata.version(n) for n in ['snappy','spherogram','regina','sympy','networkx']}
        require(versions['spherogram']=='2.4.1' and versions['regina']=='7.4.1','Unsupported topology version')
        result['versions']=versions
        result['source_sha256']={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('runner.py','INPUTS.json','requirements.txt')}
        result['source_commit']=os.environ.get('GITHUB_SHA','LOCAL_TEST')
        for name,expected in [('3_1',3),('4_1',5),('6_1',9),('6_3',13),('8_8',25)]:
            L=normal(Link(name));require(determinant(L)==expected,'Fox determinant control '+name)
            R=regina_link(L);require(R.size()==len(L.crossings) and R.countComponents()==1,'PD adapter control')
        ok('Five exact determinant and oriented-PD adapter controls')
        require(signature(normal(Link('3_1')))!=signature(normal(Link('3_1').mirror())),'Mirror-sensitive signature failed')
        ok('Trefoil and mirror are NOT matched')
        births=0
        for name in ['3_1','6_1']:
            L=normal(Link(name))
            for p in range(4):
                for under in [False,True]:
                    B=birth(L,[0,p],under)
                    eliminated,_=simplify.reidemeister_I_and_II(B,B.crossings[-2]);rebuild(B)
                    require(len(eliminated)==2 and B.unlinked_unknot_components==1,'Birth is not a cancelling RII pair')
                    B.unlinked_unknot_components=0
                    require(signature(B)==signature(L),'Birth changed the original knot')
                    births+=1
        ok(str(births)+' births cancel to the original knot plus one split circle')
        pairs,_=inputs();hyp={}
        import sympy as sp
        t=sp.Symbol('t')
        for family,(A,B) in pairs.items():
            records=[]
            for L in (A,B):
                h=L.knot_floer_homology();coeff=Counter()
                for (a,m),v in h['ranks'].items():coeff[a]+=(-1 if m%2 else 1)*v
                coeff={a:v for a,v in coeff.items() if v};lo=min(coeff)
                poly=sp.Poly(sum(v*t**(a-lo) for a,v in coeff.items()),t)
                require(h['fibered'] and poly.is_irreducible,'Nonribbon-input hypothesis failed')
                records.append({'fibered':h['fibered'],'genus':h['seifert_genus'],'alexander':str(poly.as_expr()),'jones':str(regina_link(L).jones()),'pd':pd(L)})
            require(records[0]['alexander']==records[1]['alexander'],'Alexander inputs do not match')
            require(records[0]['jones']!=records[1]['jones'],'Input distinctness control failed')
            hyp[family]=records
        result['input_hypotheses']=hyp
        ok('Both fibered-pair inputs: irreducible common Alexander polynomial; unequal exact Jones')
        ribbon=[]
        for mirrored in [False,True]:
            L=normal(Link('6_1').mirror() if mirrored else Link('6_1'))
            found=None
            for b in min_len_bands(L,max_twists=2,max_band_len=4):
                B=normal(add_one_band(L,b));after_band=state(B)
                journal=reduce_movie(B,random.Random(101),32)
                if not B.crossings:
                    e={'kind':'fission','before_band':state(L),'band':b.compressed_spec(),'after_band':after_band,'reduction':journal,'deaths':B.unlinked_unknot_components}
                    B.unlinked_unknot_components=0
                    require(e['deaths']==2 and verify_step(state(L),e,state(B)),'Ribbon movie control failed')
                    bad=json.loads(compact(e));bad['deaths']+=1
                    rejected=False
                    try:verify_step(state(L),bad,state(B))
                    except ControlFailure:rejected=True
                    require(rejected,'Corrupted death ledger accepted')
                    found={'input':state(L),'step':e,'output':state(B)};break
            require(found is not None,'Stevedore ribbon positive control not found')
            ribbon.append(found)
        result['ribbon_controls']=ribbon;ok('Stevedore and mirror: replayed one-band/two-death movies; corrupt ledgers rejected')
        L=normal(Link('6_1'));r=random.Random(234);tested=0
        for mode in ['fission','fusion']:
            M=birth(L,[0,0]) if mode=='fusion' else L
            for _ in range(80):
                b=sampled_band(M,r,mode,4,6)
                if b is None:continue
                N=normal(add_one_band(M,b))
                require(N.is_planar() and total_components(N)==total_components(M)+(1 if mode=='fission' else -1),'Sampled band control failed')
                tested+=1
        require(tested>=100,'Too few sampled-band controls')
        ok(str(tested)+' sampled multiedge band component-count controls')
        result['status']='PASS'
    except BaseException:
        result['error']=traceback.format_exc();raise
    finally:
        result['seconds']=time.monotonic()-started;write_json(Path(out)/'CONTROLS.json',result)
    print(compact({'controls':result['status'],'checks':result['checks'],'seconds':result['seconds']}),flush=True)
    return result

def open_db(out):
    db=sqlite3.connect(Path(out)/'evidence.sqlite',timeout=60)
    db.execute('PRAGMA journal_mode=DELETE');db.execute('PRAGMA synchronous=FULL')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS nodes(id INTEGER PRIMARY KEY,phase TEXT,target TEXT,side INTEGER,depth INTEGER,deaths INTEGER,crossings INTEGER,sig TEXT,parent INTEGER,payload BLOB,UNIQUE(phase,target,side,depth,deaths,sig));
    CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,phase TEXT,segment INTEGER,target TEXT,side INTEGER,parent INTEGER,seed INTEGER,status TEXT,band TEXT,params TEXT,seconds REAL,child INTEGER,error TEXT);
    CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,phase TEXT,segment INTEGER,status TEXT,started TEXT,finished TEXT,seconds REAL,cpu_seconds REAL,summary TEXT);
    CREATE INDEX IF NOT EXISTS match_endpoint ON nodes(phase,target,sig,side);
    CREATE INDEX IF NOT EXISTS choose_parent ON nodes(phase,target,side,depth,crossings);
    ''');db.commit();return db

def node(db,phase,target,side,depth,deaths,L,parent,entry):
    sig=signature(L);data={'state':state(L),'step':entry}
    cur=db.execute('INSERT OR IGNORE INTO nodes(phase,target,side,depth,deaths,crossings,sig,parent,payload) VALUES(?,?,?,?,?,?,?,?,?)',(phase,target,side,depth,deaths,len(L.crossings),sig,parent,pack(data)))
    ident=db.execute('SELECT id FROM nodes WHERE phase=? AND target=? AND side=? AND depth=? AND deaths=? AND sig=?',(phase,target,side,depth,deaths,sig)).fetchone()[0]
    return ident, bool(cur.rowcount),sig

def path_to(db,ident):
    chain=[]
    while ident is not None:
        row=db.execute('SELECT id,parent,payload,depth,deaths,target,side FROM nodes WHERE id=?',(ident,)).fetchone()
        require(row is not None,'Missing movie parent')
        data=unpack(row[2]);data.update({'id':row[0],'depth':row[3],'deaths':row[4],'target':row[5],'side':row[6]});chain.append(data);ident=row[1]
    chain.reverse()
    for a,b in zip(chain,chain[1:]):verify_step(a['state'],b['step'],b['state'])
    return chain

def export(out,db,phase,segment,status,started,wall,cpu,counts):
    db.commit()
    require(db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity failure')
    runs=[{'phase':r[0],'segment':r[1],'status':r[2],'started':r[3],'finished':r[4],'seconds':r[5],'cpu_seconds':r[6],'summary':json.loads(r[7])} for r in db.execute('SELECT phase,segment,status,started,finished,seconds,cpu_seconds,summary FROM runs ORDER BY id')]
    summary={'status':status,'phase':phase,'segment':segment,'source_commit':os.environ.get('GITHUB_SHA','LOCAL_TEST'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'started':started,'updated':utc(),'current_search_seconds':wall,'current_cpu_seconds':cpu,'counts':dict(counts),'runs':runs,'measured_completed_segment_seconds':sum(r['seconds'] or 0 for r in runs),'counterexample_established':False,'scope':'Randomized bounded movie search, not an exhaustive search or an impossibility proof. Nominations need independent topology and nonribbon-hypothesis audits.'}
    write_json(Path(out)/'RUN.json',summary)
    write_json(Path(out)/f'RUN-{phase}-{segment}.json',summary)
    return summary

def search(out,phase,segment,seconds):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    control=json.loads((out/'CONTROLS.json').read_text());require(control['status']=='PASS','Controls must pass before searching')
    require(not (out/'POTENTIAL_COUNTEREXAMPLE.json').exists(),'A nomination already exists; refusing to continue')
    db=open_db(out);pairs,differences=inputs();roots={}
    if phase=='common_upper':
        for name,(A,B) in pairs.items():
            for side,L in enumerate([A,B]):roots[(name,side)]=node(db,phase,name,side,0,0,L,None,None)[0]
    else:
        for name,D in differences.items():
            for mirrored in [False,True]:
                J=normal(Link('6_1').mirror() if mirrored else Link('6_1'))
                target=name+('#mirror6_1' if mirrored else '#6_1')
                roots[(target,0)]=node(db,phase,target,0,0,0,normal(D.connected_sum(J)),None,None)[0]
    db.commit();rng=random.Random(202609190000+segment+(0 if phase=='common_upper' else 10000))
    started=utc();start=time.monotonic();cpu=time.process_time();counts=Counter();status='RUNNING';last_report=start
    rid=db.execute('INSERT INTO runs(phase,segment,status,started,seconds,cpu_seconds,summary) VALUES(?,?,?,?,?,?,?)',(phase,segment,'RUNNING',started,0,0,'{}')).lastrowid;db.commit()
    export(out,db,phase,segment,status,started,0,0,counts)
    try:
        while time.monotonic()-start<seconds:
            target,side=rng.choice(list(roots));parent=roots[(target,side)]
            max_depth=2 if phase=='common_upper' else 5
            if rng.random()<0.75:
                options=db.execute('SELECT id FROM nodes WHERE phase=? AND target=? AND side=? AND depth<? ORDER BY crossings ASC,id DESC LIMIT 384',(phase,target,side,max_depth)).fetchall()
                if options:parent=rng.choice(options)[0]
            row=db.execute('SELECT depth,deaths,payload FROM nodes WHERE id=?',(parent,)).fetchone();depth,deaths=row[:2];before=unpack(row[2])['state']
            seed=rng.randrange(2**62);r=random.Random(seed);attempt=time.monotonic();bandstr=None;child=None;error=None
            max_crossed=(2,3,4,5,6)[(segment-1)%5];max_twists=(4,6,8,6,8,10,10)[(segment-1)%7]
            params={'max_crossed_edges':max_crossed,'max_abs_half_twists':max_twists,'max_depth':max_depth,'crossing_cap':72,'RIII_trials':48,'seed':seed}
            try:
                with time_limit(min(45,max(1,seconds-(time.monotonic()-start)))):
                    L=load(before);pre=reduce_movie(L,r,r.choice([0,12,32]) if depth==0 else 0)
                    require(not L.unlinked_unknot_components,'Unexpected circle in parent deformation')
                    e={'kind':'birth_fusion' if phase=='common_upper' else 'fission','pre_reduction':pre}
                    if phase=='common_upper':
                        anchor=[r.randrange(len(L.crossings)),r.randrange(4)];under=bool(r.getrandbits(1))
                        L=birth(L,anchor,under);e.update(anchor=anchor,under=under,born=state(L))
                    e['before_band']=state(L);b=sampled_band(L,r,'fusion' if phase=='common_upper' else 'fission',max_crossed,max_twists)
                    if b is None:outcome='NO_SAMPLED_BAND'
                    else:
                        bandstr=b.compressed_spec();N=normal(add_one_band(L,b));e['band']=bandstr;e['after_band']=state(N)
                        require(total_components(N)==total_components(L)+(-1 if phase=='common_upper' else 1),'Saddle component count failed')
                        if len(N.crossings)>72:outcome='CROSSING_CAP'
                        else:
                            e['reduction']=reduce_movie(N,r,48);e['deaths']=N.unlinked_unknot_components;N.unlinked_unknot_components=0
                            if phase=='common_upper':
                                require(len(N.link_components)==1 and e['deaths']==0,'Birth-fusion did not end in one knot')
                                passed=True;why='UPPER_KNOT'
                            else:passed,why=possible_slice_components(N)
                            if not passed:outcome=why
                            else:
                                child,new,sig=node(db,phase,target,side,depth+1,deaths+e['deaths'],N,parent,e)
                                outcome='NEW_ENDPOINT' if new else 'DUPLICATE_ENDPOINT'
                                if new and counts['NEW_ENDPOINT']%100==0:verify_step(before,e,state(N))
                                match=None
                                if phase=='common_upper':
                                    match=db.execute('SELECT id FROM nodes WHERE phase=? AND target=? AND side=? AND sig=? LIMIT 1',(phase,target,1-side,sig)).fetchone()
                                elif not N.crossings:
                                    require(deaths+e['deaths']==depth+2,'Ribbon disk Euler-count failure');match=(child,)
                                if match:
                                    db.commit();chains=[path_to(db,child)]
                                    if phase=='common_upper':chains.append(path_to(db,match[0]))
                                    nomination={'status':'POTENTIAL_COUNTEREXAMPLE_NOT_INDEPENDENTLY_AUDITED','phase':phase,'target':target,'at':utc(),'node_ids':[child,match[0]],'chains':chains,'required_audit':['Independent elementary-movie replay and orientation/framing checks','Exact same-knot endpoint identification, disallowing mirror-only matches','Nonribbon hypotheses for the same actual difference knot','For stabilized disks, the partner ribbon-disk certificate'],'counterexample_established':False}
                                    write_json(out/'POTENTIAL_COUNTEREXAMPLE.json',nomination);status='POTENTIAL_COUNTEREXAMPLE';outcome=status
            except ComputationTimeout as exc:outcome='UNKNOWN_TIMEOUT';error=str(exc)
            except ControlFailure:raise
            except Exception:outcome='UNKNOWN_ERROR';error=traceback.format_exc()
            counts[outcome]+=1;counts['attempts']+=1
            # Keep every new endpoint/unknown/hit; sample other attempt rows 1/32.
            # RUN summaries retain exact counters for ALL attempts.
            if outcome in ('NEW_ENDPOINT','POTENTIAL_COUNTEREXAMPLE','UNKNOWN_ERROR','UNKNOWN_TIMEOUT') or counts['attempts']%32==0:
                db.execute('INSERT INTO attempts(phase,segment,target,side,parent,seed,status,band,params,seconds,child,error) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(phase,segment,target,side,parent,seed,outcome,bandstr,compact(params),time.monotonic()-attempt,child,error))
            db.commit()
            if status=='POTENTIAL_COUNTEREXAMPLE':break
            if counts['attempts']>=20 and counts['UNKNOWN_ERROR']>counts['attempts']//4:
                raise ControlFailure('Excessive UNKNOWN_ERROR rate; stop rather than waste the budget')
            if time.monotonic()-last_report>=60:
                elapsed=time.monotonic()-start
                db.execute('UPDATE runs SET seconds=?,cpu_seconds=?,summary=? WHERE id=?',(elapsed,time.process_time()-cpu,compact(dict(counts)),rid));db.commit()
                export(out,db,phase,segment,'RUNNING',started,elapsed,time.process_time()-cpu,counts)
                print(compact({'phase':phase,'segment':segment,'search_seconds':elapsed,'counts':dict(counts)}),flush=True);last_report=time.monotonic()
        if status=='RUNNING':status='BOUNDED_SEGMENT_COMPLETE_NO_NOMINATION'
    except BaseException:
        status='CONTROL_FAILURE_OR_INTERRUPTION';write_json(out/'FAILURE.json',{'status':status,'at':utc(),'error':traceback.format_exc(),'phase':phase,'segment':segment});raise
    finally:
        wall=time.monotonic()-start;used=time.process_time()-cpu
        db.execute('UPDATE runs SET status=?,finished=?,seconds=?,cpu_seconds=?,summary=? WHERE id=?',(status,utc(),wall,used,compact(dict(counts)),rid));db.commit()
        export(out,db,phase,segment,status,started,wall,used,counts);db.close()
        print(compact({'status':status,'seconds':wall,'counts':dict(counts)}),flush=True)
    return 42 if status=='POTENTIAL_COUNTEREXAMPLE' else 0

def main():
    def terminate(*_):raise KeyboardInterrupt('Termination signal received')
    signal.signal(signal.SIGTERM,terminate)
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='evidence');ap.add_argument('--controls',action='store_true');ap.add_argument('--phase',choices=['common_upper','stabilized_disks']);ap.add_argument('--segment',type=int,default=1);ap.add_argument('--seconds',type=float,default=1800);args=ap.parse_args()
    Path(args.out).mkdir(parents=True,exist_ok=True)
    if args.controls:controls(args.out);return 0
    require(args.phase is not None and 0<args.seconds<=1800,'Invalid search arguments')
    return search(args.out,args.phase,args.segment,args.seconds)
if __name__=='__main__':sys.exit(main())
