
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>

#include <RAT/DU/DSReader.hh>
#include <RAT/DU/Utility.hh>
#include <RAT/DU/PMTInfo.hh>
#include <RAT/DU/LightPathCalculator.hh>
#include <RAT/DU/GroupVelocity.hh>
#include <RAT/DU/EffectiveVelocity.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCEV.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>
#include <RAT/DS/Entry.hh>

void FillScintTimeResidualsPlot(std::string material, TH1D* histogram, double velocity=-999);
void FillWaterTimeResidualsPlot(std::string material, TH1D* histogram);


void GetScintPDF(std::string material, int numberOfRuns, double velocity=-999)
{
  TH1D* histogram1 = new TH1D("histogram1", "", 400, -99.5, 300.5);
  TH1D* histogram2 = new TH1D("histogram2", "", 400, -99.5, 300.5);

  std::cout << "running with velocity " << velocity << endl;

  for(int i = 0; i < numberOfRuns; i++)
  {
    std::stringstream fileNameStream;
    fileNameStream << material + "_DataForPDF_part" << (i + 1) << ".root";
    FillScintTimeResidualsPlot(fileNameStream.str(), histogram1, velocity);
  }

  // Print coordinated values to screen in RATDB format
  std::cout << std::endl;
  std::cout << "Please place the text below into the database file: ET1D.ratdb located in rat/data, replacing any existing entry with the same index." << std::endl;
  std::cout << std::endl;
  std::cout << "{" << std::endl;
  std::cout << "type : \"ET1D\"," << std::endl;
  std::cout << "version: 1," << std::endl;
  std::cout << "index: \"" << material << "\"," << std::endl;
  std::cout << "run_range: [0, 0]," << std::endl;
  std::cout << "pass: 0," << std::endl;
  std::cout << "production: false," << std::endl;
  std::cout << "timestamp: \"\"," << std::endl;
  std::cout << "comment: \"\"," << std::endl;
	
  std::cout << "time: [";
  for(int j = 0; j < 401; j++)
  {
    std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinCenter(j)) << ", ";
  }
  std::cout << "]," << std::endl;
  
  std::cout << "probability: [";
  for(int j = 0; j < 401; j++)
  {
    // Approximate early hits to a flat distribution
    if (j < 94)
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(10));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(10)) << ", ";
    }
    // Approximate late hits to a flat distribution
    else if (j > 320)
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(320));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(320)) << ", ";
    }
    else
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(j));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(j)) << ", ";
    }
  }
  std::cout << "]," << endl;  
  
  std::cout << "}" << std::endl;
  std::cout << std::endl;
  
  // histogram1 shows MC data in black
  // histogram2 shows PDF (including approximations) in red
  histogram1->Draw();
  histogram1->GetXaxis()->SetTitle("Time Residual, ns");
  histogram2->SetLineColor(2);
  histogram2->Draw("SAMES");
}

// Update the Scintillator Time Residual distribution from a single rootfile
void FillScintTimeResidualsPlot(std::string infile, TH1D* histogram, double velocity)
{
  RAT::DU::DSReader dsReader(infile);
  RAT::DU::LightPathCalculator lightPath = RAT::DU::Utility::Get()->GetLightPathCalculator();
  const RAT::DU::EffectiveVelocity& effectiveVelocity = RAT::DU::Utility::Get()->GetEffectiveVelocity();
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();
 
  for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
  {
    const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
    if(dsEntry.GetEVCount() == 0) continue;

    // Get MC info
    const RAT::DS::MC& mcEvent = dsEntry.GetMC();
    const RAT::DS::MCParticle& mcParticle = mcEvent.GetMCParticle(0);
    TVector3 mcPosition = mcParticle.GetPosition();

    // Get triggered PMT information
    const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
    const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();

    // Get event time
    double eventTime = 390 - dsEntry.GetMCEV(0).GetGTTime();

    // Loop over each triggered PMT and get the time residual
    for(size_t j = 0; j < calibratedPMTs.GetCount(); j++)
    {
      const RAT::DS::PMTCal& pmt = calibratedPMTs.GetPMT(j);
      double pmtTime = pmt.GetTime();
      TVector3 pmtPosition = pmtInfo.GetPosition(pmt.GetID());

      lightPath.CalcByPosition(mcPosition, pmtPosition);
      double distInInnerAV = lightPath.GetDistInInnerAV();
      double distInAV = lightPath.GetDistInAV();
      double distInWater = lightPath.GetDistInWater();
      double transitTime = effectiveVelocity.CalcByDistance(distInInnerAV, distInAV, distInWater);
      if(velocity>0)
        // We are overriding the velocity in EffectiveVelocity for faster processing
        transitTime = ( distInInnerAV / velocity + distInAV / effectiveVelocity.GetAVVelocity() +
                        distInWater / effectiveVelocity.GetWaterVelocity() ) + effectiveVelocity.GetOffset();
      
      double timeResid = pmtTime - transitTime - eventTime;
      histogram->Fill(timeResid);
    }
  }
}


