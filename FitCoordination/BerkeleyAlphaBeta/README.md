# BerkeleyAlphaBeta Coordinator
This folder contains the files needed to coordinate the Berkeley Alpha/Beta classifier.  
There are two methods for running this coordinator:

-------------------------

1) Standard method, which is the same as other coordinators:
- Navigate to one directory up from this, and then run:

    python fitcoordinate [options] BerkeleyAlphaBeta

The following fit coordination options apply:

For data production:
- [-l]: Load an extra .ratdb directory
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-s]: Scintillator Material to use (default = labppo_scintillator)

For data analysis:
- [-i]: RATDB index to place result (default = [empty])
- [-f]: First time (in ns) in the time residual PDF (default = 200)
- [-l]: Last time (in ns) in the time residual PDF (default = 1000)
- [-s]: Step time (in ns) in the time residual PDF (default = 1)
- [-r]: Max retrigger wait time (in ns) from start of previous event (default = 600)

This method does a full production/analysis which generates 2 ROOT files, electrons at 5MeV and alphas at 50MeV, of 100000 events at the center of the detector.  
The coordination results are written to CLASSIFIER_BERKELEY_AB.ratdb as a full ratdb table.
The contents of this file should replace the table with the same index in the similarly named file located in rat/data, or be added to that file if no table with the given index exists.  

------------------------------

2) Batch method, which needs to be invoked differently from the standard method. 
This requires a batch condiguration. There already exists a basic "batch.config" file in the "FitCoordination" folder.  
Users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- Begin batch run of data production with (executed from this folder):

    python ProduceData.py -b /path/to/batch/config/file [options]

Data production options as described above are applicable.

- After data production finishes, batch run the analysis with (executed from this folder):

    python AnalyseData.py -b /path/to/batch/config/file [options]

Data analysis options as described above are applicable.  

The output of the batch method is identical to the bare method above.

-------------------------

