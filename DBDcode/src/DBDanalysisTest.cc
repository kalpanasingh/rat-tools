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
#include "../include/DBDanalysisTest.hh"
 
void analysis::smearPDFs(int numback,int numsig,double smearvalue){

  
 
  //smear bkg
  for(int nbkg=0; nbkg<numback; nbkg++)
    {

 

      ostringstream oss;
      oss<<hback[nbkg]->GetName()<<"_pdf";
      
      //if(numback[a]<0.1)continue;
      //if(fabs(backpdf[a]->Integral())<0.001) continue;
      
      hbackpdf[nbkg]=(TH1F*)hback[nbkg]->Clone(oss.str().c_str());
      if (smearvalue!=1){
      hbackpdf[nbkg]->Reset();
	
	  double  minbin=hback[nbkg]->GetXaxis()->GetXmin();
	
	  double  maxbin=hback[nbkg]->GetXaxis()->GetXmax();
	
	  
	  int Nbins=hback[nbkg]->GetNbinsX();
	
	  double binwidth=hback[nbkg]->GetBinWidth(1);//Warning:: the bin widths have to be the same for all the bins
	  TH1F tempa("TEMPa","temp",Nbins,minbin,maxbin);
	
	  double dist=0;
	  double ene=0;
	  double sigma=0;
	  double tempsum=0;
	  for(int i=1; i<Nbins+1; i++)
	    {
	      ene = hback[nbkg]->GetBinCenter(i);
	      
	      sigma = sqrt(ene/smearvalue)+0.001;
	      tempsum=0;
	      for(int j=1; j<Nbins+1; j++)
		{
		  
		  dist = (double)(i-j)*binwidth;
		 
		  tempsum+=1./sqrt(2*3.1415)/sigma*exp(-1*dist*dist/sigma/sigma/2.);
		}
		
	      for(int j=1; j<Nbins+1; j++)
		{
		 
		  dist = (double)(i-j)*binwidth;
		  
		  double wenergy=hback[nbkg]->GetBinContent(i)*1./sqrt(2*3.1415)/sigma/tempsum*exp(-1*dist*dist/sigma/sigma/2.);

		  // if you dont want to smear
		 
		  tempa.Fill(hback[nbkg]->GetBinCenter(j),wenergy);
		  
		}
	    }
	  for(int i=1; i<Nbins+1; i++)
	    {
	     
	     
	      hbackpdf[nbkg]->SetBinContent(i, tempa.GetBinContent(i));
	    }
	  //hbackpdf[nbkg]->Scale(1/hbackpdf[nbkg]->Integral());    
      }
  

    }
  //smear signal

  for(int nsig=0; nsig<numsig; nsig++)
    {
      ostringstream oss;
      oss<<hsig[nsig]->GetName()<<"_pdf";
      
      //if(numsig[a]<0.1)continue;
      //if(fabs(sigpdf[a]->Integral())<0.001) continue;
      
      hsigpdf[nsig]=(TH1F*)hsig[nsig]->Clone(oss.str().c_str());
      if (smearvalue!=1){
      hsigpdf[nsig]->Reset();
	
      double  minbin=hsig[nsig]->GetXaxis()->GetXmin();
	
      double  maxbin=hsig[nsig]->GetXaxis()->GetXmax();
	
	  
      int Nbins=hsig[nsig]->GetNbinsX();
	
      double binwidth=hsig[nsig]->GetBinWidth(1);//Warning:: the bin widths have to be the same for all the bins
      TH1F tempa("TEMPa","temp",Nbins,minbin,maxbin);
      
      double dist=0;
	  double ene=0;
	  double sigma=0;
	  double tempsum=0;
	  for(int i=1; i<Nbins+1; i++)
	    {
	      ene = hsig[nsig]->GetBinCenter(i);
	      
	      sigma = sqrt(ene/smearvalue)+0.001;
	      tempsum=0;
	      for(int j=1; j<Nbins+1; j++)
		{
		  dist = (double)(i-j)*binwidth;
		  tempsum+=1./sqrt(2*3.1415)/sigma*exp(-1*dist*dist/sigma/sigma/2.);
		}
		  
	      for(int j=1; j<Nbins+1; j++)
		{
		 
		  dist = (double)(i-j)*binwidth;
		 
		  double wenergy=hsig[nsig]->GetBinContent(i)*1./sqrt(2*3.1415)/sigma/tempsum*exp(-1*dist*dist/sigma/sigma/2.);
		  
		  
		  tempa.Fill(hsig[nsig]->GetBinCenter(j),wenergy);
		  
		}
	    }
	  for(int i=1; i<Nbins+1; i++)
	    {
	     
	     
	      hsigpdf[nsig]->SetBinContent(i, tempa.GetBinContent(i));
	    }
	  //hsigpdf[nsig]->Scale(1./hsigpdf[nsig]->Integral());
      }

    }
  NofBkg=numback;
  NofSig=numsig;  

}

