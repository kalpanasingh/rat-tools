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
    parser.add_argument("-n", dest="runnumber",
                        help="Run number", type=int,
                        required=True)
    parser.add_argument('-c', dest='orcadb_server',
                        help='URL to CouchDB orca server',
                        default='couch.snopl.us')
    parser.add_argument("-u", dest="orcadb_username",
                        help="ORCADB Username",
                        type=str, required=True)
    parser.add_argument("-p", dest="orcadb_password",
                        help="ORCADB Password",
                        type=str, required=True)

    parser.add_argument('-w', dest='mysql_server',
                        help='URL to MySQL server',
                        type=str, default=None)
    parser.add_argument('-x', dest='mysql_dbname',
                        help='Name of pmt database on MySQL server',
                        type=str, default=None)
    parser.add_argument('-y', dest='mysql_user',
                        help='Name of user MySQL server',
                        type=str, default=None)
    parser.add_argument('-z', dest='mysql_password',
                        help='Password for MySQL server',
                        type=str, default=None)

    args = parser.parse_args()
    if args.runnumber < 8300:
        sys.stderr.write('Please supply a runnumber larger than 8300 (December 2014 dark running)\n')
        sys.exit(1)
    else:
        print "Assembling DQXX info for run " + str(args.runnumber)
        data = chstools.get_run_configuration_from_db(args.runnumber,
                                                      args.orcadb_server,
                                                      args.orcadb_username,
                                                      args.orcadb_password)
        if args.mysql_user is not None\
           and args.mysql_password is not None\
           and args.mysql_server is not None\
           and args.mysql_user is not None:
            pmtdb_data = chstools.get_current_pmtdb_info(args.mysql_server,
                                                         args.mysql_user,
                                                         args.mysql_password,
                                                         args.mysql_dbname)
        else:
            pmtdb_data = None
        # Now assemble the dqcr, dqch and dqid words
        dqcr, dqch, dqid = chstools.create_dqcr_dqch_dqid(args.runnumber,
                                                          data,
                                                          pmtdb_data)
        outfilename = "PMT_DQXX_%i.ratdb" % args.runnumber
        chstools.dqxx_write_to_file(dqcr, dqch, dqid, args.runnumber, outfilename)
