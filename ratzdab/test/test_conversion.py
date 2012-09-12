'''unit tests for ratzdab conversion utilities'''

import unittest
import numpy as np
import ratzdab
from rat import ROOT

class TestBidirectionalConversion(unittest.TestCase):
    '''Create data structures with known members, convert to zdab objects,
    convert back to rat objects, and make sure values are preserved.
    '''
    def test_event(self):
        '''Test conversion of RAT::DS::Root objects to and from ZDAB
        PmtEventRecords.

        Exceptions:
            * CAEN data (not converted to ZDAB yet)
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

        pmt = ev.AddNewPMTUnCal(1)
        pmt.id = 42
        pmt.CellID = 0
        pmt.ChanFlags = 0x5
        pmt.sQHS = 0xfaf
        pmt.sQHL = 0xfbf
        pmt.sQLX = 0xfcf
        pmt.sPMTt = 0xfdf

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

        pmt_converted = ev_converted.GetPMTUnCal(0)
        self.assertTrue(pmt.id == pmt_converted.id)
        self.assertTrue(pmt.CellID == pmt_converted.CellID)
        #self.assertTrue(pmt.ChanFlags == pmt_converted.ChanFlags) # FIXME
        self.assertTrue(pmt.sQHS == pmt_converted.sQHS)
        self.assertTrue(pmt.sQHL == pmt_converted.sQHL)
        self.assertTrue(pmt.sQLX == pmt_converted.sQLX)
        self.assertTrue(pmt.sPMTt == pmt_converted.sPMTt)

    def test_rhdr(self):
        '''Test conversion of RAT::DS::Run objects to and from ZDAB RunRecords.

        Exceptions:
            * subrun ID does not exist in RunRecord struct
        '''
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

    def test_cast(self):
        '''Test conversion of RAT::DS::ManipStat objects to and from ZDAB
        ManipStatuses.
        '''
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

    def test_caac(self):
        '''Test conversion of RAT::DS::AVStat objects to and from ZDAB
        AVStatuses.
        '''
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

    def test_eped(self):
        '''Test conversion of RAT::DS::EPEDInfo objects to and from ZDAB
        EpedRecords.

        Exceptions:
            * runID is not set by ratzdab::unpack::eped
        '''
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

