
#include <iostream>
#include <math.h>
#include <sstream>

#include <TROOT.h>
#include <TFile.h>
#include <TH1D.h>
#include <TTree.h>

#include <RAT/DU/DSReader.hh>
#include <RAT/DU/Utility.hh>
#include <RAT/DU/PMTInfo.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>
#include <RAT/DS/Entry.hh>


void GetDirectionPDF(string material)
{
  std::stringstream fileNameStream;
  fileNameStream << material << "_DataForPDF.root";
  std::string fileNameString = fileNameStream.str();  
  
  TH1D histogram ("direction", "direction", 100, 0, 3.14);

  // Fill the histogram with the angle theta: the angle between the photon direction and the MC direction
  RAT::DU::DSReader dsReader(fileNameString);
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

  for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
  {
    const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
    const RAT::DS::MC& mcEvent = dsEntry.GetMC();
    TVector3 mcPosition = mcEvent.GetMCParticle(0).GetPosition();
    TVector3 mcDirection = mcEvent.GetMCParticle(0).GetMomentum().Unit();

    if(dsEntry.GetEVCount() == 0) continue;
    const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
    const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();
    
    for(size_t j = 0; j < calibratedPMTs.GetCount(); j++)
    {
      const RAT::DS::PMTCal& pmt = calibratedPMTs.GetPMT(j);
      TVector3 pmtPosition = pmtInfo.GetPosition(pmt.GetID());
      TVector3 photonDirection = (pmtPosition - mcPosition);
      double cosTheta = (photonDirection.Unit()).Dot(mcDirection);
      double theta = acos(cosTheta);

      histogram.Fill(theta);
    }
  }

  histogram.Scale(1.0 / (histogram.Integral()));

  // Print coordinated values to screen in RATDB format
  std::cout << std::endl;
  std::cout << "Please place the text below into the database file: FIT_DIR.ratdb located in rat/data, replacing any existing entry with the same index." << std::endl;
  std::cout << std::endl;
  std::cout << "{" << std::endl;
  std::cout << "name = \"FIT_DIR\"," << std::endl;
  std::cout << "index: \"" << material << "\"," << std::endl;
  std::cout << "valid_begin : [0, 0]," << std::endl;
  std::cout << "valid_end : [0, 0]," << std::endl;
	
  std::cout << "angle: [0.0, ";
  for(int j = 1; j < 101; j++)
  {
    std::cout << histogram.GetBinCenter(j) << ", ";
  }
  std::cout << "3.14,]," << std::endl;
  
  std::cout << "probability: [";
  for(int j = 0; j < 102; j++)
  {
    std::cout << histogram.GetBinContent(j) << ", ";
  }
  std::cout << "]," << std::endl;
  
  std::cout << "}" << std::endl;
  std::cout << std::endl;
}

