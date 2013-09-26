////////////////////////////////////////////////////////
/// Loads the Aluminium Reflectivity Files
///
/// 09/08/10 - New File
////////////////////////////////////////////////////////

{
gROOT->ProcessLine(".X /home/jonesph/ROOT/LoadFunctions.c");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeNK");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeThickness");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/PhotoCathodeATR");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/ATRFunctions.cc+");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/DrawPhotoCathodeATR.cc+");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/DrawReflectivityVThickness.cc+");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/DrawReflectivityVPosition.cc+");
}
