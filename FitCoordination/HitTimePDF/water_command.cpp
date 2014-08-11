void water_command(string material, int nRuns){
  gROOT->ProcessLine(".L hitTimePDF.cpp+");
  GetH2OPDF(material, nRuns);
  gROOT->ProcessLine(".q");
}
