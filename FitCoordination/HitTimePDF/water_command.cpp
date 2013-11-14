void water_command(string material, int nRuns){
  gROOT->ProcessLine(".L hitTimePDF.cpp+");
  GetH2OPDF();
  gROOT->ProcessLine(".q");
}
