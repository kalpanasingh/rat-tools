#include <zdab_file.hpp>
#include <stdio.h>
#include <string>
#include <PZdabFile.h>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/TRIGInfo.hh>
#include <RAT/DS/EPEDInfo.hh>
#include <RAT/DS/AVStat.hh>
#include <RAT/DS/ManipStat.hh>

namespace ratzdab {

    zdabfile::zdabfile(std::string filename) {
        f = fopen(filename.c_str(), "rb");
        if (!f) {
            throw zfileex;
        }

        p = new PZdabFile();
        if (p->Init(f) < 0) {
            throw zfileex;
        }
    }

    zdabfile::~zdabfile() {
        delete p;
        fclose(f);
    }

    TObject* zdabfile::next() {
        nZDAB* z = p->NextRecord();

        if (!z) {
            return static_cast<TObject*>(NULL);
        }

        return convert(z);
    }

    TObject* zdabfile::convert(nZDAB* const z) {
        if (z->bank_name == ZDAB_RECORD) {
            PmtEventRecord* o = reinterpret_cast<PmtEventRecord*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::event(o));
        }
        else if (z->bank_name == RHDR_RECORD) {
            RunRecord* o = reinterpret_cast<RunRecord*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::rhdr(o));
        }
        else if (z->bank_name == TRIG_RECORD) {
            TriggerInfo* o = reinterpret_cast<TriggerInfo*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::trig(o));
        }
        else if (z->bank_name == EPED_RECORD) {
            EpedRecord* o = reinterpret_cast<EpedRecord*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::eped(o));
        }
        else if (z->bank_name == CAST_RECORD) {
            ManipStatus* o = reinterpret_cast<ManipStatus*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::cast(o));
        }
        else if (z->bank_name == CAAC_RECORD) {
            AVStatus* o = reinterpret_cast<AVStatus*>(p->GetBank(z));
            return dynamic_cast<TObject*>(unpack::caac(o));
        }

        throw record_unknown;
    }

}  // namespace ratzdab

