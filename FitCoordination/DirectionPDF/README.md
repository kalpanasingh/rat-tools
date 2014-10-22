# DirectionPDF Coordinator
This folder contains the files needed to coordinate the DirectionPDF fitter - a 1D PDF of the hit PMTs' angles relative to the MC direction of the particle.
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] DirectionPDF

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus_water.geo)
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = lightwater_sno)

This method first runs the ProduceData.py script, which generates 1 rootfile containing 5000 10MeV events at the AV centre.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_DIR.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-s] as described above.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_DIR.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

