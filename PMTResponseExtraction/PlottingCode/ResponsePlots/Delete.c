////////////////////////////////////////////////////////
/// Deletes the Libraries that exist
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/*_cc.d"); 
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/PlottingCode/ResponsePlots/*_cc.so");
}
