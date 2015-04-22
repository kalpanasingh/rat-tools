# QuadSpeed Coordinator
This folder contains the files needed to coordinate the QuadSpeed fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] QuadSpeed

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates a set of rootfiles (one for each effective speed) of 500 events each.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_QUAD.ratdb located in rat/data, replacing any existing entry with the same index.  

Note: this coordinator can be used to find the effective speed of an unknown material, by taking "labppo_scintillator" as a starting point and proceeding from there.  
If this is desired, please follow the instructions given in the comments of the Template_Macro.mac file.  

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
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_QUAD.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

The Utilities script contains the following function that can be used to get extra information about the Radial Bias vs. Effective Speed relation:  
- DrawPlot(): return one 2D scatter plot - Radial Bias vs. Effective Speed  

To run this function, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities; Utilities.DrawPlot()'

