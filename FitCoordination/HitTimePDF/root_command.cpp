void root_command(string material, int nRuns, float velocity){
  gROOT->ProcessLine(".L hitTimePDF.cpp+");
  GetScintPDF(material, nRuns, velocity);
  gROOT->ProcessLine(".q");
}
