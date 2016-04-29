#!/usr/bin/env python
"""dqll.py
This is a script to create and upload the DQLL file for the specified run to the central ratdb.
Syntax adapted from DataQualityTools script to match nearline scripts requirements

Author: Gersende Prior
        <gersende@lip.pt>
"""

import argparse
import sys
#import subprocess
import tempfile
import os
import dqlltools

import array
import dateutil

from pprint import pprint
from dateutil import parser

# Check if the rat environment is set
#if "RATROOT" not in os.environ:
#    print "dqll: please set RATROOT environment variable"
#    sys.exit()

def main():
    # Parse the arguments from call_dqll nearline client script
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number", type=int, required=True)
    parser.add_argument("-i", dest="runtype", help="Run type", type=int, required=True)
    parser.add_argument('-c', dest='orcadb_server', help='URL to CouchDB orca server', default='couch.snopl.us')
    parser.add_argument("-u", dest="orcadb_username", help="ORCADB Username", type=str, required=True)
    parser.add_argument("-p", dest="orcadb_password", help="ORCADB Password", type=str, required=True)
    #parser.add_argument('-s', dest='ratdb_server', help='URL to CouchDB ratdb server', default='http://localhost:5984/')
    #parser.add_argument('-d', dest='ratdb_name', help='Name of ratdb database on server', default='ratdb')
    args = parser.parse_args()

    # Print runtype
    print "Run type is {}".format(args.runtype)

    # Crate information
    numberofcrates = 19
    hv_status_a = array.array('i',(i for i in range(0,numberofcrates)))

    # Exit if no runnumber supplied
    if args.runnumber == "0":
        sys.stderr.write("Please supply a runnumber using \'-n\'")
        sys.exit(1)
    
    # Exit if runnumber is before 2014/12 dark-running
    if args.runnumber < 8270:
        sys.stderr.write("Please supply a runnumber larger than 8269 (December 2014 dark running)\n")
        sys.exit(1)
    else:
        print "Preparing DQ LL info for run " + str(args.runnumber)

        # Create the DQ LL info database file
        tablename = "run_{0}_dqll.json".format(args.runnumber)
        
        dbtable = open(tablename,'w')
        
        dqlltools.write_db_header(dbtable,args.runnumber)

        # Accessing the run document
        try:
    	    rundata = dqlltools.get_run_document_from_db(args.runnumber, args.orcadb_server, args.orcadb_username, args.orcadb_password)

        except Exception:
            print ("dqll run {}: problem retrieving the ORCA run document info").format(args.runnumber)
            return 1

        timecheck = dqlltools.write_db_times(dbtable,rundata)

        if timecheck == 'false':
            sys.stderr.write("Failed while trying to retrieve run start/end time\n")
            sys.exit(1)
            
        # Accessing the configuration document
        try:
            configurationdata = dqlltools.get_configuration_document_from_db(args.runnumber, args.orcadb_server, args.orcadb_username, args.orcadb_password)
        
        except Exception:
            print ("dqll run {}: problem retrieving the ORCA configuration document info").format(args.runnumber)
            return 1        

        hv_status_a = dqlltools.create_hv_status_a(configurationdata)

        crate_hv_status_a = "\"crate_hv_status_a\": [%s],\n" % ", ".join(hv_status_a)

        dbtable.write(crate_hv_status_a)

        hv_status_b = dqlltools.create_hv_status_b(configurationdata)

        crate_16_hv_status_b = "\"crate_16_hv_status_b\": {0},\n".format(hv_status_b)

        dbtable.write(crate_16_hv_status_b)

        dbtable.write("\n")

        hv_nominal_a = dqlltools.create_hv_nominal_a(configurationdata)

        crate_hv_nominal_a = "\"crate_hv_nominal_a\": {0},\n".format(hv_nominal_a)
        
        dbtable.write(crate_hv_nominal_a)

        hv_nominal_b = dqlltools.create_hv_nominal_b(configurationdata)

        crate_16_hv_nominal_b = "\"crate_16_hv_nominal_b\": {0},\n".format(hv_nominal_b)

        dbtable.write(crate_16_hv_nominal_b)

        dbtable.write("\n")

        hv_read_value_a = dqlltools.create_hv_read_value_a(configurationdata)

        crate_hv_read_value_a = "\"crate_hv_read_value_a\": {0},\n".format(hv_read_value_a)

        dbtable.write(crate_hv_read_value_a)

        hv_read_value_b = dqlltools.create_hv_read_value_b(configurationdata)

        crate_16_hv_read_value_b = "\"crate_16_hv_read_value_b\": {0},\n".format(hv_read_value_b)

        dbtable.write(crate_16_hv_read_value_b)

        dbtable.write("\n")

        current_read_value_a = dqlltools.create_current_read_value_a(configurationdata)

        crate_current_read_value_a = "\"crate_current_read_value_a\": {0},\n".format(current_read_value_a)

        dbtable.write(crate_current_read_value_a)

        current_read_value_b = dqlltools.create_current_read_value_b(configurationdata)

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

        dqlltools.write_db_footer(dbtable,args.runnumber)

        dbtable.close()

    # Check that the table is in JSON format and that it contains the correct number of lines
    jsonok = dqlltools.file_jsoncheck(tablename)
    if jsonok == 'false':
        sys.stderr.write("JSON file is not proper JSON or has not the correct number of lines\n")
        sys.exit(1)

    # Convert the JSON table in ratdb format
    dqlltools.json_to_ratdb(tablename)   
 
    # Upload table only if good physics or good calibration run
    # COMMENTED FOR NOW UNTIL SETTLED ON:
    # - bit 22 set to 1 for compensation coils on or off
    # - what format nearline will read exactly hex/bin/other ?         
        #try:
            # Run the command to upload the table to the 
            # central ratdb location
            # UNCOMMENT ONLY WHEN WE KNOW WHAT WE ARE DOING
            #command = ["ratdb", "upload", "-s", args.ratdb_server, "-d",
             #          args.ratdb_name, runtempf.name]
            #subprocess.check_call(command)
        #except subprocess.CalledProcessError:
         #   print ("orca2run run {}: there was a problem uploading "
          #         "the file").format(args.runnumber)
           # return 4

    return 0  # Success!


if __name__ == '__main__':
    print sys.exit(main())
