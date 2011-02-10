////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawRespVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawReflVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawRespVsLambda.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawReflVsLambda.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawRespVsEntryPos.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/DrawReflVsEntryPos.cc+");
}
