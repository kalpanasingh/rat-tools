#!/usr/bin/env python
import ROOT, rat
from array import array
import math
from ROOT import RAT
import gc
# Secondary functions and user-defined values for the EnergyRSP Coordinator
# Author J Walker - 28/09/2015 <john.walker@liverpool.ac.uk>


ScintEnergies = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0] # Use these energies if using a scintillator-filled detector
WaterEnergies = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0, 38.0, 40.0] # Use these energies if using a water-filled detector
subfiles = 100


costhetaBins = 40
# Calculate edges of costheta bins
costhetaLowBins = []
for i in range(0, costhetaBins+1):
    value = -1 + (i*2.0/costhetaBins)
    costhetaLowBins.append(value)
costhetaValues = []
for i in range(0, len(costhetaLowBins)-1):
    costhetaValues.append( (costhetaLowBins[i]+costhetaLowBins[i+1])/2 )
costhetaArray = array('d',costhetaLowBins)

uDotpBins = 40
# Calculate edges of u.p' bins
uDotpLowBins = []
for i in range(0, uDotpBins+1):
    value = -1 + (i*2.0/uDotpBins)
    uDotpLowBins.append(value)
uDotpValues = []
for i in range(0, len(uDotpLowBins)-1):
    uDotpValues.append( (uDotpLowBins[i]+uDotpLowBins[i+1])/2 )
uDotpArray = array('d',uDotpLowBins)

radialBins = 20
# Calculate edges of radial bins
radialLowBins = []
for i in range(0, radialBins+1):
    value = (i*1.0/radialBins)
    radialLowBins.append(value)
radialValues = []
for i in range(0, len(radialLowBins)-1):
    radialValues.append( (radialLowBins[i]+radialLowBins[i+1])/2 )
radialArray = array('d',radialLowBins)

angularBins = 90
# Calculate edges of angular bins
angularLowBins = []
for i in range(0, angularBins+1):
    value = (i*90.0/angularBins)
    angularLowBins.append(value)
angularValues = []
for i in range(0, len(angularLowBins)-1):
    angularValues.append( (angularLowBins[i]+angularLowBins[i+1])/2 )
angularArray = array('d',angularLowBins)


# Return a list of true Cerenkov photons per Energy, and accompanying histograms, arranged as the following for "e" energies:
# { Nphotons(energy[0]), Nphotons(energy[1]), ... , Nphotons(energy[e-1]) }
def NphotonsVsEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    nPhotonsTable = []
    histograms = []

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energies[0] * 1000)) + "keV_sf=0.root")

    for energy in energies:

        if energy == energies[0]:
            continue

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root"
        print infileName

        reader.Add(infileName)

    # Create vector of histograms
    for energy in energies:
        histograms.append(ROOT.TH1D("Nphotons_" + str(int(energy * 1000)), "Nphotons", 300, 0.0, 30000.0))

    # Fill appropriate histograms with Cerenkov photons
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "NphotonsVsEnergy:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        mc = ds.GetMC()
        kineticEnergy = mc.GetMCParticle(0).GetKineticEnergy()
        histograms[energies.index(kineticEnergy)].Fill(mc.GetNCherPhotons())

    # Fill list with histogram mean values
    for Histogram in histograms:

        tolerance = 10
        lowBin = Histogram.FindFirstBinAbove(0.0)
        lowBin = lowBin - tolerance
        highBin = Histogram.FindLastBinAbove(0.0)
        highBin = highBin + tolerance
        if lowBin < 1:
            lowBin = 1
        if highBin > Histogram.GetNbinsX():
            highBin = Histogram.GetNbinsX()

        gaussFit = ROOT.TF1("gaus", "gaus", Histogram.GetBinCenter(lowBin), Histogram.GetBinCenter(highBin))
        Histogram.Fit(gaussFit, "RQN")

        nPhotonsTable.append(gaussFit.GetParameter(1))

        del gaussFit

    return nPhotonsTable, histograms

