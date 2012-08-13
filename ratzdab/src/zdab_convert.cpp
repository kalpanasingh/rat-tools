#include <string>
#include <vector>
#include <stdlib.h>
#include <stdint.h>

#include <TObject.h>
#include <RAT/DB.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/AVStat.hh>
#include <RAT/DS/ManipStat.hh>
#include <RAT/DS/TRIGInfo.hh>
#include <RAT/DS/EPEDInfo.hh>
#include <RAT/DS/Digitiser.hh>
#include <RAT/DS/PMTUnCal.hh>

#include <PZdabFile.h>
#include <zdab_convert.hpp>

namespace ratzdab {

    /** RATDB instance to get at PMTINFO */
    static class RATDB {
        public:
            RATDB() {
                db = RAT::DB::Get();

                char* ratroot = getenv("RATROOT");
                if (!ratroot) {
                    throw no_rat;
                }

                std::string dbpath = std::string(ratroot) + "/data/PMTINFO.ratdb";
                db->Load(dbpath);

                pmtinfo = db->GetLink("PMTINFO", "sno+");

                // cache this for performance
                pmttype = pmtinfo->GetIArray("type");
            }

            virtual ~RATDB() {
                delete db;
            }

            RAT::DBLinkPtr pmtinfo;
            std::vector<int> pmttype;
        protected:
            RAT::DB* db;
    } ratdb;

    RAT::DS::Root* unpack::event(PmtEventRecord* pev) {
        RAT::DS::Root* ds = new RAT::DS::Root;
        RAT::DS::EV* ev = ds->AddNewEV();

        unsigned nhit = pev->NPmtHit;
        uint32_t run_id = pev->RunNumber;
        uint16_t subrun_id = pev->DaqStatus; // seriously
        uint32_t evorder = pev->EvNumber;
        uint16_t datatype = pev->DataType;
        MTCReadoutData mtc = pev->TriggerCardData;
        uint32_t* mtc_words = (uint32_t*) (&mtc);
        uint64_t clockstat10 = ((mtc_words[4] & 0x0f000000) >> 24); // fixme check this
        uint64_t clockcount10 = ((uint64_t) UNPK_MTC_BC10_2(mtc_words) << 32) || UNPK_MTC_BC10_1(mtc_words);
        uint64_t clockcount50 = ((uint64_t) UNPK_MTC_BC50_2(mtc_words) << 11) || UNPK_MTC_BC50_1(mtc_words);
        uint32_t trig_error = UNPK_MTC_ERROR(mtc_words);
        uint32_t trig_type = UNPK_MTC_TRIGGER(mtc_words);

        ds->SetRunID(run_id);
        ds->SetSubRunID(subrun_id);

        ev->SetClockStat10(clockstat10);
        ev->SetTrigError(trig_error);
        ev->SetTrigType(trig_type);
        ev->SetEventID(evorder);
        ev->SetClockCount50(clockcount50);
        ev->SetClockCount10(clockcount10);

        // set ut from 10mhz clock
        uint32_t total = clockcount10 * 100;
        uint32_t ns = total % ((uint64_t) 1e9);
        uint32_t s = total / 1e9;
        uint32_t d = ns / 86400;
        ns -= 86400 * d;

        ev->SetUTDays(d);
        ev->SetUTSecs(s);
        ev->SetUTNSecs(ns);

        uint32_t* caen_data = PZdabFile::GetExtendedData(pev, SUB_TYPE_CAEN);
        if (caen_data) {
            RAT::DS::Digitiser* d = ev->GetDigitiser();
            *d = unpack::caen(caen_data);
        }

        uint32_t* hits = (uint32_t*) (pev) + 1;
        for (unsigned i=0; i<nhit; i++) {
            unsigned crate_id = UNPK_CRATE_ID(hits);
            unsigned board_id = UNPK_BOARD_ID(hits);
            unsigned channel_id = UNPK_CHANNEL_ID(hits);

            if (crate_id > 18 || board_id > 15 || channel_id > 31) {
                if (VERBOSE) {
                    std::cerr << "Invalid hit PMT c/c/c: " << crate_id << "/"
                        << board_id << "/"
                        << channel_id
                        << std::endl;
                }
            }
            else {
                int lcn = 16 * 32 * crate_id + 32 * board_id + channel_id;
                int type = ratdb.pmttype[lcn];

                RAT::DS::PMTUnCal* pmtuncal = ev->AddNewPMTUnCal(type);
                *pmtuncal = unpack::pmt(hits);
            }

            hits += 3;
        }

        return ds;
    }

