This folder contains the co-ordinator for the directionPDF. This is a 1d pdf of angle of a hit pmt relative to the mc direction of the particle.

ProduceFiles.py will run Data_for_PDF.mac which simulates, by default, 5000 electron events at the centre of a lightwater filled detector.

AnalyseFiles.py calls a root macro GetDirectionPDF from direction_pdf.cpp. This compiles a histogram of the angle of PMT hits relative to the initial direction of the particle. This histogram is then translated into a text format as is used in FIT_DIR.ratdb and printed to screen.

These can be called together, each in turn, using the ./fitcoordinate DirectionPDF command.

* Initial commit 31/05/12 (I.Coulter) *
* Change a few file names and re-configure direction_pdf.cpp 06/02/13 (I.Coulter) *