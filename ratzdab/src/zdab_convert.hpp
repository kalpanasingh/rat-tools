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
        RAT::DS::Root* event(PmtEventRecord* pev);
        RAT::DS::Run* rhdr(RunRecord* rhdr);
        RAT::DS::TRIGInfo* trig(TriggerInfo* trig);
        RAT::DS::EPEDInfo* eped(EpedRecord* eped);
        RAT::DS::ManipStat* cast(ManipStatus* cast);
        RAT::DS::AVStat* caac(AVStatus* caac);

        // helpers
        RAT::DS::Digitiser caen(uint32_t* caen);
        RAT::DS::PMTUnCal pmt(uint32_t* hits);
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

