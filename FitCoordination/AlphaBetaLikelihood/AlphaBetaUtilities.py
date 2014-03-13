import ROOT, rat, sys

ParticleNames = {"212":["Bi212","Po212","Te130"],"214":["Bi214","Po214","Te130"]}
PulseDescriptions = ["wPSD","NoPSD","SeansPSD"]
ParticlePulseDict= {"Bi212":[""],"Bi214":[""],"Te130":[""],"Po212":PulseDescriptions}
PulseTimeConstants= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"-4.6d, -18d, -156d,",PulseDescriptions[2]:"-3.2d,-18d,-172d,"}
PulseTimeRatios= {"":"",PulseDescriptions[0]:"",PulseDescriptions[1]:"0.71d, 0.22d, 0.07d,",PulseDescriptions[2]:"0.61d,0.28d,0.11d,"}

def ProduceTimeResidualPDF(filename):
    Histogram = ROOT.TH1D(filename,"",1100,-100,1000)
    for ds,run in rat.dsreader(filename):
        effectiveTime = run.GetEffectiveVelocityTime()
        lightPath = run.GetLightPath()
        pmtProp = run.GetPMTProp()
        if ds.GetEVCount() > 0:
            ev = ds.GetEV(0)
            fitVertex = ev.GetFitResult("scintFitter").GetVertex(0)
            fitPos = fitVertex.GetPosition()
            fitTime = fitVertex.GetTime()
            for iPMT in range(0,ev.GetPMTCalCount()):
                pmt = ev.GetPMTCal(iPMT)
                pmtPos = pmtProp.GetPos(pmt.GetID())
                pmtTime = pmt.GetTime()
                distInScint = ROOT.Double()
                distInAV = ROOT.Double()
                distInWater = ROOT.Double()
                lightPath.CalcByPosition(fitPos,pmtPos,distInScint,distInAV,distInWater)
                flightTime = effectiveTime.CalcByDistance(distInScint,distInAV,distInWater)
                timeResidual = pmtTime - flightTime - fitTime
                Histogram.Fill(timeResidual)
    Histogram.Scale(1.0/Histogram.Integral())
    pdfVector = []
    #Note to self: Check to make sure the 0th bin means a time residual between -100 and -99 and so on.
    for i in range(0,Histogram.GetNbinsX()):
        pdfVector.append(Histogram.GetBinContent(i))
    return pdfVector

def OutputFileChunk(pdfList, options, description):#pdfList must be in the follwing order [Bi,Po,Te130]
    pdfNames = ["beta_probability","alpha_probability","two_beta_probability"]
    print("{")
    print("name: \"LIKELIHOOD_Bi"+options.particle+"_"+description+"\",")
    print("index: \""+options.scintMaterial+"\",")
    print("valid_begin: [0,0],")
    print("valid_end: [0,0],")
   
    sys.stdout.write("times: [")
    for time in range(-100,1000):
       sys.stdout.write(str(time)+", ")
    print("]")
    for pdfIndex,pdf in enumerate(pdfList):
        sys.stdout.write(str(pdfNames[pdfIndex]) + ": [")
        for pdfIndex,pdfValue in enumerate(pdf):
            sys.stdout.write(str(pdfValue)+", ")
        print("]")
    print("}")

