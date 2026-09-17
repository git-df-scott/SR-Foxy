import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import snappy
from jones_root_jet import Jet,probe
from eisermann_ribbon_link_gate import unlink
import sagefree_jones as SJ


class RootJetTests(unittest.TestCase):
    def test_published_three_parallel_integer_control(self):
        import json
        path=Path(__file__).resolve().parents[1]/'results/astra_2026_09_16_followup/root_jet_final/ribbon61_3parallel.input.json'
        data=json.loads(path.read_text())
        result=probe(snappy.Link(data['pd']),9**3,exact=True)
        self.assertEqual(result['exact_quotient_at_i'],[1785,0])
        self.assertFalse(result['ribbon_divisibility_obstructed_exact'])

    def test_ring_relations_and_inverse(self):
        for order in range(2,6):
            Jet.order=order;q=Jet([0,1])
            self.assertEqual(q*q**-1,1)
            self.assertEqual((q*q+1)**order,0)
            self.assertNotEqual((q*q+1)**(order-1),0)

    def test_full_polynomial_comparison_and_signed_controls(self):
        for name,L,d,obstructed in [('U2',unlink(2),1,False),('U3',unlink(3),1,False),
            ('3_1',snappy.Link('3_1'),-3,False),('4_1',snappy.Link('4_1'),5,False),
            ('6_1',snappy.Link('6_1'),9,False),('L9n18',snappy.Link('L9n18'),1,True)]:
            with self.subTest(name=name):
                r=probe(L,d)
                from spherogram.links import jones
                SJ.install();full=jones.jones_polynomial(L,normalized=False)
                q=Jet([0,1]);exact=Jet(0)
                for e,c in full.d.items():exact=exact+c*q**e
                self.assertEqual(list(exact.d),r['jet_mod_32'])
                self.assertEqual(r['ribbon_obstructed_mod_32'],obstructed)


if __name__=='__main__':unittest.main()
