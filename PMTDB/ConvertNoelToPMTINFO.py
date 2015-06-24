#!/usr/bin/env python
# Author P G Jones - 12/03/2012 <p.g.jones@qmul.ac.uk>
# This script converts the Noel csv file to the PMTINFO format
import optparse
import sys
import csv
import yaml # Needs installing
import numpy
from minify_json import json_minify # In this directory

parser = optparse.OptionParser(usage = "./ProducePanelInfo.py Path-to-NoelCSV PANEL_INFO Index", version="%prog 1.0")
(options, args) = parser.parse_args()
if len(args) != 3:
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
    elif type_ == '0x02' or type_ == '0x03':
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

def get_panel_dir(panel_num, panel_info):
    """ Return the panel direction."""
    for u, v, w, number in zip(panel_info["u"], panel_info["v"], panel_info["w"], panel_info["panel_number"]):
        if number == panel_num:
            return numpy.array([u, v, w])
    raise # Not found the panel

with open(args[1], "r") as panel_info_file:
    panel_data = yaml.load(json_minify(panel_info_file.read(), False))

noel_file = csv.reader(open(args[0], "r"))

new_data = {}
new_data["x"] = [-99990.0]
new_data["y"] = [-99990.0]
new_data["z"] = [-99990.0]
new_data["u"] = [-9999.0]
new_data["v"] = [-9999.0]
new_data["w"] = [-9999.0]
new_data["panelnumber"] = [-1]
new_data["pmt_type"] = [10]
#new_data["pmtid"] = []
noel_file.next() # Ignore the first line
for pmt in noel_file:
    crate = pmt[0]
    slot = pmt[1]
    channel = pmt[2]
    panel_number = int(pmt[13][1:4])
    if panel_number == 0:
        panel_number = -1
    #new_data["pmtid"].append(pmt[4]) # Queens PMT ID?
    new_data["pmt_type"].append(noel_type_to_rat_type(pmt[9]))
    new_data["x"].append(float(pmt[10]) * 10.0) # Convert cm to mm
    new_data["y"].append(float(pmt[11]) * 10.0)
    new_data["z"].append(float(pmt[12]) * 10.0)
    new_data["panelnumber"].append(panel_number)
    dir_ = numpy.array([-9999.0, -9999.0, -9999.0])
    if noel_type_to_rat_type(pmt[9]) == 1: # Normal tube direction comes from panel info
        dir_ = -get_panel_dir(panel_number, panel_data)
    elif noel_type_to_rat_type(pmt[9]) != 10:
        dir_ = numpy.array([float(pmt[10]), float(pmt[11]), float(pmt[12])])
        dir_ = -dir_
        dir_ = dir_ / numpy.linalg.norm(dir_)
    if numpy.isnan(numpy.min(dir_)): # Happens if position in Noel data is 0, 0, 0
        dir_ = numpy.array([-9999.0, -9999.0, -9999.0])
    new_data["u"].append(float(dir_[0]))
    new_data["v"].append(float(dir_[1]))
    new_data["w"].append(float(dir_[2]))

# Now have a complete dict, write to a file
panelInfoFile = open("PMTINFO.ratdb", "w")
infoText = """{
type: \"PMTINFO\",
version: 1,
index: \"%s\",
run_range: [0, 0],
pass: 0,
production: false,
timestamp: \"\",
comment: \"\",
""" % args[2]
for key,value in new_data.iteritems():
    infoText += key+": "+str(value)+","
#infoText += yaml.dump(new_data).replace("]", "],")
infoText += """
}
"""
panelInfoFile.write(infoText)
panelInfoFile.close()
