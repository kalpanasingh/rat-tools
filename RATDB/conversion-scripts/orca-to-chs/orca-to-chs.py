#!/usr/bin/env python
"""orca-to-chs.py
This is a script to run near-line,
it will create and upload the
PMT_DQXX file for the specified
run to the specified ratdb.

Author: Freija Descamps
         <fbdescamps@lbl.gov>
"""

import getpass
import argparse
import httplib
import json
import sys
import subprocess
import tempfile
import commands
import couchdb
import os
import settings

# The following is needed to access the available chstools in rat-tools
# the location should currently be defined in settings.py
# This is pretty ugly
sys.path.insert(0, settings.RAT_TOOLS + 'CHStools/')
import chstools


def file_check(filename):
    # First make sure it is not empty
    b = os.path.getsize(filename)
    if b == 0:
        raise Exception("File size is zero")
    # Other checks can be added here


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number",
                        type=int, required=True)
    parser.add_argument('-c', '--orcadb_server', dest='orcadb_server',
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
        data = chstools.get_run_configuration_from_db(args.runnumber, args.orcadb_server,
                                                      args.orcadb_username,
                                                      args.orcadb_password)
        dqcr, dqch, dqid = chstools.create_dqcr_dqch_dqid(args.runnumber,
                                                          data)
    except:
        print "orca-to-chs: problem retrieving the ORCA configuration info for run " + str(args.runnumber)
        return
    # Create a temporary file to hold the PMT_DQXX.ratdb content
    tempf = tempfile.NamedTemporaryFile(delete=False)
    # Write the PMT_DQXX table to the temporary file
    chstools.dqxx_write_to_file(dqcr, dqch, dqid, args.runnumber, tempf.name)
    tempf.close()
    # Do some checks on this file to make sure it can be uploaded
    try:
        file_check(tempf.name)
    except Exception, e:
        print "orca-to-chs run " + str(args.runnumber) + ": %s" % e 
        return
    try:
        # Run the command to upload the table to the specified ratdb location
        command = "ratdb append -s %s -d %s %s %i " % (args.ratdb_server,
                                                       args.ratdb_name,
                                                       tempf.name, 100)
        os.system(command)
    except:
        print "orca-to-chs: there was a problem uploading the file for run " + str(args.runnumber)
    # Get rid of the temporary file
    os.unlink(tempf.name)

if __name__ == '__main__':
    main()
