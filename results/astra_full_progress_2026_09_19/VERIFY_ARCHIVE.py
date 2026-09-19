#!/usr/bin/env python3
"""Read-only verification of the extracted preservation package; no research runs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def main() -> int:
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8'))
    errors=[]
    expected=set()
    for item in manifest['files']:
        rel=PurePosixPath(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            errors.append('Unsafe manifest path: '+str(rel)); continue
        name=str(rel); expected.add(name); path=root.joinpath(*rel.parts)
        if path.is_symlink() or not path.is_file():
            errors.append('Missing or nonregular file: '+name); continue
        if path.stat().st_size!=item['bytes'] or digest(path)!=item['sha256']:
            errors.append('Content mismatch: '+name)
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    allowed=set(manifest.get('unhashed_metadata_files',[]))
    extra=sorted(actual-expected-allowed)
    if extra:errors.extend('Unmanifested file: '+s for s in extra)
    print(json.dumps({'status':'FAIL' if errors else 'PASS','files_checked':len(expected),'errors':errors,
       'scope':'File sizes and SHA-256 only. No mathematical validation, network access, search, or writes.'},indent=2))
    return 1 if errors else 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,KeyError) as exc:
        print('Verification could not complete: '+str(exc),file=sys.stderr)
        raise SystemExit(2)
