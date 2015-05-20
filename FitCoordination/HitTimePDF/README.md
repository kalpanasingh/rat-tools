# HitTimePDF Coordinator
This folder contains the files needed to coordinate the HitTimePDF fitter - a histogram of the hit PMT time residuals based on MC information.
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] HitTimePDF

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates 20 rootfiles containing 5000 events each at the AV centre (the energy is automatically set by the material chosen).  
Once this is done, the AnalyseData.py script automatically begins - this automatically takes into account the different analyses that are required for a water- and scintillator-filled detector.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in either the ET1D.ratdb or the GV1D.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

Available options for this script are [-b] and [-s] as described above.  Additionally, users may pass a "-v [velocity]" option when coordinating ET1D values, this allows to recoordinate a PDF with an updated effective velocity without requiring data be re-simulated (useful when iterating coordination of ET1D and ScintEffectiveSpeed).

The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in either the ET1D.ratdb or the GV1D.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

