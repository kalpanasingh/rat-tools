'''unit tests for ratzdab conversion utilities: eped headers'''

import unittest
import ratzdab
from rat import ROOT


class TestEPED(unittest.TestCase):
    '''Test conversion of RAT::DS::EPEDInfo objects to and from ZDAB
    EpedRecords.

    Exceptions:
        * runID is not set by ratzdab::unpack::eped
    '''
    def test_eped(self):
        eped = ROOT.RAT.DS.EPEDInfo()

        eped.GTDelayCoarse = 0xf0101011
        eped.GTDelayFine = 0xf0202022
        eped.QPedAmp = 0xf0303033
        eped.QPedWidth = 0xf0404044
        eped.patternID = 0xf0505055
        eped.calType = 0xf0606066
        eped.eventID = 0xf0707077
        eped.runID = 0xf0808088

        zdab_eped = ratzdab.pack.eped(eped)
        eped_converted = ratzdab.unpack.eped(zdab_eped)

        self.assertTrue(eped.GTDelayCoarse == eped_converted.GTDelayCoarse)
        self.assertTrue(eped.GTDelayFine == eped_converted.GTDelayFine)
        self.assertTrue(eped.QPedAmp == eped_converted.QPedAmp)
        self.assertTrue(eped.QPedWidth == eped_converted.QPedWidth)
        self.assertTrue(eped.patternID == eped_converted.patternID)
        self.assertTrue(eped.calType == eped_converted.calType)
        self.assertTrue(eped.eventID == eped_converted.eventID)


if __name__ == '__main__':
    unittest.main()

