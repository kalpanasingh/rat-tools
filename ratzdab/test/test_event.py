'''unit tests for ratzdab conversion utilities: event data'''

import unittest
import ratzdab
from rat import ROOT


class TestEvent(unittest.TestCase):
    '''Test conversion of RAT::DS::Root objects to and from ZDAB
    PmtEventRecords.

    Exceptions:
        * PMT channel flags (not converted to ZDAB yet)
        * clockStat10: unimplemented in rat, meaning unclear
        * prevTrigger, nextTrigger: unknowable before processing
        * gTrigTime: can only be set by the trigger
        * uTDays, uTSecs, uTNSecs: calculated from clockStat10, not stored
        * totalQ: set by calibratePMT processor
        * damnID, damnID1, darnID: unknowable here, unimplemented
        * dataSet: unimplemented in rat, meaning unknown
        * dataCleanFlags: doesn't exist in sno structures
    '''
    def test_event(self):
        ds = ROOT.RAT.DS.Root()
        ev = ds.AddNewEV()

        ev.eventID = 0x10101011
        ev.clockCount50 = 0x7f0f1f2f3ff  # 43 bits
        ev.clockCount10 = 0x1f1f2f3f4f5f6f  # 53 bits
        ev.eSumPeak = 0x1ff  # 9 bits
        ev.eSumDiff = 0x1ff  # 9 bits
        ev.eSumInt = 0x1ff  # 9 bits
        ev.trigError = 0x3fff  # 14 bits
        ev.trigType = 0x3f1f2ff  # 26 bits

        dig = ev.GetDigitiser()
        dig.digEventID = 0xf0f0ff
        dig.trigTagTime = 0xf1f1f1ff
        dig.nWords = 110
        dig.bit24 = 1
        dig.dataFormat = 1
        dig.iopins = 0xf2ff
        dig.chanMask = 0b11111111
        ts = [dig.AddNewTrigSum() for i in range(8)]
        for i, trace in enumerate(ts):
            for s in range(110):
                trace.samples.push_back((i+1)*s)

        pmt = ev.AddNewPMTUnCal(1)
        pmt.id = 42
        pmt.CellID = 0
        pmt.ChanFlags = 0x5
        pmt.sQHS = 0xfaf
        pmt.sQHL = 0xfbf
        pmt.sQLX = 0xfcf
        pmt.sPMTt = 0xfdf

        pmtc = ev.AddNewPMTCal(1)
        pmtc.id = 42
        pmtc.CellID = 0
        pmtc.ChanFlags = 0x5
        pmtc.sQHS = 0xf1f
        pmtc.sQHL = 0xf2f
        pmtc.sQLX = 0xf3f
        pmtc.sPMTt = 0xf4f

        zdab_event = ratzdab.pack.event(ds, 0)
        ds_converted = ratzdab.unpack.event(zdab_event)
        ev_converted = ds_converted.GetEV(0)

        self.assertTrue(ev.eventID == ev_converted.eventID)
        self.assertTrue(ev.clockCount50 == ev_converted.clockCount50)
        self.assertTrue(ev.clockCount10 == ev_converted.clockCount10)
        self.assertTrue(ev.nhits == ev_converted.nhits)
        self.assertTrue(ev.eSumPeak == ev_converted.eSumPeak)
        self.assertTrue(ev.eSumDiff == ev_converted.eSumDiff)
        self.assertTrue(ev.eSumInt == ev_converted.eSumInt)
        self.assertTrue(ev.trigError == ev_converted.trigError)
        self.assertTrue(ev.trigType == ev_converted.trigType)
        self.assertTrue(ev.dataCleanFlags == ev_converted.dataCleanFlags)

        dig_converted = ev_converted.GetDigitiser()
        self.assertTrue(dig.digEventID == dig_converted.digEventID)
        self.assertTrue(dig.trigTagTime == dig_converted.trigTagTime)
        self.assertTrue(dig.nWords == dig_converted.nWords)
        self.assertTrue(dig.bit24 == dig_converted.bit24)
        self.assertTrue(dig.dataFormat == dig_converted.dataFormat)
        self.assertTrue(dig.iopins == dig_converted.iopins)
        self.assertTrue(dig.chanMask == dig_converted.chanMask)
        self.assertTrue(dig.GetTrigSumCount() == dig_converted.GetTrigSumCount())
        for i in range(dig.GetTrigSumCount()):
            for j in range(110):
                self.assertTrue(dig.trigSum[i].samples[j] == dig_converted.trigSum[i].samples[j])

        pmt_converted = ev_converted.GetPMTUnCal(0)
        self.assertTrue(pmt.id == pmt_converted.id)
        self.assertTrue(pmt.CellID == pmt_converted.CellID)
        #self.assertTrue(pmt.ChanFlags == pmt_converted.ChanFlags)  # FIXME
        self.assertTrue(pmt.sQHS == pmt_converted.sQHS)
        self.assertTrue(pmt.sQHL == pmt_converted.sQHL)
        self.assertTrue(pmt.sQLX == pmt_converted.sQLX)
        self.assertTrue(pmt.sPMTt == pmt_converted.sPMTt)

        pmtc_converted = ev_converted.GetPMTCal(0)
        self.assertTrue(pmt.id == pmtc_converted.id)
        self.assertTrue(pmt.CellID == pmtc_converted.CellID)
        #self.assertTrue(pmt.ChanFlags == pmt_converted.ChanFlags)  # FIXME
        self.assertTrue(pmtc.sQHS == pmtc_converted.sQHS)
        self.assertTrue(pmtc.sQHL == pmtc_converted.sQHL)
        self.assertTrue(pmtc.sQLX == pmtc_converted.sQLX)
        self.assertTrue(pmtc.sPMTt == pmtc_converted.sPMTt)


if __name__ == '__main__':
    unittest.main()

