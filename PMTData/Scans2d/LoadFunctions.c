////////////////////////////////////////////////////////
/// Loads the 2d scan files
///
/// 09/05/13 - New File
////////////////////////////////////////////////////////

{
  gSystem->AddIncludePath(" -I/Users/jonesph_local/pmt-data/Scans2d");
  gROOT->ProcessLine(".L /Users/jonesph_local/pmt-data/Scans2d/DrawScansAndAverage.cc+");
}
