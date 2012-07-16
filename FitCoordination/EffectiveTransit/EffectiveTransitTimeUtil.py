#!/usr/bin/env python
# Useful utility functions
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>
import ROOT
import rat

posSet = [ 0.0, 1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 5500.0, 5600.0, 5700.0, 5800.0, 5900.0 ] # 11

def UpdateData( filename, fullPlot ):
    """ Open one of the data files and extract the transit time difference between forward and backward
    photons. Consider those within 10degrees of the event axis only."""
    run = rat.runreader( filename )
    straightPath = run.GetStraightLinePath()
    groupVeloTime = run.GetGroupVelocityTime()
    pmtProp = run.GetPMTProp()

    eventNum = 0
    for ds in rat.dsreader( filename ):
        if( eventNum % 100  == 0 ):
            print eventNum
        eventNum += 1
        mc = ds.GetMC()
        startTime = mc.GetMCParticle(0).GetTime()
        startPos = mc.GetMCParticle(0).GetPos()
        for iPMT in range( 0, mc.GetMCPMTCount() ):
            mcPMT = mc.GetMCPMT( iPMT )
            endPos = pmtProp.GetPos( mcPMT.GetPMTID() )
            # 10 degree forward backward limits, unless at centre
            if( startPos.Mag() > 500.0 and startPos.Dot( endPos ) < 0.985 and startPos.Dot( endPos ) > -0.985 ):
                continue
            for iPhoton in range( 0, mcPMT.GetMCPhotonCount() ):
                mcPhoton = mcPMT.GetMCPhoton( iPhoton )
                scintDist = ROOT.Double()
                avDist = ROOT.Double()
                waterDist = ROOT.Double()
                straightPath.CalcByPosition( startPos, endPos, scintDist, avDist, waterDist )
                transitTime = groupVeloTime.CalcByDistance( 0.0, avDist, waterDist )
                fullPlot.Fill( scintDist, mcPhoton.GetHitTime() - startTime - transitTime )
    return

def ProduceAllData():
    """ Run over all the files and produce the transit time data."""
    fullPlot = ROOT.TH2D( "FullTimes", "Dist V Residual Time (no water or AV)", 1200, 0.0, 12000.0, 400, -100.5, 299.5 )
    
    for pos in posSet:
        outFileName = "P%.0f.root" % pos
        print outFileName
        UpdateData( outFileName, fullPlot )

    promptPlot = ROOT.TH1D( "PromptTimes", "Dist V Scint TransitTime", 1200, 0.0, 12000.0 );
    for iBin in range( 2, 1200 ):
        temp = fullPlot.ProjectionY( "Temp", iBin, iBin )
        temp.SetDirectory( 0 )
        #promptBin = temp.FindFirstBinAbove( 0.5 * temp.GetMaximum() )
        promptBin = temp.GetMaximumBin()
        promptPlot.Fill( fullPlot.GetXaxis().GetBinCenter( iBin ), fullPlot.GetYaxis().GetBinCenter( promptBin ) )
    
    return [ fullPlot, promptPlot ]


def ProduceProfile():
    """ Old, obsolete profile method."""
    profile = ROOT.TProfile( "hDistVTime", "Transit Dist v time (mm)", 120, 0, 12000.0, -50.0, 450.0, "s");
    for pos in posSet:
        outFileName = "P%.0f.root" % pos
        print outFileName
        UpdateProfile( outFileName, profile )

    return profile

def UpdateProfile( filename, profile ):
    """ Old, obsolete profile method."""
    run = rat.runreader( filename )
    straightPath = run.GetStraightLinePath()
    groupVeloTime = run.GetGroupVelocityTime()
    pmtProp = run.GetPMTProp()
    
    eventNum = 0
    for ds in rat.dsreader( filename ):
        if( eventNum % 100  == 0 ):
            print eventNum
        eventNum += 1
        mc = ds.GetMC()
        startTime = mc.GetMCParticle(0).GetTime()
        startPos = mc.GetMCParticle(0).GetPos()
        for iPMT in range( 0, mc.GetMCPMTCount() ):
            mcPMT = mc.GetMCPMT( iPMT )
            endPos = pmtProp.GetPos( mcPMT.GetPMTID() )
            # 10 degree forward backward limits, no centre pos condieration
            if( startPos.Mag() > 500.0 and startPos.Dot( endPos ) < 0.985 and startPos.Dot( endPos ) > -0.985 ):
                continue
            for iPhoton in range( 0, mcPMT.GetMCPhotonCount() ):
                mcPhoton = mcPMT.GetMCPhoton( iPhoton )
                scintDist = ROOT.Double()
                avDist = ROOT.Double()
                waterDist = ROOT.Double()
                straightPath.CalcByPosition( startPos, endPos, scintDist, avDist, waterDist )
                transitTime = groupVeloTime.CalcByDistance( 0.0, avDist, waterDist )
                profile.Fill( scintDist, scintDist / ( mcPhoton.GetHitTime() - startTime - transitTime ) )
                
    return
        
