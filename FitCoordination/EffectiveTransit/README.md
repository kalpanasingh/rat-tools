# EffectiveTransit Coordinator
This folder contains the files needed to coordinate the EffectiveTransit fitter.  
This method find the effective speed in the scintillator by taking measurements at several positions along a line, finding the time difference between early hits on this axis and using this to calculate the speed.  
This is in comparison to the ScintEffectiveSpeed coordinator, which takes a more pragmatic approach and calculates the effective speed as that which minimises the radial bias of 3 MeV electron events spread through the detector.  

There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EffectiveTransit

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates 11 rootfiles (one for each position in the Utilities script), each containing 500 events at 1MeV.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_EFFECTIVE_TRANSIT.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_EFFECTIVE_TRANSIT.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

The Utilities script contains the following function that can be used to get extra information about the Distance vs. Timing relation:  
- DrawPlots(): return two plots - Distance vs. Time Residual and Distance vs. Transit Time  

To run this function, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities.py; Utilities.DrawPlots()'