void analysis::smearData(int numback,int numsig,double smearvalue){
 

 //smear bkg
  for(int nbkg=0; nbkg<numback; nbkg++)
    {
      ostringstream oss;
      oss<<hback[nbkg]->GetName()<<"_d";
      
      //if(numback[a]<0.1)continue;
      //if(fabs(backd[a]->Integral())<0.001) continue;
      
      hbackd[nbkg]=(TH1F*)hback[nbkg]->Clone(oss.str().c_str());
      if (smearvalue !=1){
      hbackd[nbkg]->Reset();
	
	  double  minbin=hback[nbkg]->GetXaxis()->GetXmin();
	
	  double  maxbin=hback[nbkg]->GetXaxis()->GetXmax();
	
	  
	  int Nbins=hback[nbkg]->GetNbinsX();
	
	  double binwidth=hback[nbkg]->GetBinWidth(1);//Warning:: the bin widths have to be the same for all the bins
	  TH1F tempa("TEMPa","temp",Nbins,minbin,maxbin);
	
	  double dist=0;
	  double ene=0;
	  double sigma=0;
	  double tempsum=0;
	  for(int i=1; i<Nbins+1; i++)
	    {
	      ene = hback[nbkg]->GetBinCenter(i);
	      
	      sigma = sqrt(ene/smearvalue)+0.001;
	      tempsum=0;
	      for(int j=1; j<Nbins+1; j++)
		{
		  
		  dist = (double)(i-j)*binwidth;
		 
		  
		
		  
		  tempsum+=1./sqrt(2*3.1415)/sigma*exp(-1*dist*dist/sigma/sigma/2.);
		}
		
	      for(int j=1; j<Nbins+1; j++)
		{
		 
		  dist = (double)(i-j)*binwidth;
		  
		  double wenergy=hback[nbkg]->GetBinContent(i)*1./sqrt(2*3.1415)/sigma/tempsum*exp(-1*dist*dist/sigma/sigma/2.);
		  

		  tempa.Fill(hback[nbkg]->GetBinCenter(j),wenergy);
		  
		}
	    }
      
	  for(int i=1; i<Nbins+1; i++)
	    {
	      
	      
	      hbackd[nbkg]->SetBinContent(i, tempa.GetBinContent(i));
	    }

	  //  hbackd[nbkg]->Scale(1/hbackd[nbkg]->Integral());
      }
    
  
    }

  //smear signal

  for(int nsig=0; nsig<numsig; nsig++)
    {
      ostringstream oss;
      oss<<hsig[nsig]->GetName()<<"_d";
      
      //if(numsig[a]<0.1)continue;
      //if(fabs(sigd[a]->Integral())<0.001) continue;
      
      hsigd[nsig]=(TH1F*)hsig[nsig]->Clone(oss.str().c_str());
      if(smearvalue!=1){
      hsigd[nsig]->Reset();
	
	  double  minbin=hsig[nsig]->GetXaxis()->GetXmin();
	
	  double  maxbin=hsig[nsig]->GetXaxis()->GetXmax();
	
	  
	  int Nbins=hsig[nsig]->GetNbinsX();
	
	  double binwidth=hsig[nsig]->GetBinWidth(1);//Warning:: the bin widths have to be the same for all the bins
	  TH1F tempa("TEMPa","temp",Nbins,minbin,maxbin);
	
	  double dist=0;
	  double ene=0;
	  double sigma=0;
	  double tempsum=0;
	  for(int i=1; i<Nbins+1; i++)
	    {
	      ene = hsig[nsig]->GetBinCenter(i);
	      double bincon=hsig[nsig]->GetBinContent(i);


	      sigma = sqrt(ene/smearvalue)+0.001;
	      tempsum=0;
	      for(int j=1; j<Nbins+1; j++)
		{
		  
		  dist = (double)(i-j)*binwidth;
		 
		 
		  
		  
		  tempsum+=1./sqrt(2*3.1415)/sigma*exp(-1*dist*dist/sigma/sigma/2.);
		}
		  
	      for(int j=1; j<Nbins+1; j++)
		{
		 
		  dist = (double)(i-j)*binwidth;
		 
		  double wenergy=hsig[nsig]->GetBinContent(i)*1./sqrt(2*3.1415)/sigma/tempsum*exp(-1*dist*dist/sigma/sigma/2.);
		  

		  tempa.Fill(hsig[nsig]->GetBinCenter(j),wenergy);
		  
		}
	    }

	 
	  for(int i=1; i<Nbins+1; i++)
	    {
	     	     
	      hsigd[nsig]->SetBinContent(i, tempa.GetBinContent(i));
	      
	    }


      }
	  //hsigd[nsig]->Scale(1./hsigd[nsig]->Integral());
    }

  
  
}

