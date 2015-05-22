#!usr/bin/env python
# Benjamin Land - 15/10/14 <benland100@berkeley.edu>

from rat import *
from math import *
import sys

AlphaEnergy = 50.0      #energy of alphas to simulate
BetaEnergy = 5.0        #energy of betas to simulate

TotalEvents = 100000    #total events to simulate per particle
Batches = 10            #number of simulations to run to achieve TotalEvents

#power up RAT

def BinHitTimeResiduals(filenames, timeFirst = -200.0, timeLast = 1000.0, timeStep = 1.0, retrigcutoff = 600.0):
    '''Calculates and bins the hit time residuals for a root file using event retrigger detection.'''
    
    #retrigcutoff = RAT.DS.UniversalTime(retrigcutoff)
    lastTime = None
    
    nbins = int(floor((timeLast-timeFirst)/timeStep) + 1)
    counts = [0] * nbins
    
    #loop over triggers
    for fileidx in xrange(0,len(filenames)):
        filename = filenames[fileidx]
        
        print 'Loading file ('+str(fileidx+1)+'/'+str(len(filenames))+'): ',filename
        reader = RAT.DU.DSReader(filename)
        dsUtility = RAT.DU.Utility.Get()
        effectiveVelocity = dsUtility.GetEffectiveVelocity()
        lightPath = dsUtility.GetLightPathCalculator()
        pmtInfo = dsUtility.GetPMTInfo()
        
        for entryidx in xrange(0, reader.GetEntryCount()):
            entry = reader.GetEntry(entryidx)
            print str(int(100.0*entryidx/reader.GetEntryCount()))+'%\r',
            sys.stdout.flush()
            for evidx in xrange(0,entry.GetEVCount()):
                ev = entry.GetEV(evidx)
                
                #check for possible retrigger
                curTime = ev.GetUniversalTime()
                retrigger = lastTime != None and (curTime - lastTime).GetNanoSeconds() < retrigcutoff
                
                #update time and position accordingly
                if retrigger:
                    eventTime -= (curTime - lastTime).GetNanoSeconds();
                else:
                    if ev.FitResultExists("scintFitter"):
                        eventPos = ev.GetFitResult("scintFitter").GetVertex(0).GetPosition()
                        eventTime = ev.GetFitResult("scintFitter").GetVertex(0).GetTime()
                    else:
                        eventPos = None
                        eventTime = None
                        
                if eventPos != None:
                    lastTime = curTime
                    
                    #loop over all hits
                    for pmtidx in xrange(0, ev.GetCalPMTs().GetCount()):
                        pmt = ev.GetCalPMTs().GetPMT(pmtidx)
                        
                        pmtPos = pmtInfo.GetPosition(pmt.GetID())
                        
                        #calculate the transit time for light from the event to the hit
                        lightPath.CalcByPosition(eventPos, pmtPos)
                        distInInnerAV = lightPath.GetDistInInnerAV()
                        distInAV = lightPath.GetDistInAV()
                        distInWater = lightPath.GetDistInWater()
                        transitTime = effectiveVelocity.CalcByDistance(distInInnerAV, distInAV, distInWater)
                        
                        #calculate the time residual
                        timeResidual = pmt.GetTime() - transitTime - eventTime
                        
                        #add the residual to the bins
                        bin = int(floor((timeResidual-timeFirst)/timeStep))
                        if (bin >= nbins or bin < 0):
                            continue #ignore points outside of range
                        counts[bin] += 1
    
    # normalize and return time residual PDF
    total = 0
    for count in counts:
        total += count if count else 1e-30   
    return [count/total if count else 1e-30/total for count in counts] 
    
