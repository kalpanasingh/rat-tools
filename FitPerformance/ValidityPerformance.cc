////////////////////////////////////////////////////////
/// Produces a table of numbers characterising the validity 
/// of the fitter.
///
/// P G Jones <p.jones22@physics.ox.ac.uk>
///
/// 14/06/11 - New File
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

void
ExtractValidity(
				string lFile,
				string lFit,
				double& validity );

void
ValidityPerformance(
					string lFit )
{
  vector< pair< string, string > > posFiles = PositionFiles();
  vector< pair< string, string > > energyFiles = EnergyFiles();

  stringstream latexOut;
  latexOut.setf( ios::fixed, ios::floatfield );
  latexOut.precision( 4 );
  latexOut << "\\begin{table}" << endl << "\\begin{center}\\begin{tabular}{ @{\\extracolsep{\\fill}} | c | c | c |}" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "Egen & Rgen & Validity \\\\" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "[MeV] & [mm] & [\\%] \\\\" << endl;
  latexOut << "\\hline" << endl;

  for( vector< pair< string, string > >::iterator iTer = posFiles.begin(); iTer != posFiles.end(); iTer++ )
	{
	  double validity;
	  ExtractValidity( iTer->second, lFit, validity );
	  latexOut << "3 & " << iTer->first << " & " << validity << "\\\\" << endl;
	}
  
  latexOut << "\\hline" << endl;
  for( vector< pair< string, string > >::iterator iTer = energyFiles.begin(); iTer != energyFiles.end(); iTer++ )
    {
	  double validity;
      ExtractValidity( iTer->second, lFit, validity );
      latexOut << iTer->first << " & fill" << " & " << validity << "\\\\" << endl;
    }
  latexOut << "\\hline" << endl;
  latexOut << "\\end{tabular}\\end{center}" << endl;
  latexOut << "\\caption{Fit Result validity table as produced by the Fitter Performance tool.}" << endl;
  latexOut << "\\end{table}";

  cout << latexOut.str() << endl;
}

void
ExtractValidity(
			string lFile,
			string lFit,
			double& validity )
{
  double events = 0.0;
  double valid = 0.0;
  // Now extract the data
  // Load the first file
  RAT::DS::Root* rDS;
  RAT::DS::PMTProperties* rPMTList;
  TChain* tree;

  LoadRootFile( lFile, &tree, &rDS, &rPMTList );

  for( int iLoop = 0; iLoop < tree->GetEntries(); iLoop++ )
    {
      tree->GetEntry( iLoop );
      for( int iEvent = 0; iEvent < rDS->GetEVCount(); iEvent++ )
        {
		  if( iEvent > 0 ) // Only prompt events characterise
			continue;
		  events += 1.0;
		  RAT::DS::EV *rEV = rDS->GetEV( iEvent );
          if( rEV->GetFitResult( lFit ).GetValid() == false )
            continue;
		  valid += 1.0;
        }
    }
  validity = valid / events;
}
