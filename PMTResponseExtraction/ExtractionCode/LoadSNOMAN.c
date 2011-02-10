////////////////////////////////////////////////////////
/// Loads PMT analysis functions
///
/// 29/09/10 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath("-I$QSNO_ROOT/include");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/ExtractionCode/SNOMANCode");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/SNOMANCode/ExtractData.cc+");
}
