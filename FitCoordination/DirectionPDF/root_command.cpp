{
  gROOT->ProcessLine(".L /home/coulter/rat-tools/FitCoordination/DirectionPDF/direction_pdf.cpp+");
  PlotDirections("/home/coulter/rat-tools/FitCoordination/DirectionPDF/PDF_10MeV_5k.root");
  gROOT->ProcessLine(".q");
}
