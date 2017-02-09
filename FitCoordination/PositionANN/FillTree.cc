// FillTree.cc
//
// Fill tree with inputs and output required for ANNs used in PositionANN method.

#include <RAT/DU/DSReader.hh>
#include <RAT/DU/Utility.hh>
#include <RAT/DU/PMTInfo.hh>
#include <RAT/DS/Entry.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMTSet.hh>
#include <RAT/DS/PMT.hh>

#include <TVector3.h>
#include <TFile.h>
#include <TTree.h>

#include <iostream>
#include <vector>
#include <string>
#include <numeric>

using namespace std;
using namespace RAT;

void FillTree(string inputname, string outputname, int nTime = 20, int nAngle = 20) {

  DU::DSReader dsReader(inputname);
  const DU::PMTInfo& pmtInfo = DU::Utility::Get()->GetPMTInfo();

  // Binning values for the ntuple
  const double sTime = -10.0;
  const double eTime = 90.0;
  const double dTime = (eTime - sTime) / nTime;
  const double sAngle = -1.0;
  const double eAngle = 1.0;
  const double dAngle = (eAngle - sAngle) / nAngle;
  const int nTotal = nTime * nAngle;

  // Parameters to write to the tree
  char names[20];
  // Store both the MC and Fitted patterns (i.e. using MC position and fitted event orientation)
  // So that we can train on truth, but test on fits.
  vector<int> hitPatternFitInt(nTotal, 0);
  vector<double> hitPatternFit(nTotal, 0.0); // Normalised
  vector<int> hitPatternMCInt(nTotal, 0);
  vector<double> hitPatternMC(nTotal, 0); // Normalised
  double radius;
  TFile tf(outputname.c_str(), "recreate");
  TTree tt("tree", "tree");

  // rootpy doesn't like using arrays, assign each pixel to a separate branch
  for(int i=0; i<nTotal; i++) {
    stringstream ssBranch1, ssBranch2;
    ssBranch1 << "hitPatternFit_" << i;
    tt.Branch(ssBranch1.str().c_str(), &hitPatternFit[i], (ssBranch1.str()+"/D").c_str());
    ssBranch2 << "hitPatternMC_" << i;
    tt.Branch(ssBranch2.str().c_str(), &hitPatternMC[i], (ssBranch2.str()+"/D").c_str());
  }
  tt.Branch("radius", &radius, "radius/D");

  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ ) {

    for(int i=0; i<nTotal; i++) {
      fill(hitPatternMCInt.begin(), hitPatternMCInt.end(), 0);
      fill(hitPatternFitInt.begin(), hitPatternFitInt.end(), 0);
    }

    if(dsReader.GetEntryCount()>100)
      if(iEntry % (dsReader.GetEntryCount()/100)==0)
        cerr << "*";
    
    const DS::Entry& entry = dsReader.GetEntry(iEntry);

    if(entry.GetEVCount() == 0) continue;

    const DS::EV& ev = entry.GetEV(0);

    TVector3 mcPos = entry.GetMC().GetMCParticle(0).GetPosition();

    const DS::CalPMTs& calPMTs = ev.GetCalPMTs();

    // Fill a vector of the PMT times to get the nth (10%) time
    vector<double> times(calPMTs.GetCount(), 0);
    for(size_t iPMT = 0; iPMT < calPMTs.GetCount(); iPMT++)
      times[iPMT] = calPMTs.GetPMT(iPMT).GetTime();

    int nthElement = static_cast<int>(0.1 * calPMTs.GetCount());
    nth_element(times.begin(), times.begin() + nthElement, times.end());
    double window = times[nthElement];

    // Now get the direction to the event (using the median method
    double windowStart = window - 10;
    double windowEnd = window + 10;
    TVector3 fitAxis(0, 0, 0);

    for(size_t iPMT = 0; iPMT < calPMTs.GetCount(); iPMT++) {

      const DS::PMTCal& pmtCal = calPMTs.GetPMT(iPMT);
      double pmtTime = pmtCal.GetTime();

      if(pmtTime >= windowStart && pmtTime <= windowEnd) {
        TVector3 pmtPos = pmtInfo.GetPosition(pmtCal.GetID());
        fitAxis += pmtPos.Unit();
      }

    } // iPMT
    
    fitAxis = fitAxis.Unit();

    // Populate the images (input vectors) with hit patterns
    for(size_t iPMT = 0; iPMT < calPMTs.GetCount(); iPMT++) {

      const DS::PMTCal& pmtCal = calPMTs.GetPMT(iPMT);
      double pmtTime = pmtCal.GetTime();
      TVector3 pmtPos = pmtInfo.GetPosition(pmtCal.GetID());

      // Need to convert the pmtTime to ( pmtTime - window ) and then get the bin
      double deltaT = pmtTime - window;
      int iTime = static_cast<int>((deltaT - sTime) / dTime);

      double angleMC = mcPos.Unit().Dot(pmtPos.Unit());
      double angleFit = fitAxis.Dot(pmtPos.Unit());
      int iAngleMC = static_cast<int>((angleMC - sAngle) / dAngle);
      int iAngleFit = static_cast<int>((angleFit - sAngle) / dAngle);

      int iMC = iAngleMC * nTime + iTime;
      int iFit = iAngleFit * nTime + iTime;

      // If the hit is within our 2D area, add it
      // MUST check the individual axes here!
      if(iAngleMC >=0 && iAngleMC < nAngle &&
         iTime >=0 && iTime < nTime)
        hitPatternMCInt[iMC]++;
      if(iAngleFit >=0 && iAngleFit < nAngle &&
         iTime >=0 && iTime < nTime)
        hitPatternFitInt[iFit]++;

    } // iPMT

    // Fill the normalised vectors
    int sumMCHits = accumulate(hitPatternMCInt.begin(), hitPatternMCInt.end(), 0);
    int sumFitHits = accumulate(hitPatternFitInt.begin(), hitPatternFitInt.end(), 0);

    for(int i = 0; i < nTotal; i++) {
      hitPatternMC[i] = static_cast<double>(hitPatternMCInt[i]) / sumMCHits;
      hitPatternFit[i] = static_cast<double>(hitPatternFitInt[i]) / sumFitHits;
    }

    // output parameter from ANN
    radius = mcPos.Mag();

    // finally, fill the tree
    tt.Fill();

  }

  cerr << endl;

  tt.Write();
  tf.Close();

}
