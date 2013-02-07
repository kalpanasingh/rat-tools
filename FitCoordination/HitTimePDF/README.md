This folder contains the co-ordinator for time residual PDFs based on PDF hit time.

ProduceFiles.py will run Data_for_PDF.mac which simulates, by default, 20,000 3 MeV electron events throughtout the scintillator volume.

AnalyseFiles.py calls a root macro GetScintPDF from hitTimePDF.cpp. This compiles a histogram of the time residuals of PMT hits based on MC information. This histogram is then translated into a text format as is used in ET1D.ratdb and is printed to screen.

These can be called together, each in turn, using the ./fitcoordinate HitTimePDF command.

Notes for the user:

- To make a pdf for water, group velocitys are used to calculate the time residuals. To do this, change GetScintPDF() to GetH2OPDF() in root_command.cpp. The energy of the events simulated in the macro should also be changed as 3 MeV is too low for water events. Somewhere around 6-10 MeV would work better.

- The PDFs added to RAT use data from 100,000 events spread across 5 rootfiles. To use data from multiple rootfiles in the same PDF, simply repeat the line FillScintTimeResiduals(filename,histname) with the additional file you want to include but the same histogram.

This approach is recommended as simulating many events in a single rootfile (as opposed to parallel across several) will take longer and reduces the chance of one corrupt file ruining everything.

* Initial commit 06/02/13 (I.Coulter) *