#!/usr/bin/env python3
"""Bounded search for a recognizable closed triangulation of Sigma_2(K).

Recognition may expose a Seifert/plumbing route to correction terms. Failure
to recognize is UNKNOWN, and does not establish hyperbolicity or absence of
a definite filling. No correction term or sliceness claim is computed here.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time


def worker(knot_file, seed, output):
    import snappy
    import regina
    from branched_double_cover_gate import sigma_2
    random.seed(seed)
    card = json.loads(Path(knot_file).read_text())
    pd = card.get('pd_code_snappy_0indexed') or card['pd_code']
    cover = sigma_2(pd)
    if seed:
        cover.randomize()
    filled = cover.filled_triangulation()
    signature = filled.triangulation_isosig(decorated=False)
    triangulation = regina.Triangulation3.fromIsoSig(signature)
    assert triangulation.isValid() and triangulation.isClosed() and triangulation.isOrientable()
    homology = triangulation.homology()
    # This feasibility probe is scoped to the determinant-13 Abe--Tagami inputs.
    assert str(cover.homology()) == 'Z/13'
    assert homology.rank() == 0 and homology.countInvariantFactors() == 1
    assert int(str(homology.invariantFactor(0))) == 13
    triangulation.intelligentSimplify()
    recognition = regina.StandardTriangulation.recognise(triangulation)
    data = {'input_sha256': hashlib.sha256(Path(knot_file).read_bytes()).hexdigest(),
            'seed': seed, 'cover_homology': str(cover.homology()),
            'filled_isosig': signature, 'simplified_isosig': triangulation.isoSig(),
            'tetrahedra': triangulation.size(),
            'recognized_triangulation': str(recognition) if recognition else None,
            'recognized_manifold': str(recognition.manifold()) if recognition else None,
            'status': 'RECOGNIZED' if recognition else 'UNRECOGNIZED_UNKNOWN'}
    Path(output).write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)


def main(args):
    if args.worker:
        return worker(args.knot, args.seed, args.output)
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(output)
    start = time.monotonic()
    with output.with_suffix('.log').open('w') as log:
        try:
            result = subprocess.run([sys.executable, __file__, args.knot, args.output,
                                     '--seed', str(args.seed), '--worker'],
                                    stdout=log, stderr=subprocess.STDOUT, timeout=args.seconds)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = None
    data = json.loads(output.read_text()) if output.exists() else {}
    if code != 0:
        data['status'] = 'TIMEOUT_UNKNOWN' if code is None else 'ERROR_UNKNOWN'
    data.update(elapsed_seconds=round(time.monotonic()-start, 3), exit_code=code,
                scope=__doc__.strip())
    output.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps(data), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('knot')
    parser.add_argument('output')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--seconds', type=int, default=25)
    parser.add_argument('--worker', action='store_true')
    main(parser.parse_args())
