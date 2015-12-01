#!/usr/bin/env python
import ROOT
import rat
import math
# Secondary functions and user-defined Values for the EnergyLookup2D Coordinator
# Author M Mottram - <m.mottram@qmul.ac.uk>

CentralEnergies = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0]
LookupEnergy = 1.0

CentralHistFilename = "hAtCentre.root"
MapHistFilename = "hMap.root"

NumberOfSegments = 10

# Create theta bins and inclusion radii so that all events at RMax are included in one of the fits
NThetaBins = 60 # This gives a segment width (on either side) of ~150mm ~ position resolution
ThetaValues = []
SinThetaValues = []
CosThetaValues = []
for i in range(NThetaBins+1):
    ThetaValues.append(i * math.pi / NThetaBins)
    SinThetaValues.append(math.sin(ThetaValues[-1]))
    CosThetaValues.append(math.cos(ThetaValues[-1]))
SegmentWidth = 6000.0 * math.sin((ThetaValues[1] - ThetaValues[0])/2) # +/- half the segment
SegmentWidth2 = SegmentWidth * SegmentWidth


def CentralFilename(material, energy):
    return material + "_energy_" + str(int(energy*1000))

def PlaneFilename(material, i):
    return material + "_plane_" + str(i)

def CentralHistname(energy):
    return "hHistE" + str(int(energy*1000))

def GetHParameterAtCentre(material):
    '''Extract and store the h parameters as a function
    of energy at the centre of the detector.

    Fit each histogram with a gaussian before saving.
    '''

    hFile = ROOT.TFile(CentralHistFilename, "recreate")
    hGraph = ROOT.TGraphErrors() # tgraph of hparameter vs energy

    for i, energy in enumerate(CentralEnergies):

        infilename = CentralFilename(material, energy) + ".root"

        hHist = ROOT.TH1F(CentralHistname(energy), ";H parameter", 10000, 0, 10000)
        for ds, run in rat.dsreader(infilename):
            
            segmentor = rat.utility().GetSegmentor()
            segmentor.SetNumberOfDivisions(NumberOfSegments)
            rawPMTSegmentIDs = segmentor.GetSegmentIDs()
            rawPMTSegmentPopulations = segmentor.GetSegmentPopulations()
            hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)

            calPMTs = ds.GetEV(0).GetCalPMTs()
            for j in range(0, calPMTs.GetCount()):
                hitPMTSegmentPopulations[rawPMTSegmentIDs[calPMTs.GetPMT(j).GetID()]] += 1

            hValue = 0.0
            for s in range(len(rawPMTSegmentPopulations)):
                if (hitPMTSegmentPopulations[s] >= rawPMTSegmentPopulations[s]):
                    correctedHitPMTSegmentPopulation = rawPMTSegmentPopulations[s] - 1
                else:
                    correctedHitPMTSegmentPopulation = hitPMTSegmentPopulations[s]
                hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(correctedHitPMTSegmentPopulation) / float(rawPMTSegmentPopulations[s]))))
            hValue *= -1.0

            hHist.Fill(hValue)

        hFile.cd()
        hHist.Fit("gaus", "Q")
        hHist.Write()

        hGraph.SetPoint(i, energy, hHist.GetFunction("gaus").GetParameter(1))
        hGraph.SetPointError(i, 0, hHist.GetFunction("gaus").GetParError(1))

    hFit = ROOT.TF1("hFit", "x*[0]", CentralEnergies[0], CentralEnergies[-1]+1.0)
    hGraph.Fit(hFit)

    hGraph.SetName("grHVsEnergy")
    hGraph.Write()

    hFit.Write()

    hFile.Close()



