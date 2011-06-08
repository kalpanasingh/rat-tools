#!/usr/bin/env python
import string, ROOT, rat
# Useful utility functions
# Author P G Jones - 22/05/2011 <p.jones22@physics.ox.ac.uk>

def ProduceRefractiveIndexHistograms():
	""" Produces the effective refractive index histograms for scint, av, and water 400 +- 10nm."""

	# Initialise the refractive index lists
	scintR = ROOT.TH1D( "scintR", "scintR", 1000, 1.0, 2.0 )
	avR = ROOT.TH1D( "avR", "avR", 1000, 1.0, 2.0 )
	waterR = ROOT.TH1D( "waterR", "waterR", 1000, 1.0, 2.0 )

	for ds in rat.dsreader( "Tracks.root" ):
		mc = ds.GetMC()
		for iTrack in range( 0, mc.GetMCTrackCount() ):
			track = mc.GetMCTrack( iTrack )
			firstStep = track.GetMCTrackStep(0)
			# Check track is a photon and has wavelength 400 +- 10nm
			if( track.GetPDGCode() != 0 or abs( MeVToLambda( firstStep.GetKE() ) - 400 ) > 10 ):
				continue
			# Initialise the transit variables
			startTScint = firstStep.GetGlobalTime()
			endTScint = -1
			startTAV = -1
			endTAV = -1
			startTWater = -1
			endTWater = -1
			startPosScint = firstStep.GetEndPos()
			endPosScint = ROOT.TVector3()
			startPosAV = ROOT.TVector3()
			endPosAV = ROOT.TVector3()
			startPosWater = ROOT.TVector3()
			endPosWater = ROOT.TVector3()
			
			# Now find out what the transit paths are
			for iStep in range( 0, track.GetMCTrackStepCount() ):
				step = track.GetMCTrackStep( iStep )
				if( ScintToAV( step ) and endTScint == -1 ):
					endTScint = step.GetGlobalTime()
					endPosScint = step.GetEndPos() # Note a - b does not work for TVector3
					startTAV = step.GetGlobalTime()
					startPosAV = step.GetEndPos()
				if( AVToWater( step ) and endTAV == -1 ):
					endTAV = step.GetGlobalTime()
					endPosAV = step.GetEndPos()
					startTWater = step.GetGlobalTime()
					startPosWater = step.GetEndPos()
				if( OutOfWater( step ) and endTWater == -1 ):
					endTWater = step.GetGlobalTime()
					endPosWater = step.GetEndPos()
	
			# Now update the refractive index list
			endPosScint -= startPosScint
			endPosAV -= startPosAV
			endPosWater -= startPosWater
			if( endTScint != -1 ):
				scintR.Fill( ( endTScint - startTScint ) / ( endPosScint.Mag() / 299.792458 ) )
			if( endTAV != -1 ):
				avR.Fill( ( endTAV - startTAV ) / ( endPosAV.Mag() / 299.792458 ) )
			if( endTWater != -1 ):
				waterR.Fill( ( endTWater - startTWater ) / ( endPosWater.Mag() / 299.792458 ) )
	# Finished extracting data now, just return result
	return [ scintR, avR, waterR ]

def MeVToLambda( energy ):
	""" Converts a MeV energy to wavelength in nm."""
	return 2 * 3.14 * 197.33 * 1e-6 / energy

def ScintToAV( step ):
	""" Returns true if step transits from scint to AV."""
	scintToAV = ( step.GetStartVolume() == "scint" ) and ( step.GetEndVolume() == "av" )
	scintToBelly = ( step.GetStartVolume() == "scint" ) and ( "belly" in step.GetEndVolume() )
	return ( scintToAV or scintToBelly ) and step.GetEndPos().Mag() > 6000.0

def AVToWater( step ):
	""" Returns true if step transits from AV to water."""
	avToWater = ( step.GetStartVolume() == "av" ) and ( "h2o" in step.GetEndVolume() )
	bellyToWater = ( "belly" in step.GetStartVolume() ) and ( "h2o" in step.GetEndVolume() )
	return avToWater or bellyToWater

def OutOfWater( step ):
	""" Returns true if step transists from Water to PSUP."""
	return ( "h2o" in step.GetStartVolume() ) and not ( "h2o" in step.GetEndVolume() ) and not ( step.GetEndVolume() == "av" ) and not ( "belly" in step.GetEndVolume() )
