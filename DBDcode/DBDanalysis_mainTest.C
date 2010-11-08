/*/////DBD sensitivity code
** version 0.0 
** author: Nasim Fatemi-Ghomi  26/10/2010

To compile: Make
to run ./snoplusDBDanalysis.exe ListofFiles.dat

ListofFiles.dat is the rootfiles which contains the histograms 
Note: This code is still under develompment 
//////*/
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TMinuit.h"
#include "TF1.h"
#include "TVirtualFitter.h"
#include "iostream"
#include "fstream"
#include "stdio.h"
#include "TMath.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include <iomanip>
#include <sstream>
#include <ostream>
#include<fstream>
#include <string>
#include <iostream>
#include <cmath>
#include "include/DBDanalysisTest.hh"
using namespace std;


///////////////       some global variables
TRandom3 *r;
double livetimeGraph[5];
void SingleLiveTimeTest(analysis *ana,const char path[500]);
//void  LiveTimeTest(analysis *ana,const char path[500]);
void EnsembleTests(analysis *ana,TVirtualFitter *fitter);
char filenames[300][300]; 
char isotope[30][30];
char Type[10];
double livetime=1.0; //how many years
int numback(0);
int numsig(0);
double mass = 0.048;
double isotopemass=150.;
double numass = 500;//the neutrino mass in eV
double halfLifeLimitGraph[5];
Double_t nsigma =1.6;  // 90% CL = nsigma =1.6
double nat_mass = 0.048;  //Nd-150 mass in case of using natural Nd
int ensemble_size = 1000;  // how many times do you want to perform the fit
double ensemble_mean, ensemble_width, eensemble_mean, eensemble_width;
Double_t Rate[300];  
double half0 = 4.0E25/(numass/50)/(numass/50); //old QRPA matrix element
int numenteries=5; 
TF1* func;


/////////////////////////


int  main(int argc,char* argv[]){
//defining a variable which can be used to access functions/variables in the analysis class.
  analysis *ana=new analysis();
  ifstream in0;
  Int_t numFiles;
 
//open a file which contains the list of the rootfiles with histograms 
if(argc>1){
   in0.open(argv[1]);
  }

// the default file is ListofFiles.dat
 else{
  in0.open("ListofFiles.dat");
  
 }
// if there is no ListofFiles.dat and no dat files is given as an argument give users some information and then exit the program
 if(!in0) {
   cerr<<endl;
   cerr<<endl;
   cerr<<"User is expected to supply a ListofFiles.dat file with the followring format"<<endl;
   cerr<<"[type (B/S for background/signal)] [rootfile path] [item name] background rate [evt/year]"<<endl;
   cerr<<"Example :"<<endl;
   cerr <<"B  /histograms/Tl208_spec.root Tl208  604.84"<<endl;
   cerr<<endl;   
   cerr<<" This should be done for all of your backgrounds and signals "<<endl;
   return 0;
 }

 // Get the information from the dat file line by line and find the total number of files
 Int_t count=0;
 while(in0>>Type[count]>>filenames[count]>>isotope[count]>>Rate[count]){
   count++;
   }
 numFiles=count;
 std::cout<<numFiles<<" files to process"<<std::endl;
 
 //loop over the files get the background/signal rates and get the hisgrams. 
 for (Int_t j=0;j<numFiles;j++){
   //ostringstream oss;
   TFile *f=new TFile(filenames[j],"read");

   //if files does not exist, give a message and exit
   if (f->IsZombie()) {
     cerr<<"File  "<<filenames[j]<<" does not exist  "<<endl;
     cerr<<"Going to exit the program "<<endl;
     return 0;
    }

   //if background get the rate and  get the histograms. 
   if(Type[j]=='B'||Type[j]=='b'){
    
     
     ana->backRate[numback]=Rate[j];

     //note that at the moment all the files have to have same histogram name 
     //Here the name of the histograms are given: This bits needs to be softcoded later ..
     //Energy note that your rootfile must contain only one of these histograms: Spect, h1, Etrue
     //User can edit the arguments based on his/her need.
     ana->GetBackHistograms("Etrue","h1","Spect",f,numback,isotope[j]);
   
     
     numback++;

   }

  
   else if(Type[j]=='S'|| Type[j]=='s'){
     
     ana->sigRate[numsig]=Rate[j];

     //User can edit the arguments based on his/her need.
     ana->GetSigHistograms("Etrue","h1","Spect",f,numsig,isotope[j]);
     numsig++;

   }

 
  
 }//end of numfiles loop


 //smear all (signal and background) histograms by the resolution value ie: 450 ,400 etc, in case of using recostructed distributions (already smeared histograms) this value should be =1
 ana->smearPDFs(numback,numsig,1);

 //smear data
 ana->smearData(numback,numsig,1);

 // scale the histograms 
 ana->scale(numback,numsig,livetime);
 
 //Make fake data using random Poisson nums
 ana->MakeFakeData(numback,numsig);

 // create the user function class: this will have numsig+numback different parameters and starts from 0 to 15 MeV for energy
 func = new TF1("func",ana,&analysis::Evaluate,0,15,numsig+numback); 
 func->SetNumberFitPoints(100);
 TVirtualFitter *fitter=TVirtualFitter::Fitter(0,numback+numsig);

 //fit the data to func
 ana->FitData(func,fitter);
 
 //write smeared MC and fakedatahistograms as well as the fitted function in a file
 TFile *fwrite=new TFile("output_all.root","recreate");
 ana->Write(numback,numsig,func,fwrite);
 fwrite->Close();


 //set a limit on 0nbb at 90% CL and save the result in graphs
 SingleLiveTimeTest(ana,"livetime.root");
   
}




