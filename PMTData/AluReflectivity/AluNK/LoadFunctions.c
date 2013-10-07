////////////////////////////////////////////////////////
/// Loads the Aluminium N & K files
///
/// 09/08/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/AluReflectivity/AluNK");
gROOT->ProcessLine(".X /home/jonesph/ROOT/LoadFunctions.c");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/AluReflectivity/AluNK/DrawAluNK.cc+");
}
