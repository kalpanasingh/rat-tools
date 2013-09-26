////////////////////////////////////////////////////////
/// Loads the Photocathode N & K files
///
/// 10/08/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeNK");
gROOT->ProcessLine(".X /home/jonesph/ROOT/LoadFunctions.c");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeNK/DrawPhotoCathodeNK.cc+");
}
