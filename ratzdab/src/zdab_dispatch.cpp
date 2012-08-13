#include <string>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <Record_Info.h>
#include <dispatch.h>

#include <zdab_convert.hpp>
#include <zdab_dispatch.hpp>

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
        size_t len = recv(tag, (void*)&data, block);

        if (!block && len == 0) {
            return NULL;
        }

        // determine record type
        swap_int32(data, 3);
        aGenericRecordHeader* header = (aGenericRecordHeader*) data;
        uint32_t id = header->RecordID;
        swap_int32(data, 3);

        swap_int32(data, len/4);
        char* o = data + sizeof(aGenericRecordHeader);

        if (id == PMT_RECORD) {
            return (TObject*) unpack::event((PmtEventRecord*) o);
        }
        else if (id == RUN_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aRunRecord))
            return (TObject*) unpack::rhdr((RunRecord*) o);
        }
        else if (id == TRIG_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return (TObject*) unpack::trig((TriggerInfo*) o);
        }
        else if (id == EPED_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return (TObject*) unpack::eped((EpedRecord*) o);
        }
        else if (id == CAST_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return (TObject*) unpack::cast((ManipStatus*) o);
        }
        else if (id == CAAC_RECORD) {
            // fixme check (len < sizeof(aGenericRecordHeader) + sizeof(aTriggerInfo))
            return (TObject*) unpack::caac((AVStatus*) o);
        }
        else {
            throw record_unknown;
        }

        throw record_unknown;
    }

    size_t dispatch::recv(std::string& tag, void* data, bool block) {
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

        tag = std::string(dtag);

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

} // namespace ratzdab

