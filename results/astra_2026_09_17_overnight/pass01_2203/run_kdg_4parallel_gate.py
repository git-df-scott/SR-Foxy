#!/usr/bin/env python3
"""Prepare and run a bounded KDG 4-parallel Eisermann root-jet gate.

This script must be run from the SR-Foxy repository root in an environment
with the pinned SnapPy/Spherogram stack. It creates a fresh result directory
and never overwrites an existing file. A modular hit is only a nomination;
exact divisibility requires --exact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import snappy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cable import cable_braid  # noqa: E402


def rss_kib(pid: int) -> int:
    try:
        out = subprocess.run(
            ["ps", "-o", "rss=", "-p", str(pid)],
            capture_output=True, text=True, check=False
        ).stdout.strip()
        return int(out or 0)
    except Exception:
        return 0


def make_parallel(knot, p: int):
    bw = list(knot.braid_word())
    n = max(abs(x) for x in bw) + 1
    w = sum(1 if x > 0 else -1 for x in bw)
    cw, ns = cable_braid(bw, n, p, 0, w)
    link = snappy.Link(braid_closure=cw)
    raw = len(link.crossings)
    link.simplify("basic")
    linking = [[int(x) for x in row] for row in link.linking_matrix()]
    assert len(link.link_components) == p
    assert link.is_planar()
    assert all(x == 0 for row in linking for x in row)
    return link, {
        "source_braid_strands": n,
        "source_braid_length": len(bw),
        "source_braid_writhe": w,
        "cabled_braid_strands": ns,
        "raw_cabled_crossings": raw,
        "simplified_crossings": len(link.crossings),
        "linking_matrix": linking,
    }


def run_probe(out: Path, name: str, link, expected_product: int,
              exact: bool, timeout: int, rss_limit_mib: int):
    payload = {
        "pd": link.PD_code(),
        "expected_product": expected_product,
        "exact": exact,
    }
    inp = out / f"{name}.input.json"
    inp.write_text(json.dumps(payload) + "\n")
    stdout_path = out / f"{name}.output.json"
    stderr_path = out / f"{name}.stderr.log"
    row = {
        "name": name,
        "exact": exact,
        "components": len(link.link_components),
        "crossings": len(link.crossings),
        "timeout_seconds": timeout,
        "rss_limit_mib": rss_limit_mib,
        "status": "UNKNOWN",
    }
    start = time.monotonic()
    reason = None
    with inp.open() as stdin, stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
        proc = subprocess.Popen(
            [sys.executable, str(ROOT / "scripts/jones_root_jet.py")],
            stdin=stdin, stdout=stdout, stderr=stderr, cwd=ROOT
        )
        peak = 0
        while proc.poll() is None:
            rss = rss_kib(proc.pid)
            peak = max(peak, rss)
            if time.monotonic() - start > timeout:
                reason = "TIMEOUT_UNKNOWN"
                proc.kill()
                proc.wait()
                break
            if rss > rss_limit_mib * 1024:
                reason = "MEMORY_LIMIT_UNKNOWN"
                proc.kill()
                proc.wait()
                break
            time.sleep(0.5)
    row["seconds"] = round(time.monotonic() - start, 3)
    row["peak_rss_kib_observed"] = peak
    row["exit_code"] = proc.returncode
    if reason:
        row["status"] = reason
    elif proc.returncode:
        row["status"] = "ERROR_UNKNOWN"
    else:
        result = json.loads(stdout_path.read_text())
        row["result"] = result
        row["status"] = "COMPUTED"
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--exact", action="store_true",
                    help="use exact integer jet arithmetic; required for a mathematical target verdict")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--rss-mib", type=int, default=3072)
    args = ap.parse_args()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)

    card = ROOT / "data/knots/18nh00000601.json"
    data = json.loads(card.read_text())
    K = snappy.Link(data["pd_code_snappy_0indexed"])
    S = snappy.Link("6_1")

    manifest = {
        "status": "RUNNING",
        "counterexample": False,
        "scope": "Eisermann necessary conditions on the zero-framed four-parallel only.",
        "exact_mode": args.exact,
        "input_card": str(card.relative_to(ROOT)),
        "input_card_sha256": hashlib.sha256(card.read_bytes()).hexdigest(),
        "jones_root_jet_sha256": hashlib.sha256(
            (ROOT / "scripts/jones_root_jet.py").read_bytes()
        ).hexdigest(),
        "cable_script_sha256": hashlib.sha256(
            (ROOT / "scripts/cable.py").read_bytes()
        ).hexdigest(),
        "runs": [],
        "qualification": (
            "A modular nonzero lower remainder is a real obstruction nomination. "
            "A modular zero does not certify exact divisibility. Exact mode is required "
            "before declaring a target hit or pass on Jones nullity."
        ),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    for name, knot, det in [
        ("ribbon61_4parallel", S, 9),
        ("KDG_4parallel", K, 25),
    ]:
        link, build = make_parallel(knot, 4)
        (out / f"{name}.pd.json").write_text(
            json.dumps({"pd": link.PD_code(), "build": build}, indent=2) + "\n"
        )
        row = {"name": name, "build": build}
        probe = run_probe(
            out, name, link, det ** 4, args.exact, args.timeout, args.rss_mib
        )
        row["probe"] = probe
        manifest["runs"].append(row)
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(json.dumps(row), flush=True)

        if name == "ribbon61_4parallel":
            if probe["status"] != "COMPUTED":
                manifest["status"] = "BLOCKED_BY_CONTROL_UNKNOWN"
                break
            if probe["result"]["ribbon_obstructed_mod_32"]:
                manifest["status"] = "CONTROL_FAILED"
                break

        if name == "KDG_4parallel" and probe["status"] == "COMPUTED":
            r = probe["result"]
            if args.exact:
                exact_div_fail = bool(r.get("ribbon_divisibility_obstructed_exact"))
                mod_fail = bool(r.get("ribbon_obstructed_mod_32"))
                if exact_div_fail or mod_fail:
                    manifest["status"] = "CANDIDATE_OBSTRUCTION_REQUIRES_INDEPENDENT_VERIFICATION"
                    manifest["candidate_counterexample_if_all_dependencies_verify"] = True
                else:
                    manifest["status"] = "COMPUTED_PASS_INCONCLUSIVE"
            elif r["ribbon_obstructed_mod_32"]:
                manifest["status"] = "MODULAR_HIT_REQUIRES_EXACT_RERUN"
            else:
                manifest["status"] = "MODULAR_PASS_EXACT_NULLITY_UNKNOWN"

    if manifest["status"] == "RUNNING":
        manifest["status"] = "INCOMPLETE_UNKNOWN"
    manifest["complete"] = True
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
