#ifndef __ZDAB_CONVERT__
#define __ZDAB_CONVERT__

#ifndef VERBOSE
#define VERBOSE false
#endif

#include <stdint.h>
#include <exception>

class TObject;

class PZdabFile;
class PmtEventRecord;
class RunRecord;
class TriggerInfo;
class EpedRecord;
class ManipStatus;
class AVStatus;

namespace RAT {
    namespace DS {
        class Root;
        class Run;
        class AVStat;
        class ManipStat;
        class TRIGInfo;
        class EPEDInfo;
        class Digitiser;
        class PMTUnCal;
    }
}

namespace ratzdab {

    /** Convert nZDAB pointers to various RAT ROOT objects */
    namespace unpack {
        RAT::DS::Root* event(PmtEventRecord* const o);
        RAT::DS::Run* rhdr(RunRecord* const o);
        RAT::DS::ManipStat* cast(ManipStatus* const o);
        RAT::DS::AVStat* caac(AVStatus* const o);

        // note: TRIGInfo::runID is not set
        RAT::DS::TRIGInfo* trig(TriggerInfo* const o);

        // note: EPEDInfo::runID is not set
        RAT::DS::EPEDInfo* eped(EpedRecord* const o);

        // helpers
        RAT::DS::Digitiser caen(uint32_t* const p);
        RAT::DS::PMTUnCal pmt(uint32_t* const p);
    }

    /** Convert RAT ROOT objects to ZDAB records */
    namespace pack {
        PmtEventRecord* event(RAT::DS::Root* o, int ev_id=0);
        RunRecord* rhdr(RAT::DS::Run* const o);
        ManipStatus* cast(RAT::DS::ManipStat* const o);
        AVStatus* caac(RAT::DS::AVStat* const o);
        TriggerInfo* trig(RAT::DS::TRIGInfo* const o);
        EpedRecord* eped(RAT::DS::EPEDInfo* const o);
    }

    /** Exception thrown if unable to handle a record */
    static class unknown_record_error : public std::exception {
        public:
            virtual const char* what() const throw() {
                return "Unable to convert unknown record type.";
            }
    } record_unknown;

}  // namespace ratzdab

#endif  // __ZDAB_CONVERT__

