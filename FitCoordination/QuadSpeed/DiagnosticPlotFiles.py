#!/usr/bin/env python
# Plots useful to the quadFitter speed coordination
# Author I Coulter - 09/11/2012
import ROOT
import rat
import QuadSpeedUtil

def PlotDistVTime():
    """ Draws the RadialBias v EffectiveSpeed plot."""
    histograms = QuadSpeedUtil.ProduceAllData()
    histograms[0].Draw( "*" )
    histograms[0].GetXaxis().SetTitle( "Radial Bias [mm]" )
    histograms[0].GetYaxis().SetTitle( "Effective Speed [mm/ns]" )
    histograms[0].SetMarkerStyle(20)
    raw_input( "Hit Enter to exit." )

# Make ROOT look nicer
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
    
import optparse
if __name__ == '__main__':
    PlotDistVTime()
