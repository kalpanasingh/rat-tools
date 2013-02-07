{
  gROOT->ProcessLine(".L direction_pdf.cpp+");
  GetDirectionPDF();
  gROOT->ProcessLine(".q");
}
