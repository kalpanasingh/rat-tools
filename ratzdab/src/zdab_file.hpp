#ifndef __ZDAB_FILE__
#define __ZDAB_FILE__

#ifndef VERBOSE
#define VERBOSE false
#endif

#include <zdab_convert.hpp>
#include <stdio.h>
#include <exception>
#include <string>

class TObject;
class PZdabFile;
class nZDAB;

namespace ratzdab {

    /** A ZDAB file */
    class zdabfile {
        public:
            /** Load a ZDAB file.
             * Throws a ratzdab::zdabfile::file_read_error if an error is
             * encountered.
             */
            zdabfile(std::string filename);

            /** Close the ZDAB file */
            virtual ~zdabfile();

            /** Get the next record in the file as a ROOT object */
            TObject* next();

            /** Exception thrown if there are problems reading the file */
            class zdab_file_read_error : public std::exception {
                virtual const char* what() const throw() {
                    return "Error occurred reading ZDAB file.";
                }
            } zfileex;

        protected:
            /** Convert a ZDAB record of any type */
            TObject* convert(nZDAB* const z);

            FILE* f;
            PZdabFile* p;
    };

}  // namespace ratzdab

#endif  // __ZDAB_FILE__

