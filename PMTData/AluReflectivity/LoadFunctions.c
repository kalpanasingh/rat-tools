////////////////////////////////////////////////////////
/// Loads the Aluminium Reflectivity Files
///
/// 09/08/10 - New File
////////////////////////////////////////////////////////

{
gROOT->ProcessLine(".X /home/jonesph/ROOT/LoadFunctions.c");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/AluReflectivity/AluNK");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/AluReflectivity");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/AluReflectivity/DrawAluReflectivity.cc+");
}
