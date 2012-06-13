{
  gROOT->ProcessLine(".L direction_pdf.cpp+");
  PlotDirections("PDF_10MeV_5k.root");
  gROOT->ProcessLine(".q");
}
