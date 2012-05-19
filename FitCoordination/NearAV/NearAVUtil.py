#!/usr/bin/env python
import ROOT, rat
# Useful utility functions
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def ProduceEventRatios( histograms, windowStart, windowEnd ):
    """ Produces a list of ratios for the events in histograms."""
    ratios = []
    for histogram in histograms:
        ratios.append( histogram.Integral( histogram.GetXaxis().FindBin( windowStart ),  histogram.GetXaxis().FindBin( windowEnd ) ) / histogram.GetSumOfWeights() )

    return ratios

def ProduceTimeCorrectedAverageHistogram( fileName ):
    """ Produces the summed histogram from all events."""
    histograms = ProduceTimeCorrectedHistograms( fileName )
    averageHistogram = ROOT.TH1D( fileName, fileName, 500, 0.0, 500.0 )
    for histogram in histograms:
        averageHistogram.Add( histogram )

    return averageHistogram

def ProduceTimeCorrectedHistograms( fileName ):
    """ Produces histograms of the PMTCal hit times, corrected such that
    the first bin with more than 3 hits lies at 250ns."""
    histograms = []
    for ds in rat.dsreader( fileName ):
        if( ds.GetEVCount() == 0 ):
            continue
        eventHistogram = ROOT.TH1D( fileName + str( len( histograms ) ) , fileName + str( len( histograms ) ), 500, 0.0, 500.0 )
        eventHistogram.SetDirectory(0)
        ev = ds.GetEV( 0 )
        
        for iPMT in range( 0, ev.GetPMTCalCount() ):
            eventHistogram.Fill( ev.GetPMTCal( iPMT ).GetTime() )

        # No add to the list after correction
        try:
            histograms.append( TimeCorrectHistogram( eventHistogram ) )
        except NameError:
            print "Negative offset, event ignored." 

    return histograms

def TimeCorrectHistogram( histogram ):
    """ Corrects the histogram such that the first bin with more than 3 hits lies at 250ns."""

    riseBin = histogram.FindFirstBinAbove( 3.0 )
    offset = riseBin - histogram.GetXaxis().FindBin( 250.0 )
    if( offset < 0 ):
        raise NameError( "Negative offset, " + str( offset ) )
    for bin in range( 1, histogram.GetNbinsX() + 1 ): # 0 is underflow, Nbins+1 is overflow
        oldBin = bin + offset;
        if( oldBin < 1 or oldBin > histogram.GetNbinsX() ):
            histogram.SetBinContent( bin, 0.0 )
        else:
            histogram.SetBinContent( bin, histogram.GetBinContent( oldBin ) );

    return histogram
