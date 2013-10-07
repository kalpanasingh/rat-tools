////////////////////////////////////////////////////////
/// Loads the Omega Reflectivity files.
///
/// 21/07/10 - New File
////////////////////////////////////////////////////////

{
  gROOT->ProcessLine(".X /home/jonesph/ROOT/PHILUtil/LoadFunctions.c");

  gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/GreyDisc");
  gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/GreyDisc/DrawGreyDiscParameters.cc+");
  gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/GreyDisc/DrawGreyDiscCalibResponse.cc+");
}