void GetWaterPDF(std::string material)
{
  TH1D* histogram1 = new TH1D("histogram1", "", 800, -99.875, 100.125);
  TH1D* histogram2 = new TH1D("histogram2", "", 800, -99.875, 100.125);

  for(int i = 1; i < 21; i++)
  {
    std::stringstream fileNameStream;
    fileNameStream << material + "_DataForPDF_part" << i << ".root";
    FillWaterTimeResidualsPlot(fileNameStream.str(), histogram1);
  }

  // Print coordinated values to screen in RATDB format
  std::cout << std::endl;
  std::cout << "Please place the text below into the database file: GV1D.ratdb located in rat/data, replacing any existing entry with the same index." << std::endl;
  std::cout << std::endl;
  std::cout << "{" << std::endl;
  std::cout << "type: \"GV1D\"," << std::endl;
  std::cout << "version: 1," << std::endl;
  std::cout << "index: \"" << material << "\"," << std::endl;
  std::cout << "run_range: [0, 0]," << std::endl;
  std::cout << "pass: 0," << std::endl;
  std::cout << "production: false," << std::endl;
  std::cout << "timestamp: \"\"," << std::endl;
  std::cout << "comment: \"\"," << std::endl;

  std::cout << "time: [";
  for(int j = 0; j < 801; j++)
  {
    std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinCenter(j)) << ", ";
  }
  std::cout << "]," << std::endl;
  
  std::cout << "probability: [";
  for(int j = 0; j < 801; j++)
  {
    // Approximate early hits to a flat distribution
    if (j < 360)
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(360));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(360)) << ", ";
    }
    // Approximate late hits to a flat distribution
    else if (j > 440)
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(440));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(440)) << ", ";
    }
    else
	{
      histogram2->Fill(histogram1->GetBinCenter(j), histogram1->GetBinContent(j));
      std::cout << std::fixed << std::setprecision(2)<< float(histogram1->GetBinContent(j)) << ", ";
    }
  }
  std::cout << "]," << endl;
  
  std::cout << "}" << std::endl;
  std::cout << std::endl;
  
  // histogram1 shows MC data in black
  // histogram2 shows PDF (including approximations) in red
  histogram1->Draw();
  histogram1->GetXaxis()->SetTitle("Time Residual, ns");
  histogram2->SetLineColor(2);
  histogram2->Draw("SAMES");
}

// Update the Water Time Residual distribution from a single rootfile
void FillWaterTimeResidualsPlot(std::string infile, TH1D* histogram)
{
  RAT::DU::DSReader dsReader(infile);
  RAT::DU::LightPathCalculator lightPath = RAT::DU::Utility::Get()->GetLightPathCalculator();
  const RAT::DU::GroupVelocity& groupVelocity = RAT::DU::Utility::Get()->GetGroupVelocity();
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

  for(size_t i = 0; i < dsReader.GetEntryCount(); i++) 
  {
    const RAT::DS::Entry& dsEntry = dsReader.GetEntry(i);
    if(dsEntry.GetEVCount() == 0) continue;

    // Get MC info
    const RAT::DS::MC& mcEvent = dsEntry.GetMC();
    const RAT::DS::MCParticle& mcParticle = mcEvent.GetMCParticle(0);
    TVector3 mcPosition = mcParticle.GetPosition();

    // Get triggered PMT information
    const RAT::DS::EV& triggeredEvent = dsEntry.GetEV(0);
    const RAT::DS::CalPMTs& calibratedPMTs = triggeredEvent.GetCalPMTs();

    // Get event time
    double eventTime = 390 - dsEntry.GetMCEV(0).GetGTTime();

    // Loop over each triggered PMT and get the time residual
    for(size_t j = 0; j < calibratedPMTs.GetCount(); j++)
    {
      const RAT::DS::PMTCal& pmt = calibratedPMTs.GetPMT(j);
      double pmtTime = pmt.GetTime();
      TVector3 pmtPosition = pmtInfo.GetPosition(pmt.GetID());

      lightPath.CalcByPosition(mcPosition, pmtPosition);
      double distInInnerAV = lightPath.GetDistInInnerAV();
      double distInAV = lightPath.GetDistInAV();
      double distInWater = lightPath.GetDistInWater();
      double transitTime = groupVelocity.CalcByDistance(distInInnerAV, distInAV, distInWater);

      double timeResid = pmtTime - transitTime - eventTime;

      // Fill histogram with those within a fiducial volume of 5.5m
      if (mcPosition.Mag() < 5500) histogram->Fill(timeResid);
    }
  }
}

