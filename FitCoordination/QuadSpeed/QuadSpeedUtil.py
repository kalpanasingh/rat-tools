#!/usr/bin/env python
# Useful utility functions
# Author I Coulter - 09/11/2012
import ROOT
import rat 

transitTime = [ 170.0, 175.0, 180.0, 185.0, 190.0, 195.0, 200.0,]
fiducialCut = 5500

def UpdateData( filename ):
    #run = rat.runreader( filename )
    biasPlot = ROOT.TH1D( "RadialBias", "RadialBias", 200, -1000.0, 1000.0, )
    biasFit = ROOT.TF1("fitr","gaus",-1000.0,1000.0)
    eventNum = 0
    for ds in rat.dsreader( filename ):
        eventNum += 1
        evc = ds.GetEVCount()
        if(evc):
            mc = ds.GetMC()
            ev = ds.GetEV(0)
            startTime = mc.GetMCParticle(0).GetTime()
            startPos = mc.GetMCParticle(0).GetPos()
        
            try:
                fitPos = ev.GetFitResult("quad").GetVertex(0).GetPosition()
                radial = (fitPos-startPos).Dot(startPos.Unit())
                if(fitPos.Mag()<fiducialCut):
                    biasPlot.Fill(radial)
            except:
                pass

    biasPlot.Fit(biasFit)
    return biasFit.GetParameter(1)

def ProduceAllData():
    """ Run over all the files and produce the transit time data."""
    fullPlot = ROOT.TH2D( "FullSpeed", "RadialBias V EffectiveSpeed", 2000, -1000.0, 1000.0, 150, 100, 250)
    oneDPlot = ROOT.TH1D( "oneDTimes", "RadialBias V EffectiveSpeed in One Dim", 2000, -1000.0, 1000.0 );
    
    for speed in transitTime:
        outFileName = "quad_%.0f.root" % speed
        print outFileName
        mean=0
        mean = UpdateData( outFileName )
        print speed
        print mean
        fullPlot.Fill(mean,speed)
        oneDPlot.Fill(mean,speed)

    return [ fullPlot, oneDPlot ]