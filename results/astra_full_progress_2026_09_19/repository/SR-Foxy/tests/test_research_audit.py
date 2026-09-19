"""Negative controls for the new algebra, filter, and certification gate."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verify_hp_norms import Z, ONE, ZERO, add, mul, neg, multiplicity, parse
from filter_common_successors import dominates
import teichner_certify


class ResearchAuditTests(unittest.TestCase):
    def test_cyclotomic_relation(self):
        self.assertEqual(add(add(mul(Z,Z),Z),ONE),ZERO)

    def test_norm_positive_control(self):
        # (t-z)^2 is a norm up to an allowed nonzero unit. Its multiplicity
        # must be even, so it must not be flagged by the odd-root witness.
        coefficients=[mul(Z,Z),neg(add(Z,Z)),ONE]
        self.assertEqual(multiplicity(coefficients,Z),2)
        self.assertEqual(multiplicity(coefficients,neg(Z)),0)

    def test_nonnorm_negative_control(self):
        self.assertEqual(multiplicity([neg(Z),ONE],Z),1)

    def test_coefficient_parser_rejects_code(self):
        with self.assertRaises(ValueError): parse("__import__('os')")

    def test_rank_total_is_not_enough(self):
        self.assertFalse(dominates({(0,0):100},{(1,0):1}))
        self.assertTrue(dominates({(0,0):2,(1,0):1},{(0,0):1,(1,0):1}))

    def test_failed_replay_cannot_certify(self):
        with patch.object(teichner_certify,'verify_ribbon_to_unknot',return_value=False):
            self.assertFalse(teichner_certify.certificate_status(object(),{'unknot':'invalid'}))

    def test_missing_endpoint_cannot_certify(self):
        with patch.object(teichner_certify,'verify_ribbon_to_unknot') as checker:
            self.assertFalse(teichner_certify.certificate_status(object(),{}))
            checker.assert_not_called()


if __name__=='__main__': unittest.main()
