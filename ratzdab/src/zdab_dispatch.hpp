#ifndef __ZDAB_DISPATCH__
#define __ZDAB_DISPATCH__

#include <string>
#include <exception>

#define BUFFER_SIZE 130000

class TObject;

namespace ratzdab {

    /** A connection to a ZDAB dispatcher */
    class dispatch {
        public:
            /** Connect to dispatch on host _hostname. _records controls which
             * record types are subscribed to.
             */
            dispatch(std::string _hostname, std::string _records="w RAWDATA w RECHDR");

            /** Close the dispatcher connection */
            virtual ~dispatch();

            /** Get the next record in the stream as a ROOT object */
            TObject* next(bool block=true);

        protected:
            /** Receive the next block of bytes from the stream */
            virtual size_t recv(std::string* tag, void* data, bool block=true);
    };

    void swap_int32(char* data, size_t n);

    static class dispatcher_connection_error : public std::exception {
        virtual const char* what() const throw() {
            return "Error connecting to dispatcher";
        }
    } disp_conn_error;

    static class insufficient_buffer_error : public std::exception {
        virtual const char* what() const throw() {
            return "Record exceeded maximum buffer size";
        }
    } insufficient_buffer;

}  // namespace ratzdab

#endif  // __ZDAB_DISPATCH__

