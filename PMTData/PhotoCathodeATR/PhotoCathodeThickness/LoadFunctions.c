////////////////////////////////////////////////////////
/// Loads the PhotoCathode Thickness files.
///
/// 05/08/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeThickness");
gROOT->ProcessLine(".X /home/jonesph/ROOT/LoadFunctions.c");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/PhotoCathodeATR/PhotoCathodeThickness/DrawPhotoCathodeThickness.cc+");
}
