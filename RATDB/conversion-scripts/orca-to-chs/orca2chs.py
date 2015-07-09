#!/usr/bin/env python
"""orca2chs.py
This is a script to run near-line,
it will create and upload the
PMT_DQXX file for the specified
run to the specified ratdb.

Author: Freija Descamps
         <fbdescamps@lbl.gov>
"""

import argparse
import sys
import subprocess
import tempfile
import os

# The following is needed to access the available chstools in rat-tools
if "RATTOOLS" in os.environ:
    sys.path.insert(0, os.path.join(os.environ.get("RATTOOLS"), 'CHSTools'))
    import chstools
else:
    print "orca2chs: please set RATTOOLS environment variable"
    sys.exit()


def file_check(filename):
    """Function to check the PMT_DQXX info
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
    # Get the DQXX information using the CHStools functions
    try:
        data = chstools.get_run_configuration_from_db(args.runnumber,
                                                      args.orcadb_server,
                                                      args.orcadb_username,
                                                      args.orcadb_password)
        dqcr, dqch, dqid = chstools.create_dqcr_dqch_dqid(args.runnumber,
                                                          data)
    # The following is too general. Meh.
    except Exception:
        print ("orca2chs run {}: problem retrieving the ORCA configuration "
               "info").format(args.runnumber)
        return 1
    # Create a temporary file to hold the PMT_DQXX.ratdb content
    with tempfile.NamedTemporaryFile() as tempf:
        # Write the PMT_DQXX table to the temporary file
        chstools.dqxx_write_to_file(dqcr, dqch, dqid,
                                    args.runnumber, tempf.name)
        tempf.flush()
        # Do some checks on this file to make sure it can be uploaded
        try:
            file_check(tempf.name)
        except RuntimeError, e:
            print "orca2chs run {}: {}".format(args.runnumber, e)
            return 2
        except UnicodeDecodeError:
            print ("orca2chs run {}: non-ASCII characters present "
                   "in file").format(args.runnumber)
            return 3
        try:
            # Run the command to upload the table to the specified
            # ratdb location
            command = ["ratdb", "upload", "-s", args.ratdb_server, "-d",
                       args.ratdb_name, tempf.name]
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print ("orca2chs run {}: there was a problem uploading "
                   "the file").format(args.runnumber)
            return 4
    return 0  # Success!


if __name__ == '__main__':
    print sys.exit(main())
