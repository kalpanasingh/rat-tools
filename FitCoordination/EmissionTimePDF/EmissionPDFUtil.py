#!/usr/bin/env python
import string, ROOT, rat, math
# Useful utility functions
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def ProducePDF():
	""" Produce a pdf of the photon emission times."""

	emissionTimes = ROOT.TH1D( "emissionTime", "emissionTime", 600, -100.5, 499.5 )
	eventNum = 0
	for ds, run in rat.dsreader( "Tracks.root" ):
		print eventNum
		eventNum += 1
		mc = ds.GetMC()
		startTime = mc.GetMCParticle(0).GetTime()
		startPos = mc.GetMCParticle(0).GetPosition()
		for iTrack in range( 0, mc.GetMCTrackCount() ):
			# Only Photons here
			track = mc.GetMCTrack( iTrack )
			if( track.GetPDGCode() != 0 ):
				continue
			emissionTimes.Fill( track.GetMCTrackStep(0).GetGlobalTime() )


	c = 1.6
	N = 1.0 / ( c * math.sqrt( 2.0 * math.pi ) ) # Normalisation factor
	convolved = ROOT.TH1D( "emissionTime", "emissionTime", 600, -100.5, 499.5 )
	for iBin in range( 1, 601 ):
		hVal = convolved.GetBinContent( iBin )
		for iBin2 in range( 1, 601 ):
			diff = convolved.GetBinCenter( iBin ) - convolved.GetBinCenter( iBin2 )
			if diff > -100.5 and diff < 499.5:
				hVal = hVal + emissionTimes.GetBinContent( iBin2 ) * N * math.exp( -( diff - 0.0 )**2 / ( 2.0 * c * c ) )
				convolved.SetBinContent( iBin, hVal )

	convolved.Scale( 1.0 / emissionTimes.GetSumOfWeights() )

	return convolved
