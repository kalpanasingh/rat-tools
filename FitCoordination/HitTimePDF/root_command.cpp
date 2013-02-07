{
  gROOT->ProcessLine(".L hitTimePDF.cpp+");
  GetScintPDF();
  gROOT->ProcessLine(".q");
}
