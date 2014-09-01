#include <iostream>
#include <fstream>
#include <sstream>

#include <TROOT.h>
#include <TFile.h>
#include <TNtuple.h>
#include <TH1D.h>

#include <RAT/DU/DSReader.hh>
#include <RAT/DU/Utility.hh>
#include <RAT/DU/LightPathCalculator.hh>
#include <RAT/DU/GroupVelocity.hh>
#include <RAT/DU/EffectiveVelocity.hh>

#include <RAT/DS/MC.hh>
#include <RAT/DS/MCEV.hh
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>
#include <RAT/DS/PMTSet.hh>
#include <RAT/DS/Entry.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DB.hh>

void FillScintTimeResiduals( string pFile, TH1D* hist, double velocity=-999 )
{

  RAT::DU::DSReader dsReader(pFile);

  RAT::DU::LightPathCalculator lightPath = RAT::DU::Utility::Get()->GetLightPathCalculator();
  const RAT::DU::EffectiveVelocity& effectiveVelocity = RAT::DU::Utility::Get()->GetEffectiveVelocity();
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

  if( velocity > 0 )
    {
      cout << "Attempting to update VG from " << pmtds->GetEffectiveVelocityTime()->GetVg() << " to " << velocity << newline;
      pmtds->GetEffectiveVelocityTime()->UpdateVg( velocity );
      cout << "Using effective velocity: " << pmtds->GetEffectiveVelocityTime()->GetVg() << endl;
    }
  else
    cout << "Running with default velocity: " << pmtds->GetEffectiveVelocityTime()->GetVg() << newline;

  // loop over each event

  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ ) 
    {

      const RAT::DS::Entry& rDS = dsReader.GetEntry( iEntry );

      int evc = rds.GetEVCount();
      if(evc==0) continue;

      // Get MC info
      const RAT::DS::MC& pmc = rds.GetMC();
      const RAT::DS::MCParticle& mcPart = pmc.GetMCParticle(0);
      TVector3 mcPos = mcPart.GetPosition();

      // Get Number of PMT hits
      const RAT::DS::EV& pev = rds.GetEV(0);
      const RAT::DS::CalPMTs& calPMTs = pev.GetCalPMTs();

      // Get event time
      double eventTime = 390 - pmc.GetMCEV(0).GetGTTime();

      // Loop over each PMT hit and get time
      for( size_t loop=0; loop < calPMTs.GetCount(); loop++)
        {

          const RAT::DS::PMTCal& pCal = calPMTs.GetPMT(loop);
          double pmtTime = pCal.GetTime();
          TVector3 pmtPos = pmtInfo.GetPos(pCal.GetID());

          // Get straight line travel time to PMT
          lightPath.CalcByPosition( mcPosition, pmtPos, distInScint, distInAV, distInWater);
          double distInScint = lightPath.GetDistInScint();
          double distInAV = lightPath.GetDistInAV();
          double distInWater = lightPath.GetDistInWater();
          const double straightTime = effectiveVelocity.CalcByDistance( distInScint, distInAV, distInWater);
                    
          // Finally, get time residual
          double tres= pmtTime - straightTime - eventTime;

          // Fill histogram with those within a fiducial volume of 5.5m
          if(mcPos.Mag() < 5500)  hist->Fill(tres);
        }
    }
}

