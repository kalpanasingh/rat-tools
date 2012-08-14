#ifndef __ZDAB_CONVERT__
#define __ZDAB_CONVERT__

#ifndef VERBOSE
#define VERBOSE false
#endif

#include <exception>
#include <stdint.h>

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
        RAT::DS::Root* event(PmtEventRecord* o);
        RAT::DS::Run* rhdr(RunRecord* o);
        RAT::DS::ManipStat* cast(ManipStatus* o);
        RAT::DS::AVStat* caac(AVStatus* o);

        // note: TRIGInfo::runID is not set
        RAT::DS::TRIGInfo* trig(TriggerInfo* o);

        // note: EPEDInfo::runID is not set
        RAT::DS::EPEDInfo* eped(EpedRecord* o);

        // helpers
        RAT::DS::Digitiser caen(uint32_t* p);
        RAT::DS::PMTUnCal pmt(uint32_t* p);
    }

    /** Convert RAT ROOT objects to ZDAB records */
    namespace pack {
        PmtEventRecord* event(RAT::DS::Root* o, int ev_id=0);
        RunRecord* rhdr(RAT::DS::Run* o);
        ManipStatus* cast(RAT::DS::ManipStat* o);
        AVStatus* caac(RAT::DS::AVStat* o);
        TriggerInfo* trig(RAT::DS::TRIGInfo* o);
        EpedRecord* eped(RAT::DS::EPEDInfo* o);
    }

    /** Exception thrown if unable to handle a record */
    static class unknown_record_error : public std::exception {
        public:
            virtual const char* what() const throw() {
                return "Unable to convert unknown record type.";
            }
    } record_unknown;

    /** Exception thrown if unable to handle a record */
    static class missing_ratroot_error : public std::exception {
        public:
            virtual const char* what() const throw() {
                return "Unable to find RAT. Is RATROOT set?";
            }
    } no_rat;

} // namespace ratzdab

#endif