# Return the Cerenkov angular distribution for each energy, arranged as the following for "e" energies and "c" u.p's:
# { D(energy[0],u.p'[0]), D(energy[0],u.p'[1]), ... , D(energy[0],u.p'[c-1]), ...,
# D(energy[e-1],u.p'[0]), D(energy[e-1],u.p'[1]), ... , D(energy[e-1],u.p'[c-1]) }
def CerenkovAngularDist(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    angularDist = []
    histograms = []

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energies[0] * 1000)) + "keV_sf=0.root")

    for energy in energies:

        if energy == energies[0]:
            continue

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root"
        print infileName

        reader.Add(infileName)

    # Create vector of histograms
    for energy in energies:
        histograms.append(ROOT.TH1D("Nphotons_" + str(int(energy * 1000)), "Nphotons", len(costhetaValues), costhetaArray))

    # Fill appropriate histograms with angular distribution
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "CerenkovAngularDist:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        mc = ds.GetMC()
        kineticEnergy = mc.GetMCParticle(0).GetKineticEnergy()
        initialDir = mc.GetMCParticle( 0 ).GetMomentum().Unit()
        for itrack in range(0, mc.GetMCTrackCount()):
            mctrack = mc.GetMCTrack(itrack)
            if mctrack.GetPDGCode() != 0:
                continue
            initialStep = mctrack.GetMCTrackStep( 0 )
            if initialStep.GetProcess() != "Cerenkov":
                continue
            histograms[energies.index(kineticEnergy)].Fill(initialStep.GetMomentum().Unit().Dot( initialDir ))

    # Store angular distributions in list
    for Histogram in histograms:
        singleEnergyAngularDist = []
        integral = Histogram.Integral("width")
        if integral > 0:
            Histogram.Scale( 1/integral )
        for costhetaIndex, costheta in enumerate(costhetaValues):
            singleEnergyAngularDist.append(Histogram.GetBinContent( costhetaIndex+1 ))
        angularDist.append(singleEnergyAngularDist)
        del singleEnergyAngularDist

    return angularDist


