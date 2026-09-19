#!/usr/bin/env python3
"""Read-only integrity verification for the complete SR-Foxy handoff."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile


def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def git_hash(kind: str, data: bytes) -> str:
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def tree_hash(entries: list[dict]) -> str:
    root: dict = {}
    for entry in entries:
        parts=entry['path'].split('/')
        node=root
        for part in parts[:-1]:
            node=node.setdefault(part,{})
        node[parts[-1]]=(entry['mode'],entry['git_blob_sha1'])
    def visit(node: dict) -> str:
        records=[]
        for name,value in node.items():
            if isinstance(value,dict):
                mode,sha,key='40000',visit(value),name.encode()+b'/'
            else:
                mode,sha=value; key=name.encode()
            records.append((key,mode.encode()+b' '+name.encode()+b'\0'+bytes.fromhex(sha)))
        return git_hash('tree',b''.join(record for _,record in sorted(records)))
    return visit(root)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--archives',action='store_true',help='Also CRC-test every included ZIP archive.')
    args=parser.parse_args()
    root=args.root.resolve(); errors=[]
    try:
        package=json.loads((root/'PACKAGE_MANIFEST.json').read_text())
        expected=package['files']
        for row in expected:
            rel=Path(row['path'])
            if rel.is_absolute() or '..' in rel.parts:
                errors.append('Unsafe manifest path: '+str(rel)); continue
            p=root/rel
            if not p.is_file():
                errors.append('Missing file: '+str(rel)); continue
            if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:
                errors.append('Modified file: '+str(rel))
        source=json.loads((root/'source_export/SOURCE_MANIFEST.json').read_text())
        source_root=root/'SR-Foxy'
        actual={p.relative_to(source_root).as_posix() for p in source_root.rglob('*') if p.is_file()}
        wanted={row['path'] for row in source['files']}
        if actual!=wanted:
            errors.append('Source file set differs; missing='+str(sorted(wanted-actual))+'; extra='+str(sorted(actual-wanted)))
        for row in source['files']:
            p=source_root/row['path']
            if p.is_file() and git_hash('blob',p.read_bytes())!=row['git_blob_sha1']:
                errors.append('Git blob hash differs: '+row['path'])
        computed_tree=tree_hash(source['files'])
        if computed_tree!=source['source_tree']:
            errors.append('Source tree manifest differs from its recorded Git tree')
        checked_archives=0
        if args.archives:
            for p in root.rglob('*.zip'):
                with zipfile.ZipFile(p) as z:
                    bad=z.testzip()
                    if bad: errors.append('Bad ZIP member: '+str(p.relative_to(root))+': '+bad)
                checked_archives+=1
        result={'status':'PASS' if not errors else 'FAIL','manifest_files':len(expected),
                'source_files':len(wanted),'source_commit':source['source_commit'],
                'source_tree':computed_tree,'zip_archives_crc_checked':checked_archives,
                'errors':errors,
                'scope':'File integrity only. Does not certify every mathematical claim or resume any search.'}
        print(json.dumps(result,indent=2))
        return 0 if not errors else 1
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        print(json.dumps({'status':'ERROR','error':str(exc)},indent=2),file=sys.stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
