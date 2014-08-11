#include <iostream>
#include <fstream>
#include <sstream>
#include "TROOT.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TH1D.h"
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DB.hh>

void FillScintTimeResiduals( string pFile, TH1D* hist, double velocity=-999 )
{
  TFile *file = new TFile(pFile.c_str());
  TTree *tree = (TTree*) file->Get("T");
  RAT::DS::Root *rds = new RAT::DS::Root();
  tree->SetBranchAddress("ds", &rds);

  // PMT Properties are contained in different tree
  TTree *runtree = (TTree*) file->Get( "runT");
  RAT::DS::Run *pmtds = new RAT::DS::Run();
  runtree->SetBranchAddress("run", &pmtds);
  runtree->GetEntry();
  RAT::DS::PMTProperties *pmtProp = pmtds->GetPMTProp();

  if( velocity > 0 )
    {
      cout << "Attempting to update VG from " << pmtds->GetEffectiveVelocityTime()->GetVg() << " to " << velocity << newline;
      pmtds->GetEffectiveVelocityTime()->UpdateVg( velocity );
      cout << "Using effective velocity: " << pmtds->GetEffectiveVelocityTime()->GetVg() << endl;
    }
  else
    cout << "Running with default velocity: " << pmtds->GetEffectiveVelocityTime()->GetVg() << newline;

  // loop over each event
  for(int j=0; j<tree->GetEntries(); j++)
    {
      tree->GetEntry(j);
      int evc = rds->GetEVCount();
      if(evc==0) continue;

      // Get MC info
      RAT::DS::MC *pmc = rds->GetMC();
      RAT::DS::MCParticle *mc_part = pmc->GetMCParticle(0);
      TVector3 mc_pos = mc_part->GetPos();

      // Get Number of PMT hits
      RAT::DS::EV *pev = rds->GetEV(0);
      Int_t PMThits = pev->GetPMTCalCount();

      // Get event time
      double eventTime = 390 - pev->GetGTrigTime();

      // Loop over each PMT hit and get time
      for( Int_t loop=0; loop < PMThits; loop++)
        {
          RAT::DS::PMTCal *pCal = pev->GetPMTCal(loop);
          double pmtTime = pCal->GetTime();
          TVector3 pmtPos = pmtProp->GetPos(pCal->GetID());

          // Get straight line travel time to PMT
          double distInScint, distInAV, distInWater;
          pmtds->GetLightPath()->CalcByPosition( mc_pos, pmtPos, distInScint, distInAV, distInWater);
          double straightTime = pmtds->GetEffectiveVelocityTime()->CalcByDistance( distInScint, distInAV, distInWater);

          // Finally, get time residual
          double tres= pmtTime - straightTime - eventTime;

          // Fill histogram with those within a fiducial volume of 5.5m
          if(mc_pos.Mag() < 5500)  hist->Fill(tres);
        }
    }
}

void FillH2OTimeResiduals( string pFile, TH1D* hist )
{
  TFile *file = new TFile(pFile.c_str());
  TTree *tree = (TTree*) file->Get("T");
  RAT::DS::Root *rds = new RAT::DS::Root();
  tree->SetBranchAddress("ds", &rds);

  // PMT Properties are contained in different tree
  TTree *runtree = (TTree*) file->Get( "runT");
  RAT::DS::Run *pmtds = new RAT::DS::Run();
  runtree->SetBranchAddress("run", &pmtds);
  runtree->GetEntry();
  RAT::DS::PMTProperties *pmtProp = pmtds->GetPMTProp();

  // loop over each event
  for(int j=0; j<tree->GetEntries(); j++)
    {
      tree->GetEntry(j);
      int evc = rds->GetEVCount();
      if(evc==0) continue;

      // Get MC info
      RAT::DS::MC *pmc = rds->GetMC();
      RAT::DS::MCParticle *mc_part = pmc->GetMCParticle(0);
      TVector3 mc_pos = mc_part->GetPos();

      // Get Number of PMT hits
      RAT::DS::EV *pev = rds->GetEV(0);
      Int_t PMThits = pev->GetPMTCalCount();

      // Get event time
      double eventTime = 390 - pev->GetGTrigTime();

      // Loop over each PMT hit and get time
      for( Int_t loop=0; loop < PMThits; loop++)
        {
          RAT::DS::PMTCal *pCal = pev->GetPMTCal(loop);
          double pmtTime = pCal->GetTime();
          TVector3 pmtPos = pmtProp->GetPos(pCal->GetID());

          double distInScint, distInAV, distInWater;
          pmtds->GetLightPath()->CalcByPosition( mc_pos, pmtPos, distInScint, distInAV, distInWater);
          double straightTime = pmtds->GetGroupVelocityTime()->CalcByDistance(distInScint,distInAV,distInWater);

          // Finally, get time residual
          double tres= pmtTime - straightTime - eventTime;

          // Fill histogram with a fiducial volume of 5.5m
          if(mc_pos.Mag() < 5500)  hist->Fill(tres);
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