def CreateHMap(material):
    '''Create a TTree filled with h parameters, rho and z
    '''

    # First, get the central H value
    hCentralFile = ROOT.TFile(CentralHistFilename, "read")
    centralFit = hCentralFile.Get("hFit")
    centralH = centralFit.Eval(LookupEnergy)

    hFile = ROOT.TFile(MapHistFilename, "recreate")

    hHist = ROOT.TH2F("hMap", ";rho;z", 50, 0, 6000, 100, -6000, 6000)
    hEntries = ROOT.TH2F("hEntries", ";rho;z", 50, 0, 6000, 100, -6000, 6000)
    hGraphs = []
    ctr = []
    for i, theta in enumerate(ThetaValues):
        hGraphs.append(ROOT.TGraph())
        hGraphs[-1].SetName("hAtTheta%d" % (int(theta * 1000))) ## Make it easier to draw
        ctr.append(0)

    for iEntry, (ds, run) in enumerate(rat.dsreader(material + "_plane_*.root")):

        if (iEntry % 1000) == 0:
            print iEntry

        if ds.GetEVCount() == 0:
            continue

        # Segment at the specified event point
        mcPosition = ds.GetMC().GetMCParticle(0).GetPosition()
        segmentor = rat.utility().GetSegmentor()
        # segmentor.SetPatternOrigin(mcPosition, ROOT.TVector3(0.0, 0.0, 1.0), 10)
        segmentor.SetNumberOfDivisions(NumberOfSegments)
        rawPMTSegmentIDs = segmentor.GetSegmentIDs()
        rawPMTSegmentPopulations = segmentor.GetSegmentPopulations()
        hitPMTSegmentPopulations = [0] * len(rawPMTSegmentPopulations)

        calPMTs = ds.GetEV(0).GetCalPMTs()
        for j in range(0, calPMTs.GetCount()):
            hitPMTSegmentPopulations[rawPMTSegmentIDs[calPMTs.GetPMT(j).GetID()]] += 1

        hValue = 0.0

        # It is possible to get 0 raw PMTs with the moved segmentor
        # Need to skip these sectors
        for s in range(len(rawPMTSegmentPopulations)):
            if (hitPMTSegmentPopulations[s] >= rawPMTSegmentPopulations[s]):
                correctedHitPMTSegmentPopulation = rawPMTSegmentPopulations[s] - 1
            else:
                correctedHitPMTSegmentPopulation = hitPMTSegmentPopulations[s]
            if rawPMTSegmentPopulations[s] > 0:
                hValue += (rawPMTSegmentPopulations[s] * math.log(1.0 - (float(correctedHitPMTSegmentPopulation) / float(rawPMTSegmentPopulations[s]))))
        hValue *= -1.0

        hRatio = hValue / centralH
        
        # Check which segments this event will contribute to
        rhoEvent = math.sqrt(mcPosition.X()*mcPosition.X() + mcPosition.Y()*mcPosition.Y())
        zEvent = mcPosition.Z()
        rEvent = mcPosition.Mag()

        for i, (sintheta, costheta) in enumerate(zip(SinThetaValues, CosThetaValues)):
            centralRho = rEvent * sintheta
            centralZ = rEvent * costheta
            rhoDiff = centralRho - rhoEvent
            zDiff = centralZ - zEvent
            diff2 = rhoDiff*rhoDiff + zDiff*zDiff
            if diff2 < SegmentWidth2:
                hGraphs[i].SetPoint(ctr[i], rEvent, hRatio)
                ctr[i]+=1

        hHist.Fill(rhoEvent, zEvent, hRatio)
        hEntries.Fill(rhoEvent, zEvent)

    # Get the mean for each bin in the map
    for i in range(hHist.GetNbinsX()):
        for j in range(hHist.GetNbinsY()):
            if hEntries.GetBinContent(i+1, j+1) > 0.1:
                hHist.SetBinContent(i+1, j+1, hHist.GetBinContent(i+1, j+1) / 
                                    hEntries.GetBinContent(i+1, j+1))
    
    hHist.Write()
    for hGraph in hGraphs:
        hGraph.Write()
    hFile.Close()


def FitMappingHists(material):
    '''Fit piecewise polynomials for bulk (pol3) and outer region
    where TIR affects nhits (pol1).
    '''

    hFile = ROOT.TFile(MapHistFilename, "update")

    # Assume each plot has a peak at 5200 mm.
    # Enforce continuity across this boundary, but do not enforce
    # constant derivatives.
    # To enforce continuity, must fit one function first, then second
    function1 = ROOT.TF1("function1", "[0] + [1]*x + [2]*x*x + [3]*x*x*x", 0, 5200) # Seems to not like pol3 when [0] is fixed
    function1.FixParameter(0, 1) # Ensure H ratio = 1 at origin

    function2 = ROOT.TF1("function2", "[0] + [2]*(x-[1]) + [3]*(x-[1])*(x-[1]) + [4]*(x-[1])*(x-[1])*(x-[1])", 5200, 6000)
    function2.FixParameter(1, 5200)
    
    hHist = hFile.Get("hMap")
    hGraphs = []
    hFits = []
    for i, theta in enumerate(ThetaValues):
        hGraphs.append(hFile.Get("hAtTheta%d" % int(theta*1000)))

        # First fit the first polynomial up to 5.2 m
        hGraphs[-1].Fit(function1, "R")
        # Get the value at 5200 and use this as the constant for function2
        # Then fit
        function2.FixParameter(0, function1.Eval(5200))
        hGraphs[-1].Fit(function2, "R")

        # Save these functions to the file (with unique names)
        f1temp = ROOT.TF1(function1)
        f2temp = ROOT.TF1(function2)
        f1temp.SetName("f1_%s" % int(theta*1000))
        f2temp.SetName("f2_%s" % int(theta*1000))
        f1temp.Write("", ROOT.TObject.kOverwrite)
        f2temp.Write("", ROOT.TObject.kOverwrite)

        # Now create a new function that is the sum of the two previous functions
        # To save to the file (just for plotting later)
        hFits.append(ROOT.TF1("fitAtTheta%d" % int(theta*1000),
                              "(x<5200)*function1 + (x>5200)*function2", 0, 6000))
        hFits[-1].Write("", ROOT.TObject.kOverwrite)
    hFile.Close()


