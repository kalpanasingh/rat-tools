////////////////////////////////////////////////////////
/// Loads the Quantum Efficiencies files.
///
/// 21/07/10 - New File
////////////////////////////////////////////////////////

{
gSystem->AddIncludePath(" -I/home/jonesph/PMTResponseData/QuantumEfficiency");
gROOT->ProcessLine(".L /home/jonesph/PMTResponseData/QuantumEfficiency/DrawQuantumEfficiencies.cc+");
}
