import os, sys, string, AlphaBetaUtilities

def ProduceRunMacFiles(options):
    # produces and then runs the required mac files
    
    # load the basic mac file
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    # load any batch options
    batch_params = None
    if options.batch:
        batch_params = {}
	execfile( options.batch, {}, batch_params )

    inFile = open( "batch.sh", "r" )
    rawScriptText = string.Template( inFile.read() )
    inFile.close()

    extraDB = ""
    if options.loadDB:
        extraDB = "/rat/db/load " + options.loadDB

    particleNames = AlphaBetaUtilities.ParticleNames[options.particle]
     
    # generate the specific mac files for each particle, and the Po212 done 3 times for each possible pulse shape.
    for particleIndex, particle in enumerate(particleNames):
        for pulseIndex, pulseDescription in enumerate(AlphaBetaUtilities.ParticlePulseDict[particle]):
            outfile = particle+pulseDescription

            if str(particle) == "Te130":
                generator = "/generator/vtx/set 2beta " + str(particle) + " 0 1"
                hadrons= "/PhysicsList/OmitHadronicProcesses true" 
            else:
               
                generator = "/generator/vtx/set backg " + str(particle)
                hadrons = ""
            if ( pulseIndex!=0 and pulseDescription!=""): #If it's Po21X and there is a non-default pulse shape then add that to .mac file.
                timeConstant = "/rat/db/set OPTICS["+ str(options.scintMaterial) + "] SCINTWAVEFORMalpha_value1 [ " + str(AlphaBetaUtilities.PulseTimeConstants[pulseDescription]) + "]"
                pulseRatio = "/rat/db/set OPTICS[" + str(options.scintMaterial) + "] SCINTWAVEFORMalpha_value2 [ " + str(AlphaBetaUtilities.PulseTimeRatios[pulseDescription]) + "]"
            else:
                timeConstant=""
                pulseRatio=""     

            outText = rawText.substitute(Generator = generator,
                                         ExtraDB = extraDB,
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     OmitHadrons = hadrons,
                                     OutFileName = outfile + ".root",
                                     PulseLengthTimeConstant = timeConstant,
                                     PulseLengthRatio = pulseRatio)
            
            outFile = open(outfile + ".mac", "w")
            outFile.write(outText)
            outFile.close()

            print "Running " + outfile + ".mac and generating " + outfile + ".root"

            if options.batch:
                # run the macro on a batch system 
                outText = rawScriptText.substitute( Preamble = "\n".join(s for s in batch_params['preamble']),
                                                    Cwd = os.environ['PWD'].replace("/.", "/"),
                                                    Macro = outfile + ".mac",
                                                    Ratenv = batch_params['ratenv'] )
                outFile = open(outfile + ".sh", "w")
                outFile.write(outText)
                outFile.close()
                os.system( batch_params["submit"] + " " + outfile +".sh" )

            else:
                # run the mac file for the particle
                os.system("rat " + outfile + ".mac")
            
                # delete the particle-specific mac file when running is complete
                os.remove(outfile + ".mac")

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Isotope desired, either 212 or 214.", default = "")
    parser.add_option("-b", type="string", dest="batch", help="Run in batch mode" )
    parser.add_option("-l", type="string", dest="loadDB", help="Load an extra DB directory")
    (options, args) = parser.parse_args()
    if(options.particle == "212" or options.particle == "214"): 
        ProduceRunMacFiles(options)
    else:
        print "You must specify if you want PDFs for Bi212 or Bi214. This can be done by adding the option -p IsotopeNumber to your command"
