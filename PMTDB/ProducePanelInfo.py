#!/usr/bin/env python
# Author P G Jones - 12/03/2012 <p.g.jones@qmul.ac.uk>
# Author P G Jones - 16/07/2012 <p.g.jones@qmul.ac.uk> : Updated to add panel local x axis and panel centre
# This script parses the PMTINFO.ratdb file to produce a PANELINFO.ratdb file
import yaml # Needs installing
import sys
import numpy
from minify_json import json_minify # In this directory

def CorrectPosition( pos, direction ):
    """ All panel pmts are in PMTINFO by front face, change to equator/useful."""
    pos += -direction * 131.6
    return pos

def CalculateCentroid( pmtPos ):
    """ Sum over pmtPositions and get the mean pos."""
    origin = numpy.array( [0.0, 0.0, 0.0] )
    for pmt in pmtPos:
        origin += pmt
    origin /= float( len( pmtPos ) )
    return origin

def CalculateSCoordAxis( pmtPos ):
    """ Calculate the origin/centre of the panel."""
    origin = CalculateCentroid( pmtPos )
    # Now the axis
    xAxis = numpy.array( [0.0,0.0,0.0] )
    for pmt in pmtPos:
        if numpy.linalg.norm( pmt - origin ) > 137.00 and numpy.linalg.norm( pmt - origin ) < 2.0 * 137.0: # Conc radius
            xAxis = pmt - origin
            break
    xAxis = pmtPos[-1] - origin
    xAxis /= numpy.linalg.norm( xAxis )
    return ( origin, xAxis )

def CalculateTCoord( pmtPos ):
    """ Calculate the origin of the panel."""
    origin = CalculateCentroid( pmtPos )
    # Now choose the pmtPos nearest the origin
    dists = [ numpy.linalg.norm( pmt - origin ) for pmt in pmtPos ]
    minIndex = dists.index( min( dists ) )
    return pmtPos[minIndex]

def CalculateT14Coord( pmtPos ):
    """ Calculate the origin of the panel."""
    origin = CalculateCentroid( pmtPos )
    # Now choose the 3 pmtPos nearest to the origin
    dists = sorted( [ [numpy.linalg.norm( pmt - origin ), index] for index, pmt in enumerate( pmtPos ) ], key=lambda tup: tup[0] )
    return ( pmtPos[dists[0][1]] + pmtPos[dists[1][1]] + pmtPos[dists[2][1]] ) / 3.0 

def CalculateTAxis( pmtPos ):
    """ Calculate the T10, T14 axis, choose the furthest PMT from the origin."""
    origin = CalculateCentroid( pmtPos )
    dists = sorted( [ [numpy.linalg.norm( pmt - origin ), index] for index, pmt in enumerate( pmtPos ) ], key=lambda tup: tup[0] )
    xAxis = pmtPos[dists[-1][1]] - origin
    return xAxis / numpy.linalg.norm( xAxis )

def CalculateT21Axis( pmtPos ):
    """ Calculate the T21 axis, use furthest pmts."""
    origin = CalculateCentroid( pmtPos )
    # Now choose the 2 pmtPos furthest from the origin
    dists = sorted( [ [numpy.linalg.norm( pmt - origin ), index] for index, pmt in enumerate( pmtPos ) ], key=lambda tup: tup[0] )
    xAxis = ( pmtPos[dists[-1][1]] + pmtPos[dists[-2][1]] ) / 2.0 - origin
    return xAxis / numpy.linalg.norm( xAxis )

# Now start parsing the file
pmtInfoFile = open( "data/PMTINFO.ratdb", "r" )
data = yaml.load( json_minify( pmtInfoFile.read(), False ) )
pmtInfoFile.close()
# Loop over the pmts, and condense data to once per panel
newData = {}
newData["panel_number"] = []
newData["panel_type"] = []
newData["r"] = []
newData["s"] = []
newData["t"] = []
newData["u"] = []
newData["v"] = []
newData["w"] = []
newData["x"] = []
newData["y"] = []
newData["z"] = []

pmts = [0] * 1000
pmtPos = [[]] * 1000
pmtDir = [[]] * 1000
for x, y, z, u, v, w, number in zip( data["x"], data["y"], data["z"], data["u"], data["v"], data["w"], data["panelnumber"] ):
    if number >= 0:
        pmts[number] += 1
        # Add the panel information once only
        if pmts[number] == 1:
            newData["panel_number"].append( number )
            newData["u"].append( u )
            newData["v"].append( v )
            newData["w"].append( w )
            pmtDir[number] = numpy.array( [-u, -v, -w] ) # All Panel PMTs point the wrong way!
            pmtPos[number] = [ CorrectPosition( numpy.array( [ x, y, z ] ), pmtDir[number] ) ]
        else:
            pmtPos[number].append( CorrectPosition( numpy.array( [ x, y, z ] ), pmtDir[number] ) )
# Now calculate the panel type
for number in newData["panel_number"]:
    origin = numpy.array( [0.0, 0.0, 0.0] )
    xAxis = numpy.array( [0.0, 0.0, 0.0] )
    if pmts[number] == 7: #S7 == 0
        newData["panel_type"].append( 0 )
        origin, xAxis = CalculateSCoordAxis( pmtPos[number] )
    elif pmts[number] == 19: #S19 == 1
        newData["panel_type"].append( 1 )
        origin, xAxis = CalculateSCoordAxis( pmtPos[number] )
    elif pmts[number] == 21: #T21 == 2
        newData["panel_type"].append( 2 )
        origin = CalculateTCoord( pmtPos[number] )
        xAxis = CalculateT21Axis( pmtPos[number] )
    elif pmts[number] == 14: #T14 == 3
        newData["panel_type"].append( 3 )
        origin = CalculateT14Coord( pmtPos[number] )
        xAxis = CalculateTAxis( pmtPos[number] )
    elif pmts[number] == 10: #T10 == 4
        newData["panel_type"].append( 4 )
        origin = CalculateTCoord( pmtPos[number] )
        xAxis = CalculateTAxis( pmtPos[number] )
    elif pmts[number] == 9 or pmts[number] == 8: #T10M == T10
        newData["panel_type"].append( 4 )
        origin = CalculateTCoord( pmtPos[number] )
        xAxis = CalculateTAxis( pmtPos[number] )
    elif pmts[number] == 13 or pmts[number] == 12: #T14M == T14
        newData["panel_type"].append( 3 )
        origin = CalculateT14Coord( pmtPos[number] )
        xAxis = CalculateTAxis( pmtPos[number] )
    if number == 64 or number == 82 or number == 100 or number == 102 or number == 106 or number == 263 or number == 576 or number == 711 or number == 712 or number == 130 or number == 139:
        print number, ":", origin[0], ",", origin[1], ",", origin[2], "|", xAxis[0], ",", xAxis[1], ",", xAxis[2]
    newData["r"].append( float( xAxis[0] ) )
    newData["s"].append( float( xAxis[1] ) )
    newData["t"].append( float( xAxis[2] ) )
    newData["x"].append( float( origin[0] ) )
    newData["y"].append( float( origin[1] ) )
    newData["z"].append( float( origin[2] ) )

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
