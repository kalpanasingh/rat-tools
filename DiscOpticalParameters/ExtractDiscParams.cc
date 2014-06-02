////////////////////////////////////////////////////////////////////
/// \file ExtractDiscParams.cc
///
/// \brief Function to extract the Disc Optical Model Parameters and 
///        produce a ratdb file
///
/// \author P G Jones <p.g.jones@qmul.ac.uk>
///
/// REVISION HISTORY:\n
///     2014-06-02: P. Jones - First Revision.\n
///
/// \detail A file called DISC_PARAMETERS.ratdb will be created.
///
////////////////////////////////////////////////////////////////////

#include <RAT/DU/DSReader.hh>
#include <RAT/DS/Entry.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCTrack.hh>
#include <RAT/DS/MCTrackStep.hh>

#include <TH1D.h>
#include <TH2D.h>
#include <TStyle.h>
#include <TMath.h>
#include <TCanvas.h>

#include <fstream>
using namespace std;


/// Extract the disc parameters
///
/// The photolectron response is the number of photoelectrons/number of hits per bin.
/// The reflection response is the number of reflected photons/number of hits per bin.
///
/// @param[in] fileName of the RAT::DS root file to analyse
/// @return the histogram plot
void ExtractDiscParams( const string& fileName )
{
  gStyle->SetOptStat(111111); // to show overflow / underflow stats

  const int thetaBins = 90; const double thetaLow = 0.0; const double thetaHigh = 89.0;
  const int lambdaBins = 49; const double lambdaLow = 220.0; const double lambdaHigh = 710.0;
  TH2D* hResponse = new TH2D( "hResponse", "PMT Response as function of angle", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* hReflected = new TH2D( "hReflected", "PMT Response as function of angle", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH2D* hHits = new TH2D( "hHits", "PMT hits as function of angle", thetaBins, thetaLow, thetaHigh, lambdaBins, lambdaLow, lambdaHigh );
  TH1D* hTiming = new TH1D( "hTiming", "Transit time in PMT", 100, 0.0, 1.0 );
  
  RAT::DU::DSReader dsReader( fileName );
  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ ) 
    {
      const RAT::DS::Entry& rDS = dsReader.GetEntry( iEntry );
      const RAT::DS::MC& mc = rDS.GetMC();
      for( size_t iPMT = 0; iPMT < mc.GetMCPMTCount(); iPMT++ )
        {
          const RAT::DS::MCPMT& mcPMT = mc.GetMCPMT( iPMT );
          const TVector3 pmtDirection = TVector3( 0.0, 0.0, -1.0 );
          double inTime = 0.0;
          double hitTime = 0.0;
          for( size_t iPhoton = 0; iPhoton < mcPMT.GetMCPhotonCount(); iPhoton++ )
            {
              const RAT::DS::MCPhoton& mcPhoton = mcPMT.GetMCPhoton( iPhoton );
              if( mcPhoton.GetInPosition().Z() < 132.0 )
                continue;
              const double angle = TMath::ACos( mcPhoton.GetInDirection().Dot( pmtDirection ) ) * TMath::RadToDeg();
              const double wavelength = 2.0 * 3.14159265358979323846 * 197.32705e-6 / mcPhoton.GetEnergy(); // In nm
              hHits->Fill( angle, wavelength );
              if( mcPhoton.GetFate() == RAT::DS::MCPhoton::ePhotoelectron )
                {
                  hResponse->Fill( angle, wavelength );
                  inTime = mcPhoton.GetInTime();
                }
              else if( mcPhoton.GetFate() == RAT::DS::MCPhoton::eReflected )
                hReflected->Fill( angle, wavelength );
            }
          for( size_t iPhotoelectron = 0; iPhotoelectron < mcPMT.GetMCPhotoelectronCount(); iPhotoelectron++ )
            hitTime = mcPMT.GetMCPhotoelectron( iPhotoelectron ).GetCreationTime();
          hTiming->Fill( hitTime - inTime );
        }
    }
  hResponse->Sumw2();
  hHits->Sumw2();
  hReflected->Sumw2();
  hResponse->Divide( hHits );
  new TCanvas();
  hResponse->Draw("COLZ");
  hReflected->Divide( hHits );
  hReflected->SetLineColor( kRed );
  new TCanvas();
  hReflected->Draw("COLZ");
  new TCanvas();
  hTiming->Draw();

  // Now to write out the arrays
  ofstream discParams("DISC_PARAMETERS.ratdb");
  discParams << "{\nname: \"GREY_DISC_PARAMETERS\",\nindex: \"DiscOptics0_New\",\ntravel_time: 0.25d,\ndecay_constant: 0.25d,\nbounce_spread: 0.10d,\ndisc_radius: 137.7d,\ncollection_efficiency: 1.0d,\nabsorption_probability: [";
  for( int iLambda = 0; iLambda < lambdaBins; iLambda++ )
    {
      for( int iTheta = 0; iTheta < thetaBins; iTheta++ )
        {
          discParams << hResponse->GetBinContent( iTheta + 1, iLambda + 1) << ", ";
        }
    }
  discParams << "],\nreflection_probability: [";
  for( int iLambda = 0; iLambda < lambdaBins; iLambda++ )
    {
      for( int iTheta = 0; iTheta < thetaBins; iTheta++ )
        {
          discParams << hReflected->GetBinContent( iTheta + 1, iLambda + 1) << ", ";
        }
    }
  discParams <<"],\n}\n";
  discParams.close();
}
