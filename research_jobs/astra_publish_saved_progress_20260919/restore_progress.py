#!/usr/bin/env python3
"""Restore saved evidence bytes; do not execute research or infer scientific results.
Every reconstructed database, archive and package manifest has an expected digest.
"""
import argparse, base64, functools, hashlib, io, json, lzma, os
from pathlib import Path
import sqlite3, subprocess, zipfile, zlib

def sha(data): return hashlib.sha256(data).hexdigest()
def check(data, digest, label):
    if sha(data) != digest: raise RuntimeError('Digest mismatch: '+label+' actual='+sha(data))
    return data

def decode_plan(root):
    parts = ''.join((root/'transfer'/f'plan-{i:02}.b64').read_text().strip() for i in range(21))
    if parts[163888:163894] != 'RqhdtQ': raise RuntimeError('Unexpected transfer prefix')
    parts=parts[:163888]+'DFtZTw'+parts[163894:]
    for i in range(21,24): parts+=(root/'repair'/f'tail-{i}.b64').read_text().strip()
    data=base64.b64decode(parts,validate=True)
    check(data,'55a46bcae475e7cd3a7343481b46d699bb985ef1eae82379dae1c37f3afddacf','restored plan')
    return json.loads(lzma.decompress(data))

HEADERS={
'completed':'U1FMaXRlIGZvcm1hdCAzABAAAQEAQCAgAABkdQAAHXkAAAAAAAAAAAAAAAUAAAAEAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGR1AC52iQ==',
'recovered':'U1FMaXRlIGZvcm1hdCAzABAAAQEAQCAgAAAABAAAI7oAAAAAAAAAAAAAAAUAAAAEAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAC56cQ=='
}
DBHASH={'completed':'8003e6108f89b30028735c47381f3dce69b80ed478934327b071e1b13e6c8888','recovered':'11ccb2a35246786f1235ab24aa0d75b35c680a3fe04c55d1426a76f6510a7348'}

def restore_databases(terminal, work):
    src=sqlite3.connect(f'file:{terminal.resolve()}?mode=ro',uri=True)
    schema=src.execute('select type,name,sql from sqlite_master where sql is not null').fetchall()
    def rows(table,cap):
        out=[]
        try:
            for r in src.execute(f'SELECT * FROM {table} NOT INDEXED ORDER BY id'):
                if r[0]>cap:break
                out.append(r)
        except sqlite3.DatabaseError:
            if len(out)!=cap: raise
        if len(out)!=cap:raise RuntimeError('Unexpected readable row count '+table)
        return out
    nodes=rows('nodes',25669);attempts=rows('attempts',31235);runs=rows('runs',3)
    def insert(db,table,row):db.execute(f'INSERT INTO {table} VALUES ({",".join("?" for _ in row)})',row)
    def finalize(db,row):
        db.execute('UPDATE runs SET status=?,finished=?,seconds=?,cpu_seconds=?,summary=? WHERE id=?',(row[3],row[5],row[6],row[7],row[8],row[0]));db.commit()
    paths={}
    for kind in ('completed','recovered'):
        path=work/(kind+'.sqlite')
        if path.exists():path.unlink()
        db=sqlite3.connect(path)
        if kind=='completed':
            db.execute('PRAGMA journal_mode=DELETE');db.execute('PRAGMA synchronous=FULL')
            for _,_,sql in schema:db.execute(sql)
            for row in nodes[:4]:insert(db,'nodes',row)
            db.commit();old=None
            for a in attempts[:25649]:
                seg=a[2]
                if seg!=old:
                    if old is not None:finalize(db,runs[old-1])
                    r=runs[seg-1];insert(db,'runs',(r[0],r[1],r[2],'RUNNING',r[4],None,0,0,'{}'));db.commit();old=seg
                if a[7]=='NEW_ENDPOINT':insert(db,'nodes',nodes[a[11]-1])
                insert(db,'attempts',a);db.commit()
            finalize(db,runs[1])
        else:
            for typ,_,sql in schema:
                if typ=='table':db.execute(sql)
            for table,rr in [('nodes',nodes),('attempts',attempts),('runs',runs)]:
                for row in rr:
                    if table=='nodes':
                        obj=json.loads(zlib.decompress(row[-1]))
                        if not isinstance(obj,dict) or 'state' not in obj:raise RuntimeError('Corrupt node')
                    insert(db,table,row)
            for typ,_,sql in schema:
                if typ=='index':db.execute(sql)
            db.commit()
        if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Restored DB integrity failed')
        db.close()
        # Restore original SQLite header metadata (write counters / writer version).
        # This is accepted only when the COMPLETE file equals the saved SHA-256.
        raw=path.read_bytes();raw=base64.b64decode(HEADERS[kind])+raw[100:]
        check(raw,DBHASH[kind],kind+' SQLite');path.write_bytes(raw);paths[kind]=path
    src.close();return paths

