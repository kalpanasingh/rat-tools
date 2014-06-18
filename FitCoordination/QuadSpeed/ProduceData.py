#!/usr/bin/env python
# Run rat and produce data for each effective speed
# Author I T Coulter - 9/11/2012
import os
import sys
import string
import QuadSpeedUtil

def ProduceRunMacFile( options ):
    """Produces and then runs the appropriate mac files."""
    inFile = open( "Base.mac", "r" )
    rawText = string.Template( inFile.read() )
    inFile.close()
    print options.transitTimes
    print QuadSpeedUtil.transitTime
    if options.transitTimes:
        QuadSpeedUtil.SetTransitTimes(options.transitTimes)
    print QuadSpeedUtil.transitTime
    for speed in QuadSpeedUtil.transitTime:
        transitTimeText = "/rat/db/set QUAD_FIT light_speed %sd" % speed
        if not options.default:
            transitTimeText = "/rat/db/set QUAD_FIT[%s] light_speed %sd" % ( options.scintMaterial, speed )
        outText = rawText.substitute( Speed = str( "%.0f" % speed ),
                                      GeoFile = options.geoFile,
                                      ScintMaterial = options.scintMaterial,
                                      Particle = options.particle,
                                      TransitTime = transitTimeText)
        outFileName = "quad_%.0f.mac" % speed
        outFile = open( outFileName, "w" )
        print "MACRO:"
        print outText
        outFile.write( outText )
        outFile.close()
        os.system( "rat " + outFileName )
        os.remove( outFileName )
    
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser( usage = "usage: %prog [options] target", version="%prog 1.0" )
    parser.add_option( "-g", type="string", dest="geoFile", help="Geometry File to use, location must be absolute or relative to target.", default="geo/snoplus.geo" )
    parser.add_option( "-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator" )
    parser.add_option( "-p", type="string", dest="particle", help="Particle type.", default="e-" )
    parser.add_option( "-t", type="string", dest="transitTimes", help="Transit times (accepts a list).",
                       action="callback", callback=QuadSpeedUtil.parse_list_arg)
    parser.add_option( "-d", action="store_true", dest="default",
                       help="Set this option if no QUAD table is currently available for the material specified" )
    (options, args) = parser.parse_args()
    ProduceRunMacFile( options )
    
            
