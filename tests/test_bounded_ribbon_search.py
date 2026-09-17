"""Failure-path regressions: losing a candidate or inventing coverage is fatal."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import snappy
from spherogram.links.bands import core, search
import bounded_ribbon_search as bounded
import sagefree_slice_filter as filters
from hfk_worker import validate_hfk


class CheckpointTests(unittest.TestCase):
    def test_hfk_rejects_observed_invalid_library_output(self):
        record = json.loads((ROOT / 'results/astra_2026_09_16/three_factor_continuation_hfk_diagnostic.json').read_text())
        failed = next(c['HFK'] for c in record['components'].values() if c['status'] == 'UNKNOWN')
        failed = dict(failed, ranks={(a, m): n for a, m, n in failed['ranks']})
        with self.assertRaisesRegex(ValueError, 'normalized at 1'):
            validate_hfk(failed)

    def test_hfk_consistency_accepts_ribbon_control(self):
        import knot_floer_homology
        h = knot_floer_homology.pd_to_hfk(snappy.Link('6_1').PD_code())
        self.assertIs(validate_hfk(h), h)

    def old_runner(self, output, source):
        with patch.object(sys, 'argv', [str(ROOT / 'scripts/teichner_frontier_resumable.py'),
                                       str(output), str(source), '6_1', '1', '2']), contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(ROOT / 'scripts/teichner_frontier_resumable.py'), run_name='__main__')

    def test_failure_is_unknown_and_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'in.json', Path(directory) / 'out.json'
            source.write_text(json.dumps({'name': 'control', 'pd_code': snappy.Link('6_1').PD_code()}))
            with patch.object(search, 'ribbon_concordant_links', side_effect=RuntimeError('injected')) as engine:
                self.old_runner(output, source)
                self.old_runner(output, source)
                self.assertEqual(engine.call_count, 2)
            record = json.loads(output.read_text())
            self.assertEqual(record['completed'], {})
            self.assertFalse(record['coverage']['6_1']['complete'])
            self.assertEqual(record['coverage']['6_1']['zero_survivor_diagrams'], [])
            self.assertEqual(len(next(iter(record['failures'].values()))), 2)

    def test_success_saves_paths_and_changed_input_refuses_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'in.json', Path(directory) / 'out.json'
            pd = snappy.Link('6_1').PD_code()
            source.write_text(json.dumps({'name': 'control', 'pd_code': pd}))
            certificate = [pd, 'test_band', pd]
            with patch.object(search, 'ribbon_concordant_links', return_value={'link': certificate}) as engine:
                self.old_runner(output, source)
                self.old_runner(output, source)
                self.assertEqual(engine.call_count, 1)
            record = json.loads(output.read_text())
            self.assertEqual(next(iter(record['completed'].values()))['frontier_certificates'],
                             json.loads(json.dumps([certificate])))
            source.write_text(json.dumps({'name': 'control', 'pd_code': snappy.Link('8_8').PD_code()}))
            with self.assertRaises(SystemExit):
                self.old_runner(output, source)

    def test_false_certificate_replay_is_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'in.json', Path(directory) / 'out.json'
            source.write_text(json.dumps({'name': 'control', 'pd_code': snappy.Link('6_1').PD_code()}))
            with patch.object(search, 'ribbon_concordant_links', return_value={'unknot': ['invalid']}), \
                 patch('spherogram.links.bands.search.verify_ribbon_to_unknot', return_value=False):
                self.old_runner(output, source)
            record = json.loads(output.read_text())
            self.assertFalse(record['completed'])
            self.assertFalse(record['hits'])

    def test_large_square_exact(self):
        root = 2**150 + 12345
        self.assertTrue(filters._is_square(root * root))
        self.assertFalse(filters._is_square(root * root + 1))

    def test_component_screen_actually_rejects_nonslice_control(self):
        rejection, unknown = bounded.cheap_screen(snappy.Link('3_1'), {})
        self.assertEqual(unknown, 0)
        self.assertEqual(rejection['reason'], 'component_obstruction')
        self.assertEqual(abs(rejection['signature']), 2)
        self.assertEqual(abs(rejection['determinant']), 3)

    def test_list_and_sage_matrix_interfaces_agree(self):
        knot = snappy.Link('6_3')
        rows = filters._seifert_rows(knot)
        expected = filters.signature_and_det(knot)
        with patch.object(knot, 'seifert_matrix', return_value=rows):
            self.assertEqual(filters.signature_and_det(knot), expected)

    def test_streaming_error_not_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'in.json', Path(directory) / 'out.json'
            source.write_text(json.dumps({'jobs': [{'label': 'control', 'prefix': [snappy.Link('6_1').PD_code()]}],
                                         'parameters': {'seed': 1, 'seconds': 5, 'twists': 2, 'length': 2, 'paths': 'shortest'}}))
            with patch.object(core, 'banded_links', side_effect=RuntimeError('injected')):
                bounded.worker(source, 0, output)
            record = json.loads(output.read_text())
            self.assertEqual(record['status'], 'ERROR_UNKNOWN')
            self.assertFalse(record['complete'])

    def test_failed_component_calculation_keeps_candidate(self):
        with patch.object(filters, 'signature_and_det', side_effect=RuntimeError('injected')):
            rejection, unknown = bounded.cheap_screen(snappy.Link('6_1'), {})
        self.assertIsNone(rejection)
        self.assertEqual(unknown, 1)


if __name__ == '__main__':
    unittest.main()
