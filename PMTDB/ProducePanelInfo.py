#!/usr/bin/env python
# Author P G Jones - 12/03/2012 <p.g.jones@qmul.ac.uk>
# This script parses the PMTINFO.ratdb file to produce a PANELINFO.ratdb file
import optparse
import yaml # Needs installing
import sys
from minify_json import json_minify # In this directory

parser = optparse.OptionParser( usage = "./ProducePanelInfo.py Path-to-PMTINFO.ratdb", version="%prog 1.0" )
(options, args) = parser.parse_args()
if len( args ) != 1:
    parser.print_help()
    sys.exit(0)
# Now start parsing the file
pmtInfoFile = open( args[0], "r" )
data = yaml.load( json_minify( pmtInfoFile.read(), False ) )
pmtInfoFile.close()
# Loop over the pmts, and condense data to once per panel
newData = {}
newData["panel_number"] = []
newData["panel_type"] = []
newData["u"] = []
newData["v"] = []
newData["w"] = []
pmts = [0] * 1000
for u, v, w, number in zip( data["u"], data["v"], data["w"], data["panelnumber"] ):
    if number >= 0:
        pmts[number] += 1
        # Add the panel information once only
        if pmts[number] == 1:
            newData["panel_number"].append( number )
            newData["u"].append( u )
            newData["v"].append( v )
            newData["w"].append( w )
# Now calculate the panel type
for number in newData["panel_number"]:
    if pmts[number] == 7: #S7 == 0
        newData["panel_type"].append( 0 )
    elif pmts[number] == 19: #S19 == 1
        newData["panel_type"].append( 1 )
    elif pmts[number] == 21: #T21 == 2
        newData["panel_type"].append( 2 )
    elif pmts[number] == 14: #T14 == 3
        newData["panel_type"].append( 3 )
    elif pmts[number] == 10: #T10 == 4
        newData["panel_type"].append( 4 )
    elif pmts[number] == 9 or pmts[number] == 8: #T10M == T10
        newData["panel_type"].append( 4 )
    elif pmts[number] == 13 or pmts[number] == 12: #T14M == T14
        newData["panel_type"].append( 3 )
# Now have a complete dict, write to a file
panelInfoFile = open( "PANELINFO.ratdb", "w" )
infoText = """{
name: \"PMTINFO\",
index: \"sno+\",
valid_begin : [0, 0],
valid_end : [0, 0],
"""
infoText += yaml.dump( newData ).replace( "]", "]," )
infoText += """}
"""
panelInfoFile.write( infoText )
panelInfoFile.close()
