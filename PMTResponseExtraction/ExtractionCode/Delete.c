////////////////////////////////////////////////////////
/// Deletes the Libraries that exist
///
/// 12/01/11 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/*_cc.d"); 
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/*_cc.so");
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/RATCode/*_cc.d"); 
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/RATCode/*_cc.so");  
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/SNOMANCode/*_cc.d"); 
  gROOT->ProcessLine(".! rm $RATTOOLS/PMTResponseExtraction/ExtractionCode/SNOMANCode/*_cc.so");
}
