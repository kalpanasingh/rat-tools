'''unit tests for ratzdab conversion utilities: caac headers'''

import unittest
import ratzdab
from rat import ROOT


class TestCAAC(unittest.TestCase):
    '''Test conversion of RAT::DS::AVStat objects to and from ZDAB AVStatuses.
    '''
    def test_caac(self):
        caac = ROOT.RAT.DS.AVStat()

        for i in range(3):
            caac.position[i] = 111.1 * i
            caac.roll[i] = 222.2 * i

        for i in range(7):
            caac.ropeLength[i] = 333.3 * i

        zdab_caac = ratzdab.pack.caac(caac)
        caac_converted = ratzdab.unpack.caac(zdab_caac)

        for i in range(3):
            self.assertTrue(caac.position[i] == caac_converted.position[i])
            self.assertTrue(caac.roll[i] == caac_converted.roll[i])

        for i in range(7):
            self.assertTrue(caac.ropeLength[i] == caac_converted.ropeLength[i])


if __name__ == '__main__':
    unittest.main()

