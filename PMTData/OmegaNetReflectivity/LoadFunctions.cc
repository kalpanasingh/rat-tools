////////////////////////////////////////////////////////
/// Loads the Omega Reflectivity files.
///
/// 21/07/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/OmegaNetReflectivity/OmegaReflectivity");
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/OmegaNetReflectivity/OmegaPromptScaling");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/OmegaNetReflectivity/DrawOmegaNetReflectivity.cc+");
}
