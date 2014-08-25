import AlphaBetaUtilities as ABU
def AnalyseData(options):
    pdfs={}
    energies={}
    energyRatio={}
    betaEnergies=[]
    particleNames = ABU.ParticleNames[options.particle]
    for particleIndex, particle in enumerate(particleNames):
        for pulseIndex, pulseDescription in enumerate(ABU.ParticlePulseDict[particle]):
            fileName = particle+pulseDescription 
            fileInfo = ABU.GetFileInfo(fileName+".root")
            pdfs[fileName] = fileInfo[0]
            energies[fileName] = fileInfo[1]
            if (fileName.find("Bi")!=-1): #The Bi212 file has beta energies
                 betaEnergies = energies[fileName]
    for fileName in energies:
        if fileName.find("Po") != -1 :
            energyRatio[fileName] = ABU.GetEnergyRatio(betaEnergies,energies[fileName])
    outfile = "AlphaBetaOutput"+options.particle+".txt"
    print "The relevant PDFs for the AlphaBetaClassifier have been output to "+str(outfile) 
    print "Replace the appropriate portion of ALPHA_BETA_CLASSIFIER.ratdb with the text found there"
    f = open(outfile,'w')
    for pulseIndex, pulseDescription in enumerate(ABU.ParticlePulseDict[particleNames[1]]):
        ABU.OutputFileChunk([pdfs[particleNames[0]],pdfs[particleNames[1]+pulseDescription],pdfs[particleNames[2]]],energyRatio[particleNames[1]+pulseDescription],options, pulseDescription, f )
    f.close()
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-g", type = "string", dest = "geoFile", help = "Geometry File to use - location must be absolute or relative to target.", default = "geo/snoplus.geo")
    parser.add_option("-s", type = "string", dest = "scintMaterial", help = "Scintillator material.", default = "labppo_scintillator")
    parser.add_option("-p", type = "string", dest = "particle", help = "Isotope desired, either 212 or 214.", default = "")
    (options, args) = parser.parse_args()
    if(options.particle == "212" or options.particle == "214"):
        AnalyseData(options)
    else:
        print "You must specify if you want PDFs for Bi212 or Bi214. This can be done by adding the option -p IsotopeNumber to your command"
