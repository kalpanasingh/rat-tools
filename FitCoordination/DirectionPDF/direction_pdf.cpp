#include <iostream>
#include <fstream>

#include <TROOT.h>
#include <TFile.h>
#include <TH1D.h>
#include <TTree.h>

#include <RAT/DSReader.hh>

#include <RAT/DU/LightPath.hh>
#include <RAT/DU/GroupVelocity.hh>
#include <RAT/DU/EffectiveVelocity.hh>

#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>
#include <RAT/DS/PMTSet.hh>
#include <RAT/DS/PMT.hh>

void FillDirection(char* pFile, TH1D* hist)
{
  RAT::DSReader dsReader(pFile);

  RAT::DU::LightPath lightPath = RAT::DU::Utility::Get()->GetLightPath();
  const RAT::DU::EffectiveVelocity& effectiveVelocity = RAT::DU::Utility::Get()->GetEffectiveVelocity();
  const RAT::DU::PMTInfo& pmtInfo = RAT::DU::Utility::Get()->GetPMTInfo();

  // loop over each event

  for( size_t iEvent = 0; iEvent < dsReader.GetEventCount(); iEvent++ ) 

      tree->GetEntry( iLoop );
      const RAT::DS::MC& pmc = rds->GetMC();
      TVector3 mcPos = pmc.GetMCParticle(0).GetPosition();
      TVector3 mcDir = pmc.GetMCParticle(0).GetMomentum().Unit();

      int evc = rds.GetEVCount();
      if( evc == 0 ) continue;
      const RAT::DS::EV& pev= rds.GetEV(0);
      const RAT::DS::CalibratedPMTs& calPMTs = pev.GetCalibratedPMTs();
      size_t PMThits = pev.GetCalibratedPMTs.GetCount();

      for(size_t jLoop=0; jLoop<PMThits; jLoop++)
        {
          const RAT::DS::PMTCal& pCal = pev.GetCalibratedPMTs.GetPMT(jLoop);
          TVector3 pmtPos = pmtInfo.GetPos(pCal.GetID());
          TVector3 photonDir = (pmtPos-mcPos);
          double ctheta = (photonDir.Unit()).Dot(mcDir);
          double theta = acos(ctheta);

          hist->Fill(theta);
        }
    }
}

void GetDirectionPDF()
{
  TH1D* hist = new TH1D("dir","dir",100,0,3.14);

  FillDirection("data_for_pdf_1.root",hist);

  hist->Scale(1/hist->Integral());

  // Read out data in ratdb format
  cout << "angle: [0.0d, ";
  for(int j=1; j<101; j++){
    cout << hist->GetBinCenter(j) << "d, ";
  }
  cout << "3.14d,]," << endl;
  cout << "probability: [";
  for(int j=0; j<102; j++){
    cout << hist->GetBinContent(j) << "d, ";
  }
  cout << "]," << endl;  
}