void analysis::scale(int numback,int numsig,double livetime){
 
TFile *f=new TFile("test.root","recreate");
 hsigd[0]->Write();
 
 f->Close();

  for (int i=0;i<numback;i++){
    numbackevents[i]=livetime*backRate[i];
    cout<<"numback  "<<numback<< " Scale    "<<numbackevents[i]<<endl;   
    hbackpdf[i]->Scale(numbackevents[i]/hbackpdf[i]->Integral());
    hback[i]->Scale(numbackevents[i]/hback[i]->Integral());
    hbackd[i]->Scale(numbackevents[i]/hbackd[i]->Integral());
  }

  for (int i=0;i<numsig;i++){
    numsigevents[i]=livetime*sigRate[i];
    cout<<"numsig  "<<numsig<< "Scale    "<<numsigevents[i]<<endl;  
    //0nbb signal is  scaled to 1
    hsigpdf[i]->Scale(1/hsigpdf[i]->Integral());
    hsigd[i]->Scale(numsigevents[i]/hsigd[i]->Integral());
    hsig[i]->Scale(numbackevents[i]/hsig[i]->Integral());
 
  }



}

void analysis::MakeFakeData(int numback,int numsig){
  Rand=new TRandom3(0);
  double nbins=0;
  double xmax=0;
  double xmin=0;
 
  if (numsig>0) {
  

    
  for (int i=0;i<numsig;i++){
    double tempmax=hsigd[i]->GetXaxis()->GetXmax();
    hsigd[i]->GetXaxis()->GetXmax();
    if ((hsigd[i]->GetNbinsX())>nbins){nbins=hsigd[i]->GetNbinsX();}
    if (tempmax>xmax) {xmax=tempmax;}
  }

  
  }

  
  xmin=(double)hsigd[0]->GetXaxis()->GetXmin();
  data=new TH1F("data","",nbins,xmin,xmax);

 for (int nbkg=0;nbkg<numback;nbkg++){
 
   int nbins=hbackd[nbkg]->GetNbinsX();
   for (int i=0;i<nbins;i++){ 
  double     temp=Rand->Poisson(hbackd[nbkg]->GetBinContent(i));
 
     data->Fill(hbackd[nbkg]->GetBinCenter(i),temp);

    }

 }

for (int nsig=0;nsig<numsig;nsig++){
 
  int nbins=hsigd[nsig]->GetNbinsX();
 
    for (int i=0;i<nbins;i++){
 
     double temp=(double)Rand->Poisson(hsigd[nsig]->GetBinContent(i));

     data->Fill(hsigd[nsig]->GetBinCenter(i),temp);

    }

 }

}



void analysis::FitData(TF1* func,TVirtualFitter* fitter){



  int totalpar=NofBkg+NofSig;
  double efitUp[totalpar], efitLow[totalpar], efit[totalpar], globcc[totalpar];
      
  char name[30];
  for (int i=0;i<NofBkg;i++){
    sprintf(name,hbackpdf[i]->GetName());
   
    func->SetParName(i,name);
   
  }
 
  for (int i=NofBkg;i<NofBkg+NofSig;i++){
    sprintf(name,hsigpdf[i-NofBkg]->GetName());
   

    func->SetParName(i,name);

  }
  for (int i=0;i<NofBkg+NofSig;i++){
  func->SetParameter(i,1);

  }


 
  data->Fit(func,"LQE","",2.5,5);

 fitter=TVirtualFitter::GetFitter();

  for (int i=0;i<NofBkg;i++){
    fitter->GetErrors(i,efitUp[i], efitLow[i], efit[i], globcc[i]);
    efitUp[i]*=hbackpdf[i]->Integral();
    efitLow[i]*=hbackpdf[i]->Integral();

    fitresult[i]=func->GetParameter(i)*hbackpdf[i]->Integral();

  }

  for (int i=NofBkg;i<totalpar;i++){
    fitter->GetErrors(i,efitUp[i], efitLow[i], efit[i], globcc[i]);
    efitUp[i]*=hsigpdf[i-NofBkg]->Integral();
    efitLow[i]*=hsigpdf[i-NofBkg]->Integral();
    efitSigUp[i]=efitUp[i];
    efitSigLow[i]=efitLow[i];
    cout<<"EfitUP     *************  "<<efitUp[i]<<endl;
    // I found out that for root version 5.20 and higher (maybe due to a bug) EfitUp is too small which statistically not correct

    if (efitUp[i]<1.0) {cout<< "Going to skip this fit----- "<<endl;}
    fitresult[i]=func->GetParameter(i)*hsigpdf[i-NofBkg]->Integral();
    

  }
}



