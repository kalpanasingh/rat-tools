#AlphaBetaLikelihood Coordinator
This folder contains the files needed to coordinate the AlphaBetaLikelihood classifier.  
There are two methods for running this coordinator:

-------------------------


1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] AlphaBetaLikelihood


The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-l]: Load an extra .ratdb directory
- [-p]: REQUIRED Isotope, either '212' or '214' (default = [empty]).  Note that the coordinator will exit automatically if this options is not specified at all.
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates 5 rootfiles of 5000 events: double-beta events, Bi-Beta decays, and Po-alpha decays (one for each pulse-shape scenario), all filling the detector.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to the textfile whose name is given on screen - there will be a complete RATDB entry that should be placed in the ALPHA_BETA_CLASSIFIER.ratdb located in rat/data, replacing any existing entry with the same index.  

------------------------------


2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

This production script generates the same 5 rootfiles as the standard method, but runs them in parallel, cutting the required time for the whole production script.  
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a batch script.

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-p] and [-s] as described above.  
Note that the analysis script also requires an explicit [-p] to be set - it will exit if this is not done.    
The coordination results are written to the textfile whose name is given in the Batch logfile - there will be a complete RATDB entry that should be placed in the ALPHA_BETA_CLASSIFIER.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------