void SingleLiveTimeTest(analysis *ana,const char path[500]){
  func = new TF1("func",ana,&analysis::Evaluate,0,15,numsig+numback); 
  func->SetNumberFitPoints(100);
 TVirtualFitter *fitter=TVirtualFitter::Fitter(0,numback+numsig);
;

 

  //resolotuon 400 nhits/MeV
 
 ana->smearData(numback,numsig,400);
 ana->smearPDFs(numback,numsig,400);
 ana->scale(numback,numsig,livetime);
 ana->MakeFakeData(numback,numsig);
 
 // 5 years of running the detector
  int numtries=5;

  // 1000 times fit
  ensemble_size=1000;

  
  double livetimeArray[numtries];
  double elivetimeArray[numtries];
  double halfLifeLimitArray[numtries];
  double ehalfLifeLimitArray[numtries];
  double massLimitArray[numtries]; 
  double massLimitArray2[numtries];
  double meanArray[numtries];
  double widthArray[numtries];
  double emeanArray[numtries];
  double ewidthArray[numtries];
  ana->ReStart();
  //finds the sensitivity: year 1 to year 5
  for(int i=0; i<5; i++){

    livetime=5-i;

    //make sure that you reset your histograms 
    ana->ReStart();
    ana->smearData(numback,numsig,400);
    ana->smearPDFs(numback,numsig,400);
    ana->scale(numback,numsig,livetime);

    //fit ensemble_size times
 
    EnsembleTests(ana,fitter);
 
    livetimeArray[i]=livetime;
    livetimeGraph[i]=livetime;
    elivetimeArray[i]=0.0000001;

    meanArray[i] = ensemble_mean;
    emeanArray[i] = eensemble_mean;
    widthArray[i] = ensemble_width;
    ewidthArray[i] = eensemble_width;

    halfLifeLimitArray[i]= mass*1000000./isotopemass*6.02E23*log(2.)*livetime/(ensemble_mean+nsigma*ensemble_width);
    halfLifeLimitGraph[i]= halfLifeLimitArray[i];

    massLimitArray[i]=sqrt(half0/halfLifeLimitArray[i])*numass;//need to change this later to new NME
    massLimitArray2[i]=(0.511/(2.32*sqrt(halfLifeLimitArray[i]*2.69E-13)));

  }
  
  TGraph *halfLife=new TGraph(numtries,livetimeArray,halfLifeLimitArray);
  TGraph *mass=new TGraph(numtries,livetimeArray, massLimitArray);
  TGraph *mass2=new TGraph(numtries,livetimeArray, massLimitArray2); TFile fin(path,"recreate");


  halfLife->Draw("APL");
  halfLife->Draw();
  halfLife->Write("HalfLife");
  mass->Draw("APL");
  mass2->Draw("APL");
  mass->Write("Mass_QRPA");
  mass2->Write("Mass_newIBM2");
  //events.Write("events");
  fin.Close();

  cout<<"Latex table output  ***************starts here ******"<<endl; 
printf("\\begin{table}[htb]\n \\begin{center}\n \\begin{tabular}{|| c || c | c |  c | c |c||} \\hline\\hline\n");
  
  printf(" Livetime & $T^{0\\nu}_{1/2}$ Limit & $\\left< m_\\nu \\right>$ Limit & $\\left< m_\\nu \\right>$ IBM-2 Limit    &$\\left< \\text{NFit}_{0\\nu\\beta\\beta}\\right>$");
  
  printf(" & $\\left< \\Delta \\text{NFit}_{0\\nu\\beta\\beta}\\right>$\\\\ \n");
  printf("(kT$\\cdot$a) & (x10$^{24}$a) &  (meV) & & \\\\ \\hline\\hline\n");

  for(int i=0; i<numtries; i++)
    {
      printf(" %0.2f & %0.1f & %0.0f & %0.0f&%0.1f $\\pm$ %0.1f & %0.2f $\\pm$ %0.2f\\\\ \\hline\n", livetimeArray[i], halfLifeLimitArray[i]/1E24, massLimitArray[i], massLimitArray2[i],meanArray[i], emeanArray[i], widthArray[i], ewidthArray[i]); 
    }
  
  printf("\\hline\n \\end{tabular}\n \\end{center}\n \\caption{}\n \\label{}\n \\end{table}\n");

  cout<<"Latex table output  ***************ends here ******"<<endl; 

}

