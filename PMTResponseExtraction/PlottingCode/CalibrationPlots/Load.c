////////////////////////////////////////////////////////
/// Loads PMT extraction functions
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Load.c");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode");
  gSystem->AddIncludePath(" -I$RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/DrawCalibRespVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/DrawCalibReflVsAngle.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/DrawCalibRespVsEntryPos.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/DrawCalibReflVsEntryPos.cc+");
  gROOT->ProcessLine(".L $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/DrawCalibTransitTime.cc+");
}
