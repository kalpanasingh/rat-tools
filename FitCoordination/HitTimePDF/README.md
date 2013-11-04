This folder contains the co-ordinator for time residual PDFs based on PDF hit time.

ProduceFiles.py will run Data_for_PDF.mac which simulates, by default, 100,000 3 MeV electron events throughtout the scintillator volume.

AnalyseFiles.py calls a root macro GetScintPDF from hitTimePDF.cpp. This compiles a histogram of the time residuals of PMT hits based on MC information. This histogram is then translated into a text format as is used in ET1D.ratdb and is printed to screen.

These can be called together, each in turn, using the ./fitcoordinate HitTimePDF command.

Alternatively, to split the number of events generated up, call (e.g. from batch jobs):

    ./ProduceFiles.py -s <scint material> -r <run number> -n <number of events>

It is recommended that you split at least to 5 runs (i.e. run number from 1 through 5) sets of 20000 events.

Once these jobs have finished, call:

    ./AnalyseFiles.py -s <scint material> -r <total number of runs, starting from 1>

To produce the RATDB tables.

Notes for the user:

- Water and scintillator phase results are already accounted for (with 8 MeV electrons generated for lightwater_sno), the analysis is also different.

- It is recommended to run 100,000 events to generate the velocity tables (e.g. runs 1-10 inclusive with 10k events each)

* Initial commit 06/02/13 (I.Coulter) *