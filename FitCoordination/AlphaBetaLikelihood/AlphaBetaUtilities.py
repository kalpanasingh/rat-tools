import ROOT, rat, sys

ParticleNames = {"212":["Bi212","Po212","Te130"],"214":["Bi214","Po214","Te130"]}
PulseDescriptions = ["wPSD","NoPSD","SeansPSD"]
ParticlePulseDict= {"Bi212":[""],"Bi214":[""],"Te130":[""],"Po212":PulseDescriptions,"Po214":PulseDescriptions}
PulseTimeConstants= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"-4.6d, -18d, -156d,",PulseDescriptions[2]:"-3.2d,-18d,-172d,"}
PulseTimeRatios= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"0.71d, 0.22d, 0.07d,",PulseDescriptions[2]:"0.61d,0.28d,0.11d,"}

#Creates a normalized time residual PDF for a given root file.
def ProduceTimeResidualPDF(filename):
    Histogram = ROOT.TH1D(filename,"",1400,-300,1000)
    for ds,run in rat.dsreader(filename):
        groupVelocity = rat.utility().GetGroupVelocity()
        lightPath = rat.utility().GetLightPathCalculator()
        pmtInfo = rat.utility().GetPMTInfo()
        if ds.GetEVCount() > 0:
            ev = ds.GetEV(0)
            rmc = ds.GetMC()
            mcParticle = rmc.GetMCParticle(0);
            mcPos = mcParticle.GetPosition();
            fitTime = mcParticle.GetTime()
            fitVertex = ev.GetFitResult("scintFitter").GetVertex(0)
            fitTime = fitVertex.GetTime()
            calPMTs = ev.GetCalPMTs()
            for iPMT in range(0,calPMTs.GetCount()):
                pmt = calPMTs.GetPMT(iPMT)
                pmtPos = pmtInfo.GetPosition(pmt.GetID())
                pmtTime = pmt.GetTime()
                distInScint = ROOT.Double()
                distInAV = ROOT.Double()
                distInWater = ROOT.Double()
                lightPath.CalcByPosition(mcPos,pmtPos)
                distInScint = lightPath.GetDistInScint()
                distInAv = lightPath.GetDistInAV()
                distInWater = lightPath.GetDistInWater()
                flightTime = groupVelocity.CalcByDistance(distInScint,distInAV,distInWater)
                timeResidual = pmtTime - flightTime - fitTime
                Histogram.Fill(timeResidual)
    Histogram.Scale(1.0/Histogram.Integral())
    pdfVector = []
    for i in range(1,Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    return pdfVector
#Outputs 3 pdfs in the same format as in CLASSIFIER_ALPHA_BETA_LIKELIHOOD.ratdb
def OutputFileChunk(pdfList, options, description,f):#pdfList must be in the follwing order [Bi,Po,Te130]
    pdfNames = ["beta_probability","alpha_probability","two_beta_probability"]
    f.write("{\n")
    f.write("name: \"LIKELIHOOD_Bi"+options.particle+"_"+description+"\",\n")
    f.write("index: \""+options.scintMaterial+"\",\n")
    f.write("valid_begin: [0,0],\n")
    f.write("valid_end: [0,0],\n")
   
    f.write("times: [")
    for time in range(-300,1000):
       f.write(str(time)+"d, ")
    f.write("],\n")
    for pdfIndex,pdf in enumerate(pdfList):
        f.write(str(pdfNames[pdfIndex]) + ": [")
        for pdfIndex,pdfValue in enumerate(pdf):
            f.write(str(pdfValue)+"d, ")
        f.write("],\n")
    f.write("}\n")

