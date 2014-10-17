# BerkeleyAlphaBeta Coordinator
This folder contains the files needed to coordinate the Berkeley Alpha/Beta classifier.  
There are two methods for running this coordinator:

-------------------------


1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

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

This method first runs the ProduceData.py script, which generates 2 rootfiles of 100000 events: electrons at 5MeV and alphas at 50MeV, at the center of the detector.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to CLASSIFIER_BERKELEY_AB.ratdb as a full ratdb table.
The contents of this file should replace the table with the same index in the similarly named file located in rat/data, or be added to that file if no table with the given index exists.  

------------------------------


2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

Data analysis options as described above are applicable.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the CLASSIFIER_ALPHA_UNSEEDED.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

