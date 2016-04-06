#!/usr/bin/env python
# Author P G Jones - 12/03/2012 <p.g.jones@qmul.ac.uk>
# Modified J R Wilson - 5/10/2015 <j.r.wilson@qmul.ac.uk>
# This script converts the Noel csv file to the PMTINFO format
# Now includes calculated Neck positions and mapping of Low Gain to physical PMTs via LCN
# There are now 5 tubes of type 0x13 which are normal tubes but with no petals - treat as normal for now.
import optparse
import sys
import csv
import yaml # Needs installing
import numpy
from minify_json import json_minify # In this directory

parser = optparse.OptionParser(usage = "./ConvertNoelToPMTINFO.py Path-to-NoelCSV PANEL_INFO", version="%prog 1.0")
(options, args) = parser.parse_args()
if len(args) != 2:
    parser.print_help()
    sys.exit(0)

def noel_type_to_rat_type(type_):
    """ Convert the noel type into a rat type for the tube."""
    if type_ == '0x00':
        return 10 # Spare??
    elif type_ == '0x01':
        # PMT is active mask explains 0x03, 0x09, 0x21, 0x41 and 0x81
        print type_
        raise
    elif type_ == '0x02' or type_ == '0x03' or type_ == '0x13':
        return 1 # Normal
    elif type_ == '0x08' or type_ == '0x09':
        return 5 # Neck
    elif type_ == '0x10':
        return 6 # FECD
    elif type_ == '0x20' or type_ == '0x21':
        return 3 # Low Gain
    elif type_ == '0x40' or type_ == '0x41':
        return 2 # OWL
    elif type_ == '0x80' or type_ == '0x81':
        return 4 # BUTT
    else:
        print type_
        #raise # Error?

def noel_type_to_petal_status(type_):
    """ Return the petal status for this type of tube."""
    if type_ == '0x00':
        return 0 # Spare, no petals
    elif type_ == '0x01':
        # PMT is active mask explains 0x03, 0x09, 0x21, 0x41 and 0x81
        print type_
        raise
    elif type_ == '0x02' or type_ == '0x03':
        return 1 # normal tube, normal petals
    elif type_ == '0x13':
        return 0 # Balck = no petals - special type of normal tube
    elif type_ == '0x08' or type_ == '0x09':
        return 0 # Neck, no concentrators
    elif type_ == '0x10':
        return 0 # FECD
    elif type_ == '0x20' or type_ == '0x21':
        return 0 # Low Gain
    elif type_ == '0x40' or type_ == '0x41':
        return 0 # OWL
    elif type_ == '0x80' or type_ == '0x81':
        return 0 # BUTT
    else:
        print type_

def get_panel_dir(panel_num, panel_info):
    """ Return the panel direction."""
    for u, v, w, number in zip(panel_info["u"], panel_info["v"], panel_info["w"], panel_info["panel_number"]):
        if number == panel_num:
            return numpy.array([u, v, w])
    raise # Not found the panel

def is_physical(type_):
    # Don't build BUTTS at the moment, just normal, OWL and Neck
    if(type_ == 1):
        return 1
    if(type_ == 5):
        return 1
    if(type_ == 2):
        return 1
    else:
        return 0

def neck_pos_dir(num_):
    pos_dir_ = numpy.array([-99999.0,-99999.0,-99999.0,-9999.0,-9999.0,-9999.0])
    # These are calculated based on UI drawings
    # https://www.snolab.ca/snoplus/private/DocDB/0003/000323/004/XDE1216D_October%2019th%20Revision.pdf
    # convert from inches to mm *25.4
    # Check units - have increase by order of mag as think in cm not mm (need to be given in mm in detector units)
    if(num_ == 0):
        pos_dir_ = numpy.array([131., 524.,14340.1,0,0,-1])
    elif(num_ == 1):
        pos_dir_ = numpy.array([-364.,32.,14340.1,0,0,-1])
    elif(num_ == 2):
        pos_dir_ = numpy.array([356.,0.,14340.1,0,0,-1])
    elif(num_ == 3):
        pos_dir_ = numpy.array([298.,-396.,14340.1,0,0,-1])
    # Only expect 4 neck tubes
    return pos_dir_



with open(args[1], "r") as panel_info_file:
    panel_data = yaml.load(json_minify(panel_info_file.read(), False))

f = open(args[0], "rU")
noel_file = csv.reader(f)
# Add dictionary that will map PMT location to a list of PMTs at that location
mapping = {}
# Make the map first
noel_file.next() # Ignore the first line
for pmt in noel_file:
    # location is pmt[13]
    if pmt[13] not in mapping:
        mapping[pmt[13]] = []
    # Add whatever descriptor here that tells you e.g. LCN and pmt type
    # Here I've added a tuple with ccc and pmt type
    mapping[pmt[13]].append((pmt[0], pmt[1], pmt[2], noel_type_to_rat_type(pmt[9])))
