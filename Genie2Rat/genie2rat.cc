// takes the output of gevgen_atmo and creates a RAT root file
//
// genie2rat -i [input genie filename] -o [output root filename] (-n [number of events to process])

#include <string>

#include <TSystem.h>
#include <TFile.h>
#include <TTree.h>
#include <TIterator.h>
#include <TVector3.h>

#include "EVGCore/EventRecord.h"
#include "GHEP/GHepParticle.h"
#include "Ntuple/NtpMCFormat.h"
#include "Ntuple/NtpMCTreeHeader.h"
#include "Ntuple/NtpMCEventRecord.h"
#include "Messenger/Messenger.h"
#include "PDG/PDGCodes.h"
#include "Utils/CmdLnArgParser.h"

#include <RAT/DS/Root.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>

using std::string;
using namespace genie;

void GetCommandLineArgs (int argc, char ** argv);

int    gOptNEvt;
string gOptInpFilename;
string gOptOutFilename;

int main(int argc, char ** argv)
{
  GetCommandLineArgs (argc, argv);

  //-- open the ROOT file and get the TTree & its header
  TTree *           tree = 0;
  NtpMCTreeHeader * thdr = 0;

  TFile file(gOptInpFilename.c_str(),"READ");

  tree = dynamic_cast <TTree *>           ( file.Get("gtree")  );
  thdr = dynamic_cast <NtpMCTreeHeader *> ( file.Get("header") );

  if(!tree) return 1;

  NtpMCEventRecord * mcrec = 0;
  tree->SetBranchAddress("gmcrec", &mcrec);

  int nev = (gOptNEvt > 0) ?
    TMath::Min(gOptNEvt, (int)tree->GetEntries()) :
    (int) tree->GetEntries();

  // set up output file
  TFile *outfile = new TFile(gOptOutFilename.c_str(),"RECREATE");
  TTree *outtree = new TTree("T","RAT Tree");
  RAT::DS::Root *branchDS = new RAT::DS::Root();
  outtree->Branch("ds",branchDS->ClassName(),&branchDS,32000,99);

  //
  // Loop over all events
  //
  double time = 0;
  for(int i = 0; i < nev; i++) {

    // get next tree entry
    tree->GetEntry(i);

    // get the GENIE event
    EventRecord &  event = *(mcrec->event);
    double x = 1000.0*event.Vertex()->X(); // distances from GENIE are in meters
    double y = 1000.0*event.Vertex()->Y(); // distances from GENIE are in meters
    double z = 1000.0*event.Vertex()->Z(); // distances from GENIE are in meters

    RAT::DS::Root *ds = new RAT::DS::Root();
    RAT::DS::MC *mc = ds->GetMC();

    mc->SetMCTime(time); // GENIE does not give global time, so we just add arbitrary times for RAT 
    mc->SetEventID(i);

    //
    // Loop over all particles in this event
    //

    GHepParticle * p = 0;
    TIter event_iter(&event);

    while((p=dynamic_cast<GHepParticle *>(event_iter.Next())))
    {
      // check if it is the initial state neutrino
      if (p->Status() == kIStInitialState && 
          (p->Pdg() == kPdgNuE || p->Pdg() == kPdgAntiNuE ||
           p->Pdg() == kPdgNuMu || p->Pdg() == kPdgAntiNuMu ||
           p->Pdg() == kPdgNuTau || p->Pdg() == kPdgAntiNuTau)){
        RAT::DS::MCParticle *parent = mc->AddNewMCParent();
        parent->SetPDGCode(p->Pdg());
        parent->SetTime(0); // GENIE does not give particles time separate from event
        parent->SetPos(TVector3(x,y,z)); // GENIE outputs particle distance from event in fm, basically 0
        parent->SetMom(TVector3(1000.0*p->Px(),1000.0*p->Py(),1000.0*p->Pz())); // GENIE outputs momentum and energy in GeV
        parent->SetKE(1000.0*p->KinE());
      }
      if (p->Status() == kIStStableFinalState){
        // skip if it is a GENIE special particle (final state unsimulated hadronic energy etc)
        if (p->Pdg() > 2000000000){
          continue;
        }
        RAT::DS::MCParticle *particle = mc->AddNewMCParticle();
        particle->SetPDGCode(p->Pdg());
        particle->SetTime(0); // GENIE does not give particles time separate from event
        particle->SetPos(TVector3(x,y,z)); // GENIE outputs particle distance from event in fm, basically 0  
        particle->SetMom(TVector3(1000.0*p->Px(),1000.0*p->Py(),1000.0*p->Pz())); // GENIE outputs momentum and energy in GeV
        particle->SetKE(1000.0*p->KinE());
      }
    }// end loop over particles	

    // clear current mc event record
    mcrec->Clear();
    *branchDS = *ds;
    outtree->Fill();

    time += 1e9; // GENIE does not calculate time of events so we arbitrarily add a second
  }//end loop over events

  // close input GHEP event file
  file.Close();
  outfile->Write();
  outfile->Close();

  LOG("genie2rat", pNOTICE)  << "Done!";

  return 0;
}

void GetCommandLineArgs(int argc, char ** argv)
{
  LOG("genie2rat", pINFO) << "Parsing commad line arguments";

  CmdLnArgParser parser(argc,argv);

  // get GENIE event sample
  if( parser.OptionExists('i') ) {
    LOG("genie2rat", pINFO) 
      << "Reading event sample filename";
    gOptInpFilename = parser.ArgAsString('i');
  } else {
    LOG("genie2rat", pFATAL) 
      << "Unspecified input filename - Exiting";
    exit(1);
  }

  if ( parser.OptionExists('o') ) {
    gOptOutFilename = parser.ArgAsString('o');
  } else{
    gOptOutFilename = "output.ntuple.root";
  }

  // number of events to analyse
  if( parser.OptionExists('n') ) {
    LOG("genie2rat", pINFO) 
      << "Reading number of events to analyze";
    gOptNEvt = parser.ArgAsInt('n');
  } else {
    LOG("genie2rat", pINFO)
      << "Unspecified number of events to analyze - Use all";
    gOptNEvt = -1;
  }
}
