#!/usr/bin/env python
# Author P G Jones - 22/04/2012 <p.g.jones@qmul.ac.uk>
# This script converts the SNOMAN title files to rat db PMTINFO

pmtPosLines = []
for line in open( "pmt_positions_20040923_ver2.dat", "r" ).readlines(): # According to QSNO the latter versions of SNOMAN had pmt positions hard wired to this file
    if line[0] != "#": # Ignore comment lines
        pmtPosLines.append( line )
# Now ignore the first 30 Lines (form the header)