void FillH2OTimeResiduals( string pFile, TH1D* hist )
{

  RAT::DU::DSReader dsReader(pFile);

  RAT::DU::LightPathCalculator lightPath = RAT::DU::Utility::Get()->GetLightPathCalculator();
  const RAT::DU::GroupVelocity& groupVelocity = RAT::DU::Utility::Get()->GetGroupVelocity();
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

  // loop over each event

  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ ) 
    {

      const RAT::DS::Entry& rDS = dsReader.GetEntry( iEntry );

      int evc = rds.GetEVCount();
      if(evc==0) continue;

      // Get MC info
      const RAT::DS::MC& pmc = rds.GetMC();
      const RAT::DS::MCParticle& mcPart = pmc.GetMCParticle(0);
      TVector3 mcPos = mcPart.GetPosition();

      // Get Number of PMT hits
      const RAT::DS::EV& pev = rds.GetEV(0);
      const RAT::DS::CalPMTs& calPMTs = pev.GetCalPMTs();

      // Get event time
      double eventTime = 390 - pmc.GetMCEV(0).GetGTTime();

      // Loop over each PMT hit and get time
      for( size_t loop=0; loop < calPMTs.GetCount(); loop++)
        {

          const RAT::DS::PMTCal& pCal = calPMTs.GetPMT(loop);
          double pmtTime = pCal.GetTime();
          TVector3 pmtPos = pmtInfo.GetPos(pCal.GetID());

          // Get straight line travel time to PMT
          double distInScint, distInAV, distInWater;
          lightPath.CalcByPosition( mcPosition, pmtPos, distInScint, distInAV, distInWater);
          const double straightTime = groupVelocity.CalcByDistance( distInScint, distInAV, distInWater);
                    
          // Finally, get time residual
          double tres= pmtTime - straightTime - eventTime;

          // Fill histogram with those within a fiducial volume of 5.5m
          if(mcPos.Mag() < 5500)  hist->Fill(tres);
        }
    }

}

void GetScintPDF(string material="labppo_scintillator", int nFiles=1, double velocity=-999)
{
  // Create and fill time residual histogram
  TH1D* hist = new TH1D("H","",400,-99.5,300.5);
  TH1D* hist2 = new TH1D("H2","",400,-99.5,300.5);

  for(int i=1;i<nFiles+1;i++){
    stringstream ss;
    ss << "HitTime_" << material << "_" << i << ".root";
    FillScintTimeResiduals(ss.str(),hist,velocity);
  }

  // Read out data in ratdb format
  cout << "time: [";
  for(int j=0; j<401; j++){
    cout << hist->GetBinCenter(j) << "d, ";
  }
  cout << "]," << endl;
  cout << "probability: [";
  for(int j=0; j<401; j++){
    if(j<94){
      // Approximate early hits to flat
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(10));
      cout << hist->GetBinContent(10) << "d, ";
    }
    else if(j>320){
      // Approximate late hits to flat
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(320));
      cout << hist->GetBinContent(320) << "d, ";
    }
    else{
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(j));
      cout << hist->GetBinContent(j) << "d, ";
    }
  }
  cout << "]," << endl;  

  // hist shows MC data in black
  // hist2 shows PDF (including approximations) in red
  hist->Draw();
  hist->GetXaxis()->SetTitle("Time Residual (ns)");
  hist2->SetLineColor(2);
  hist2->Draw("sames");
}

void GetH2OPDF(string material="lightwater_sno", int nFiles=1)
{
  TH1D* hist = new TH1D("H","",800,-99.875,100.125);
  TH1D* hist2 = new TH1D("G","",800,-99.875,100.125);

  for(int i=1;i<nFiles+1;i++){
    stringstream ss;
    ss << "HitTime_" << material << "_" << i << ".root";
    FillH2OTimeResiduals(ss.str(),hist);
  }

  // Read out data in ratdb format
  cout << "time: [";
  for(int j=0; j<801; j++){
    cout << hist->GetBinCenter(j) << "d, ";
  }
  cout << "]," << endl;
  cout << "probability: [";
  for(int j=0; j<801; j++){
    if(j<360){
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(360));
      cout << hist->GetBinContent(360) << "d, ";
    }
    else if(j>440){
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(440));
      cout << hist->GetBinContent(440) << "d, ";
    }
    else{
      hist2->Fill(hist->GetBinCenter(j),hist->GetBinContent(j));
      cout << hist->GetBinContent(j) << "d, ";
    }
  }
  cout << "]," << endl;  

  // hist shows MC data in black
  // hist2 shows PDF (including approximations) in red
  hist->Draw();
  hist->GetXaxis()->SetTitle("Time Residual (ns)");
  hist2->SetLineColor(2);
  hist2->Draw("sames");
}
