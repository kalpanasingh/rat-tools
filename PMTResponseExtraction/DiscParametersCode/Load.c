////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/DiscParametersCode");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/DiscParametersCode/ProduceDiscParameters.cc+");
}
