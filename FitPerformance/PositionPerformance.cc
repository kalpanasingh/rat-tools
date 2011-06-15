////////////////////////////////////////////////////////
/// Produces a table of numbers characterising the position
/// resolution.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 12/06/11 - New File
////////////////////////////////////////////////////////

#include <FitPerformanceUtil.hh>

#include <RAT/DS/Root.hh>
#include <RAT/DS/PMTProperties.hh>
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
FitPositionRes(
			   TH1D* hXRes,
               TH1D* hYRes,
               TH1D* hZRes );

void
ExtractPosition(
                string lFile,
                string lFit,
				TH1D** hCountVResX,
                TH1D** hCountVResY,
                TH1D** hCountVResZ );

const double gkStartBin = -750.0;
const double gkEndBin = 750.0;

void
PositionPerformance(
					string lFit )
{
  vector< pair< string, string > > posFiles = PositionFiles();
  vector< pair< string, string > > energyFiles = EnergyFiles();

  stringstream latexOut;
  latexOut.setf( ios::fixed, ios::floatfield );
  latexOut.precision( 1 );
  latexOut << "\\begin{table}" << endl << "\\begin{tabular*}{1.1\\textwidth}{ @{\\extracolsep{\\fill}} | c | c | c | c | c | c | c | c | c | c | c | c | c |}" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "Egen & Rgen &";
  latexOut << "$\\langle\\Delta x\\rangle$ & $ \\delta (\\Delta x) $ & $\\frac{ \\chi^2 }{ ndf }$ &";
  latexOut << "$\\langle\\Delta y\\rangle$ & $ \\delta (\\Delta y) $ & $\\frac{ \\chi^2 }{ ndf }$ &";
  latexOut << "$\\langle\\Delta z\\rangle$ & $ \\delta (\\Delta z) $ & $\\frac{ \\chi^2 }{ ndf }$ &" << endl;
  latexOut << "$\\langle\\Delta r\\rangle$ & $ \\delta (\\Delta r) $ \\\\" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "[MeV] & [mm] & \\multicolumn{2}{c|}{[mm]} & & \\multicolumn{2}{c|}{[mm]} & & \\multicolumn{2}{c|}{[mm]} & & \\multicolumn{2}{c|}{[mm]}  \\\\" << endl;
  latexOut << "\\hline" << endl;

  for( vector< pair< string, string > >::iterator iTer = posFiles.begin(); iTer != posFiles.end(); iTer++ )
	{
      TH1D* hXRes;TH1D* hYRes;TH1D* hZRes;
	  ExtractPosition( iTer->second, lFit, &hXRes, &hYRes, &hZRes );
	  vector<double> resolutions = FitPositionRes( hXRes, hYRes, hZRes );
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
	  TH1D* hXRes;TH1D* hYRes;TH1D* hZRes;
      ExtractPosition( iTer->second, lFit, &hXRes, &hYRes, &hZRes );
	  vector<double> resolutions = FitPositionRes( hXRes, hYRes, hZRes );
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
  latexOut << "\\end{tabular*}" << endl;
  latexOut << "\\caption{Fit Result position resolution table as produced by the Fitter Performance tool.}" << endl;
  latexOut << "\\end{table}";

  cout << latexOut.str() << endl;
}

vector<double>
FitPositionRes(
			   TH1D* hXRes,
			   TH1D* hYRes,
			   TH1D* hZRes )
{
  vector<double> results;
  double rRes = 0.0;
  double rSigma = 0.0;

  TF1* gausFit = new TF1( "gaus", "gaus", gkStartBin, gkEndBin );
  hXRes->Fit( gausFit );
  results.push_back( gausFit->GetParameter(1) );
  results.push_back( gausFit->GetParameter(2) );
  results.push_back( gausFit->GetChisquare() );
  results.push_back( gausFit->GetNDF() );
  rRes += gausFit->GetParameter(1) * gausFit->GetParameter(1);
  rSigma += gausFit->GetParameter(2) * gausFit->GetParameter(2);

  hYRes->Fit( gausFit );
  results.push_back( gausFit->GetParameter(1) );
  results.push_back( gausFit->GetParameter(2) );
  results.push_back( gausFit->GetChisquare() );
  results.push_back( gausFit->GetNDF() );
  rRes += gausFit->GetParameter(1) * gausFit->GetParameter(1);
  rSigma += gausFit->GetParameter(2) * gausFit->GetParameter(2);

  hZRes->Fit( gausFit );
  results.push_back( gausFit->GetParameter(1) );
  results.push_back( gausFit->GetParameter(2) );
  results.push_back( gausFit->GetChisquare() );
  results.push_back( gausFit->GetNDF() );
  rRes += gausFit->GetParameter(1) * gausFit->GetParameter(1);
  rSigma += gausFit->GetParameter(2) * gausFit->GetParameter(2);

  results.push_back( sqrt( rRes ) );
  results.push_back( sqrt( rSigma ) );

  return results;
}

void
ExtractPosition(
                string lFile,
                string lFit,
                TH1D** hCountVResX,
                TH1D** hCountVResY,
                TH1D** hCountVResZ )
{
  // First new the histograms
  const int kBins = 20;

  *hCountVResX = new TH1D( "XRes", "XRes", kBins, gkStartBin, gkEndBin );
  (*hCountVResX)->SetDirectory( 0 );
  *hCountVResY = new TH1D( "YRes", "YRes", kBins, gkStartBin, gkEndBin );
  (*hCountVResY)->SetDirectory( 0 );
  *hCountVResZ = new TH1D( "zRes", "zRes", kBins, gkStartBin, gkEndBin );
  (*hCountVResZ)->SetDirectory( 0 );

  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
	  RAT::DS::MC *rMC = rDS->GetMC();

      TVector3 mcPos = rMC->GetMCParticle(0)->GetPos();
      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
        {
		  if( iEvent > 0 ) // Only prompt events characterise
			continue;
		  RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          if( rEV->GetFitResult( lFit ).GetValid() == false )
            continue;

          TVector3 fitPos;
          try
            {
              fitPos = rEV->GetFitResult( lFit ).GetVertex(0).GetPosition();
            }
          catch( RAT::DS::FitVertex::NoValueError& e )
            {
              cout << "Position has not been fit." << endl;
              throw;
            }
          TVector3 deltaR = fitPos - mcPos;

          (*hCountVResX)->Fill( fitPos.x() - mcPos.x() );
          (*hCountVResY)->Fill( fitPos.y() - mcPos.y() );
          (*hCountVResZ)->Fill( fitPos.z() - mcPos.z() );
        }
    }
}