// function which fits MC to fake data several times and then finds the mean of the fit results and the mean of the errors of the fit. 
void EnsembleTests(analysis *ana,TVirtualFitter *fitter){

  TH1F mean("mean","Mean", 100,-500,500);
  TH1F width("width","Width", 100, -50, 50);
  //fitter=TVirtualFitter::Fitter(0,numback+numsig);
  
  double chisum =0;
  double leaksum =0;
  Int_t count=0;
  for(int i=0; i<ensemble_size; i++)
    {
      
      
      ana->MakeFakeData(numback,numsig);
      ana->FitData(func,fitter);

   
      
      int count2=0;    
      for (int j=0;j<numback;j++){


	if (ana->fitresult[j]<0) { count2++; count++; }
	
      }
   
      if (count2!=0) continue;
      if (ana->efitSigUp[numback]<1.0 ) continue;// this is for root version 5.20 and higher where the fitter sometimes failes to finds the error on the fit and gives a wrong small error
      

      //  Fill the mean with fit values
      mean.Fill(ana->fitresult[numback]);

      // fill the with with errors on the fit
      width.Fill(ana->efitSigUp[numback]);
     
    }

  ///just to have a count of negative fit results
  cout<<"number of events with negative fit"<<count<<endl;

  //Write the witdh and mean histograms in a file, perform a gausan fit to find the overall fit result and error.
   TFile fin("temp_ratnd.root","recreate");
  width.Write();
  //
  TF1 *f1=new TF1("f1","gaus",-100,100);
  mean.Fit(f1,"LQ");
  mean.Write();
  fin.Close();
  ensemble_mean = f1->GetParameter(1);
  cout<<"ensemble_mean "<<ensemble_mean<<endl;
  eensemble_mean = f1->GetParError(1);
  
  TF1 *f2=new TF1("f2","gaus",-100,100);
  width.Fit(f2,"LQ");

  ensemble_width =f2->GetParameter(1);
  eensemble_width =f2->GetParError(1);

  if(fabs(ensemble_width-width.GetMean())>1.0)
    {
      printf("*\n*\n*\n*\n*\n*\n*\nError in width fits*\n*\n*\n*\n*\n*\n\n");
      ensemble_width =width.GetMean();
    }

 

}