    RAT::DS::Run* unpack::rhdr(RunRecord* r) {
        RAT::DS::Run* run = new RAT::DS::Run;

        run->SetDate(r->Date);
        run->SetTime(r->Time);
        run->SetDAQVer(r->DAQCodeVersion);
        run->SetRunID(r->RunNumber);
        run->SetCalibTrialID(r->CalibrationTrialNumber);
        run->SetSrcMask(r->SourceMask);
        run->SetRunType(r->RunMask);
        run->SetCrateMask(r->GTCrateMsk);
        run->SetFirstEventID(r->FirstGTID);
        run->SetValidEventID(r->ValidGTID);

        // load pmt position and orientation from the database
        RAT::DS::PMTProperties* prop = run->GetPMTProp();

        vector<int> snomannumber = ratdb.pmtinfo->GetIArray("snomannumber");
        prop->SetSNOMANNumber(snomannumber);
        vector<int> panelnumber = ratdb.pmtinfo->GetIArray("panelnumber");
        prop->SetPanelNumber(panelnumber);
        vector<int> type = ratdb.pmtinfo->GetIArray("type");
        prop->SetType(type);
        vector<float> pmtx = ratdb.pmtinfo->GetFArrayFromD("x");
        vector<float> pmty = ratdb.pmtinfo->GetFArrayFromD("y");
        vector<float> pmtz = ratdb.pmtinfo->GetFArrayFromD("z");
        vector<float> dirx = ratdb.pmtinfo->GetFArrayFromD("u");
        vector<float> diry = ratdb.pmtinfo->GetFArrayFromD("v");
        vector<float> dirz = ratdb.pmtinfo->GetFArrayFromD("w");

        for(size_t id=0; id<type.size(); id++) {
            TVector3* pos = new TVector3(pmtx[id], pmty[id], pmtz[id]);
            prop->AddPos(pos);
            TVector3* dir = new TVector3(dirx[id], diry[id], dirz[id]);
            prop->AddDir(dir);
        }

        return run;
    }

    RAT::DS::TRIGInfo* unpack::trig(TriggerInfo* t) {
        throw record_unknown;
    }

    RAT::DS::EPEDInfo* unpack::eped(EpedRecord* e) {
        throw record_unknown;
    }

    RAT::DS::ManipStat* unpack::cast(ManipStatus* c) {
        throw record_unknown;
    }

    RAT::DS::AVStat* unpack::caac(AVStatus* c) {
        throw record_unknown;
    }

    RAT::DS::Digitiser unpack::caen(uint32_t* c) {
        RAT::DS::Digitiser d;

        uint32_t channel_mask = UNPK_CAEN_CHANNEL_MASK(c);
        uint32_t pattern = UNPK_CAEN_PATTERN(c);
        uint32_t event_count = UNPK_CAEN_EVENT_COUNT(c);
        uint32_t clock = UNPK_CAEN_TRIGGER_TIME(c);

        d.SetDigEventID(event_count);
        d.SetTrigTagTime(clock);
        d.SetChanMask(channel_mask);
        d.SetDataFormat(pattern); // fixme right place for this?

        unsigned nchannels = 0;
        for (int i=0; i<8; i++) {
            if (channel_mask & (1 << i)) {
                nchannels++;
            }
        }

        if (nchannels > 0) {
            int trace_length = (UNPK_CAEN_WORD_COUNT(c) - 4) / nchannels;
            int trace_samples = trace_length * 2;
            d.SetNWords(trace_length);

            unsigned n = 0;
            for (unsigned i=0; i<8; i++) {
                if (!(channel_mask & (1 << i))) {
                    continue;
                }

                RAT::DS::TrigSum* ts = d.AddNewTrigSum();
                std::vector<int> trace(trace_samples); // it's an int in the ds

                uint32_t* pword = c + 4 + n * trace_length;
                for (int j=0; j<trace_samples; pword++) {
                    trace[j++] = *(pword) & 0x0000ffff;
                    trace[j++] = *(pword) >> 16;
                }
                n++;

                ts->SetSamples(trace);
            }
        }

        return d;
    }

    RAT::DS::PMTUnCal unpack::pmt(uint32_t* hits) {
        RAT::DS::PMTUnCal p;

        unsigned crate_id = UNPK_CRATE_ID(hits);
        unsigned board_id = UNPK_BOARD_ID(hits);
        unsigned channel_id = UNPK_CHANNEL_ID(hits);

        int lcn = 16 * 32 * crate_id + 32 * board_id + channel_id;
        int cell = UNPK_CELL_ID(hits);
        char flags = UNPK_CGT_ES_16(hits)    << 0 ||
            UNPK_CGT_ES_24(hits)    << 1 ||
            UNPK_MISSED_COUNT(hits) << 2 ||
            UNPK_NC_CC(hits)        << 3 ||
            UNPK_LGI_SELECT(hits)   << 4 ||
            UNPK_CMOS_ES_16(hits)   << 5;

        uint32_t qhs = UNPK_QHS(hits);
        uint32_t qhl = UNPK_QHL(hits);
        uint32_t qlx = UNPK_QLX(hits);
        uint32_t tac = UNPK_TAC(hits);

        p.SetID(lcn);
        p.SetCellID(cell);
        p.SetChanFlags(flags);
        p.SetsQHS(qhs);
        p.SetsQHL(qhl);
        p.SetsQLX(qlx);
        p.SetsPMTt(tac);

        return p;
    }

} // namespace ratzdab