def PrintRATDB(material):
    '''Print out RATDB constants
    '''
    centralFile = ROOT.TFile(CentralHistFilename, "read")
    mappingFile = ROOT.TFile(MapHistFilename, "read")
    # Fit is of the form H = [0] * E
    centralFit = centralFile.Get("hFit")
    # Fit1 and Fit2 are both pol3s
    mappingFits1 = [mappingFile.Get("f1_%s" % (int(theta*1000))) for theta in ThetaValues]
    mappingFits2 = [mappingFile.Get("f2_%s" % (int(theta*1000))) for theta in ThetaValues]
    print "\nPlease place the text below into the database file FIT_ENERGY_RTHETA_FUNCTIONAL.ratdb\n"
    print "{"
    print "type: \"FIT_ENERGY_RTHETA_FUNCTIONAL\","
    print "version: 1,"
    print "index: \"%s\"," % material
    print "run_range: [0, 0],"
    print "pass: 0,"
    print "production: false,"
    print "timestamp: \"\","
    print "comment: \"\","
    print "r_cutoff: %s," % 6000.0
    print "h_per_MeV: %s," % centralFit.GetParameter(0)
    print "thetas: [%s]," % (", ".join(str(theta) for theta in ThetaValues))
    print "r_piecewise: %s," % mappingFits2[0].GetParameter(1)
    # The offset of f1 is always 1, but print to the table anyway for consistency
    print "f1_pol0: [%s]," % (", ".join(str(f1.GetParameter(0)) for f1 in mappingFits1))
    print "f1_pol1: [%s]," % (", ".join(str(f1.GetParameter(1)) for f1 in mappingFits1))
    print "f1_pol2: [%s]," % (", ".join(str(f1.GetParameter(2)) for f1 in mappingFits1))
    print "f1_pol3: [%s]," % (", ".join(str(f1.GetParameter(3)) for f1 in mappingFits1))
    # The constant (x-c) is always the same (should be 5200) but print to table for consistency
    print "f2_x_const: [%s]," % (", ".join(str(f2.GetParameter(1)) for f2 in mappingFits2))
    print "f2_pol0: [%s]," % (", ".join(str(f2.GetParameter(0)) for f2 in mappingFits2))
    print "f2_pol1: [%s]," % (", ".join(str(f2.GetParameter(2)) for f2 in mappingFits2))
    print "f2_pol2: [%s]," % (", ".join(str(f2.GetParameter(3)) for f2 in mappingFits2))
    print "f2_pol3: [%s]," % (", ".join(str(f2.GetParameter(4)) for f2 in mappingFits2))
    print "}\n"


def CompareMaps(material):
    '''Compare the mapping predictions to the generated histogram
    
    Use much finer binning for the prediction
    '''
    hFile = ROOT.TFile(MapHistFilename, "read")
    hMap = hFile.Get("hMap")
    can1 = ROOT.TCanvas("can1", "can1")
    hMap.GetZaxis().SetRangeUser(0.9, 1.6)
    hMap.SetTitle("Data")
    hMap.Draw("colz")

    binsx = 300
    binsy = 600
    hPrediction = ROOT.TH2F("hPrediction", "Prediction", binsx, 0, 6000, binsy, -6000, 6000)

    hFits = []
    for i, theta in enumerate(ThetaValues):
        hFits.append(hFile.Get("fitAtTheta%s" % int(theta*1000)))

    for i in range(binsx):
        if binsx > 20:
            if i % (binsx/20) == 0:
                print i, 'of', binsx
        for j in range(binsy):
            rho = hPrediction.GetXaxis().GetBinCenter(i+1)
            z = hPrediction.GetYaxis().GetBinCenter(j+1)
            r2 = rho*rho+z*z
            if r2 > 36000000:
                continue
            r = math.sqrt(r2)
            theta = math.acos(z / r) # tan needs 1/0 for some bins
            # Find the upper and lower theta index
            thetaBinLow = int(theta / (math.pi / NThetaBins))
            thetaBinHigh = thetaBinLow+1
            thetaLow = ThetaValues[thetaBinLow]
            thetaHigh = ThetaValues[thetaBinHigh]
            predThetaLow = hFits[thetaBinLow].Eval(r)
            predThetaHigh = hFits[thetaBinHigh].Eval(r)
            # Linear interpolation to get the prediction (could use splines...)
            prediction = predThetaLow + (predThetaHigh - predThetaLow) * (theta - thetaLow) / (thetaHigh - thetaLow)
            hPrediction.SetBinContent(i+1, j+1, prediction)

    can2 = ROOT.TCanvas("can2", "can2")
    hPrediction.GetZaxis().SetRangeUser(0.9, 1.6)
    hPrediction.Draw("colz")
    raw_input("RTN to exit")



ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

