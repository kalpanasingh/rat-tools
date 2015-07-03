#!/usr/bin/env python
"""CreateDQLL.py
This code create the DQ LL ratdb table for a given run.
Work in progress:
- does not read the XL3 error and screwed messages (from run Log files)
- does not read the slow control database yet
- does not read the PIE database yet

Author: Gersende Prior
        <gersende@lip.pt>

Inspired by CHSTools/ code from F. Descamps
"""

import argparse
import sys
import dataqualitytools

# Parse the ORCA run and configuration documents
# Write DQ LL values in a data file

import array
import json
import dateutil
import pytz
import datetime

from dateutil import parser
from pprint import pprint
from math import trunc

# Reading out the run that we want to process and db information
if __name__ == "__main__":

    # Crate information
    numberofcrates = 19
    hv_status_a = array.array('i',(i for i in range(0,numberofcrates)))

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number", type=int, required=True)
    parser.add_argument("-u", dest="db_username", help="[%s] Username" % dataqualitytools.db_server, type=str, required=True)
    parser.add_argument("-p", dest="db_password", help="[%s] Password" % dataqualitytools.db_server, type=str, required=True)
    
    args = parser.parse_args()
    if args.runnumber == "0":
        print "Please supply a runnumber using \'-n\'"
    if args.runnumber < 8270:
        sys.stderr.write("Please supply a runnumber larger than 8269 (December 2014 dark running)\n")
        sys.exit(1)
    else:
        print "Preparing DQ LL info for run " + str(args.runnumber)

        # Create the DQ LL info database file
        filename = "run_{0}_dqll.json".format(args.runnumber)
        
        dbtable = open(filename,'w')
        
        dataqualitytools.write_db_header(dbtable,args.runnumber)

        
        # Accessing the run document
        rundata = dataqualitytools.get_run_document_from_db(args.runnumber, args.db_username, args.db_password)
        
        timecheck = dataqualitytools.write_db_times(dbtable,rundata)

        if timecheck == 'false':
            sys.stderr.write("Failed while trying to retrieve run start/end time\n")
            sys.exit(1)
            
        # Accessing the configuration document
        configurationdata = dataqualitytools.get_configuration_document_from_db(args.runnumber, args.db_username, args.db_password)
        
        hv_status_a = dataqualitytools.create_hv_status_a(configurationdata)

        # Seems to be willing to dump the [u''..] format if trying to pass the array not index by index
        crate_hv_status_a = "\"crate_hv_status_a\": [{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}],\n".format(hv_status_a[0],
                                                                                                                                                     hv_status_a[1],
                                                                                                                                                     hv_status_a[2],
                                                                                                                                                     hv_status_a[3],
                                                                                                                                                     hv_status_a[4],
                                                                                                                                                     hv_status_a[5],
                                                                                                                                                     hv_status_a[6],
                                                                                                                                                     hv_status_a[7],
                                                                                                                                                     hv_status_a[8],
                                                                                                                                                     hv_status_a[9],
                                                                                                                                                     hv_status_a[10],
                                                                                                                                                     hv_status_a[11],
                                                                                                                                                     hv_status_a[12],
                                                                                                                                                     hv_status_a[13],
                                                                                                                                                     hv_status_a[14],
                                                                                                                                                     hv_status_a[15],
                                                                                                                                                     hv_status_a[16],
                                                                                                                                                     hv_status_a[17],
                                                                                                                                                     hv_status_a[18])

        dbtable.write(crate_hv_status_a)

        hv_status_b = dataqualitytools.create_hv_status_b(configurationdata)

        crate_16_hv_status_b = "\"crate_16_hv_status_b\": {0},\n".format(hv_status_b)

        dbtable.write(crate_16_hv_status_b)

        dbtable.write("\n")

        hv_nominal_a = dataqualitytools.create_hv_nominal_a(configurationdata)

        crate_hv_nominal_a = "\"crate_hv_nominal_a\": {0},\n".format(hv_nominal_a)
        
        dbtable.write(crate_hv_nominal_a)

        hv_nominal_b = dataqualitytools.create_hv_nominal_b(configurationdata)

        crate_16_hv_nominal_b = "\"crate_16_hv_nominal_b\": {0},\n".format(hv_nominal_b)

        dbtable.write(crate_16_hv_nominal_b)

        dbtable.write("\n")

        hv_read_value_a = dataqualitytools.create_hv_read_value_a(configurationdata)

        crate_hv_read_value_a = "\"crate_hv_read_value_a\": {0},\n".format(hv_read_value_a)

        dbtable.write(crate_hv_read_value_a)

        hv_read_value_b = dataqualitytools.create_hv_read_value_b(configurationdata)

        crate_16_hv_read_value_b = "\"crate_16_hv_read_value_b\": {0},\n".format(hv_read_value_b)

        dbtable.write(crate_16_hv_read_value_b)

        dbtable.write("\n")

        current_read_value_a = dataqualitytools.create_current_read_value_a(configurationdata)

        crate_current_read_value_a = "\"crate_current_read_value_a\": {0},\n".format(current_read_value_a)

        dbtable.write(crate_current_read_value_a)

        current_read_value_b = dataqualitytools.create_current_read_value_b(configurationdata)

        crate_16_current_read_value_b = "\"crate_16_current_read_value_b\": {0},\n".format(current_read_value_b)

        dbtable.write(crate_16_current_read_value_b)

        dbtable.write("\n")
        
        # Should read later from Run/Status logs Xl3s ErrorPackets
        cmdrejected = [0 for i in range(19)]
        transfererror = [0 for i in range(19)]
        xl3dataavailunknown = [0 for i in range(19)]
        fecbundlereaderror = [0 for i in range(19)]
        fecbundleresyncherror = [0 for i in range(19)]
        fecmemlevelunknown = [0 for i in range(19)]
        
        # XL3 ErrorPacket
        cmd_rejected = "\"xl3_error_packet_cmd_rejected\": {0},\n".format(cmdrejected)
        
        dbtable.write(cmd_rejected)

        transfer_error = "\"xl3_error_packet_transfer_error\": {0},\n".format(transfererror)
        
        dbtable.write(transfer_error)

        xl3_data_avail_unknown = "\"xl3_error_packet_xl3_data_avail_unknown\": {0},\n".format(xl3dataavailunknown)
       
        dbtable.write(xl3_data_avail_unknown)

        fec_bundle_read_error = "\"xl3_error_packet_fec_bundle_read_error\": {0},\n".format(fecbundlereaderror)
        
        dbtable.write(fec_bundle_read_error)

        fec_bundle_resynch_error = "\"xl3_error_packet_fec_bundle_resynch_error\": {0},\n".format(fecbundleresyncherror)

        dbtable.write(fec_bundle_resynch_error)

        fec_mem_level_unknown = "\"xl3_error_packet_fec_mem_level_unknown\": {0},\n".format(fecmemlevelunknown)
       
        dbtable.write(fec_mem_level_unknown)
        
        dbtable.write("\n")

        # Should read later from Run/Status logs Xl3s Screwed packets
        fecscrewed = [0 for i in range(19)]

        fec_screwed = "\"xl3_screwed_packet_fec_screwed\": {0}\n".format(fecscrewed)
       
        dbtable.write(fec_screwed)

        dataqualitytools.write_db_footer(dbtable,args.runnumber)

        dbtable.close()




