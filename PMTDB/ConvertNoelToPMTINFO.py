#!/usr/bin/env python
# Author P G Jones - 12/03/2012 <p.g.jones@qmul.ac.uk>
# This script converts the Noel csv file to the PMTINFO format
import optparse
import sys
import csv

parser = optparse.OptionParser( usage = "./ProducePanelInfo.py Path-to-NoelCSV Path-to-PANELINFO.ratdb Index", version="%prog 1.0" )
(options, args) = parser.parse_args()
if len( args ) != 3:
    parser.print_help()
    sys.exit(0)

noelFile = csv.reader( open( args[0], "r" ) )

newData = {}
newData["x"] = []
newData["y"] = []
newData["z"] = []
newData["u"] = []
newData["v"] = []
newData["w"] = []
newData["panel_number"] = []
newData["type"] = []
newData["pmtid"] = []
noelFile.next() # Ignore the first line
for pmt in noelFile:
    crate = pmt[0]
    slot = pmt[1]
    channel = pmt[2]
    panelNumber = int( pmt[13][1:4] )
    if panelNumber != 0:
        newData["pmtid"].append( pmt[4] ) # Queens PMT ID?
        newData["type"].append( pmt[9] )
        newData["x"].append( pmt[10] )
        newData["y"].append( pmt[11] )
        newData["z"].append( pmt[12] )
        newData["panel_number"] = panelNumber
    else:
        print pmt
