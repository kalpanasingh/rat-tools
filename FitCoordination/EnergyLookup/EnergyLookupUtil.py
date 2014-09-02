#!/usr/bin/env python
import ROOT, rat
import optparse
# Useful utility functions
# Author P G Jones - 13/09/2011 <p.jones22@physics.ox.ac.uk>

Material = "labppo_scintillator"
PosSet = [ 0.0, 2000.0, 4000.0, 5000.0, 5500.0, 5750.0, 5950.0, 6100.0, 6500.0, 7000.0, 7500.0, 8000.0 ]
EnergySet = [ 1.0, 2.0, 3.0, 3.5, 4.0, 5.0 ]
## Energies if using water-filled detector
#EnergySet = [ 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 ]


def parse_list_arg(option, opt, value, parser):
    """Parse a comma delimited list, return list of floats
    """
    value_list = []
    # Strip any brackets
    value_str = value.strip("]})").strip("[{(")
    value_list = value_str.split(",")
    for i, v in enumerate(value_list):
        try:
            value_list[i] = float(value_list[i])
        except ValueError:
            print "Parser issue: %s must be set as a comma delimited string"
            print "You used: %s" % value
            raise
    setattr(parser.values, option.dest, value_list)

def SetPositions(positions):
    """Set the positions list."""
    global PosSet
    PosSet = positions

def SetEnergies(energies):
    """Set the energies list."""
    global EnergySet
    EnergySet = energies

def SetMaterial(material):
    """Set the material."""
    global Material
    Material = material

def GetFileName(p, e):
    """Get the ROOT output name for position & energy."""
    global Material
    fileName = "%s_P%.0fE%.0f" % (Material, p, (e*10))
    return fileName

def NhitsHistogram( fileName ):

    nhitHist = ROOT.TH1D( fileName, "Nhit", 300, 0.0, 3000.0 )

    for ds, run in rat.dsreader( fileName ):
        if( ds.GetEVCount() == 0 ):
            continue
        nhitHist.Fill( ds.GetEV(0).GetCalbratedPMTs.GetCount() )

    return nhitHist

def FitGauss( nhitHist ):

    tolerance = 10
    lowBin = nhitHist.FindFirstBinAbove( 0.0 )
    lowBin = lowBin - tolerance
    highBin = nhitHist.FindLastBinAbove( 0.0 )
    highBin = highBin + tolerance
    if( lowBin < 1 ):
        lowBin = 1
    if( highBin > nhitHist.GetNbinsX() ):
        highBin = nhitHist.GetNbinsX()

    fitGauss = ROOT.TF1( "gaus", "gaus", nhitHist.GetBinCenter( lowBin ), nhitHist.GetBinCenter( highBin ) )
    nhitHist.Fit( fitGauss, "rN" )

    return [ fitGauss.GetParameter( 1 ), fitGauss.GetParameter( 2 ) ]

def NhitPerMeVEnergyPos():
    """ Return 2d array (energy, pos) of the nhit per MeV values."""
    global EnergySet, PosSet
    resultTable = []

    for energy in EnergySet:
        posList = []
        for pos in PosSet:
            fileName = "%s.root" % GetFileName(pos, energy)
            print fileName
            posList.append( FitGauss( NhitsHistogram( fileName ) )[0] )
        resultTable.append( posList )

    return resultTable

def SigmaPerMeVEnergyPos():
    """ Return 2d array (energy, pos) of the nhit per MeV values."""
    global EnergySet, PosSet
    resultTable = []
    
    for energy in EnergySet:
        posList = []
        for pos in PosSet:
            fileName = "%s.root" % GetFileName(pos, energy)
            print fileName
            posList.append( FitGauss( NhitsHistogram( fileName ) )[1] )
        resultTable.append( posList )
        
    return resultTable

def NhitPerMeVPosEnergy():
    """ Return 2d array (pos, energy) of the nhit per MeV values."""
    global EnergySet, PosSet
    resultTable = []

    for pos in PosSet:
        energyList = []
        for energy in EnergySet:
            fileName = "%s.root" % GetFileName(pos, energy)
            print fileName
            energyList.append( FitGauss( NhitsHistogram( fileName ) )[0] )
        resultTable.append( energyList )
            
    return resultTable
