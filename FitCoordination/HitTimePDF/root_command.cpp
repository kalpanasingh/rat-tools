void root_command(string material, int nRuns){
  gROOT->ProcessLine(".L hitTimePDF.cpp+");
  GetScintPDF();
  gROOT->ProcessLine(".q");
}
