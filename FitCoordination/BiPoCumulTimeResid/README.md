# BiPoCumulTimeResid Coordinator
This folder contains the files needed to coordinate the BiPo (Cumulative Time Residuals Method) classifier.  
There are two methods for running this coordinator:

-------------------------


1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] BiPoCumulTimeResid

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = te_0p3_labppo_scintillator_bisMSB_Dec2013)

Note that this coordinator does not take a "-p" option.

This method first runs the ProduceData.py script, which generates 1 rootfile of 8000 events: electrons at 2.527MeV filling the detector.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the CLASSIFIER_BIPO_CUMULTIMERESID.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: the standard method of coordination takes a long time to complete, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

This production script generates the same rootfile as the standard method, but running on a batch system cuts the required time for the simulation.  
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a batch script.

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the CLASSIFIER_BIPO_CUMULTIMERESID.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

