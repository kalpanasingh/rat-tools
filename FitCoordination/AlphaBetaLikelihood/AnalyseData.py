import AlphaBetaUtilities
def AnalyseData(options):
    pdfs={}
    particleNames = AlphaBetaUtilities.ParticleNames[options.particle]
    for particleIndex, particle in enumerate(particleNames):
        for pulseIndex, pulseDescription in enumerate(AlphaBetaUtilities.ParticlePulseDict[particle]):
            fileName = particle+pulseDescription 
            pdfs[fileName] = AlphaBetaUtilities.ProduceTimeResidualPDF(fileName+".root")

    print "The following are the relevant PDFs for the AlphaBetaClassifier. Replace the relevant portion of ALPHA_BETA_CLASSIFIER.ratdb with the following text"
    for pulseIndex, pulseDescription in enumerate(AlphaBetaUtilities.ParticlePulseDict[particleNames[1]]):
        AlphaBetaUtilities.OutputFileChunk([pdfs[particleNames[0]],pdfs[particleNames[1]+pulseDescription],pdfs[particleNames[2]]],options, pulseDescription )

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