class Restore:
    def __init__(self, plan, repo, artifacts, out, work):
        self.p=plan;self.repo=repo;self.a=artifacts;self.out=out;self.work=work
        self.blobs={};self.zips={};self.modes={}
        for k,v in plan['artifacts'].items():check((artifacts/(k+'.zip')).read_bytes(),v['sha256'],'artifact '+k)
        self.out.mkdir(parents=True,exist_ok=True)
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.repo),*args])
    @functools.lru_cache(None)
    def tree(self,commit):
        entries=[]
        for record in self.git('ls-tree','-rz',commit).split(b'\0'):
            if not record:continue
            meta,path=record.split(b'\t');mode,kind,blob=meta.decode().split()
            if kind!='blob':raise RuntimeError('Non-blob snapshot member')
            entries.append((path.decode(),mode,blob))
        return sorted(entries,key=lambda entry:Path(entry[0]).parts)
    def blob(self,key):
        if key not in self.blobs:
            data=self.git('cat-file','blob',key)
            if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=key:raise RuntimeError('Git blob mismatch')
            self.blobs[key]=data
        return self.blobs[key]
    def literal(self,key):
        value=self.p['literals'][key];typ=value[0]
        if typ=='t':data=value[1].encode()
        elif typ=='j':data=(json.dumps(value[1],indent=2)+'\n').encode()
        elif typ=='source_manifest':
            record=dict(value[1]);record['files']=[]
            for path,mode,blob in self.tree(record['commit']):
                data=self.blob(blob)
                record['files'].append({'path':path,'bytes':len(data),'sha256':sha(data),'git_blob_sha1':blob,'git_mode':mode})
            data=(json.dumps(record,indent=2)+'\n').encode()
        else:raise RuntimeError('Unknown literal '+typ)
        return check(data,key,'literal')
    def source(self,descriptor):
        typ,key=descriptor[:2]
        if typ=='g':return self.blob(key)
        if typ=='l':return self.literal(key)
        if typ=='p':return self.file(key)
        if typ=='z':return self.archive(key)
        if typ=='a':
            key=str(key);member=descriptor[2]
            if member is None:return (self.a/(key+'.zip')).read_bytes()
            if key not in self.zips:self.zips[key]=zipfile.ZipFile(self.a/(key+'.zip'))
            return self.zips[key].read(member)
        raise RuntimeError('Unknown source '+typ)
    def save(self,path,data,mode=0o644):
        target=self.out/path
        if Path(path).is_absolute() or '..' in Path(path).parts:raise RuntimeError('Unsafe output path')
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and target.read_bytes()!=data:raise RuntimeError('Refusing to replace different bytes '+path)
        target.write_bytes(data);target.chmod(mode);self.modes[path]=mode
        return data
    def file(self,path):
        target=self.out/path
        if target.exists():
            self.modes.setdefault(path,0o600 if path.startswith('earlier_saved_packages/combined_readable/') else 0o644)
            return target.read_bytes()
        mode=0o600 if path.startswith('earlier_saved_packages/combined_readable/') else 0o644
        return self.save(path,self.source(self.p['files'][path]),mode)
    def archive(self,path):
        rec=self.p['zip_recipes'][path];buf=io.BytesIO()
        if rec.get('python_zip'):
            with zipfile.ZipFile(buf,'w') as z:
                z.comment=base64.b64decode(rec['comment'])
                def put(name,data,metaid):
                    m=rec['metas'][metaid];info=zipfile.ZipInfo(name,tuple(m[0]))
                    for field,val in zip(('compress_type','create_system','create_version','extract_version','reserved','flag_bits','volume','internal_attr','external_attr'),m[1:10]):setattr(info,field,val)
                    info.extra=base64.b64decode(m[10]);info.comment=base64.b64decode(m[11])
                    level=m[12][0] if m[12] else None
                    z.writestr(info,data,compresslevel=level)
                g=rec.get('git_source_prefix')
                if g:
                    entries=self.tree(g['commit'])
                    if len(entries)!=g['file_count']:raise RuntimeError('Historical snapshot count')
                    for name,mode,blob in entries:put(g['prefix']+name,self.blob(blob),g['metadata_executable'] if mode=='100755' else g['metadata_regular'])
                for name,src,metaid in rec['entries']:put(name,self.source(src),metaid)
        else:
            for header,src,compression in rec['entries']:
                buf.write(base64.b64decode(header));data=self.source(src)
                compressed=subprocess.check_output(['node','-e',"const fs=require('fs'),z=require('zlib');process.stdout.write(z.deflateRawSync(fs.readFileSync(0),{level:Number(process.argv[1])}));",str(compression[1])],input=data)
                buf.write(compressed)
            buf.write(base64.b64decode(rec['tail']))
        data=buf.getvalue();check(data,rec['sha256'],'archive '+path)
        print('Restored exact ZIP',path,len(data),flush=True);return data
    def run(self):
        tree=self.tree(self.p['snapshot'])
        if len(tree)!=2287:raise RuntimeError('Snapshot file count changed')
        for path,mode,blob in tree:self.save('repository/SR-Foxy/'+path,self.blob(blob),0o755 if mode=='100755' else 0o644)
        print('Restored 2287 snapshot files',flush=True)
        terminal=self.work/'terminal.sqlite';terminal.write_bytes(self.source(['a',10589621369,'evidence.sqlite']))
        dbs=restore_databases(terminal,self.work)
        self.save('search_run/completed_checkpoint/evidence.sqlite',dbs['completed'].read_bytes())
        self.save('search_run/recovered_partial/readable_partial.sqlite',dbs['recovered'].read_bytes())
        print('Both exact SQLite digests match',flush=True)
        for path in self.p['files']:self.file(path)
        entries=[]
        for path in sorted((p for p in self.modes if p not in ('MANIFEST.json','VERIFICATION_RESULT.json')),key=lambda p:Path(p).parts):
            data=(self.out/path).read_bytes();entries.append({'path':path,'bytes':len(data),'sha256':sha(data),'mode_octal':oct(self.modes[path])})
        manifest={'format':'sha256-per-file-v1','package':'SR_Foxy_Full_Progress_2026-09-19','files':entries,'payload_files':len(entries),'payload_bytes':sum(e['bytes'] for e in entries),'unhashed_metadata_files':['MANIFEST.json','VERIFICATION_RESULT.json'],'scope':'Preservation of the pinned repository and recovered evidence. File integrity does not imply mathematical correctness.'}
        raw=(json.dumps(manifest,indent=2)+'\n').encode()
        check(raw,'21ed4c4d79a629791d88ea2a87892574b428e9730d00d41acf0f53bc5fd8da92','COMPLETE ORIGINAL MANIFEST')
        self.save('MANIFEST.json',raw)
        print('FULL ORIGINAL PACKAGE RESTORED:',len(entries),'payload files;',manifest['payload_bytes'],'bytes',flush=True)
        return manifest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--plan',type=Path);ap.add_argument('--transfer-root',type=Path);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--artifacts',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args()
    a.work.mkdir(parents=True,exist_ok=True)
    p=json.loads(a.plan.read_text()) if a.plan else decode_plan(a.transfer_root)
    result=Restore(p,a.repo,a.artifacts,a.out,a.work).run()
    (a.work/'RESTORATION_VERIFIED.json').write_text(json.dumps({'status':'ALL_ORIGINAL_PAYLOAD_HASHES_MATCH','payload_files':result['payload_files'],'payload_bytes':result['payload_bytes'],'original_manifest_sha256':'21ed4c4d79a629791d88ea2a87892574b428e9730d00d41acf0f53bc5fd8da92','search_restarted':False,'counterexample_established':False},indent=2)+'\n')
if __name__=='__main__':main()
