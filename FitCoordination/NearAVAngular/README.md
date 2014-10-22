# NearAVAngular Coordinator
This folder contains the files needed to coordinate the NearAV (Angular Positions Method) fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] NearAVAngular

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates 8 rootfiles (1 for each of the radius values given in the ProduceData.py script) of 5000 events each.  Each one takes roughly 6-7 hours to complete, depending mainly on the scintillator material being used in the simulation.  
Once this is done, the AnalyseData.py script automatically begins - this takes around 6-7 hours to complete.  
The coordination results are written to the Coordinate_Results.txt file - there will be a complete RATDB entry that should be placed in the FIT_NEAR_AV_ANGULAR.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 8GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above, and it takes a few hours to complete.  
The coordination results are written to the Coordinate_Results.txt file - there will be a complete RATDB entry that should be placed in the FIT_NEAR_AV_ANGULAR.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

