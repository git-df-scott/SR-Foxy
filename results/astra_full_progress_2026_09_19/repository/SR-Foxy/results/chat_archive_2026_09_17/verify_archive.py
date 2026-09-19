#!/usr/bin/env python3
"""Check archival bytes and ZIP extraction coverage; does not run research code."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

def safe_path(root: Path, value: str) -> Path:
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '\\' in value:
        raise ValueError('Unsafe manifest path')
    out = root.joinpath(*p.parts)
    if out.is_symlink():
        raise ValueError('Symlink is not an archived regular file')
    return out

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify(root: Path) -> dict:
    root = root.resolve()
    manifest = json.loads((root / 'ARCHIVE_MANIFEST.json').read_text())
    entries = manifest['files']
    expected = {r['path'] for r in entries}
    if len(expected) != len(entries):
        raise ValueError('Duplicate manifest paths')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != expected | {'ARCHIVE_MANIFEST.json'}:
        raise ValueError('Missing or unexpected archive files: ' + repr(sorted(actual ^ (expected | {'ARCHIVE_MANIFEST.json'}))))
    for item in entries:
        data = safe_path(root, item['path']).read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('Hash/size mismatch: ' + item['path'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if blob != item['git_blob_sha1']:
            raise ValueError('Git blob mismatch: ' + item['path'])
    inventory = json.loads((root / 'SOURCE_INVENTORY.json').read_text())
    indexed_members = {}
    for item in inventory['zip_members']:
        key = item['attachment'], item['member']
        if key in indexed_members:
            raise ValueError('Duplicate ZIP inventory key')
        indexed_members[key] = item
    observed = set()
    zip_count = 0
    for source in inventory['sources']:
        path = safe_path(root, source['archive_path'])
        data = path.read_bytes()
        if digest(data) != source['sha256'] or len(data) != source['bytes']:
            raise ValueError('Original attachment was changed: ' + source['attachment'])
        if zipfile.is_zipfile(path):
            zip_count += 1
            with zipfile.ZipFile(path) as z:
                if z.testzip() is not None:
                    raise ValueError('ZIP CRC failure')
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    key = source['attachment'], info.filename
                    if key in observed or key not in indexed_members:
                        raise ValueError('Unindexed or duplicate ZIP member')
                    observed.add(key)
                    item = indexed_members[key]
                    raw = z.read(info)
                    if raw != safe_path(root, item['archive_path']).read_bytes():
                        raise ValueError('ZIP/extracted bytes differ: ' + item['archive_path'])
                    if digest(raw) != item['sha256'] or len(raw) != item['bytes']:
                        raise ValueError('ZIP inventory mismatch')
    if observed != set(indexed_members):
        raise ValueError('Inventory contains unavailable ZIP members')
    if len(inventory['sources']) != 24 or zip_count != 10 or len(observed) != 207:
        raise ValueError('Recovered source counts differ from expected 24 / 10 / 207')
    return {'status': 'VERIFIED_ARCHIVAL_BYTES', 'manifested_files': len(entries),
            'archive_files_including_manifest': len(entries) + 1,
            'original_attachments': 24, 'original_zips': 10,
            'extracted_zip_files': 207,
            'mathematical_verification': 'NOT_PERFORMED',
            'scope': 'All manifested recovered attachments and all their non-directory ZIP entries; not an entire chat export.'}

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive_dir', type=Path, nargs='?', default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    print(json.dumps(verify(args.archive_dir), indent=2))

if __name__ == '__main__':
    main()
