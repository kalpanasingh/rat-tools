#!/usr/bin/env python
"""orca2run.py
This is a script to create and upload the
RUN file for the specified
run to the specified ratdb.

Author: Freija Descamps
         <fbdescamps@lbl.gov>
"""

import argparse
import sys
import subprocess
import tempfile
import os
import runtools

# Check if the rat environment is set
if "RATROOT" not in os.environ:
    print "orca2run: please set RATROOT environment variable"
    sys.exit()

def file_check(filename):
    """Function to check a ratdb file
    :param: The name of the temporary file (string).
    :returns: Nothing so far.
    """
    # First make sure it is not empty
    if os.path.getsize(filename) == 0:
        raise RuntimeError("File size is zero")
    # Second, check to make sure it is all ASCII
    # Do this by reading in the lines of the file
    # and try to decode as ascii
    with open(filename, 'r') as f:
        for line in f:
            line.decode('ascii')
    # Other checks can be added here


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number",
                        type=int, required=True)
    parser.add_argument('-c', dest='orcadb_server',
                        help='URL to CouchDB orca server',
                        default='couch.snopl.us')
    parser.add_argument("-u", dest="orcadb_username",
                        help="ORCADB Username",
                        type=str, required=True)
    parser.add_argument("-p", dest="orcadb_password",
                        help="ORCADB Password",
                        type=str, required=True)
    parser.add_argument('-s', dest='ratdb_server',
                        help='URL to CouchDB ratdb server',
                        default='http://localhost:5984/')
    parser.add_argument('-d', dest='ratdb_name',
                        help='Name of ratdb database on server',
                        default='ratdb')
    args = parser.parse_args()
    # Get the run information using the CHStools functions
    try:
        data = runtools.get_run_document_from_db(args.runnumber,
                                                 args.orcadb_server,
                                                 args.orcadb_username,
                                                 args.orcadb_password)
    # The following is too general. Meh.
    except Exception:
        print ("orca2run run {}: problem retrieving the ORCA configuration "
               "info").format(args.runnumber)
        return 1
    # Create the temporary files to hold the RUN.ratdb content
    with tempfile.NamedTemporaryFile() as runtempf:
        # Write the RUN.ratdb table to the temporary file
        runtools.write_run_document_to_file(args.runnumber, data,
                                            runtempf.name)
        runtempf.flush()

        # Do some checks on this file to make sure it can be uploaded
        try:
            file_check(runtempf.name)
        except RuntimeError, e:
            print "orca2run run {}: {}".format(args.runnumber, e)
            return 2
        except UnicodeDecodeError:
            print ("orca2run run {}: non-ASCII characters present "
                   "in file").format(args.runnumber)
            return 3
        try:
            # Run the command to upload the table to the specified
            # ratdb location
            command = ["ratdb", "upload", "-s", args.ratdb_server, "-d",
                       args.ratdb_name, runtempf.name]
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print ("orca2run run {}: there was a problem uploading "
                   "the file").format(args.runnumber)
            return 4
    return 0  # Success!


if __name__ == '__main__':
    print sys.exit(main())
