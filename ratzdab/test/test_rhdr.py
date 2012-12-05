'''unit tests for ratzdab conversion utilities: rhdr headers'''

import unittest
import ratzdab
from rat import ROOT


class TestRHDR(unittest.TestCase):
    '''Test conversion of RAT::DS::Run objects to and from ZDAB RunRecords.

    Exceptions:
        * subrun ID does not exist in RunRecord struct
    '''
    def test_rhdr(self):
        rhdr = ROOT.RAT.DS.Run()

        rhdr.runID = 0xf0101011
        rhdr.subRunID = 0xf0202022
        rhdr.date = 0xf0303033
        rhdr.time = 0xf0404044
        rhdr.calibTrialID = 0xf0505055
        rhdr.firstEventID = 0xf0606066
        rhdr.validEventID = 0xf0707077
        rhdr.srcMask = 0xf0808088
        rhdr.crateMask = 0xf0909099
        rhdr.runType = 0xf0a0a0aa
        rhdr.DAQVer = 0xf

        zdab_rhdr = ratzdab.pack.rhdr(rhdr)
        rhdr_converted = ratzdab.unpack.rhdr(zdab_rhdr)

        self.assertTrue(rhdr.runID == rhdr_converted.runID)
        self.assertTrue(rhdr.date == rhdr_converted.date)
        self.assertTrue(rhdr.time == rhdr_converted.time)
        self.assertTrue(rhdr.calibTrialID == rhdr_converted.calibTrialID)
        self.assertTrue(rhdr.firstEventID == rhdr_converted.firstEventID)
        self.assertTrue(rhdr.validEventID == rhdr_converted.validEventID)
        self.assertTrue(rhdr.srcMask == rhdr_converted.srcMask)
        self.assertTrue(rhdr.crateMask == rhdr_converted.crateMask)
        self.assertTrue(rhdr.runType == rhdr_converted.runType)
        self.assertTrue(rhdr.DAQVer == rhdr_converted.DAQVer)


if __name__ == '__main__':
    unittest.main()

