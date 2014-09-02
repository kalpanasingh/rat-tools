////////////////////////////////////////////////////////
/// Produces a table of numbers characterising the execution
/// time of the fitter.
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

#include <TGraph.h>
#include <TChain.h>
#include <TFile.h>
#include <TF1.h>
using namespace ROOT;

#include <string>
#include <sstream>
#include <utility>
using namespace std;

vector<double>
FitExecutionTimeRes(
					TGraph* gPos,
					TGraph* gNhit );

void
ExtractExecutionTime(
					 string lFile,
					 string lFit,
					 TGraph* gPlot,
                     int& plotPoint,
                     bool pos );

void
ExecutionTimePerformance(
						 string lFit )
{
  vector< pair< string, string > > posFiles = PositionFiles();
  vector< pair< string, string > > energyFiles = EnergyFiles();

  stringstream latexOut;
  latexOut.setf( ios::scientific, ios::floatfield );
  latexOut.precision( 1 );
  latexOut << "\\begin{table}" << endl << "\\begin{center}\\begin{tabular}{ @{\\extracolsep{\\fill}} | c | c | c | c |}" << endl;
  latexOut << "\\hline" << endl;
  latexOut << " & Parameter 0 ($P_0$)[s] & Parameter 1 ($P_1$)[s/nhit] & $\\frac{ \\chi^2 }{ ndf }$ \\\\" << endl; 
  latexOut << "\\hline" << endl;

  TGraph* gPos = new TGraph();
  int posPoint = 0;
  TGraph* gNhit = new TGraph();
  int nhitPoint = 0;

  for( vector< pair< string, string > >::iterator iTer = posFiles.begin(); iTer != posFiles.end(); iTer++ )
	ExtractExecutionTime( iTer->second, lFit, gPos, posPoint, true );
  for( vector< pair< string, string > >::iterator iTer = energyFiles.begin(); iTer != energyFiles.end(); iTer++ )
	ExtractExecutionTime( iTer->second, lFit, gNhit, nhitPoint, false );

  vector<double> fitResults = FitExecutionTimeRes( gPos, gNhit );
  latexOut << "Position, $ t = P_0 $ & " << fitResults[0] << "$\\pm$" << fitResults[1] << " & & $\\frac{ " << fitResults[2] << " }{ " << fitResults[3] << "}$ \\\\" << endl;
  latexOut << "\\hline" << endl;
  latexOut << "NHit, $ t = P_0 + P_1 \\cdot r $ & " << fitResults[4] << "$\\pm$" << fitResults[5] << " & " << fitResults[6] << "$\\pm$" << fitResults[7] << " & $\\frac{ " << fitResults[8] << " }{ " << fitResults[9] << "}$ \\\\" << endl;
  

  latexOut << "\\hline" << endl;
  latexOut << "\\end{tabular}\\end{center}" << endl;
  latexOut << "\\caption{Fitter execution time table as produced by the Fitter Performance tool.}" << endl;
  latexOut << "\\end{table}";

  cout << latexOut.str() << endl;
}

vector<double>
FitExecutionTimeRes(
					TGraph* gPos,
					TGraph* gNhit )

{
  vector<double> results;
  TF1* constFit = new TF1( "pol0", "pol0", 0.0, 6000.0 );
  gPos->Fit( constFit );
  results.push_back( constFit->GetParameter(0) );
  results.push_back( constFit->GetParError(0) );
  results.push_back( constFit->GetChisquare() );
  results.push_back( constFit->GetNDF() );

  TF1* linearFit = new TF1( "pol1", "pol1", 0, 3000 );
  gNhit->Fit( linearFit );
  results.push_back( linearFit->GetParameter(0) );
  results.push_back( linearFit->GetParError(0) );
  results.push_back( linearFit->GetParameter(1) );
  results.push_back( linearFit->GetParError(1) );
  results.push_back( linearFit->GetChisquare() );
  results.push_back( linearFit->GetNDF() );

  return results;
}

void
ExtractExecutionTime(
					 string lFile,
					 string lFit,
					 TGraph* gPlot,
					 int& plotPoint,
					 bool pos )
{
  // Now extract the data

  RAT::DU::DSReader dsReader( lFile );
  const RAT::DU::PMTInfo rPMTList = DS::DU::Utility::Get()->GetPMTInfo();

  for( int iEntry = 0; iEntry < dsReader.GetEntryCount(); iEntry++ )
    {
      const RAT::DS::Entry& rDS = dsReader.GetEntry( iEntry );

      for( int iEvent = 0; iEvent < rDS.GetEVCount(); iEvent++ )
        {
		  if( iEvent > 0 ) // Only prompt events characterise
			continue;
		  const RAT::DS::EV& rEV = rDS.GetEV( iEvent );
          if( rEV->GetFitResult( lFit ).GetValid() == false )
            continue;

		  if( pos )
			gPlot->SetPoint( plotPoint, rDS.GetMC().GetMCParticle(0).GetPosition().Mag(), GetFitResult( lFit ).GetExecutionTime() );
		  else
			gPlot->SetPoint( plotPoint, rEV.GetCalPMTs().GetCount(), rEV.GetFitResult( lFit ).GetExecutionTime() );
		  plotPoint++;
        }
    }
}
