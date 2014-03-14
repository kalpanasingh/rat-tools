import os, sys, string, AlphaBetaUtilities

def ProduceRunMacFiles(options):
    # produces and then runs the required mac files
    
    # load the basic mac file
    inFile = open("Base.mac", "r")
    rawText = string.Template(inFile.read())
    inFile.close()
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
                                     GeoFile = options.geoFile,
                                     ScintMaterial = options.scintMaterial,
                                     OmitHadrons = hadrons,
                                     OutFileName = outfile + ".root",
                                     PulseLengthTimeConstant = timeConstant,
                                     PulseLengthRatio = pulseRatio )
            
            
            outFile = open(outfile + ".mac", "w")
            outFile.write(outText)
            outFile.close()
        
                # run the mac file for the particle
            print "Running " + outfile + ".mac and generating " + outfile + ".root"
            os.system("rat " + outfile + ".mac")
            
                # delete the particle-specific mac file when running is complete
            os.remove(outfile + ".mac")

import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Isotope desired, either 212 or 214.", default = "")
    (options, args) = parser.parse_args()
    if(options.particle == "212" or options.particle == "214"): 
        ProduceRunMacFiles(options)
    else:
        print "You must specify if you want PDFs for Bi212 or Bi214. This can be done by adding the option -p IsotopeNumber to your command"
