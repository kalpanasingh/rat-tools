#include <iostream>
#include <fstream>
#include "TROOT.h"
#include "TFile.h"
#include "TH1D.h"
#include "TTree.h"
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMTCal.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/Run.hh>

void PlotDirections(char* pFile)
{
  TFile *file = new TFile(pFile);
  TTree *tree = (TTree*) file->Get("T");
  RAT::DS::Root *rds = new RAT::DS::Root();
  tree->SetBranchAddress("ds", &rds);

  // PMT Properties are contained in different tree
  TTree *runtree = (TTree*) file->Get( "runT");
  RAT::DS::Run *pmtds = new RAT::DS::Run();
  runtree->SetBranchAddress("run", &pmtds);
  runtree->GetEntry();
  RAT::DS::PMTProperties *pmtProp = pmtds->GetPMTProp();

  TH1D* hist = new TH1D("dir","dir",100,0,3.14);
  for(int iLoop =0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
      RAT::DS::MC *pmc = rds->GetMC();
      TVector3 mcPos = pmc->GetMCParticle(0)->GetPos();
      TVector3 mcDir = pmc->GetMCParticle(0)->GetMom().Unit();

      int evc = rds->GetEVCount();
      if( evc == 0 ) continue;
      RAT::DS::EV *pev= rds->GetEV(0);
      int PMThits = pev->GetPMTCalCount();

      for(int jLoop=0; jLoop<PMThits; jLoop++)
	{
	  RAT::DS::PMTCal *pCal = pev->GetPMTCal(jLoop);
	  TVector3 pmtPos = pmtProp->GetPos(pCal->GetID());
	  TVector3 photonDir = (pmtPos-mcPos);
	  double ctheta = (photonDir.Unit()).Dot(mcDir);
	  double theta = acos(ctheta);

	  hist->Fill(theta);
	}
    }
  hist->Scale(1/hist->Integral());
  hist->GetYaxis()->SetTitle("Probability");
  hist->GetXaxis()->SetTitle("Angle of PMT relative to initial direction");
  hist->Draw();

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
