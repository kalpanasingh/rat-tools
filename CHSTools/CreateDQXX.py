#!/usr/bin/env python
#######################
#
# createDQXX.py
# This code will output a PMT_DQXX ratdb file
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
        chstools.dqxx_print(dqcr, dqch, dqid, args.runnumber)