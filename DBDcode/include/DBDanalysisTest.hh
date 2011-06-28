#include "TH2.h"
#include "TStyle.h"
#include "TNtuple.h"
#include "TCanvas.h"
#include "TMath.h"
#include "TFile.h"
#include "TF1.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <string>
#include <TChain.h>
#include <TRandom.h>
#include "TRandom3.h"
#include "TVirtualFitter.h"
using namespace std;
class analysis{
  public:
  analysis(){};
  int numBack;
  int numSig;
  double sigRate[30];
  double backRate[30];
  double numsigevents[30];
  double numbackevents[30];
  double nhits;
  double efitSigUp[10];
  double globcc[10]; // modified
  double fitresult[30];
  double efitSigLow[10];
  TH1F *hback[30];
  TH1F *hsig[10];
  TH1F *hbackpdf[30];
  TH1F *hsigpdf[10];
  TH1F *hbackd[30];
  TH1F *hsigd[10];
  int NofBkg;
  int NofSig;
  TRandom3 *Rand;
  TH1F *data;
  //TVirtualFitter* fitter;
  void smearPDFs(int numback,int numsig,double smearvalue);
  void GetBackHistograms(char hname1[10], char hname2[10], char hname3[10],TFile *f,int numback,char isotope[30]);
  void GetSigHistograms(char hname1[10], char hname2[10], char hname3[10],TFile *f,int numsig,char isotope[30]);
  void smearData(int numback,int numsig,double smearvalue);
  void Write(int numback, int numsig,TF1* func,TFile *f1);
  void scale(int numback,int numsig,double livetime);
  Double_t fitFunc(Double_t *x, Double_t *par);  
  void MakeFakeData(int numback,int numsig);
  void ReStart();
  double Evaluate (double *x, double *par) {
      // function implementation
   double val=0;
  
  int bin=hbackpdf[0]->FindBin(x[0]);

  //do the background

  for (int i=0;i<NofBkg;i++){

    val+=par[i]*hbackpdf[i]->GetBinContent(bin);

  }

  // now for signal
  int totalhisto=NofBkg+NofSig;
  for (int j=NofBkg;j<totalhisto;j++){

    val+=par[j]*hsigpdf[j-NofBkg]->GetBinContent(bin);
  }

  return val;


  }

  void FitData(TF1* func,TVirtualFitter* fitter);
  ~analysis(){};
};