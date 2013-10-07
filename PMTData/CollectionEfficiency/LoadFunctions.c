////////////////////////////////////////////////////////
/// Loads the Quantum Efficiencies files.
///
/// 21/07/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/CollectionEfficiency");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/CollectionEfficiency/DrawCollectionEfficiencies.cc+");
}
