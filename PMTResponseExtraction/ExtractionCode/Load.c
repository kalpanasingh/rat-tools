////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/ExtractionCode");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/HitDataFull.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/HitDataMinimal.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/EventData.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/FullDataManager.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/MergeFiles.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/ReduceFile.cc+");  
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/ExtractionCode/Extraction.cc+");
}
