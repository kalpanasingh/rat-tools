////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/DrawEntryPosVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/DrawReflAngleDistVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/DrawTransitTimeVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/DrawAngleDist.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/DrawEntryPosDistVsAngle.cc+");
}
