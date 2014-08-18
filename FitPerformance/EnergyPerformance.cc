////////////////////////////////////////////////////////
/// Produces a table of numbers characterising the timing
/// resolution.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 12/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPerformanceUtil.hh>

#include <RAT/DSReader.hh>

#include <RAT/DS/Root.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/FitResult.hh>
#include <RAT/DS/FitVertex.hh>

#include <TH1D.h>
#include <TChain.h>
#include <TFile.h>
#include <TF1.h>
using namespace ROOT;

#include <string>
#include <sstream>
#include <utility>
using namespace std;

vector<double>
FitEnergyRes(
           TH1D* hRes );

void
ExtractEnergy(
            string lFile,
            string lFit,
            TH1D** hCountVRes );

const double gkStartBin = -50.0;
const double gkEndBin = 50.0;

void
EnergyPerformance(
				  string lFit )
{
  vector< pair< string, string > > posFiles = PositionFiles();
  vector< pair< string, string > > energyFiles = EnergyFiles();

  stringstream latexOut;
  latexOut.setf( ios::fixed, ios::floatfield );
  latexOut.precision( 1 );
  latexOut << "\\begin{table}" << endl << "\\begin{center}\\begin{tabular}{ @{\\extracolsep{\\fill}} | c | c | c | c | c |}" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "Egen & Rgen &";
  latexOut << "$\\langle\\Delta t\\rangle$ & $ \\delta (\\Delta t) $ & $\\frac{ \\chi^2 }{ ndf }$ \\\\" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "(MeV) & (mm) & \\multicolumn{2}{c|}{(ns)} & \\\\" << endl;
  latexOut << "\\hline" << endl;

  for( vector< pair< string, string > >::iterator iTer = posFiles.begin(); iTer != posFiles.end(); iTer++ )
	{
      TH1D* hERes;
	  ExtractEnergy( iTer->second, lFit, &hERes );
	  vector<double> resolutions = FitEnergyRes( hERes );
	  latexOut << "3 & " << iTer->first;
	  for( unsigned int uLoop = 0; uLoop < resolutions.size(); uLoop++ )
		{
		  if( ( uLoop + 1 ) % 4 == 3 && uLoop != 0 )
			latexOut << " & $\\frac{ " << resolutions[uLoop] << "}";
          else if( ( uLoop + 1 ) % 4 == 0 && uLoop != 0 )
			latexOut << "{ " << resolutions[uLoop] << " }$";
		  else
			latexOut << " & " << resolutions[uLoop];
		}
	  latexOut << "\\\\" << endl;
	}
  
  latexOut << "\\hline" << endl;
  for( vector< pair< string, string > >::iterator iTer = energyFiles.begin(); iTer != energyFiles.end(); iTer++ )
    {
      TH1D* hERes;
      ExtractEnergy( iTer->second, lFit, &hERes );
	  vector<double> resolutions = FitEnergyRes( hERes );
      latexOut << iTer->first << " & fill";
	  for( unsigned int uLoop = 0; uLoop < resolutions.size(); uLoop++ )
		{
		  if( ( uLoop + 1 ) % 4 == 3 && uLoop != 0 )
            latexOut << " & $\\frac{ " << resolutions[uLoop] << "}";
          else if( ( uLoop + 1 ) % 4 == 0 && uLoop != 0 )
            latexOut << "{ " << resolutions[uLoop] << " }$";
          else
            latexOut << " & " << resolutions[uLoop];
        }
      latexOut << "\\\\" << endl;
    }
  latexOut << "\\hline" << endl;
  latexOut << "\\end{tabular}\\end{center}" << endl;
  latexOut << "\\caption{Fit Result energy resolution table as produced by the Fitter Performance tool.}" << endl;
  latexOut << "\\end{table}";

  cout << latexOut.str() << endl;
}

vector<double>
FitEnergyRes(
		   TH1D* hRes )
{
  vector<double> results;
  TF1* gausFit = new TF1( "gaus", "gaus", gkStartBin, gkEndBin );
  hRes->Fit( gausFit );
  results.push_back( gausFit->GetParameter(1) );
  results.push_back( gausFit->GetParameter(2) );
  results.push_back( gausFit->GetChisquare() );
  results.push_back( gausFit->GetNDF() );

  return results;
}

void
ExtractEnergy(
			string lFile,
			string lFit,
			TH1D** hCountVRes )
{
  // First new the histograms
  const int kBins = 100;

  *hCountVRes  = new TH1D( "RRes", "RRes", kBins, gkStartBin, gkEndBin );
  (*hCountVRes)->SetDirectory( 0 );

  // Now extract the data
  // Load the first file

  RAT::DSReader dsReader(lFile.c_str());
  RAT::DU::PMTInfo rPMTList = DS::DU::Utility::Get()->GetPMTInfo();

  for( size_t iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ )
    {
      const RAT::DS::Root& rDS = dsReader.GetEntry( iEntry );
	  const RAT::DS::MC& rMC = rDS.GetMC();

      double mcEnergy = rMC.GetMCParticle(0).GetKineticEnergy();
      for( int iEV = 0; iEV < rDS->GetEVCount(); iEV++ )
        {
		  if( iEV > 0 ) // Only prompt events characterise
			continue;
		  const RAT::DS::EV& rEV = rDS.GetEV( iEV );
          if( rEV.GetFitResult( lFit ).GetValid() == false )
            continue;

		  double fitEnergy;
          try
            {
              fitEnergy = rEV.GetFitResult( lFit ).GetVertex(0).GetEnergy();
            }
          catch( RAT::DS::FitVertex::NoValueError& e )
            {
              cout << "Energy has not been fit." << endl;
              throw;
            }
          double delta = fitEnergy - mcEnergy;

          (*hCountVRes)->Fill( delta );
        }
    }
}
