#!/usr/bin/env python3
"""Serial, resource-bounded fission search retaining every surviving raw move.

Input: JSON {jobs: [{label, prefix: [PD, band, ..., PD]}], parameters: {...}}.
Each job extends one fixed prefix by one band. A cached ribbon-link match or
same-library certificate replay is a candidate, never a counterexample claim.
Incomplete/error jobs are UNKNOWN, and may be retried in a new attempt file.
Only pairwise linking, exact component signature and square determinant reject.
No isometry deduplication, floating determinant test or symbolic polynomial
calculation is used. Exact duplicate endpoint diagrams are kept as distinct moves.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import time


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, separators=(',', ':')) + '\n')
    temporary.replace(path)


def cheap_screen(link, cache):
    """Return (rejection witness or None, undecidable component count)."""
    from sagefree_slice_filter import linking_nums_all_zero, signature_and_det, _is_square
    if not linking_nums_all_zero(link):
        return {'reason': 'nonzero_linking'}, 0
    unknown = 0
    for i in range(len(link.link_components)):
        try:
            component = link.sublink([i])
            component.simplify('basic')
            if not component.crossings:
                continue
            key = digest(component.PD_code())
            if key not in cache:
                cache[key] = signature_and_det(component)
            signature, determinant = cache[key]
            if signature != 0 or not _is_square(determinant):
                return {'reason': 'component_obstruction', 'component': i,
                        'signature': signature, 'determinant': determinant}, unknown
        except Exception:
            unknown += 1  # Failure cannot reject a potentially slice component.
    return None, unknown


def worker(config_path, index, output):
    import warnings
    warnings.filterwarnings('ignore', message='Plink failed')
    import snappy
    import spherogram
    from spherogram.links.bands import core, search
    import sagefree_slice_filter

    config = json.loads(Path(config_path).read_text())
    job, p = config['jobs'][index], config['parameters']
    random.seed(p['seed'])
    prefix = job['prefix']
    if not prefix or len(prefix) % 2 != 1:
        raise ValueError('Expected alternating PD/band prefix ending in PD')
    parent = snappy.Link(prefix[-1])
    core.normalize_crossing_labels(parent)
    if json.loads(json.dumps(parent.PD_code())) != prefix[-1]:
        raise ValueError('Parent PD failed exact reconstruction')
    record = {
        'status': 'RUNNING_UNKNOWN', 'complete': False, 'label': job['label'],
        'config_sha256': hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        'job_sha256': digest(job), 'parameters': p, 'prefix': prefix,
        'provenance': {str(Path(f).name): hashlib.sha256(Path(f).read_bytes()).hexdigest()
                       for f in (__file__, core.__file__, search.__file__, sagefree_slice_filter.__file__)},
        'versions': {'snappy': snappy.__version__, 'spherogram': spherogram.__version__},
        'counts': Counter(), 'frontier': [], 'hits': [], 'errors': [],
        'certified_counterexample': False,
        'scope': 'One band from this exact prefix in the named generator. Survivors are unknown. '
                 'Prior prefix isotopies, terminal identifications and orientation require separate verification.'}
    save(output, record)
    cache = {}
    started = time.monotonic()
    last_save = started
    exhausted = True
    try:
        if p['paths'] == 'mixed_sample':
            from mixed_stabilization_bands import generate
            stream = generate(parent, p, job, record['counts'])
            record['scope'] += ' Biased random sample; completion means only the attempt budget was consumed.'
        else:
            stream = core.banded_links(parent, max_twists=p['twists'],
                                      max_band_len=p['length'], paths=p['paths'])
        for link, band in stream:
            if time.monotonic() - started >= p['seconds']:
                exhausted = False
                break
            record['counts']['generated'] += 1
            raw_pd = link.PD_code()
            raw_components = len(link.link_components)
            rejection, unknown = cheap_screen(link, cache)
            record['counts']['undecidable_component_calculations'] += unknown
            if rejection:
                record['counts'][rejection['reason']] += 1
            else:
                # Split unknots removed by simplification are explicit caps in
                # this pure-fission movie, not lost link-invariant input.
                link.simplify('global')
                core.normalize_crossing_labels(link)
                capped = link.unlinked_unknot_components
                link.unlinked_unknot_components = 0
                terminal = None
                terminal_error = None
                if not link.link_components:
                    terminal = 'unknot'
                elif p.get('recognize_terminal', True):
                    try:
                        exterior = link.exterior()
                        if search.is_unlink_exterior(exterior):
                            terminal = 'unknot'
                        elif p.get('ribbon_cache', False) and exterior.solution_type(enum=True) in {1, 2}:
                            match = snappy.RibbonLinks.identify(exterior, extends_to_link=True)
                            if match:
                                terminal = match.name()
                    except Exception as e:
                        terminal_error = repr(e)
                row = {'band': band, 'raw_pd': raw_pd,
                       'raw_components': raw_components, 'capped_split_unknots': capped,
                       'endpoint_pd': link.PD_code(),
                       'certificate_prefix': prefix + [band, link.PD_code()],
                       'terminal_identification_error': terminal_error}
                if terminal:
                    certificate = prefix + [band, terminal]
                    try:
                        replay = bool(search.verify_ribbon_to_unknot(snappy.Link(prefix[0]), certificate))
                        replay_error = None
                    except Exception as e:
                        replay, replay_error = False, repr(e)
                    record['hits'].append(dict(row, terminal=terminal, certificate=certificate,
                                               same_library_replay=replay, replay_error=replay_error))
                    record['status'] = 'CANDIDATE_REQUIRES_INDEPENDENT_VERIFICATION'
                    exhausted = False
                    save(output, record)
                    break
                record['frontier'].append(row)
                record['counts']['retained_unknown'] += 1
                save(output, record)
            if time.monotonic() - last_save >= 2:
                record['elapsed_seconds'] = round(time.monotonic() - started, 3)
                save(output, record)
                last_save = time.monotonic()
    except Exception as e:
        exhausted = False
        record['errors'].append(repr(e))
        record['status'] = 'ERROR_UNKNOWN'
    if not record['hits'] and not record['errors']:
        record['status'] = 'COMPLETE_NO_CERTIFICATE' if exhausted else 'TIMEOUT_UNKNOWN'
    record['complete'] = exhausted
    record['elapsed_seconds'] = round(time.monotonic() - started, 3)
    save(output, record)


def stop_process(process):
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
    except ProcessLookupError:
        process.wait()


def run(config_path, directory):
    config_path = Path(config_path).resolve()
    config = json.loads(config_path.read_text())
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    implementation = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in
                      [Path(__file__), Path(__file__).with_name('sagefree_slice_filter.py'),
                       Path(__file__).with_name('mixed_stabilization_bands.py'),
                       Path(__file__).with_name('nonfibered_reverse_audit.py')]}
    from spherogram.links.bands import core, search
    import importlib.metadata
    implementation.update({str(Path(f).name): hashlib.sha256(Path(f).read_bytes()).hexdigest()
                           for f in [core.__file__, search.__file__]})
    implementation['versions'] = {name: importlib.metadata.version(name)
                                  for name in ['snappy', 'spherogram']}
    identity = digest({'config': config, 'implementation': implementation})
    header = directory / 'manifest.json'
    if header.exists() and json.loads(header.read_text())['identity'] != identity:
        raise ValueError('Configuration/code changed: choose a new result directory')
    manifest = {'identity': identity, 'config': config, 'implementation': implementation,
                'scope': 'Serial local workers. Completed means only this bounded generator.', 'jobs': []}
    for index, job in enumerate(config['jobs']):
        previous = sorted(directory.glob(f'job-{index:03d}-attempt-*.json'))
        if any(json.loads(f.read_text()).get('complete') for f in previous):
            manifest['jobs'].append({'index': index, 'status': 'ALREADY_COMPLETE'})
            continue
        output = directory / f'job-{index:03d}-attempt-{len(previous):03d}.json'
        command = [sys.executable, str(Path(__file__).resolve()), str(config_path),
                   str(output.resolve()), '--worker', str(index)]
        started = time.monotonic()
        reason = None
        peak_rss_kib = 0
        with output.with_suffix('.log').open('w') as log:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True, env=dict(os.environ,
                                       OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1'))
            try:
                while process.poll() is None:
                    if time.monotonic() - started > config['parameters']['seconds'] + 8:
                        reason = 'HARD_TIMEOUT_UNKNOWN'
                        stop_process(process)
                        break
                    rss_text = subprocess.run(['ps', '-o', 'rss=', '-p', str(process.pid)],
                                              capture_output=True, text=True).stdout.strip()
                    rss = int(rss_text or 0)
                    peak_rss_kib = max(peak_rss_kib, rss)
                    if rss > config['parameters'].get('rss_limit_mib', 1536) * 1024:
                        reason = 'MEMORY_LIMIT_UNKNOWN'
                        stop_process(process)
                        break
                    time.sleep(0.5)
            except BaseException:
                stop_process(process)
                raise
        record = json.loads(output.read_text()) if output.exists() else {'complete': False, 'frontier': [], 'hits': []}
        if reason or process.returncode != 0:
            record.update(status=reason or 'WORKER_FAILURE_UNKNOWN', complete=False)
        record.update(exit_code=process.returncode, peak_rss_kib=peak_rss_kib,
                      supervised_seconds=round(time.monotonic() - started, 3))
        save(output, record)
        summary = {'index': index, 'label': job['label'], 'status': record['status'],
                   'frontier': len(record['frontier']), 'hits': len(record['hits']),
                   'seconds': record['supervised_seconds'], 'peak_rss_kib': peak_rss_kib}
        manifest['jobs'].append(summary)
        save(header, manifest)
        print(json.dumps(summary), flush=True)
        if record['hits']:
            break  # Inspect a candidate before spending on any other job.
    save(header, manifest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config')
    parser.add_argument('output')
    parser.add_argument('--worker', type=int)
    args = parser.parse_args()
    if args.worker is None:
        run(args.config, args.output)
    else:
        os.nice(10)
        worker(args.config, args.worker, args.output)
