#!/usr/bin/env python3
"""Verify the preserved source snapshot; this does not validate mathematics.

Run from anywhere: python3 VERIFY_BACKUP.py
No external dependencies, network calls, repository writes, or branch operations.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path


def git_hash(kind: bytes, data: bytes) -> bytes:
    return hashlib.sha1(kind + b" " + str(len(data)).encode() + b"\0" + data).digest()


def git_tree(entries: dict[str, dict]) -> str:
    root: dict = {}
    for name, record in entries.items():
        parts = name.split("/")
        cursor = root
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = (record["git_mode"], record["git_blob_sha1"])

    def encode(node: dict) -> bytes:
        items = []
        for name, value in node.items():
            key = name.encode("utf-8")
            if isinstance(value, dict):
                items.append((key + b"/", b"40000 " + key + b"\0" + encode(value)))
            else:
                mode, digest = value
                items.append((key, mode.encode() + b" " + key + b"\0" + bytes.fromhex(digest)))
        return git_hash(b"tree", b"".join(value for _, value in sorted(items)))

    return encode(root).hex()


def main() -> int:
    here = Path(__file__).resolve().parent
    try:
        manifest = json.loads((here / "SOURCE_MANIFEST.json").read_text(encoding="utf-8"))
        source = here / "SR-Foxy"
        expected = {row["path"]: row for row in manifest["files"]}
        found = {p.relative_to(source).as_posix(): p for p in source.rglob("*") if p.is_file()}
        errors = []
        missing = sorted(set(expected) - set(found))
        extra = sorted(set(found) - set(expected))
        if missing:
            errors.append({"missing": missing})
        if extra:
            errors.append({"extra": extra})
        for name in sorted(set(expected) & set(found)):
            path, row = found[name], expected[name]
            if path.is_symlink():
                errors.append({"symlink_not_expected": name})
                continue
            data = path.read_bytes()
            if (len(data) != row["bytes"] or
                    hashlib.sha256(data).hexdigest() != row["sha256"] or
                    git_hash(b"blob", data).hex() != row["git_blob_sha1"]):
                errors.append({"content_mismatch": name})
        computed = git_tree(expected)
        if computed != manifest["git_tree"]:
            errors.append({"manifest_tree_mismatch": computed})
        result = {
            "commit": manifest["commit"],
            "expected_files": len(expected),
            "present_files": len(found),
            "git_tree": computed,
            "all_file_content_verified": not errors,
            "errors": errors,
            "scope": "Historical 53f800f snapshot, not current main; no mathematical or runtime certification.",
            "mode_note": "Git tree is recomputed using recorded Git modes; cross-platform unzip may change filesystem executable bits."
        }
        print(json.dumps(result, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Verification failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