# Return the probability that a Rayleigh scattered photon will be late, arranged as the following for "c" u.p's and "r" radiis:
# { R(u.p'[0],radius[0]), R(u.p'[0],radius[1]), ... , R(u.p'[0],radius[c-1]), ...,
# R(u.p'[e-1],radius[0]), R(u.p'[e-1],radius[1]), ... , R(u.p'[e-1],radius[c-1]) }
def RayleighAttenuationProb(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    attenuationProb = []

    mcphotonTrackIDs = []
    mcphotonTimes = []
    mcphotonPositions = []

    hRayleighTotal = ROOT.TH2D("hRayleighTotal", "hRayleighTotal", len(radialValues), radialArray, len(uDotpValues), uDotpArray)
    hRayleighLate = ROOT.TH2D("hRayleighLate", "hRayleighLate", len(radialValues), radialArray, len(uDotpValues), uDotpArray)

    energy = 5.0

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for subfile in range(1, subfiles):

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(subfile)) + ".root"
        print infileName

        reader.Add(infileName)

    # Loop through events
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "RayleighAttenuationProb:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()

        # Ignore events beyond inner AV
        zeroPosition = mc.GetMCParticle( 0 ).GetPosition()
        if zeroPosition.Mag() > 6005.0:
            continue

        # Store photon information from PMT hits
        for ipmt in range(0, mc.GetMCPMTCount()):
            mcpmt = mc.GetMCPMT(ipmt)
            mcpmtid = mcpmt.GetID()
            for iphoton in range(0, mcpmt.GetMCPhotonCount()):
                if iphoton != 0:
                    continue
                mcphoton = mcpmt.GetMCPhoton(iphoton)
                mcphotonTrackIDs.append(mcphoton.GetPhotonTrackID())
                mcphotonTimes.append(mcphoton.GetInTime())
                mcphotonPositions.append(pmt_info.GetPosition(mcpmtid))

        # Loop through MC tracks
        for itrack in range(0, mc.GetMCTrackCount()):
            mctrack = mc.GetMCTrack(itrack)

            # Check if track hit PMT
            mctrackID = mctrack.GetTrackID()
            if mctrackID in mcphotonTrackIDs:
                photonTime = mcphotonTimes[mcphotonTrackIDs.index(mctrackID)]
                photonPosition = mcphotonPositions[mcphotonTrackIDs.index(mctrackID)]

                # Only consider optical photons
                if mctrack.GetPDGCode() != 0:
                    continue

                initialStep = mctrack.GetMCTrackStep( 0 )

                # Only consider Cerenkov photons
                if initialStep.GetProcess() != "Cerenkov":
                    continue

                # Want tracks which Rayleigh scattered and then hit a PMT
                if mctrack.GetSummaryFlag( mctrack.OpRayleigh ) and mctrack.GetSummaryFlag( mctrack.HitPMT ):

                    # Get initial position, direction and time
                    initialPosition = initialStep.GetPosition()
                    initialDirection = initialStep.GetMomentum().Unit()
                    initialTime = initialStep.GetGlobalTime()

                    # Fill for Rayleigh scattered photons hitting a PMT
                    hRayleighTotal.Fill(math.pow(initialPosition.Mag()/6005.0,3.0), initialDirection.Dot( initialPosition.Unit() ))

                    # Calculate time residual
                    light_path.CalcByPosition(initialPosition, photonPosition)
                    inner_av_distance = light_path.GetDistInInnerAV()
                    av_distance = light_path.GetDistInAV()
                    water_distance = light_path.GetDistInWater()
                    transit_time = group_velocity.CalcByDistance(inner_av_distance, av_distance, water_distance)
                    time_residual = photonTime - transit_time - initialTime

                    # Fill for Rayleigh scattered photons hitting PMT that are late
                    if time_residual > 8 or time_residual < -10:
                        hRayleighLate.Fill(math.pow(initialPosition.Mag()/6005.0,3.0), initialDirection.Dot( initialPosition.Unit() ))

        del mcphotonTrackIDs[:]
        del mcphotonTimes[:]
        del mcphotonPositions[:]

    # Divide to find fraction of Rayleigh scattered photons that are late
    hRayleighLate.Divide(hRayleighTotal)

    Attenuation = []
    for binj in range(0, len(uDotpValues)):
        singleuDotpAttenuation = []
        for bini in range(0, len(radialValues)):
            singleuDotpAttenuation.append(hRayleighLate.GetBinContent( bini+1, binj+1 ))
        Attenuation.append(singleuDotpAttenuation)

    del hRayleighLate
    del hRayleighTotal

    return Attenuation


