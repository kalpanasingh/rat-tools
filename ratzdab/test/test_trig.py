'''unit tests for ratzdab conversion utilities: trig headers'''

import unittest
import ratzdab
from rat import ROOT


class TestTRIG(unittest.TestCase):
    def test_trig(self):
        '''Test conversion of RAT::DS::TRIGInfo objects to and from ZDAB
        TriggerInfos.

        Exceptions:
            * runID is not set by ratzdab::unpack::trig
        '''
        trig = ROOT.RAT.DS.TRIGInfo()

        trig.trigMask = 0x10101011
        trig.pulserRate = 0x20202022
        trig.MTC_CSR = 0x30303033
        trig.lockoutWidth = 0x40404044
        trig.prescaleFreq = 0x50505055
        trig.eventID = 0x60606066
        trig.runID = 0x70707077

        for i in range(10):
            trig.trigTHold.push_back(11 * i)
            trig.trigZeroOffset.push_back(22 * i)

        zdab_trig = ratzdab.pack.trig(trig)
        trig_converted = ratzdab.unpack.trig(zdab_trig)

        self.assertTrue(trig.trigMask == trig_converted.trigMask)
        self.assertTrue(trig.pulserRate == trig_converted.pulserRate)
        self.assertTrue(trig.MTC_CSR == trig_converted.MTC_CSR)
        self.assertTrue(trig.lockoutWidth == trig_converted.lockoutWidth)
        self.assertTrue(trig.prescaleFreq == trig_converted.prescaleFreq)
        self.assertTrue(trig.eventID == trig_converted.eventID)

        for i in range(10):
            self.assertTrue(trig.trigTHold[i] == trig_converted.trigTHold[i])
            self.assertTrue(trig.trigZeroOffset[i] == trig_converted.trigZeroOffset[i])


if __name__ == '__main__':
    unittest.main()

