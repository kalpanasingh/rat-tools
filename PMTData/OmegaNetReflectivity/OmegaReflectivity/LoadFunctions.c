////////////////////////////////////////////////////////
/// Loads the Omega Reflectivity files.
///
/// 21/07/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/OmegaNetReflectivity/OmegaReflectivity");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/OmegaNetReflectivity/OmegaReflectivity/DrawOmegaReflectivity.cc+");
}