void analysis::Write(int numback,int numsig,TF1* func,TFile *f1){
  // TFile *f1=new TFile("outputhistograms_energy_nd150.root","recreate");
  TH1F *hsum=(TH1F*)hbackpdf[0]->Clone("hsum");
  hsum->Reset();

  for (int i=0;i<numback;i++){
    hbackpdf[i]->Write();
    hbackd[i]->Write();
    hsum->Add(hbackpdf[i]);
    cout<<hbackpdf[i]->GetNbinsX()<<endl;

  }

  for (int i=0;i<numsig;i++){
    hsigpdf[i]->Write();
    hsigd[i]->Write();
    hsum->Add(hsigpdf[i]);
  }
  
  // hsum->Write();
  //data->Write();
  //func->Write();
  // f1->Close();
  


}
void analysis::ReStart(){
  cout<<"hello world"<<endl;
 data->Reset();

  for(int i=0; i<NofBkg; i++)
    {
      hbackd[i]->Reset();
      hbackpdf[i]->Reset();
    }
  for(int i=0; i<NofSig; i++)
    {
      hsigd[i]->Reset();
      hsigpdf[i]->Reset();
    }


}
void analysis::GetBackHistograms(char hname1[10],char hname2[10],char hname3[10],TFile *f,int numback,char isotope[30]){
  char hname[10];
 
  ostringstream osshisto,hb_i;
  TKey *key=f->FindKey(hname1);
  if(key!=0) {sprintf(hname,hname1);  }
  TKey *key1=f->FindKey(hname2);
  if(key1!=0) {sprintf(hname,hname2);  }
  TKey *key2=f->FindKey(hname3);
  if(key2!=0) {sprintf(hname,hname3); }
  hb_i<<isotope<<"_"<<hname;

  TH1F *htemp=(TH1F*)f->Get(hname);

  if(!htemp){cerr<<"histogram "<<htemp<<" does not exist::: Oh NO!!! going to segma fault !!!!"<<endl;}
  hback[numback]=(TH1F*)htemp->Clone(hb_i.str().c_str());
  hback[numback]->Reset();
  hback[numback]=(TH1F*)htemp->Clone(hb_i.str().c_str());

  
  if (numback>0){

    //this is if the histograms dont have the same bin width as long as the ratio is an integer it rebins the histograms to match with bin number
       if (hback[numback]->GetBinWidth(1)<hback[numback-1]->GetBinWidth(1)){
	 int rebin=hback[numback-1]->GetBinWidth(1)/hback[numback]->GetBinWidth(1);
	 cout<<"rebining the histogram   "<<hback[numback]->GetName()<< " By   "<<rebin<<endl;
	 hback[numback]->Rebin(rebin);

       }


  }
}


void analysis::GetSigHistograms(char hname1[10], char hname2[10], char hname3[10],TFile *f,int numsig,char isotope[30]){

  char hname[10];
  
  ostringstream osshisto,hs_i;
  TKey *key=f->FindKey(hname1);
  if(key!=0) {sprintf(hname,hname1);  }
  TKey *key1=f->FindKey(hname2);
  if(key1!=0) {sprintf(hname,hname2);  }
  TKey *key2=f->FindKey(hname3);
  if(key2!=0) {sprintf(hname,hname3); }
  hs_i<<isotope<<"_"<<hname;

  
  TH1F *htemp=(TH1F*)f->Get(hname);
  if(!htemp){
    cerr<<"histogram "<<htemp<<" does not exist::::::::: Oh NO!!! going to segma fault!!!!!!!!!!!!!!!!! "<<endl;
   
  }
  hsig[numsig]=(TH1F*)htemp->Clone(hs_i.str().c_str());
  hsig[numsig]->Reset();
  hsig[numsig]=(TH1F*)htemp->Clone(hs_i.str().c_str());
 
  cout<<hsig[numsig]->GetBinWidth(1)<<endl;
  cout<<hback[0]->GetBinWidth(1)<<endl;
  if (hsig[numsig]->GetBinWidth(1)!=hback[0]->GetBinWidth(1)){
    int rebin=hback[0]->GetBinWidth(1)/hsig[numsig]->GetBinWidth(1);
    cout<<"rebining the histogram   "<<hsig[numsig]->GetName()<< " By   "<<rebin<<endl;
    hsig[numsig]->Rebin(rebin);
  }

}



