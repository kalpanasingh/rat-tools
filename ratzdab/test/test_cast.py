'''unit tests for ratzdab conversion utilities: cast headers'''

import unittest
import numpy as np
import ratzdab
from rat import ROOT


class TestCAST(unittest.TestCase):
    '''Test conversion of RAT::DS::ManipStat objects to and from ZDAB
    ManipStatuses.
    '''
    def test_cast(self):
        cast = ROOT.RAT.DS.ManipStat()

        cast.srcID = 0xf011
        cast.srcStatus = 0xf022
        cast.nRopes = 6

        cast.manipPos = np.array([1234.56, 7890.12, 3456.78], dtype=np.float32)
        cast.manipDest = np.array([9012.34, 5678.90, 1234.57], dtype=np.float32)
        cast.srcPosUnc1 = 42.42
        cast.srcPosUnc2 = np.array([8901.23, 4567.89, 123.456], dtype=np.float32)
        cast.laserballOrient = 9876.54

        # kMaxManipulatorRopes = 6
        for i in range(6):
            cast.ropeID.push_back(i)
            cast.ropeLength.push_back(111.1*i)
            cast.ropeTargLength.push_back(222.2*i)
            cast.ropeVelocity.push_back(333.3*i)
            cast.ropeTension.push_back(444.4*i)
            cast.ropeErr.push_back(555.5*i)

        zdab_cast = ratzdab.pack.cast(cast)
        cast_converted = ratzdab.unpack.cast(zdab_cast)

        self.assertTrue(cast.srcID == cast_converted.srcID)
        self.assertTrue(cast.srcStatus == cast_converted.srcStatus)
        self.assertTrue(cast.nRopes == cast_converted.nRopes)
        self.assertTrue(cast.srcPosUnc1 == cast_converted.srcPosUnc1)
        self.assertTrue(cast.laserballOrient == cast_converted.laserballOrient)

        for i in range(3):
            self.assertTrue(cast.manipPos[i] == cast_converted.manipPos[i])
            self.assertTrue(cast.manipDest[i] == cast_converted.manipDest[i])
            self.assertTrue(cast.srcPosUnc2[i] == cast_converted.srcPosUnc2[i])

        for i in range(6):
            self.assertTrue(cast.ropeID[i] == cast_converted.ropeID[i])
            self.assertTrue(cast.ropeLength[i] == cast_converted.ropeLength[i])
            self.assertTrue(cast.ropeTargLength[i] == cast_converted.ropeTargLength[i])
            self.assertTrue(cast.ropeVelocity[i] == cast_converted.ropeVelocity[i])
            self.assertTrue(cast.ropeTension[i] == cast_converted.ropeTension[i])
            self.assertTrue(cast.ropeErr[i] == cast_converted.ropeErr[i])


if __name__ == '__main__':
    unittest.main()

