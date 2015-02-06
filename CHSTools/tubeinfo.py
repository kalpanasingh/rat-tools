#!/usr/bin/env python
#######################
#
# tubeinfo.py
# This code will output the status of a tube
# for the specified runnumber and lcn. It is work in progress
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
    parser.add_argument("-t", dest="lcn", help="Tube number", default="0")
    args = parser.parse_args()
    if args.runnumber == "0":
        print "Please supply a runnumber using \'-n\' and a lcn number using \'-t\'"
    if int(args.runnumber) < 8300:
        print "Please supply a runnumber larger than 8300 (December 2014 dark running)"
    if int(args.lcn) > 9728:
        print "Please supply a tube number between 0 and 9728"
    else:
        print "Assembling DQXX info for run " + args.runnumber
        dqcr, dqch, dqid = chstools.create_dqxx(args.runnumber)
        dqxx = chstools.form_dqxx(dqcr, dqch)
        print "DQXX status for tube " + args.lcn + " is: "
        for bit in chstools.DQXX_DEFINITION:
            if bit[2] == '1':
                print bit[1], chstools.checkbit(dqxx[int(args.lcn)], int(bit[0]))
        print_dqxx = raw_input("Print out SNO-style DQXX file? [Y,n] : ")
        if print_dqxx == 'n':
            print 'Not printing DQXX file, have a nice day!!'
        else:
            chstools.dqxx_print(dqcr, dqch, dqid, args.runnumber)        