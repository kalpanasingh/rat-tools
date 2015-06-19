#!/usr/bin/env python
"""runinfo.py
This code will output the status of a run
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
                        help="Run number",
                        type=int,
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
    parser.add_argument("-o", "--output", action="store_true",
                        help="Output the SNO-style dqxx file")
    args = parser.parse_args()
    if args.runnumber == "0":
        print "Please supply a runnumber using \'-n\'"
    if args.runnumber < 8300:
        sys.stderr.write("Please supply a runnumber larger than 8300 (December 2014 dark running)\n")
        sys.exit(1)
    else:
        print "Assembling DQXX info for run " + str(args.runnumber)
        data = chstools.get_run_configuration_from_db(args.runnumber,
                                                      args.orcadb_server,
                                                      args.orcadb_username,
                                                      args.orcadb_password)
        dqcr, dqch, dqid = chstools.create_dqcr_dqch_dqid(args.runnumber, data)
        dqxx = chstools.form_dqxx_word(dqcr, dqch)
        number_offline_tubes = chstools.count_offline_tubes(dqxx)
        print ""
        print " ++++++++++ Run " + str(args.runnumber) + " ++++++++++ "
        print " Number of offline tubes is " + str(number_offline_tubes)
        print " Tube status summary: "
        for bit in chstools.DQXX_DEFINITION:
            if bit[2]:
                print "   " + str(bit[1]).rjust(10) + "  ->  " + str(chstools.count_bits(dqxx, bit[0]))
            else:
                print "   " + str(bit[1]).rjust(10) + "  ->  N/A"
        print ""
        if not args.output:
            print "Not outputting DQXX file, have a nice day!!"
            print "You can enable the DQXX file output by specifying \'-o\'."
        else:
            outfilename = "PMT_DQXX_%i.ratdb" % args.runnumber
            chstools.dqxx_write_to_file(dqcr, dqch, dqid, args.runnumber, outfilename)
            print "DQXX file written, have a nice day!!"
