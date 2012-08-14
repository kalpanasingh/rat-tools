#include <stdio.h>
#include <string>

#include <PZdabFile.h>
#include <zdab_file.hpp>

class TObject;

namespace ratzdab {

    file::file(std::string filename) {
        f = fopen(filename.c_str(), "rb");
        if (!f) {
            throw zfileex;
        }

        p = new PZdabFile();
        if (p->Init(f) < 0) {
            throw zfileex;
        }
    }

    file::~file() {
        delete p;
        fclose(f);
    }

    TObject* file::next() {
        nZDAB* z = p->NextRecord();

        if (!z) {
            return NULL;
        }

        return convert(z);
    }

    TObject* file::convert(nZDAB* z) {
        if (z->bank_name == ZDAB_RECORD) {
            PmtEventRecord* o = (PmtEventRecord*) p->GetBank(z);
            return (TObject*) unpack::event(o);
        }
        else if (z->bank_name == RHDR_RECORD) {
            RunRecord* o = (RunRecord*) p->GetBank(z);
            return (TObject*) unpack::rhdr(o);
        }
        else if (z->bank_name == TRIG_RECORD) {
            TriggerInfo* o = (TriggerInfo*) p->GetBank(z);
            return (TObject*) unpack::trig(o);
        }
        else if (z->bank_name == EPED_RECORD) {
            EpedRecord* o = (EpedRecord*) p->GetBank(z);
            return (TObject*) unpack::eped(o);
        }
        else if (z->bank_name == CAST_RECORD) {
            ManipStatus* o = (ManipStatus*) p->GetBank(z);
            return (TObject*) unpack::cast(o);
        }
        else if (z->bank_name == CAAC_RECORD) {
            AVStatus* o = (AVStatus*) p->GetBank(z);
            return (TObject*) unpack::caac(o);
        }

        throw record_unknown;
    }

} // namespace ratzdab