# Go back to start again
f.seek(0)


noel_file = csv.reader(open(args[0], "rU"))
new_data = {}
new_data["x"] = [-99999.0]
new_data["y"] = [-99999.0]
new_data["z"] = [-99999.0]
new_data["u"] = [-9999.0]
new_data["v"] = [-9999.0]
new_data["w"] = [-9999.0]
new_data["panelnumber"] = [-1]
new_data["pmt_type"] = [10]
new_data["linked_lcn"] = [-9999]
new_data["petal_status"] = [-9999]
#new_data["is_physical"] = [0]  # Decide this is redundant to output
#new_data["pmtid"] = []
noel_file.next() # Ignore the first line
neck_num = 0
for pmt in noel_file:
    crate = pmt[0]
    slot = pmt[1]
    channel = pmt[2]
    panel_number = int(pmt[13][1:4])
    if panel_number == 0:
        panel_number = -1
    dir_ = numpy.array([-9999.0, -9999.0, -9999.0])
    pos_ = numpy.array([-99999.0,-99999.0,-99999.0])
    is_physical_ = is_physical(noel_type_to_rat_type(pmt[9]))
    thelcn_ = -9999
    if is_physical_ == 1:
        pos_ = numpy.array([float(pmt[10]) * 10.0,float(pmt[11]) * 10.0,float(pmt[12]) * 10.0])
        if noel_type_to_rat_type(pmt[9]) == 1: # Normal tube direction comes from panel info
            dir_ = -get_panel_dir(panel_number, panel_data)
        elif noel_type_to_rat_type(pmt[9]) == 2:
            # OWLS point outwards
            dir_ = numpy.array([float(pmt[10]), float(pmt[11]), float(pmt[12])])
            dir_ = -dir_
            dir_ = dir_ / numpy.linalg.norm(dir_)
        elif noel_type_to_rat_type(pmt[9]) == 5:
            # NECK PMTs - need to use values entered in method above from this file
            all = neck_pos_dir(neck_num)
            pos_ = numpy.array([all[0], all[1], all[2]])
            dir_ = numpy.array([all[3], all[4], all[5]])
            neck_num =neck_num+1
            print crate, slot, channel, pos_, dir_, neck_num
    else:
        # Not physical
        current_lcn = int(pmt[0])*16*32+int(pmt[1])*32+int(pmt[2])
        if noel_type_to_rat_type(pmt[9]) == 3:
            # Low gain tubes - find matching lcn channel
            if pmt[13] in mapping.keys():
                if len(mapping[pmt[13]]) == 2:
                    # Now access the two values - the other gives the lcn we want
                    first = int(mapping[pmt[13]][0][0])*16*32+int(mapping[pmt[13]][0][1])*32+int(mapping[pmt[13]][0][2])
                    second = int(mapping[pmt[13]][1][0])*16*32+int(mapping[pmt[13]][1][1])*32+int(mapping[pmt[13]][1][2])
                    if(current_lcn == first):
                        thelcn_ = second
                    elif(current_lcn == second):
                        thelcn_ = first
                    #print pmt[13], len(mapping[pmt[13]]), mapping[pmt[13]], current_lcn, first, second, thelcn_
    if numpy.isnan(numpy.min(dir_)): # Happens if position in Noel data is 0, 0, 0
        dir_ = numpy.array([-9999.0, -9999.0, -9999.0])
    if(noel_type_to_rat_type(pmt[9]) > -1):
        new_data["panelnumber"].append(panel_number)
        new_data["pmt_type"].append(noel_type_to_rat_type(pmt[9]))
        new_data["petal_status"].append(noel_type_to_petal_status(pmt[9]))
#        new_data["is_physical"].append(is_physical_)
        new_data["x"].append(float(pos_[0])) # Convert cm to mm
        new_data["y"].append(float(pos_[1]))
        new_data["z"].append(float(pos_[2]))
        new_data["u"].append(float(dir_[0]))
        new_data["v"].append(float(dir_[1]))
        new_data["w"].append(float(dir_[2]))
        new_data["linked_lcn"].append(thelcn_)

# Now have a complete dict, write to a file
panelInfoFile = open("PMTINFO.ratdb", "w")
infoText = """{
type: \"PMTINFO\",
version: 1,
index: \"\",
run_range: [0, 0],
pass: 0,
production: false,
timestamp: \"\",
comment: \"\",
"""
for key,value in new_data.iteritems():
    infoText += key+": "+str(value)+","
infoText += """
}
"""
panelInfoFile.write(infoText)
panelInfoFile.close()
