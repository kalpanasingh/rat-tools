////////////////////////////////////////////////////////
/// Loads RAT extraction function
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/ExtractionCode/RATCode");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/RATCode/ExtractData.cc+");
}
