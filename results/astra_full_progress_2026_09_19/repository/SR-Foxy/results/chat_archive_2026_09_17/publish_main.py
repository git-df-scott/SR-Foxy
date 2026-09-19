#!/usr/bin/env python3
"""Publish the recovered archive to existing main, with non-force remote verification.

Default mode is read-only preflight. --push authorizes fetch/fast-forward,
copying new archive paths, committing and a non-force push to main only.
Uses existing Git authentication; never accepts or saves a token.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.parse

ARCHIVE_REL = 'results/chat_archive_2026_09_17'
REMOTE_REPO = 'git-df-scott/SR-Foxy'
BASE = '5448376b6ef3b2d5551836bd1479200588cd24be'
SECRET = re.compile(rb'(?:github_pat_[A-Za-z0-9_]{35,}|gh[pousr]_[A-Za-z0-9]{30,})')

def cleaned(data: bytes) -> str:
    return SECRET.sub(b'[REDACTED]', data).decode('utf-8', 'replace')

def git(repo: Path, *args: str, timeout: int = 120) -> bytes:
    env = dict(os.environ)
    env['GIT_TERMINAL_PROMPT'] = '0'
    proc = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(repo), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=timeout, env=env, check=False)
    if proc.returncode:
        raise RuntimeError('Git operation failed: ' + args[0] + '\n' + cleaned(proc.stderr))
    return proc.stdout

def is_ancestor(repo: Path, before: str, after: str) -> bool:
    proc = subprocess.run(['git', '-C', str(repo), 'merge-base', '--is-ancestor', before, after],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
    if proc.returncode not in (0, 1):
        raise RuntimeError('Cannot check Git ancestry')
    return proc.returncode == 0

def check_remote(value: str) -> None:
    if value.startswith('git@github.com:'):
        path = value[len('git@github.com:'):]
    else:
        u = urllib.parse.urlsplit(value)
        if u.hostname != 'github.com' or u.scheme not in ('https', 'ssh'):
            raise RuntimeError('Origin is not the intended GitHub repository')
        if u.password or (u.scheme == 'https' and u.username) or (u.scheme == 'ssh' and u.username not in (None, 'git')):
            raise RuntimeError('Remove embedded credentials from origin before publishing')
        if u.query or u.fragment:
            raise RuntimeError('Unexpected origin URL parameters')
        path = u.path.lstrip('/')
    if path.endswith('.git'):
        path = path[:-4]
    if path.lower() != REMOTE_REPO.lower():
        raise RuntimeError('Wrong origin repository')

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('repository', type=Path)
    ap.add_argument('--push', action='store_true')
    ap.add_argument('--payload', type=Path,
                    help='Optional repository_payload directory; default is alongside this script.')
    args = ap.parse_args()
    home = Path(__file__).resolve().parent
    payload = (args.payload or home / 'repository_payload').resolve()
    src = payload / ARCHIVE_REL
    if not src.is_dir():
        raise RuntimeError('repository_payload is missing; use the outer extracted bundle or --payload')
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('sr_archive_verifier', src / 'verify_archive.py')
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    verified = module.verify(src)
    repo = args.repository.resolve()
    top = Path(git(repo, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
    if top != repo:
        raise RuntimeError('Pass the root of an existing repository')
    if git(repo, 'branch', '--show-current').decode().strip() != 'main':
        raise RuntimeError('Refusing to create or switch branches: existing main is required')
    check_remote(git(repo, 'remote', 'get-url', 'origin').decode().strip())
    check_remote(git(repo, 'remote', 'get-url', '--push', 'origin').decode().strip())
    if git(repo, 'status', '--porcelain').strip():
        raise RuntimeError('Working tree/index is not clean; preserve other work and stop')
    print(json.dumps({'preflight': 'PASS', 'branch': 'main', 'archive': verified,
                      'mode': 'PUBLISH' if args.push else 'READ_ONLY'}, indent=2), flush=True)
    if not args.push:
        return
    # Always work from the actual remote main; never rewrite another worker.
    git(repo, 'fetch', '--no-tags', 'origin', 'main')
    remote_before = git(repo, 'rev-parse', 'FETCH_HEAD').decode().strip()
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    if not is_ancestor(repo, BASE, remote_before):
        raise RuntimeError('Remote main no longer contains the verified archival merge; stop')
    if head != remote_before:
        if not is_ancestor(repo, head, remote_before):
            raise RuntimeError('Local main has unpushed or divergent commits; do not mix work')
        git(repo, 'merge', '--ff-only', remote_before)
    if git(repo, 'status', '--porcelain').strip():
        raise RuntimeError('Working tree changed during preflight; stop')
    files = sorted(p for p in src.rglob('*') if p.is_file())
    dst_root = repo / ARCHIVE_REL
    # Compare every collision before copying even one file.
    for p in files:
        dst = dst_root / p.relative_to(src)
        for parent in [dst, *dst.parents]:
            if parent == repo:
                break
            if parent.is_symlink():
                raise RuntimeError('Refusing an archive path containing a symlink')
        if dst.exists() and (not dst.is_file() or dst.read_bytes() != p.read_bytes()):
            raise RuntimeError('Existing archive file differs; nothing overwritten: ' + str(p.relative_to(src)))
    for p in files:
        dst = dst_root / p.relative_to(src)
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dst)
    git(repo, 'add', '-f', '--', ARCHIVE_REL)
    if git(repo, 'diff', '--cached', '--name-only').strip():
        git(repo, '-c', 'user.name=SR-Foxy Archive', '-c', 'user.email=archive@users.noreply.github.com',
            'commit', '-m', 'Archive all recovered chat attachments, expanded evidence, corrections and Codex handoff')
    commit = git(repo, 'rev-parse', 'HEAD').decode().strip()
    if commit != remote_before:
        git(repo, 'push', 'origin', 'HEAD:refs/heads/main')
    git(repo, 'fetch', '--no-tags', 'origin', 'main')
    remote_after = git(repo, 'rev-parse', 'FETCH_HEAD').decode().strip()
    if not is_ancestor(repo, commit, remote_after):
        raise RuntimeError('Remote main does not contain the publication commit')
    for p in files:
        rel = ARCHIVE_REL + '/' + p.relative_to(src).as_posix()
        remote_data = git(repo, 'show', remote_after + ':' + rel, timeout=30)
        if remote_data != p.read_bytes():
            raise RuntimeError('Remote bytes differ: ' + rel)
    report = {'status': 'PUSHED_AND_REMOTE_BYTES_VERIFIED', 'repository': REMOTE_REPO,
              'branch': 'main', 'publication_commit': commit, 'verified_remote_main': remote_after,
              'files_verified': len(files), 'recovered_attachment_count': 24,
              'expanded_zip_member_count': 207, 'archive_path': ARCHIVE_REL,
              'scope': 'Recovered manifest, not a verbatim chat export or inaccessible past files.'}
    report_path = home / ('PUBLICATION_' + commit[:12] + '.json')
    if report_path.exists():
        old = json.loads(report_path.read_text())
        if old != report:
            raise RuntimeError('Existing external publication report differs; report printed below: ' + json.dumps(report))
    else:
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    print('Publication report: ' + str(report_path))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('STOPPED — ' + cleaned(str(exc).encode()), file=sys.stderr)
        print('No automatic reset, branch creation, stash, rebase or force-push was performed.', file=sys.stderr)
        raise SystemExit(1)
