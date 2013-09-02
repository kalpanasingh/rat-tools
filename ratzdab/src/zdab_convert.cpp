#include <zdab_convert.hpp>
#include <stdint.h>
#include <utility>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <PZdabFile.h>
#include <TObject.h>
#include <TMath.h>
#include <RAT/DB.hh>
#include <RAT/Log.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/AVStat.hh>
#include <RAT/DS/ManipStat.hh>
#include <RAT/DS/TRIGInfo.hh>
#include <RAT/DS/EPEDInfo.hh>
#include <RAT/DS/Digitiser.hh>
#include <RAT/DS/PMTUnCal.hh>

namespace ratzdab {

    /** RATDB instance to get at PMTINFO, since PMT type is needed to
        populate the RAT DS. */
    static class RATDB {
        public:
            RATDB() {
                RAT::Log::Init("/dev/null");

                db = RAT::DB::Get();
                assert(db);

                char* glg4data = getenv("GLG4DATA");
                if (glg4data == static_cast<char*>(NULL)) {
                    std::cerr << "ratzdab::ratdb: Environment variable $GLG4DATA must be set" << std::endl;
                    assert(glg4data);
                }
                std::string data = std::string(glg4data);
                assert(data != "");
                db->Load(data + "/pmt/airfill2.ratdb");

                pmtinfo = db->GetLink("PMTINFO");
                assert(pmtinfo);

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

    /** initialize static maps */

    std::map<int, int> get_pdg_to_snoman_map() {
        std::map<int, int> m;
        m[0] = 1;  // Photon, G4 also uses 0 for geantino and unknown
        m[22] = 2;  // Gamma
        m[11] = 20;  // Electron
        m[-11] = 21;  // Positron
        m[13] = 22;  // Mu-
        m[-13] = 23;  // Mu+
        m[15] = 24;  // Tau-
        m[-15] = 25;  // Tau+
        m[12] = 30;  // Nu-e
        m[-12] = 31;  // Nu-e-bar
        m[14] = 32;  // Nu-mu
        m[-14] = 33;  // Nu-mu-bar
        m[16] = 34;  // Nu-tau
        m[-16] = 35;  // Nu-tau-bar
        m[111] = 40;  // Pi0
        m[211] = 41;  // Pi+
        m[-211] = 42;  // Pi-
        m[311] = 50;  // K0
        m[-311] = 51;  // K0-bar
        m[321] = 52;  // K+
        m[-321] = 53;  // K-
        m[2212] = 80;  // Proton
        m[2112] = 81;  // Neutron
        return m;
    }
    static std::map<int, int> pdg_to_snoman = get_pdg_to_snoman_map();

    std::map<int, float> get_pdg_to_mass_map() {
        std::map<int, float> m;
        m[0] = 0;  // Photon, G4 also uses 0 for geantino and unknown
        m[22] = 0;  // Gamma
        m[11] = 0.510998928;  // Electron
        m[-11] = 0.510998928;  // Positron
        m[13] = 105.6583715;  // Mu-
        m[-13] = 105.6583715;  // Mu+
        m[15] = 1776.82;  // Tau-
        m[-15] = 1776.82;  // Tau+
        m[12] = 0;  // Nu-e
        m[-12] = 0;  // Nu-e-bar
        m[14] = 0;  // Nu-mu
        m[-14] = 0;  // Nu-mu-bar
        m[16] = 0;  // Nu-tau
        m[-16] = 0;  // Nu-tau-bar
        m[111] = 134.9766;  // Pi0
        m[211] = 139.57018;  // Pi+
        m[-211] = 139.57018;  // Pi-
        m[311] = 497.648;  // K0
        m[-311] = 497.648;  // K0-bar
        m[321] = 493.667;  // K+
        m[-321] = 493.667;  // K-
        m[2212] = 938.272046;  // Proton
        m[2112] = 939.565378;  // Neutron
        return m;
    }
    static std::map<int, float> pdg_to_mass = get_pdg_to_mass_map();

    /** unpacking functions */

    RAT::DS::Root* unpack::event(PmtEventRecord* const pev) {
        RAT::DS::Root* ds = new RAT::DS::Root;
        RAT::DS::EV* ev = ds->AddNewEV();

        unsigned nhit = pev->NPmtHit;
        uint32_t run_id = pev->RunNumber;
        uint16_t subrun_id = pev->DaqStatus; // seriously
        //uint32_t evorder = pev->EvNumber;  // unused in RAT
        uint16_t datatype = pev->DataType;
        MTCReadoutData mtc = pev->TriggerCardData;
        uint32_t* mtc_words = reinterpret_cast<uint32_t*>(&mtc);
        uint32_t gtid = static_cast<uint32_t>(UNPK_MTC_GT_ID(mtc_words));
        uint64_t clockcount10 = (static_cast<uint64_t>(UNPK_MTC_BC10_2(mtc_words)) << 32) |
                                (static_cast<uint64_t>(UNPK_MTC_BC10_1(mtc_words)));
        uint64_t clockcount50 = (static_cast<uint64_t>(UNPK_MTC_BC50_2(mtc_words)) << 11) |
                                (static_cast<uint64_t>(UNPK_MTC_BC50_1(mtc_words)));
        uint32_t trig_error = UNPK_MTC_ERROR(mtc_words);
        uint32_t esumpeak = UNPK_MTC_PEAK(mtc_words);
        uint32_t esumdiff = UNPK_MTC_DIFF(mtc_words);
        uint32_t esumint = UNPK_MTC_INT(mtc_words);

        // trigger word
        uint32_t trig_type = ((mtc_words[3] & 0xff000000) >> 24) | ((mtc_words[4] & 0x3ffff) << 8);

        ds->SetRunID(run_id);
        ds->SetSubRunID(subrun_id);

        ev->SetClockStat10(0);  // FIXME: what is this?
        ev->SetTrigError(trig_error);
        ev->SetESumPeak(esumpeak);
        ev->SetESumDiff(esumdiff);
        ev->SetESumInt(esumint);
        ev->SetTrigType(trig_type);
        ev->SetEventID(gtid);
        ev->SetClockCount50(clockcount50);
        ev->SetClockCount10(clockcount10);

        // set ut from 10mhz clock
        uint64_t total = clockcount10 * 100;
        uint64_t ns = total % (static_cast<uint64_t>(1e9));
        uint64_t s = total / 1e9;
        uint64_t d = s / 86400;
        s -= (86400 * d);

        ev->SetUTDays(d);
        ev->SetUTSecs(s);
        ev->SetUTNSecs(ns);

        // loop over sub fields and extract extra info
        CalibratedPMT* calhits = static_cast<CalibratedPMT*>(NULL);
        MonteCarloHeader* mcdata = static_cast<MonteCarloHeader*>(NULL);
        FittedEvent* fitdata = static_cast<FittedEvent*>(NULL);
        uint32_t* caen_data = static_cast<uint32_t*>(NULL);
        uint32_t* extrahitinfo = static_cast<uint32_t*>(NULL);
        uint32_t* extraeventinfo = static_cast<uint32_t*>(NULL);
        unsigned nfits = 0;

        uint32_t* sub_header = &pev->CalPckType;
        while (*sub_header & SUB_NOT_LAST) {
            sub_header += (*sub_header & SUB_LENGTH_MASK);
            uint32_t subtype_id = *sub_header >> SUB_TYPE_BITNUM;
            if (subtype_id == SUB_TYPE_CALIBRATED) {
                calhits = reinterpret_cast<CalibratedPMT*>(sub_header + 1);
            }
            else if (subtype_id == SUB_TYPE_MONTE_CARLO) {
                mcdata = reinterpret_cast<MonteCarloHeader*>(sub_header + 1);
            }
            else if (subtype_id == SUB_TYPE_FIT) {
                fitdata = reinterpret_cast<FittedEvent*>(sub_header + 1);
                nfits = ((*sub_header & SUB_LENGTH_MASK) * sizeof(uint32_t) - sizeof(SubFieldHeader)) / sizeof(FittedEvent);
            }
            else if (subtype_id == SUB_TYPE_CAEN) {
                caen_data = static_cast<uint32_t*>(sub_header + 1);
            }
            else if (subtype_id == SUB_TYPE_HIT_DATA) {
                extrahitinfo = static_cast<uint32_t*>(sub_header + 1);
            }
            else if (subtype_id == SUB_TYPE_EVENT_DATA) {
                extraeventinfo = static_cast<uint32_t*>(sub_header + 1);
            }
        }

        // pmt hit data
        uint32_t* hits = reinterpret_cast<uint32_t*>(pev + 1);
        for (unsigned i=0; i<nhit; i++) {
            unsigned crate_id = UNPK_CRATE_ID(hits);
            unsigned board_id = UNPK_BOARD_ID(hits);
            unsigned channel_id = UNPK_CHANNEL_ID(hits);

            if (crate_id > 18 || board_id > 15 || channel_id > 31) {
                if (VERBOSE) {
                    std::cerr << "ratzdab::unpack::event: "
                              << "Invalid hit PMT c/c/c: "
                              << crate_id << "/"
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

                if (calhits) {
                    RAT::DS::PMTCal* pmtcal = ev->AddNewPMTCal(type);
                    pmtcal->SetID(pmtuncal->GetID());
                    pmtcal->SetChanFlags(pmtuncal->GetChanFlags());
                    pmtcal->SetCellID(pmtuncal->GetCellID());

                    pmtcal->SetsQHS(calhits->qhs);
                    pmtcal->SetsQHL(calhits->qhl);
                    pmtcal->SetsQLX(calhits->qlx);
                    pmtcal->SetsPMTt(calhits->tac);
                }
            }

            hits += 3;
        }

        // caen data
        if (caen_data) {
            RAT::DS::Digitiser* d = ev->GetDigitiser();
            *d = unpack::caen(caen_data);
        }

        // extra hit info -- no place in RAT DS currently
        if (extrahitinfo) {
            ExtraHitData* ehd = reinterpret_cast<ExtraHitData*>(extrahitinfo);
            float* p = reinterpret_cast<float*>(ehd + 1);
            std::cerr << "ratzdab::unpack::event: Extra hit data of type "
                      << ehd->name << " not converted." << std::endl;
            if (false) {
                for (unsigned i=0; i<nhit; i++) {
                    //float f = *p;  // set something somewhere
                    p++;
                }
            }
        }

        // extra event data -- no place in RAT DS currently
        if (extraeventinfo) {
            ExtraEventData* eed = reinterpret_cast<ExtraEventData*>(extraeventinfo);
            char* name = eed->name;
            float value = eed->value;
            std::cerr << "ratzdab::unpack::event: Extra event data " << name
                      << " = " << value << " not converted." << std::endl;
        }

        // monte carlo data
        if (mcdata) {
            MonteCarloHeader* mchdr = mcdata;
            MonteCarloVertex* mcvtx = reinterpret_cast<MonteCarloVertex*>(mchdr + 1);
            for (unsigned i=0; i<mchdr->nVertices; i++, ++mcvtx) {
                RAT::DS::MCParticle* p = ds->GetMC()->AddNewMCParticle();
                int snoman_code = mcvtx->particle;

                // convert cm -> mm
                p->SetPos(TVector3(mcvtx->x * 10, mcvtx->y * 10, mcvtx->z * 10));

                // convert SNOMAN code to PDG
                int pdgcode = 0;
                bool found_code = false;
                std::map<int, int>::const_iterator it_code;
                for (it_code=ratzdab::pdg_to_snoman.begin(); it_code!=ratzdab::pdg_to_snoman.end(); it_code++) {
                    if (it_code->second == snoman_code) {
                        pdgcode = it_code->first;
                        found_code = true;
                        break;
                    }
                }
                if (!found_code) {
                    cerr << "ratzdab::pack::event: No PDG code available for SNOMAN code "
                         << snoman_code << ", using zero." << std::endl;
                }
                p->SetPDGCode(pdgcode);

                // convert total energy to kinetic
                float mass = 0;
                std::map<int, float>::const_iterator it_mass = ratzdab::pdg_to_mass.find(pdgcode);
                if (it_mass != ratzdab::pdg_to_mass.end()) {
                    mass = it_mass->second;
                }
                else {
                    cerr << "ratzdab::pack::event: No mass code available for PDG code "
                         << pdgcode << ", using zero." << std::endl;
                }
                float momentum = mcvtx->energy * mcvtx->energy - mass * mass;
                float ke = momentum * momentum / (2 * mass);
                p->SetKE(ke);

                // convert direction cosines to cartesian momentum vector
                double px = momentum * TMath::Cos(mcvtx->u);
                double py = momentum * TMath::Cos(mcvtx->v);
                double pz = momentum * TMath::Cos(mcvtx->w);
                p->SetMom(TVector3(px, py, pz));

                p->SetTime(mcvtx->time);
            }
        }

        // fit results
        if (fitdata) {
            for (unsigned i=0; i<nfits; i++, ++fitdata) {
                RAT::DS::FitVertex fv;
                fv.SetPosition(TVector3(fitdata->x, fitdata->y, fitdata->z));
                fv.SetDirection(TVector3(fitdata->u, fitdata->v, fitdata->w));
                fv.SetTime(fitdata->time);

                RAT::DS::FitResult fr;
                fr.SetFOM("quality", fitdata->quality);
                fr.SetVertex(0, fv);

                ev->SetFitResult(fitdata->name, fr);
            }
        }

        return ds;
    }

    RAT::DS::Run* unpack::rhdr(RunRecord* const r) {
        // sno DAQCodeVersion is uint32, rat DAQVer is char
        if (r->DAQCodeVersion > 0xff) {
            std::cerr << "ratzdab::unpack::rhdr: DAQCodeVersion ("
                      << std::hex << r->DAQCodeVersion << std::dec
                      << ") overflows char type" << std::endl;
        }

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

    RAT::DS::TRIGInfo* unpack::trig(TriggerInfo* const t) {
        RAT::DS::TRIGInfo* triginfo = new RAT::DS::TRIGInfo;

        triginfo->SetTrigMask(t->TriggerMask);
        triginfo->SetPulserRate(t->PulserRate);
        triginfo->SetMTC_CSR(t->ControlRegister);
        triginfo->SetLockoutWidth(t->reg_LockoutWidth);
        triginfo->SetPrescaleFreq(t->reg_Prescale);
        triginfo->SetEventID(t->GTID);
        triginfo->SetNTrigTHold(10);  // number of trigger thresholds
        triginfo->SetNTrigZeroOffset(10);  // number of trigger zero offsets

        // triggers are separate members in TriggerInfo, array in TRIGInfo
        triginfo->SetNTrigTHold(10);
        triginfo->SetNTrigZeroOffset(10);
        triginfo->SetTrigTHold(0, t->n100lo);
        triginfo->SetTrigZeroOffset(0, t->n100lo_zero);
        triginfo->SetTrigTHold(1, t->n100med);
        triginfo->SetTrigZeroOffset(1, t->n100med_zero);
        triginfo->SetTrigTHold(2, t->n100hi);
        triginfo->SetTrigZeroOffset(2, t->n100hi_zero);
        triginfo->SetTrigTHold(3, t->n20);
        triginfo->SetTrigZeroOffset(3, t->n20_zero);
        triginfo->SetTrigTHold(4, t->n20lb);
        triginfo->SetTrigZeroOffset(4, t->n20lb_zero);
        triginfo->SetTrigTHold(5, t->esumlo);
        triginfo->SetTrigZeroOffset(5, t->esumlo_zero);
        triginfo->SetTrigTHold(6, t->esumhi);
        triginfo->SetTrigZeroOffset(6, t->esumhi_zero);
        triginfo->SetTrigTHold(7, t->owln);
        triginfo->SetTrigZeroOffset(7, t->owln_zero);
        triginfo->SetTrigTHold(8, t->owlelo);
        triginfo->SetTrigZeroOffset(8, t->owlelo_zero);
        triginfo->SetTrigTHold(9, t->owlehi);
        triginfo->SetTrigZeroOffset(9, t->owlehi_zero);

        return triginfo;
    }

    RAT::DS::EPEDInfo* unpack::eped(EpedRecord* const e) {
        RAT::DS::EPEDInfo* eped = new RAT::DS::EPEDInfo;

        eped->SetGTDelayCoarse(e->ped_delay_coarse);
        eped->SetGTDelayFine(e->ped_delay_fine);
        eped->SetQPedAmp(e->qinj_dacsetting);
        eped->SetQPedWidth(e->ped_width);
        eped->SetPatternID(e->halfCrateID);
        eped->SetCalType(e->CalibrationType);
        eped->SetEventID(e->GTID);

        return eped;
    }

    RAT::DS::ManipStat* unpack::cast(ManipStatus* const c) {
        RAT::DS::ManipStat* manip = new RAT::DS::ManipStat;

        manip->SetSrcID(c->sourceID);
        manip->SetSrcStatus(c->status);
        manip->SetNRopes(c->numRopes);
        manip->SetSrcPosUnc(c->positionError);
        manip->SetLaserballOrient(c->orientation);

        for (unsigned i=0; i<3; i++) {
            manip->SetManipPos(i, c->position[i]);
            manip->SetManipDest(i, c->destination[i]);
            manip->SetSrcPosUnc(i, c->obsoletePosErr[i]);
        }

        for (unsigned i=0; i<manip->GetNRopes(); i++) {
            manip->SetRopeID(i, c->ropeStatus[i].ropeID);
            manip->SetRopeLength(i, c->ropeStatus[i].length);
            manip->SetRopeTargLength(i, c->ropeStatus[i].targetLength);
            manip->SetRopeVelocity(i, c->ropeStatus[i].velocity);
            manip->SetRopeTension(i, c->ropeStatus[i].tension);
            manip->SetRopeErr(i, c->ropeStatus[i].encoderError);
        }

        return manip;
    }

    RAT::DS::AVStat* unpack::caac(AVStatus* const c) {
        RAT::DS::AVStat* av = new RAT::DS::AVStat;

        for (unsigned i=0; i<3; i++) {
            av->SetPosition(i, c->position[i]);
            av->SetRoll(i, c->rotation[i]);
        }

        for (unsigned i=0; i<7; i++) {
            av->SetRopeLength(i, c->ropeLength[i]);
        }

        return av;
    }

    RAT::DS::Digitiser unpack::caen(uint32_t* const c) {
        RAT::DS::Digitiser d;

        uint32_t channel_mask = UNPK_CAEN_CHANNEL_MASK(c);
        uint32_t magic = UNPK_CAEN_MAGIC(c);
        uint32_t pattern = UNPK_CAEN_PATTERN(c);
        uint32_t event_count = UNPK_CAEN_EVENT_COUNT(c);
        uint32_t clock = UNPK_CAEN_TRIGGER_TIME(c);
        uint32_t pack_flag = UNPK_CAEN_PACK_FLAG(c);

        d.SetBit24(pack_flag);
        d.SetDataFormat(magic);  // FIXME?
        d.SetDigEventID(event_count);
        d.SetTrigTagTime(clock);
        d.SetChanMask(channel_mask);
        d.SetIOPins(pattern);

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
                std::vector<int> trace(trace_samples);  // it's an int in the ds

                uint32_t* pword = c + 4 + n * trace_length / 2;
                for (int j=0; j<trace_length; pword++) {
                    trace[j++] = *(pword) & 0xffff;
                    trace[j++] = (*(pword) >> 16) & 0xffff;
                }
                n++;

                ts->SetSamples(trace);
            }
        }

        return d;
    }

    RAT::DS::PMTUnCal unpack::pmt(uint32_t* const hits) {
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

    /** packing functions */

    PmtEventRecord* pack::event(RAT::DS::Root *ds, int ev_id) {
        if (!ds || ev_id > ds->GetEVCount() - 1) {
            return static_cast<PmtEventRecord*>(NULL);
        }

        RAT::DS::EV* ev = ds->GetEV(ev_id);
        RAT::DS::MC* mc = ds->ExistMC() ? ds->GetMC() : static_cast<RAT::DS::MC*>(NULL);
        RAT::DS::Digitiser* digitizer = ev->GetDigitiser();

        int npmts = ev->GetPMTUnCalCount();

        // calculate buffer size (length)
        // there is no GenericRecordHeader here, as they are only used in
        // dispatched data, not in files
        int length = sizeof(PmtEventRecord) + npmts * sizeof(FECReadoutData);

        int nfits = 0;
        int caen_length = 0;

        // calibrated pmt data
        if (ev->GetPMTCalCount() > 0) {
            assert(ev->GetPMTCalCount() == ev->GetPMTUnCalCount());
            length += npmts * sizeof(CalibratedPMT) + sizeof(SubFieldHeader);
        }

        // monte carlo data
        if (mc) {
            int nvertices = 0;
            if (mc->GetMCTrackCount() > 0) {
                for (int itrack=0; itrack<mc->GetMCTrackCount(); itrack++) {
                    RAT::DS::MCTrack* track = mc->GetMCTrack(itrack);
                    for (int istep=0; istep<track->GetMCTrackStepCount(); istep++) {
                        nvertices++;
                    }
                }
            }
            else {
                nvertices = mc->GetMCParticleCount();
            }
            length += nvertices * sizeof(MonteCarloVertex) + sizeof(MonteCarloHeader) + sizeof(SubFieldHeader);
        }

        // fits
        // fit result map size not exposed by api, grumble grumble
        std::map<std::string, RAT::DS::FitResult>::iterator it;
        nfits = 0;
        for (it=ev->GetFitResultIterBegin(); it!=ev->GetFitResultIterEnd(); ++it) {
            nfits++;
        }
        if (nfits > 0) {
            length += nfits * (sizeof(FittedEvent) + sizeof(SubFieldHeader));
        }

        // caen data
        if (digitizer->GetTrigSumCount() > 0) {
            int caen_header_length = 4 * sizeof(uint32_t);
            int caen_total_sample_count = 0;
            for (int i=0; i<digitizer->GetTrigSumCount(); i++) {
                caen_total_sample_count += digitizer->GetTrigSum(i)->GetSampleCount();
            }
            caen_length = caen_header_length + caen_total_sample_count * sizeof(uint16_t);
            length += sizeof(SubFieldHeader) + caen_length;
        }

        // allocate PmtEventRecord atop char buffer
        char* buffer = new char[length];
        PmtEventRecord* r = reinterpret_cast<PmtEventRecord*>(buffer);

        // get pointer to first MTC and FEC words
        uint32_t* mtc_word = reinterpret_cast<uint32_t*>(&(r->TriggerCardData));
        uint32_t* fec_word = reinterpret_cast<uint32_t*>(r + 1);

        r->RunNumber = ds->GetRunID();
        //r->EvNumber = ev->GetEventID();  // event order not implemented in RAT
        r->NPmtHit = npmts;

        r->PmtEventRecordInfo = PMT_EVR_RECTYPE | PMT_EVR_NOT_MC | PMT_EVR_ZDAB_VER;  // from xsnoed... ???
        r->DataType = PMT_EVR_DATA_TYPE;
        r->DaqStatus = ds->GetSubRunID();
        r->CalPckType = PMT_EVR_PCK_TYPE | PMT_EVR_CAL_TYPE;

        CalibratedPMT* cal_pmt = static_cast<CalibratedPMT*>(NULL);

        uint32_t* sub_header = &(r->CalPckType);

        // must set the size of this sub-field before calling AddSubField()
        // (from the sub-field header to the end)
        *sub_header |= (static_cast<uint32_t*>(fec_word + npmts * 3) - sub_header);

        // calibrated hit information
        if (ev->GetPMTCalCount() > 0) {
            PZdabFile::AddSubField(&sub_header, SUB_TYPE_CALIBRATED, npmts * sizeof(CalibratedPMT));
            cal_pmt = reinterpret_cast<CalibratedPMT*>(sub_header + 1);
        }

        // add monte carlo data
        if (mc) {
            // if tracking is enabled, add track steps. otherwise, just add
            // the primary vertex MCParticles
            if (mc->GetMCTrackCount() > 0) {
                // build table to look up sequential vertex id by track and step index
                std::map<std::pair<int, int>, int> step_to_vertex_id;
                std::map<int, int> track_id_to_index;
                int nvertices = 0;
                for (int itrack=0; itrack<mc->GetMCTrackCount(); itrack++) {
                    RAT::DS::MCTrack* track = mc->GetMCTrack(itrack);
                    track_id_to_index[track->GetTrackID()] = itrack;
                    for (int istep=0; istep<track->GetMCTrackStepCount(); istep++) {
                        step_to_vertex_id[std::make_pair(itrack, istep)] = nvertices++;
                    }
                }
                assert(nvertices == step_to_vertex_id.size());

                if (nvertices > 0) {
                    PZdabFile::AddSubField(&sub_header, SUB_TYPE_MONTE_CARLO, sizeof(MonteCarloHeader) + nvertices * sizeof(MonteCarloVertex));

                    // get pointer to start of monte-carlo data and vertices
                    MonteCarloHeader* mc_hdr = reinterpret_cast<MonteCarloHeader*>(sub_header + 1);
                    MonteCarloVertex* mc_vtx = reinterpret_cast<MonteCarloVertex*>(mc_hdr + 1);

                    // fill in the monte carlo data
                    mc_hdr->nVertices = nvertices;

                    int vertex_id = 0;
                    for (int itrack=0; itrack<mc->GetMCTrackCount(); itrack++) {
                        RAT::DS::MCTrack* track = mc->GetMCTrack(itrack);
                        for (int istep=0; istep<track->GetMCTrackStepCount(); istep++) {
                            RAT::DS::MCTrackStep* step = track->GetMCTrackStep(istep);

                            int pdgcode = track->GetPDGCode();
                            float momentum = step->GetMom().Mag();

                            // convert kinetic to total energy
                            double mass = 0;
                            std::map<int, float>::const_iterator it_mass = ratzdab::pdg_to_mass.find(pdgcode);
                            if (it_mass != ratzdab::pdg_to_mass.end()) {
                                mass = it_mass->second;
                            }
                            else {
                                cerr << "ratzdab::unpack::event: No mass available for PDG code "
                                     << pdgcode << ", using zero." << std::endl;
                            }
                            mc_vtx->energy = TMath::Sqrt(mass*mass + momentum*momentum);  // all MeV, c=1

                            // convert mm -> cm
                            mc_vtx->x = step->GetEndPos()[0] / 10;
                            mc_vtx->y = step->GetEndPos()[1] / 10;
                            mc_vtx->z = step->GetEndPos()[2] / 10;

                            // u, v, w are direction cosines
                            mc_vtx->u = step->GetMom()[0] / momentum;
                            mc_vtx->v = step->GetMom()[1] / momentum;
                            mc_vtx->w = step->GetMom()[2] / momentum;

                            // convert from PDG to SNOMAN code
                            int code = 0;  // 0 indicates unknown particle
                            std::map<int, int>::const_iterator it_code = ratzdab::pdg_to_snoman.find(pdgcode);
                            if (it_code != ratzdab::pdg_to_snoman.end()) {
                                code = it_code->second;
                            }
                            mc_vtx->particle = code;

                            mc_vtx->int_code = 100;  // interaction code; FIXME: 100 = start

                            // parent is previous step, or if this is the first
                            // step in the track, look up parent track and
                            // fuzzy match to determine which step
                            int parent = vertex_id - 1;
                            if (istep == 0) {
                                int parent_track_id = track->GetParentID();
                                std::map<int, int>::iterator it_ptid = track_id_to_index.find(parent_track_id);
                                if (it_ptid == track_id_to_index.end()) {
                                    parent = -1;
                                }
                                else {
                                    RAT::DS::MCTrack* parent_track = mc->GetMCTrack(it_ptid->second);

                                    assert(parent_track->GetMCTrackStepCount() > 0);
                                    double closest_distance = (parent_track->GetMCTrackStep(0)->GetEndPos() - step->GetEndPos()).Mag();
                                    int closest_step_id = 0;
                                    for (int jstep=0; jstep<parent_track->GetMCTrackStepCount(); jstep++) {
                                        RAT::DS::MCTrackStep* parent_step = parent_track->GetMCTrackStep(jstep);
                                        double dist = (parent_step->GetEndPos() - step->GetEndPos()).Mag();
                                        if (dist < closest_distance) {
                                            closest_distance = dist;
                                            closest_step_id = jstep;
                                        }
                                    }
                                    parent = step_to_vertex_id[std::make_pair(it_ptid->second, closest_step_id)];
                                }
                            }

                            mc_vtx->parent = parent;

                            mc_vtx->time = step->GetGlobalTime();
                            mc_vtx->flags = 0;

                            vertex_id++;
                            mc_vtx++;
                        }
                    }
                }
            }
            else {
                int nvertices = mc->GetMCParticleCount();
                if (nvertices > 0) {
                    PZdabFile::AddSubField(&sub_header, SUB_TYPE_MONTE_CARLO, sizeof(MonteCarloHeader) + nvertices * sizeof(MonteCarloVertex));

                    // get pointer to start of monte-carlo data and vertices
                    MonteCarloHeader* mc_hdr = reinterpret_cast<MonteCarloHeader*>(sub_header + 1);
                    MonteCarloVertex* mc_vtx = reinterpret_cast<MonteCarloVertex*>(mc_hdr + 1);

                    // fill in the monte carlo data values
                    mc_hdr->nVertices = nvertices;
                    for (int i=0; i<nvertices; i++, mc_vtx++) {
                        RAT::DS::MCParticle* p = mc->GetMCParticle(i);
                        int pdgcode = p->GetPDGCode();
                        float momentum = p->GetMom().Mag();
     
                        // convert kinetic to total energy
                        double mass = 0;
                        std::map<int, float>::const_iterator it_mass = ratzdab::pdg_to_mass.find(pdgcode);
                        if (it_mass != ratzdab::pdg_to_mass.end()) {
                            mass = it_mass->second;
                        }
                        else {
                            cerr << "ratzdab::unpack::event: No mass available for PDG code "
                                 << pdgcode << ", using zero." << std::endl;
                        }
                        mc_vtx->energy = TMath::Sqrt(mass*mass + momentum*momentum);  // all MeV, c=1
     
                        // convert mm -> cm
                        mc_vtx->x = p->GetPos()[0] / 10;
                        mc_vtx->y = p->GetPos()[1] / 10;
                        mc_vtx->z = p->GetPos()[2] / 10;
     
                        // u, v, w are direction cosines
                        mc_vtx->u = p->GetMom()[0] / momentum;
                        mc_vtx->v = p->GetMom()[1] / momentum;
                        mc_vtx->w = p->GetMom()[2] / momentum;
     
                        // convert from PDG to SNOMAN code
                        int code = 0;  // 0 indicates unknown particle
                        std::map<int, int>::const_iterator it_code = ratzdab::pdg_to_snoman.find(pdgcode);
                        if (it_code != ratzdab::pdg_to_snoman.end()) {
                            code = it_code->second;
                        }
                        mc_vtx->particle = code;
     
                        mc_vtx->int_code = 100;  // interaction code; FIXME: 100 = start
                        mc_vtx->parent = -1;  // p->GetIndex() in QSNO
                        mc_vtx->time = p->GetTime();
                        mc_vtx->flags = 0;
                    }
                }
            }
        }
     
        // add all available fits
        for (it=ev->GetFitResultIterBegin(); it!=ev->GetFitResultIterEnd(); ++it) {
            PZdabFile::AddSubField(&sub_header, SUB_TYPE_FIT, sizeof(FittedEvent));

            // get pointer to start of fit data
            FittedEvent* fit = reinterpret_cast<FittedEvent*>(sub_header + 1);
            RAT::DS::FitResult* rfit = &(*it).second;

            if (rfit->GetVertexCount() == 0) {
                continue;
            }

            RAT::DS::FitVertex rv = rfit->GetVertex(0);  // FIXME can zdab handle >1 vertices?

            if (rv.ContainsPosition()) {
                fit->x = rv.GetPosition()[0]/10;
                fit->y = rv.GetPosition()[1]/10;
                fit->z = rv.GetPosition()[2]/10;
            }
            else {
                fit->x = -9999;
                fit->y = -9999;
                fit->z = -9999;
            }

            if (rv.ContainsDirection()) {
                fit->u = rv.GetDirection()[0];
                fit->v = rv.GetDirection()[1];
                fit->w = rv.GetDirection()[2];
            }
            else {
                fit->u = 0;
                fit->v = 0;
                fit->w = 0;
            }

            if (rv.ContainsTime()) {
                fit->time = rv.GetTime();
            }
            else {
                fit-> time = -9999;
            }

            fit->quality = rfit->GetFOM((*it).first);
            fit->npmts = npmts;
            fit->spare = 0;
            const char* pt = (*it).first.c_str();
            char buff[256];
            if (!pt) {
                pt = "<null>";
            }
            snprintf(buff, 256, "%s", pt);
            memset(fit->name, 0, 32);
            strncpy(fit->name, buff, 31);  // copy fit name (31 chars max)
        }

        // caen digitizer waveforms
        if (caen_length) {
            PZdabFile::AddSubField(&sub_header, SUB_TYPE_CAEN, caen_length);
            uint32_t* caen = sub_header + 1;

            RAT::DS::Digitiser* d = ev->GetDigitiser();
            uint16_t magic = d->GetDataFormat();  // FIXME ???
            uint16_t channel_mask = d->GetChanMask();
            uint16_t pattern = d->GetIOPins();
            uint16_t pack_flag = d->GetBit24();
            uint32_t word_count = d->GetNWords();
            uint32_t board_id = d->GetBoardID();
            uint32_t event_id = d->GetDigEventID();
            uint32_t trigger_time = d->GetTrigTagTime();

            // pack header
            *(caen++) = ((magic & 0xf) << 28) | word_count;
            *(caen++) = (board_id << 25) | ((pack_flag & 1) << 24) | ((pattern & 0xffff) << 8) | (channel_mask & 0xff);
            *(caen++) = event_id & 0xffffff;
            *(caen++) = trigger_time;

            // copy samples
            uint16_t* psample = reinterpret_cast<uint16_t*>(caen);
            for (unsigned i=0; i<d->GetTrigSumCount(); i++) {
                RAT::DS::TrigSum* s = d->GetTrigSum(i);
                for (unsigned j=0; j<s->GetSampleCount(); j++) {
                    *(psample++) = static_cast<uint16_t>(s->GetSample(j));
                }
            }
        }

        // trigger
        uint32_t gtid = ev->GetEventID();
        uint32_t trigger = ev->GetTrigType();
        uint32_t error = ev->GetTrigError();

        uint32_t peak = ev->GetESumPeak() & 0x3ff;
        uint32_t inte = ev->GetESumInt() & 0x3ff;
        uint32_t diff = ev->GetESumDiff() & 0x3ff;

        *(mtc_word++) = static_cast<uint32_t>(ev->GetClockCount10());
        *(mtc_word++) = ((ev->GetClockCount10() >> 32) & 0x7fffff) | ((ev->GetClockCount50() & 0x7ff) << 21);
        *(mtc_word++) = static_cast<uint32_t>(ev->GetClockCount50() >> 11);
        *(mtc_word++) = ((trigger & 0x000000ff) << 24) | (gtid & 0xffffff);
        *(mtc_word++) = ((trigger & 0x07ffff00) >> 8) | (peak << 19) | (diff << 29);
        *(mtc_word++) = ((error & 0x3fff) << 17) | (inte << 7) | (diff >> 3);

        // pmts
        for (int i=0; i<npmts; i++) {
            RAT::DS::PMTUnCal* pmt = ev->GetPMTUnCal(i);

            uint32_t crate_id = static_cast<uint32_t>((pmt->GetID() >> 9) & 0x1f);
            uint32_t card_id = static_cast<uint32_t>((pmt->GetID() >> 5) & 0xf);
            uint32_t channel_id = static_cast<uint32_t>(pmt->GetID() & 0x1f);
            uint32_t cell_id = static_cast<uint32_t>(pmt->GetCellID());

            *(fec_word++) = (card_id << 26) | (crate_id << 21) | (channel_id << 16) | (gtid & 0xffffUL);

            *(fec_word++) = ((static_cast<uint32_t>(pmt->GetsQHS()) ^ 0x800) << 16) | (cell_id << 12) |
                ((static_cast<uint32_t>(pmt->GetsQLX()) ^ 0x800));

            *(fec_word++) = ((gtid & 0x00f00000UL) << 8) |
                ((static_cast<uint32_t>(pmt->GetsPMTt()) ^ 0x800) << 16) |
                ((gtid & 0x000f0000UL) >> 4) |
                ((static_cast<uint32_t>(pmt->GetsQHL()) ^ 0x800));

            // fill in calibrated PmtEventRecord entries if available
            if (cal_pmt) {
                RAT::DS::PMTCal* rpmtcal = ev->GetPMTCal(i);
                cal_pmt->tac = rpmtcal->GetsPMTt();
                cal_pmt->qhs = rpmtcal->GetsQHS();
                cal_pmt->qhl = rpmtcal->GetsQHL();
                cal_pmt->qlx = rpmtcal->GetsQLX();
                cal_pmt++;
            }
        }

        return r;
    }

    RunRecord* pack::rhdr(RAT::DS::Run* const run) {
        // run type is 64-bit in rat, but 32-bit in sno
        if (run->GetRunType() > 0xffffffff) {
            std::cerr << "ratzdab::pack::rhdr: Run type overflows 32-bit int" << std::endl;
            return static_cast<RunRecord*>(NULL);
        }

        RunRecord* rr = new RunRecord;

        rr->Date = run->GetDate();
        rr->Time = run->GetTime();
        rr->DAQCodeVersion = run->GetDAQVer();
        rr->RunNumber = run->GetRunID();
        rr->CalibrationTrialNumber = run->GetCalibTrialID();
        rr->SourceMask = run->GetSrcMask();
        rr->RunMask = run->GetRunType();
        rr->GTCrateMsk = run->GetCrateMask();
        rr->FirstGTID = run->GetFirstEventID();
        rr->ValidGTID = run->GetValidEventID();

        return rr;
    }

    ManipStatus* pack::cast(RAT::DS::ManipStat* const manip) {
        // length of ManipStatus::ropeStatus is bounded by kMaxManipulatorRopes
        if (manip->GetNRopes() > kMaxManipulatorRopes) {
            std::cerr << "ratzdab::pack::cast: ManipStatus defines more than kMaxManiplatorRopes ropes" << std::endl;
            return static_cast<ManipStatus*>(NULL);
        }

        ManipStatus* ms = new ManipStatus;

        ms->sourceID = manip->GetSrcID();
        ms->status = manip->GetSrcStatus();
        ms->numRopes = manip->GetNRopes();
        ms->positionError = manip->GetSrcPosUnc();
        ms->orientation = manip->GetLaserballOrient();

        for (unsigned i=0; i<3; i++) {
            ms->position[i] = manip->GetManipPos(i);
            ms->destination[i] = manip->GetManipDest(i);
            ms->obsoletePosErr[i] = manip->GetSrcPosUnc(i);
        }

        for (unsigned i=0; i<kMaxManipulatorRopes; i++) {
            ms->ropeStatus[i].ropeID = manip->GetRopeID(i);
            ms->ropeStatus[i].length = manip->GetRopeLength(i);
            ms->ropeStatus[i].targetLength = manip->GetRopeTargLength(i);
            ms->ropeStatus[i].velocity = manip->GetRopeVelocity(i);
            ms->ropeStatus[i].tension = manip->GetRopeTension(i);
            ms->ropeStatus[i].encoderError = manip->GetRopeErr(i);
        }

        return ms;
    }

    AVStatus* pack::caac(RAT::DS::AVStat* const avstat) {
        AVStatus* as = new AVStatus;

        for (unsigned i=0; i<3; i++) {
            as->position[i] = avstat->GetPosition(i);
            as->rotation[i] = avstat->GetRoll(i);
        }

        for (unsigned i=0; i<7; i++) {
            as->ropeLength[i] = avstat->GetRopeLength(i);
        }

        return as;
    }

    TriggerInfo* pack::trig(RAT::DS::TRIGInfo* const triginfo) {
        // TriggerInfo needs exactly 10 triggers
        if (triginfo->GetNTrigTHold() != 10 || triginfo->GetNTrigZeroOffset() != 10) {
            std::cerr << "ratzdab::pack::trig: TriggerInfo requires exactly 10 triggers defined" << std::endl;
            return static_cast<TriggerInfo*>(NULL);
        }
        TriggerInfo* ti = new TriggerInfo;

        ti->TriggerMask = triginfo->GetTrigMask();

        if (triginfo->GetNTrigTHold() > 0)
            ti->n100lo = triginfo->GetTrigTHold(0);
        if (triginfo->GetNTrigTHold() > 1)
            ti->n100med = triginfo->GetTrigTHold(1);
        if (triginfo->GetNTrigTHold() > 2)
            ti->n100hi = triginfo->GetTrigTHold(2);
        if (triginfo->GetNTrigTHold() > 3)
            ti->n20 = triginfo->GetTrigTHold(3);
        if (triginfo->GetNTrigTHold() > 4)
            ti->n20lb = triginfo->GetTrigTHold(4);
        if (triginfo->GetNTrigTHold() > 5)
            ti->esumlo = triginfo->GetTrigTHold(5);
        if (triginfo->GetNTrigTHold() > 6)
            ti->esumhi = triginfo->GetTrigTHold(6);
        if (triginfo->GetNTrigTHold() > 7)
            ti->owln = triginfo->GetTrigTHold(7);
        if (triginfo->GetNTrigTHold() > 8)
            ti->owlelo = triginfo->GetTrigTHold(8);
        if (triginfo->GetNTrigTHold() > 9)
            ti->owlehi = triginfo->GetTrigTHold(9);

        if (triginfo->GetNTrigZeroOffset() > 0)
            ti->n100lo_zero = triginfo->GetTrigZeroOffset(0);
        if (triginfo->GetNTrigZeroOffset() > 1)
            ti->n100med_zero = triginfo->GetTrigZeroOffset(1);
        if (triginfo->GetNTrigZeroOffset() > 2)
            ti->n100hi_zero = triginfo->GetTrigZeroOffset(2);
        if (triginfo->GetNTrigZeroOffset() > 3)
            ti->n20_zero = triginfo->GetTrigZeroOffset(3);
        if (triginfo->GetNTrigZeroOffset() > 4)
            ti->n20lb_zero = triginfo->GetTrigZeroOffset(4);
        if (triginfo->GetNTrigZeroOffset() > 5)
            ti->esumlo_zero = triginfo->GetTrigZeroOffset(5);
        if (triginfo->GetNTrigZeroOffset() > 6)
            ti->esumhi_zero = triginfo->GetTrigZeroOffset(6);
        if (triginfo->GetNTrigZeroOffset() > 7)
            ti->owln_zero = triginfo->GetTrigZeroOffset(7);
        if (triginfo->GetNTrigZeroOffset() > 8)
            ti->owlelo_zero = triginfo->GetTrigZeroOffset(8);
        if (triginfo->GetNTrigZeroOffset() > 9)
            ti->owlehi_zero = triginfo->GetTrigZeroOffset(9);

        ti->PulserRate = triginfo->GetPulserRate();
        ti->ControlRegister = triginfo->GetMTC_CSR();
        ti->reg_LockoutWidth = triginfo->GetLockoutWidth();
        ti->reg_Prescale = triginfo->GetPrescaleFreq();
        ti->GTID = triginfo->GetEventID();

        return ti;
    }

    EpedRecord* pack::eped(RAT::DS::EPEDInfo* const epedinfo) {
        EpedRecord* er = new EpedRecord;

        er->ped_width = epedinfo->GetQPedWidth();
        er->ped_delay_coarse = epedinfo->GetGTDelayCoarse();
        er->ped_delay_fine = epedinfo->GetGTDelayFine();
        er->qinj_dacsetting = epedinfo->GetQPedAmp();
        er->halfCrateID = epedinfo->GetPatternID();
        er->CalibrationType = epedinfo->GetCalType();
        er->GTID = epedinfo->GetEventID();
        er->Flag = 0;

        return er;
    }

}  // namespace ratzdab

