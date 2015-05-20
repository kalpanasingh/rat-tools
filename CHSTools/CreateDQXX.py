#!/usr/bin/env python
"""createDQXX.py
This code will output a PMT_DQXX ratdb file
for the specified runnumber. It is work in progress
as many DQXX definitions are not yet available in
the ORCA configuration file.

Author: Freija Descamps
        <fbdescamps@lbl.gov>
"""

import argparse
import sys
import chstools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number", type=int, required=True)
    parser.add_argument("-u", dest="db_username", help="[%s] Username" % chstools.db_server, required=True)
    parser.add_argument("-p", dest="db_password", help="[%s] Password" % chstools.db_server, required=True)
    args = parser.parse_args()
    if args.runnumber < 8300:
        sys.stderr.write('Please supply a runnumber larger than 8300 (December 2014 dark running)\n')
        sys.exit(1)
    else:
        print "Assembling DQXX info for run " + str(args.runnumber)
        data = chstools.get_run_configuration_from_db(args.runnumber, args.db_username, args.db_password)
        dqcr, dqch, dqid = chstools.create_dqcr_dqch_dqid(args.runnumber, data)
        chstools.dqxx_write_to_file(dqcr, dqch, dqid, args.runnumber)