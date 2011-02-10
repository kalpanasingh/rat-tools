////////////////////////////////////////////////////////
/// Deletes the Libraries that exist
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/ExtractionCode/Delete.c");
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/CalibrationPlots/Delete.c"); 
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/Delete.c");
  gROOT->ProcessLine(".X $RATTOOLS/PMTResponseExtraction/PlottingCode/InfoPlots/Delete.c");
}
