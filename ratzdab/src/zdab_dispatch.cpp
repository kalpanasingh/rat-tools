#include <zdab_convert.hpp>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <zdab_dispatch.hpp>
#include <Record_Info.h>
#include <dispatch.h>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/TRIGInfo.hh>
#include <RAT/DS/EPEDInfo.hh>
#include <RAT/DS/AVStat.hh>
#include <RAT/DS/ManipStat.hh>

namespace ratzdab {

    dispatch::dispatch(std::string _hostname, std::string _records) {
        int rc = init_disp_link(_hostname.c_str(), _records.c_str());

        if (rc >= 0) {
            send_me_always();
            my_id("QDISPATCH");
        }
        else {
            throw disp_conn_error;
        }
    }

    dispatch::~dispatch() {
        drop_connection();
    }

    TObject* dispatch::next(bool block) {
        // get data with recv
        char data[BUFFER_SIZE];
        std::string tag;
        size_t len = recv(&tag, static_cast<void*>(&data), block);

        if (!block && len == 0) {
            return static_cast<TObject*>(NULL);
        }

        // determine record type
        swap_int32(data, 3);
        aGenericRecordHeader* header = reinterpret_cast<aGenericRecordHeader*>(data);
        uint32_t id = header->RecordID;
        swap_int32(data, 3);

        swap_int32(data, len/4);
        char* o = data + sizeof(aGenericRecordHeader);

        if (id == PMT_RECORD) {
            return dynamic_cast<TObject*>(unpack::event(reinterpret_cast<PmtEventRecord*>(o)));
        }
        else if (id == RUN_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aRunRecord))
            return dynamic_cast<TObject*>(unpack::rhdr(reinterpret_cast<RunRecord*>(o)));
        }
        else if (id == TRIG_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return dynamic_cast<TObject*>(unpack::trig(reinterpret_cast<TriggerInfo*>(o)));
        }
        else if (id == EPED_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return dynamic_cast<TObject*>(unpack::eped(reinterpret_cast<EpedRecord*>(o)));
        }
        else if (id == CAST_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return dynamic_cast<TObject*>(unpack::cast(reinterpret_cast<ManipStatus*>(o)));
        }
        else if (id == CAAC_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return dynamic_cast<TObject*>(unpack::caac(reinterpret_cast<AVStatus*>(o)));
        }
        else {
            throw record_unknown;
        }

        throw record_unknown;
    }

    size_t dispatch::recv(std::string* tag, void* data, bool block) {
        int rc;
        int nbytes;
        char dtag[TAGSIZE + 1];
        memset(&dtag, 0, TAGSIZE+1);

        if (block) {
            rc = wait_head(dtag, &nbytes);
        }
        else {
            rc = check_head(dtag, &nbytes);
            if (!rc) {
                return 0;
            }
        }

        if (rc > 0) {
            if (nbytes < BUFFER_SIZE) {
                rc = get_data(data, nbytes);
            }
            else {
                throw insufficient_buffer;
            }
        }

        *tag = std::string(dtag);

        return (size_t) nbytes;
    }

    void swap_int32(char* data, size_t n) {
#ifdef SWAP_BYTES
        char ctemp;
        char* cptr;
        for (size_t i=0; i<n; i++) {
            cptr = data + 4 * i;

            ctemp = *cptr;
            *cptr = *(cptr + 3);
            *(cptr + 3) = ctemp;

            ctemp = *(cptr + 1);
            *(cptr + 1) = *(cptr + 2);
            *(cptr + 2) = ctemp;
        }
#endif
    }

}  // namespace ratzdab