# Return the PMT angular response, arranged as the following for "c" costhetas:
# { R(costheta[0]), R(costheta[1]), ... , R(costheta[c-1]) }
# Prompt hits only. MC angle.
def PMTAngularResponse(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    hHitsMC = ROOT.TH1D("hHitsMC", "PMT hits as function of mc angle", len(angularValues), angularArray)
    hResponseMCandOptics = ROOT.TH1D("hResponseMCandOptics", "PMT response from Optics with MC for tail", len(angularValues), angularArray)

    energy = 5.0

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for subfile in range(1, subfiles):

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(subfile)) + ".root"
        print infileName

        reader.Add(infileName)

    # Loop through events
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PMTAngularResponse:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()

        # Get MC event position and time
        initialPosition = mc.GetMCParticle( 0 ).GetPosition()
        initialTime = mc.GetMCParticle( 0 ).GetTime()

        # Ignore events beyond inner AV
        if initialPosition.Mag() > 6005.0:
            continue

        # Loop through PMTs
        for iPMT in range(0, mc.GetMCPMTCount()):
            mcPMT = mc.GetMCPMT( iPMT )

            # Only consider "normal" PMTs
            pmtID = mcPMT.GetID()
            if pmt_info.GetType( pmtID ) != pmt_info.NORMAL:
                continue

            # Calculate transit time and angle with PMT as calculated by light_path
            light_path.CalcByPosition(initialPosition, pmt_info.GetPosition(mcPMT.GetID()))
            inner_av_distance = light_path.GetDistInInnerAV()
            av_distance = light_path.GetDistInAV()
            water_distance = light_path.GetDistInWater()
            transit_time = group_velocity.CalcByDistance(inner_av_distance, av_distance, water_distance)

            # PMT direction in PMT local coordinates
            pmtDirection = ROOT.TVector3( 0.0, 0.0, -1.0 );

            # Loop through photons
            for iPhoton in range(0, mcPMT.GetMCPhotonCount()):
                mcPhoton = mcPMT.GetMCPhoton( iPhoton )

                # Calculate time residual
                lastTime = mcPhoton.GetInTime()
                time_residual = lastTime - transit_time - initialTime

                # Check in position not beyond radius of PMT
                xyRadius = math.sqrt( mcPhoton.GetInPosition().X() * mcPhoton.GetInPosition().X() + mcPhoton.GetInPosition().Y() * mcPhoton.GetInPosition().Y() )
                if mcPhoton.GetInPosition().Z() < 132.0 or xyRadius > 137.0:
                    continue

                # Get true photon incident angle with PMT
                mc_angle = ROOT.TMath.ACos( mcPhoton.GetInDirection().Dot( pmtDirection ) ) * ROOT.TMath.RadToDeg();

                # Fill if photon is prompt
                if time_residual > -10 and time_residual < 8:
                    hHitsMC.Fill( mc_angle )

                    # Fill if photon results in a photoelectron
                    if mcPhoton.GetFate() == mcPhoton.ePhotoelectron:
                        hResponseMCandOptics.Fill( mc_angle )

    # Divide to find fraction of prompt photons resulting in a photoelectron
    hHitsMC.Sumw2()
    hResponseMCandOptics.Sumw2()
    hResponseMCandOptics.Divide( hHitsMC )

    # The output of an optics fit for the PMT angular response - hard coded for now!!!!!
    optics_values = [ 1, 1.00116, 1.00281, 1.00426, 1.00861, 1.01179, 1.01551, 1.01972, 1.02457, 1.02928, 1.03309, 1.03827, 1.04423, 1.04904, 1.056, 1.06018, 1.06401, 1.06884, 1.07541, 1.08086, 1.08649, 1.09198, 1.09905, 1.10051, 1.10806, 1.111, 1.11984, 1.12772, 1.13161, 1.13924, 1.13904, 1.14615, 1.14351, 1.14567, 1.1315, 1.14798, 1.12914, 1.12197, 1.12262, 1.11159, 1.11434, 1.11812, 1.12082, 1.10308, 1.07932, 1.09548, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]

    optics_errors = [ 0, 0.000545447, 0.000508987, 0.000516206, 0.000522549, 0.000993215, 0.000962659, 0.000909435, 0.000880224, 0.00086217, 0.000823764, 0.000812432, 0.00080622, 0.000805476, 0.00080843, 0.000835871, 0.000862054, 0.000897842, 0.000939236, 0.000964726, 0.000969903, 0.00097783, 0.000985927, 0.00103344, 0.00107909, 0.00114315, 0.00124654, 0.00131553, 0.00133006, 0.00135414, 0.0013889, 0.00145807, 0.00151927, 0.00164041, 0.00173792, 0.00186205, 0.00186791, 0.0019548, 0.00203682, 0.00210602, 0.00223987, 0.00236149, 0.00245823, 0.00264676, 0.00323336, 0.00568283, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    # Get values by which to scale
    # Use average of last five bins to scale the MC tail to optics fit
    hResponseMCandOptics_av_value = hResponseMCandOptics.GetBinContent( 39 )
    for i in range(40, 44):
        hResponseMCandOptics_av_value += hResponseMCandOptics.GetBinContent( i )
    hResponseMCandOptics_av_value /= 5.0

    optics_av_value = optics_values[38]
    for i in range(39, 43):
        optics_av_value += optics_values[i]
    optics_av_value /= 5.0

    # Scale response so the MC and optics fit overlap
    hResponseMCandOptics.Scale( optics_av_value/hResponseMCandOptics_av_value )

    # Replace MC values with optics fit for first 43 bins
    for bin in range(1, 44):
        hResponseMCandOptics.SetBinContent( bin, optics_values[bin-1] )

    for bin in range(1, 44):
        hResponseMCandOptics.SetBinError( bin, optics_errors[bin-1] )

    angularResponse = []
    for bin in range(0, angularBins):
        angularResponse.append( hResponseMCandOptics.GetBinContent( bin+1 ) )

    del hResponseMCandOptics
    del hHitsMC

    return angularResponse


##### DIAGNOSTIC FUNCTIONS #####

# Return a true Cerenkov photons vs. Energy plot
def PlotMeanNphotonsPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    nPhotonsTable = NphotonsVsEnergy(material)[0]

    graph = ROOT.TGraph()
    for energyIndex, energy in enumerate(energies):
        graph.SetPoint(energyIndex, energy, nPhotonsTable[energyIndex])

    canvas = ROOT.TCanvas()
    graph.Draw("A*")
    graph.GetYaxis().SetTitle("Cerenkov photons")
    graph.GetXaxis().SetTitle("Energy [MeV]")
    canvas.SaveAs("MeanNphotonsPerEnergy.eps")
    canvas.SaveAs("MeanNphotonsPerEnergy.root")

    raw_input("Press 'Enter' to exit")


# Return a set of true Cerenkov photons distribution plots (one for each Energy)
def PlotNphotonsPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    histList = NphotonsVsEnergy(material)[1]

    canvas = ROOT.TCanvas()
    canvas.Divide(2, len(energies) / 2)
    for histIndex, hist in enumerate(histList):
        canvas.cd(histIndex + 1)
        hist.Draw()
    canvas.SaveAs("NphotonsPerEnergy.eps")
    canvas.SaveAs("NphotonsPerEnergy.root")

    raw_input("Press 'Enter' to exit")


# Return Cerenkov angular distribution map
def PlotCerenkovAngularDist(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    angularDist = CerenkovAngularDist(material)

    energyLowBins = [energies[0]-(energies[1]-energies[0])/2]
    for i in range(1,len(energies)):
        energyLowBins.append( (energies[i-1]+energies[i])/2 )
    energyLowBins.append( energies[-1]+(energies[-1]-energies[-2])/2 )
    energyArray = array('d',energyLowBins)

    hist = ROOT.TH2D("Cerenkov_angular_dist","Cerenkov_angular_dist",len(costhetaValues),costhetaArray,len(energies),energyArray)

    for energyIndex, energy in enumerate(energies):
        for costhetaIndex, costheta in enumerate(costhetaValues):
            hist.SetBinContent( costhetaIndex+1, energyIndex+1, angularDist[energyIndex][costhetaIndex] )

    hist.SetContour(500);
    canvas = ROOT.TCanvas()
    hist.Draw("colz")
    hist.GetYaxis().SetTitle("Energy [MeV]")
    hist.GetXaxis().SetTitle("u.p'")
    canvas.SaveAs("CerenkovAngularDist.eps")
    canvas.SaveAs("CerenkovAngularDist.root")

    raw_input("Press 'Enter' to exit")


# Return a set of Cerenkov angular distribution plots (one for each Energy)
def PlotCerenkovAngularDistPerEnergy(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    angularDist = CerenkovAngularDist(material)

    graphsList = []

    for energyIndex, energy in enumerate(energies):
        graph = ROOT.TGraph()
        for costhetaIndex, costheta in enumerate(costhetaValues):
            graph.SetPoint(costhetaIndex, costheta, angularDist[energyIndex][costhetaIndex])
        graphsList.append(graph)

    canvas = ROOT.TCanvas()
    canvas.Divide(2, len(energies) / 2)
    for graphIndex, graph in enumerate(graphsList):
        canvas.cd(graphIndex + 1)
        graph.Draw("A*")
        graph.GetXaxis().SetRangeUser(-1.0, 1.0)
        graph.GetYaxis().SetTitle("Scale factor")
        graph.GetXaxis().SetTitle("u.p'")
    canvas.SaveAs("CerenkovAngularDistPerEnergy.eps")
    canvas.SaveAs("CerenkovAngularDistPerEnergy.root")

    raw_input("Press 'Enter' to exit")


# Return Rayleigh attenuation probability plot
# Probability that a Rayleigh scattered photon will be late
def PlotRayleighAttenuationProb(material):

    attenuationProb = RayleighAttenuationProb(material)

    hist = ROOT.TH2D("hist", "Rayleigh Attenuation Probability", len(radialValues), radialArray, len(uDotpValues), uDotpArray)

    for binj in range(0,len(uDotpValues)):
        for bini in range(0,len(radialValues)):
            hist.SetBinContent( bini+1, binj+1, attenuationProb[binj][bini] )

    hist.SetContour(500);
    canvas = ROOT.TCanvas()
    hist.Draw("colz")
    hist.GetXaxis().SetTitle("|r|")
    hist.GetYaxis().SetTitle("p'.r")
    canvas.SaveAs("RayleighAttenuationProb.eps")
    canvas.SaveAs("RayleighAttenuationProb.root")

    raw_input("Press 'Enter' to exit")


# Return PMT angular response plot
def PlotPMTAngularResponse(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)

    angularResponse = PMTAngularResponse(material)

    graph = ROOT.TGraph()
    for angleIndex, angle in enumerate(angularValues):
        graph.SetPoint(angleIndex, angle, angularResponse[angleIndex])

    canvas = ROOT.TCanvas()
    graph.Draw("A*")
    graph.GetYaxis().SetTitle("PMT response")
    graph.GetXaxis().SetTitle("Angle [degrees]")
    canvas.SaveAs("PMTAngularResponse.eps")
    canvas.SaveAs("PMTAngularResponse.root")

    raw_input("Press 'Enter' to exit")


# Return the distributions used to create the PMT angular response
# The optics fit for the first 43 bins, then the MC angular response
# Angular response using angle from light path shown for validation
def PlotPMTAngularResponseInternals(material):

    # Select which energies to use based on the material in the detector
    energies = []
    if material == "lightwater_sno":
        energies = WaterEnergies
    else:
        energies = ScintEnergies

    hResponseLP = ROOT.TH1D("hResponseLP", "PMT response as function of lp angle", len(angularValues), angularArray)
    hHitsLP = ROOT.TH1D("hHitsLP", "PMT hits as function of lp angle", len(angularValues), angularArray)
    hResponseMC = ROOT.TH1D("hResponseMC", "PMT response as function of mc angle", len(angularValues), angularArray)
    hHitsMC = ROOT.TH1D("hHitsMC", "PMT hits as function of mc angle", len(angularValues), angularArray)
    hResponseOptics = ROOT.TH1D("hResponseOptics", "PMT response from Optics", len(angularValues), angularArray)
    hResponseMCandOptics = ROOT.TH1D("hResponseMCandOptics", "PMT response from Optics with MC for tail", len(angularValues), angularArray)

    energy = 5.0

    # Read in ROOT files
    reader = RAT.DU.DSReader(material + "_E=" + str(int(energy * 1000)) + "keV_sf=0.root")

    for subfile in range(1, subfiles):

        infileName = material + "_E=" + str(int(energy * 1000)) + "keV_sf=" + str(int(subfile)) + ".root"
        print infileName

        reader.Add(infileName)

    # Loop through events
    for ievent in range(0, reader.GetEntryCount()):
        if ievent % 100 == 0:
            print "PMTAngularResponse:: " + str(ievent) + " : " + str(reader.GetEntryCount())

        ds = reader.GetEntry(ievent)
        light_path = rat.utility().GetLightPathCalculator()
        group_velocity = rat.utility().GetGroupVelocity()
        pmt_info = rat.utility().GetPMTInfo()
        mc = ds.GetMC()

        # Get MC event position and time
        initialPosition = mc.GetMCParticle( 0 ).GetPosition()
        initialTime = mc.GetMCParticle( 0 ).GetTime()

        # Ignore events beyond inner AV
        if initialPosition.Mag() > 6005.0:
            continue

        # Loop through PMTs
        for iPMT in range(0, mc.GetMCPMTCount()):
            mcPMT = mc.GetMCPMT( iPMT )

            # Only consider "normal" PMTs
            pmtID = mcPMT.GetID()
            if pmt_info.GetType( pmtID ) != pmt_info.NORMAL:
                continue

            # Calculate transit time and angle with PMT as calculated by light_path
            light_path.CalcByPosition(initialPosition, pmt_info.GetPosition(mcPMT.GetID()))
            light_path.CalculateSolidAngle( pmt_info.GetDirection(mcPMT.GetID()), 0 )

            inner_av_distance = light_path.GetDistInInnerAV()
            av_distance = light_path.GetDistInAV()
            water_distance = light_path.GetDistInWater()

            transit_time = group_velocity.CalcByDistance(inner_av_distance, av_distance, water_distance)

            lp_costheta = -1.0 * light_path.GetCosThetaAvg()
            lp_angle = ROOT.TMath.ACos( lp_costheta ) * ROOT.TMath.RadToDeg();

            # PMT direction in PMT local coordinates
            pmtDirection = ROOT.TVector3( 0.0, 0.0, -1.0 );

            # Loop through photons
            for iPhoton in range(0, mcPMT.GetMCPhotonCount()):
                mcPhoton = mcPMT.GetMCPhoton( iPhoton )

                # Calculate time residual
                lastTime = mcPhoton.GetInTime()
                time_residual = lastTime - transit_time - initialTime

                # Check in position not beyond radius of PMT
                xyRadius = math.sqrt( mcPhoton.GetInPosition().X() * mcPhoton.GetInPosition().X() + mcPhoton.GetInPosition().Y() * mcPhoton.GetInPosition().Y() )
                if mcPhoton.GetInPosition().Z() < 132.0 or xyRadius > 137.0:
                    continue

                # Get true photon incident angle with PMT
                mc_angle = ROOT.TMath.ACos( mcPhoton.GetInDirection().Dot( pmtDirection ) ) * ROOT.TMath.RadToDeg();

                # Fill if photon is prompt
                if time_residual > -10 and time_residual < 8:
                    hHitsLP.Fill( lp_angle )
                    hHitsMC.Fill( mc_angle )

                    # Fill if photon results in a photoelectron
                    if mcPhoton.GetFate() == mcPhoton.ePhotoelectron:
                        hResponseLP.Fill( lp_angle )
                        hResponseMC.Fill( mc_angle )
                        hResponseMCandOptics.Fill( mc_angle )

    # Divide to find fraction of prompt photons resulting in a photoelectron
    hHitsLP.Sumw2()
    hResponseLP.Sumw2()
    hHitsMC.Sumw2()
    hResponseMC.Sumw2()
    hResponseMCandOptics.Sumw2()
    hResponseLP.Divide( hHitsLP )
    hResponseMC.Divide( hHitsMC )
    hResponseMCandOptics.Divide( hHitsMC )

    # The output of an optics fit for the PMT angular response - hard coded for now!!!!!
    optics_values = [ 1, 1.00116, 1.00281, 1.00426, 1.00861, 1.01179, 1.01551, 1.01972, 1.02457, 1.02928, 1.03309, 1.03827, 1.04423, 1.04904, 1.056, 1.06018, 1.06401, 1.06884, 1.07541, 1.08086, 1.08649, 1.09198, 1.09905, 1.10051, 1.10806, 1.111, 1.11984, 1.12772, 1.13161, 1.13924, 1.13904, 1.14615, 1.14351, 1.14567, 1.1315, 1.14798, 1.12914, 1.12197, 1.12262, 1.11159, 1.11434, 1.11812, 1.12082, 1.10308, 1.07932, 1.09548, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]

    optics_errors = [ 0, 0.000545447, 0.000508987, 0.000516206, 0.000522549, 0.000993215, 0.000962659, 0.000909435, 0.000880224, 0.00086217, 0.000823764, 0.000812432, 0.00080622, 0.000805476, 0.00080843, 0.000835871, 0.000862054, 0.000897842, 0.000939236, 0.000964726, 0.000969903, 0.00097783, 0.000985927, 0.00103344, 0.00107909, 0.00114315, 0.00124654, 0.00131553, 0.00133006, 0.00135414, 0.0013889, 0.00145807, 0.00151927, 0.00164041, 0.00173792, 0.00186205, 0.00186791, 0.0019548, 0.00203682, 0.00210602, 0.00223987, 0.00236149, 0.00245823, 0.00264676, 0.00323336, 0.00568283, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    for index, value in enumerate(optics_values):
        hResponseOptics.SetBinContent( index+1, value )

    for index, error in enumerate(optics_errors):
        hResponseOptics.SetBinError( index+1, error )

    # Get values by which to scale
    # Use average of last five bins to scale the MC tail to optics fit
    hResponseLP_first_value = hResponseLP.GetBinContent( 1 )
    hResponseMC_first_value = hResponseMC.GetBinContent( 1 )

    hResponseMCandOptics_av_value = hResponseMCandOptics.GetBinContent( 39 )
    for i in range(40, 44):
        hResponseMCandOptics_av_value += hResponseMCandOptics.GetBinContent( i )
    hResponseMCandOptics_av_value /= 5.0

    optics_av_value = optics_values[38]
    for i in range(39, 43):
        optics_av_value += optics_values[i]
    optics_av_value /= 5.0

    # Scale responses to start at 1 and so the MC and optics fit overlap
    hResponseLP.Scale( 1.0/hResponseLP_first_value )
    hResponseMC.Scale( 1.0/hResponseMC_first_value )
    hResponseMCandOptics.Scale( optics_av_value/hResponseMCandOptics_av_value )

    # Replace MC values with optics fit for first 43 bins
    for bin in range(1, 44):
        hResponseMCandOptics.SetBinContent( bin, optics_values[bin-1] )

    for bin in range(1, 44):
        hResponseMCandOptics.SetBinError( bin, optics_errors[bin-1] )

    canvas = ROOT.TCanvas()
    hResponseLP.GetXaxis().SetTitle( "angle [degrees]" )
    hResponseLP.SetTitle( "PMT angular response" )
    hResponseLP.SetLineColor( ROOT.kRed+1 )
    hResponseLP.SetMinimum( 0.0 )
    hResponseLP.Draw()
    hResponseMC.SetLineColor( ROOT.kGreen+1 )
    hResponseMC.Draw("SAME")
    hResponseOptics.SetLineColor( ROOT.kBlue+1 )
    hResponseOptics.Draw("SAME")
    hResponseMCandOptics.SetLineColor( ROOT.kBlack )
    hResponseMCandOptics.Draw("SAME")
    t1 = ROOT.TLegend(0.7, 0.7, 0.88, 0.88)
    t1.AddEntry(hResponseLP, "mc: light path", "l")
    t1.AddEntry(hResponseMC, "mc: truth", "l")
    t1.AddEntry(hResponseOptics, "optics fit", "l")
    t1.AddEntry(hResponseMCandOptics, "optics fit w/ MC tail", "l")
    t1.SetLineColor(ROOT.kWhite)
    t1.SetFillColor(ROOT.kWhite)
    t1.Draw()
    canvas.Update()
    canvas.SaveAs("PMTAngularResponseInternals.eps")
    canvas.SaveAs("PMTAngularResponseInternals.root")

    raw_input("Press 'Enter' to exit")


ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetCanvasBorderMode(0)
ROOT.gStyle.SetPadBorderMode(0)
ROOT.gStyle.SetPadColor(0)
ROOT.gStyle.SetCanvasColor(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
