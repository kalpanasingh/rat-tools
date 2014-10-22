#!/usr/bin/env python
import string, ROOT, rat
# Useful secondary functions for the SimpleEnergy Coordinator
# Author P G Jones - 07/06/2011 <p.g.jones@qmul.ac.uk>
#        K Majumdar - 08/09/2014 - Cleanup of Coordinators for new DS


# Produce a plot of Nhits vs. MC Radius (plot is not actually displayed)
def ProduceNhitsRadiusGraph():
	
    graphPoint = 0
    nhitsRadiusPlot = ROOT.TGraph()
	
    for ds, run in rat.dsreader("events_E=1MeV.root"):
        if ds.GetEVCount() == 0:
            continue

        mc = ds.GetMC()
        ev = ds.GetEV(0)

        nhitsRadiusPlot.SetPoint(graphPoint, mc.GetMCParticle(0).GetPosition().Mag(), ev.GetCalPMTs().GetCount())
        graphPoint = graphPoint + 1

	return nhitsRadiusPlot


# Plot the Nhits of events located very close to the AV Centre (plot is not actually displayed)
def ProduceNhitsOriginHistogram():

    nhitsOriginHisto = ROOT.TH1D("nhitsOriginHisto", "nhitsOriginHisto", 1000, 0, 1000)
	
    for ds, run in rat.dsreader("events_E=1MeV.root"):
        if ds.GetEVCount() == 0:
            continue

        mc = ds.GetMC()
        ev = ds.GetEV(0)

        if(mc.GetMCParticle(0).GetPosition().Mag() < 10):
            nhitsOriginHisto.Fill(ev.GetCalPMTs().GetCount())

    return nhitsOriginHisto

	
# Display the plots of Nhits vs. MC Radius and Nhits at AV Centre
def PlotNhitsGraphs():

    nhitsRadiusPlot = ProduceNhitsRadiusGraph()
    nhitsOriginHisto = ProduceNhitsOriginHistogram()
	
    c1 = ROOT.TCanvas()
    c1.Divide(1, 2)
    c1.cd(1)
    nhitsRadiusPlot.Draw("A*")
    c1.cd(2)
    nhitsOriginHisto.Draw()

    raw_input("Press 'Enter' to exit")

