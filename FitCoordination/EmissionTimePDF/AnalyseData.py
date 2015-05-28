#!/usr/bin/env python
import string, ROOT, sys, math
# Author P G Jones - 22/05/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


def AnalyseRootFiles(options):

    pdf = ProducePDF()
    startBin = pdf.FindFirstBinAbove(1e-10)
    endBin = pdf.FindLastBinAbove(1e-8)

    # Print the final results
    print "\n"
    print "Please place the text below into the database file: ET1D.ratdb located in rat/data, replacing any existing entry with the same index."
    print "\n"
    print "{"
    print "name: \"ET1D\","
    print "index: \"" + options.index + "\","
    print "run_range: [0, 0],"
    print "pass : 0,"
    print "production: false,"
    print "comment: \"\","
    print "\n",
    print "time: [",
    for bin in range(startBin, endBin):
        print str(pdf.GetXaxis().GetBinCenter(bin)) + ", ",
    print "],"
    print "probability: [",
    for bin in range(startBin, endBin):
        tempString = str(pdf.GetBinContent(bin)) + ", "
        print tempString,
    print "],"
	
    print "}"
    print "\n"


# Produce (but not display) a PDF of the photon emission times
def ProducePDF():

    emissionTimes = ROOT.TH1D("emissionTime", "emissionTime", 600, -100.5, 499.5)
    eventNumber = 0

    for ds, run in rat.dsreader("events_WithTracks.root"):
        eventNumber += 1
		
        mc = ds.GetMC()
        startTime = mc.GetMCParticle(0).GetTime()
        startPosition = mc.GetMCParticle(0).GetPosition()
		
        for trackIndex in range(0, mc.GetMCTrackCount()):
            track = mc.GetMCTrack(trackIndex)
            if(track.GetPDGCode() != 0):
                continue
            emissionTimes.Fill(track.GetMCTrackStep(0).GetGlobalTime())

    c = 1.6
    N = 1.0 / (c * math.sqrt(2.0 * math.pi))    # Normalisation factor

    convolvedHist = ROOT.TH1D("convolvedHist", "convolvedHist", 600, -100.5, 499.5)
    for bin1 in range(1, 601):
        hValue = convolvedHist.GetBinContent(bin1)
		
        for bin2 in range(1, 601):
            timeDiff = convolvedHist.GetBinCenter(bin1) - convolvedHist.GetBinCenter(bin2)
			
            if timeDiff > -100.5 and timeDiff < 499.5:
                hValue = hValue + (emissionTimes.GetBinContent(bin2) * N * math.exp(-(timeDiff - 0.0)**2 / (2.0 * c * c)))
                convolvedHist.SetBinContent(bin1, hValue)

    convolvedHist.Scale(1.0 / emissionTimes.GetSumOfWeights())

    return convolvedHist

	
# Display the PDF plot of the photon emission times
def PlotPDF():

    pdf = ProducePDF()

    c1 = ROOT.TCanvas()
    c1.cd(1)
    pdf.Draw()
	
    raw_input("Press 'Enter' to exit")
	
	
import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)
    
