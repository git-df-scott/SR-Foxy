#!/usr/bin/env python3
"""Copy readable row prefixes from an interrupted SQLite snapshot.

Never modifies either input. This is conservative data salvage, NOT a claim of
complete recovery, a mathematical movie verifier, or a search restart.
"""
from __future__ import annotations
import argparse, hashlib, json, sqlite3, zlib
from pathlib import Path

def sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('damaged',type=Path);ap.add_argument('completed',type=Path);ap.add_argument('destination',type=Path)
    a=ap.parse_args();a.destination.mkdir(parents=True,exist_ok=True)
    output=a.destination/'readable_partial.sqlite'
    if output.exists():raise FileExistsError(output)
    src=sqlite3.connect(f'file:{a.damaged.resolve()}?mode=ro',uri=True)
    base=sqlite3.connect(f'file:{a.completed.resolve()}?mode=ro',uri=True)
    dst=sqlite3.connect(output)
    report={'kind':'CONSERVATIVE_READABLE_PREFIX_SALVAGE_NOT_COMPLETE_RECOVERY','source_sha256':sha(a.damaged),'completed_checkpoint_sha256':sha(a.completed),'tables':{},'mathematical_movies_replayed':False,'search_restarted':False}
    report['completed_integrity_check']=[x[0] for x in base.execute('pragma integrity_check')]
    try:report['damaged_integrity_check']=[x[0] for x in src.execute('pragma integrity_check')]
    except sqlite3.DatabaseError as exc:report['damaged_integrity_error']=str(exc)
    schema=src.execute('select type,name,sql from sqlite_master where sql is not null').fetchall()
    for kind,name,sql in schema:
        if kind=='table':dst.execute(sql)
    for table in ('nodes','attempts','runs'):
        record={'rows_copied':0,'last_read_id':None,'read_to_end':False,'rejected_rows':[]}
        try:
            for row in src.execute(f'SELECT * FROM {table} NOT INDEXED ORDER BY id'):
                if table=='nodes':
                    try:
                        value=json.loads(zlib.decompress(row[-1]));assert isinstance(value,dict) and 'state' in value
                    except Exception as exc:
                        record['rejected_rows'].append({'id':row[0],'reason':str(exc)});continue
                dst.execute(f'INSERT INTO {table} VALUES ({",".join("?" for _ in row)})',row)
                record['rows_copied']+=1;record['last_read_id']=row[0]
            record['read_to_end']=True
        except sqlite3.DatabaseError as exc:record['source_read_error']=str(exc)
        exact=0;missing=[];different=[]
        for row in base.execute(f'SELECT * FROM {table} NOT INDEXED ORDER BY id'):
            candidate=dst.execute(f'SELECT * FROM {table} WHERE id=?',(row[0],)).fetchone()
            if candidate is None:missing.append(row[0])
            elif candidate!=row:different.append(row[0])
            else:exact+=1
        record['unchanged_completed_rows']=exact
        record['completed_rows_missing']=missing;record['completed_rows_different']=different
        report['tables'][table]=record
    for kind,name,sql in schema:
        if kind=='index':dst.execute(sql)
    dst.commit()
    report['recovered_integrity_check']=[r[0] for r in dst.execute('pragma integrity_check')]
    report['missing_parent_node_ids']=[r[0] for r in dst.execute('SELECT n.id FROM nodes n LEFT JOIN nodes p ON n.parent=p.id WHERE n.parent IS NOT NULL AND p.id IS NULL')]
    report['depth_inconsistencies']=[r[0] for r in dst.execute('SELECT n.id FROM nodes n JOIN nodes p ON n.parent=p.id WHERE n.depth != p.depth+1')]
    report['attempts_referring_to_missing_children']=[r[0] for r in dst.execute('SELECT a.id FROM attempts a LEFT JOIN nodes n ON a.child=n.id WHERE a.child IS NOT NULL AND n.id IS NULL')]
    report['nomination_attempt_rows']=dst.execute("select count(*) from attempts where status='POTENTIAL_COUNTEREXAMPLE'").fetchone()[0]
    report['unknown_attempt_rows']=dst.execute("select count(*) from attempts where status like 'UNKNOWN_%'").fetchone()[0]
    dst.close();src.close();base.close()
    report['output_sha256']=sha(output)
    (a.destination/'RECOVERY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
