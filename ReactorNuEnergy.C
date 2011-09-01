// Histogram Macro for ROOT: Events vs. Kinetic Energy
// Used to compare the oscillated and unoscillated events
// from GenReactorIBD and after it has been selected for
// events by ReactorNuSelector
// 
// We use GetPDGCode() to get rid of the neutrons, which 
// are superfluous to our retrieval of the neutrino energy
// (only positrons are required)

#include <vector>

using namespace std;

void Hist_Macro_TEST(char* pFile, char* pFile2)
{
  TFile *f = new TFile(pFile);
  TFile *f2 = new TFile(pFile2);
  TTree *tree = f->Get("T");
  TTree *tree2= f2->Get("T");
  
  RAT::DS::Root *rds = new RAT::DS::Root();
  RAT::DS::Root *rds2 = new RAT::DS::Root();
  tree->SetBranchAddress("ds", &rds);
  tree2->SetBranchAddress("ds", &rds2);
  int nEvents = tree->GetEntries();
  int nEvents2 = tree2->GetEntries();
  
  TH1F *hist = new TH1F("hist","Total Energy;KE (MeV);Number", 250, 0, 9); // bins, start, end
  TH1F *hist2 = new TH1F("hist2","Total Energy;KE (MeV);Number", 250, 0, 9);
  
  
  for (int i=0; i<nEvents;++i)
    {
      tree->GetEntry(i);
      RAT::DS::MC *rmc = rds->GetMC();
      int mcpc = rmc->GetMCParticleCount();
      // int evc = rds->GetEVCount();
      float oscEnergy = 0.0;
   
      for (int j=0; j<mcpc;j++)
	{ // printf("%d %d of %d\n", i,j, nEvents);
	  if(-11 == rmc->GetMCParticle(j)->GetPDGCode())
	    {
	      RAT::DS::MCParticle *rmcparticle = rmc->GetMCParticle(j);
	      oscEnergy += (rmcparticle->GetKE() + 1.35); // approximation to true Enu 
	    }
	} 
      hist->Fill(oscEnergy);
    }
      
  // Now unoscillated energy
  for(int m=0; m<nEvents2; m++)
    {
      tree2->GetEntry(m);
      RAT::DS::MC *rmc2 = rds2->GetMC();
      int mcpc2 = rmc2->GetMCParticleCount();
      float unoscEnergy = 0.0;
      for (int k=0; k<mcpc2; k++)
	{
	  if(-11 == rmc->GetMCParticle(k)->GetPDGCode())
	    {
	      RAT::DS::MCParticle *rmc2particle = rmc2->GetMCParticle(k);
	      unoscEnergy += (rmc2particle->GetKE() + 1.35); // approximation to true Enu    
	    }
	}
      hist2->Fill(unoscEnergy);
    }
  
  
  hist->SetLineColor(2); 
  // hist->SetFillColor(2);
  hist2->SetLineColor(1); 
  // hist2->SetFillColor(1);

  hist->GetXaxis()->SetTitle("Energy (MeV)");
  hist->GetYaxis()->SetTitle("Number");
  
  hist2->Draw();
  hist->Draw("sames");//("sames");
  
  

  legend = new TLegend(0.5,0.6,0.79,0.79);
  //legend->SetHeader(*pFile + *pFile2);
  legend->SetFillColor(0); // white background
  legend->AddEntry(hist,"oscillated","l");
  legend->AddEntry(hist2,"unoscillated","l");
  legend->SetTextSize(0.03);
  legend->Draw();
  
}
