# AlphaUnseeded Coordinator
This folder contains the files needed to coordinate the Unseeded Alpha classifier.  
There are two methods for running this coordinator:

-------------------------


1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] AlphaUnseeded

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates 2 rootfiles of 5000 events: electrons at 0.5MeV and alphas at 5.0MeV (quenched to ~0.5MeV), all filling the detector.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the CLASSIFIER_ALPHA_UNSEEDED.ratdb located in rat/data, replacing any existing entry with the same index.  

------------------------------


2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the CLASSIFIER_ALPHA_UNSEEDED.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

