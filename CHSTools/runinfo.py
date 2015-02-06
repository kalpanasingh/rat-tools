#!/usr/bin/env python
#######################
#
# runinfo.py
# This code will output the status of a run
# for the specified runnumber. It is work in progress
# as many DQXX definitions are not yet available in
# the ORCA configuration file.
#
# Author: Freija Descamps
#         <fbdescamps@lbl.gov>
#
#######################

import getpass
import argparse
import httplib
import json
import sys
import chstools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number", default="0")
    args = parser.parse_args()
    if args.runnumber == "0":
        print "Please supply a runnumber using \'-n\'"
    if int(args.runnumber) < 8300:
        print "Please supply a runnumber larger than 8300 (December 2014 dark running)"
    else:
        print "Assembling DQXX info for run " + args.runnumber
        dqcr, dqch, dqid = chstools.create_dqxx(args.runnumber)
        dqxx = chstools.form_dqxx(dqcr, dqch)
        number_offline_tubes = chstools.count_offline_channels(dqxx)
        print " ++++++++ Run " + args.runnumber + " ++++++++ "
        print " Number of offline tubes is " + str(number_offline_tubes)
        print " Tube status summary: "
        for bit in chstools.DQXX_DEFINITION:
            if bit[2] == '1':
                print "   " + bit[1] + " -> " + str(chstools.count_bits(dqxx, int(bit[0])))
            else:
                print "   " + bit[1] + " -> not yet implemented"
        print_dqxx = raw_input("Print out SNO-style DQXX file? [Y,n] : ")
        if print_dqxx == 'n':
            print 'Not printing DQXX file, have a nice day!!'
        else:
            chstools.dqxx_print(dqcr, dqch, dqid, args.runnumber)    