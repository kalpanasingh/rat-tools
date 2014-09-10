# SimpleEnergy Coordinator
This folder contains the files needed to coordinate the SimpleEnergy fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] SimpleEnergy

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates a rootfile containing 1000 events at 1MeV filling the detector, and also located at the detector centre.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_SIMPLE_ENERGY.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 5GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

This production script generates the rootfile as the standard method, but runs them on a Batch system, cutting the required time for the simulation.  
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a set of batch scripts.

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_SIMPLE_ENERGY.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

The Utilities script contains the following function that can be used to get extra information about the Nhits vs. Energy vs. Position relations:  
- PlotNhitsGraphs(): return two plots - Nhits vs. Radius, and Nhits at Detector Centre  

To run this function, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities.py; Utilities.PlotNhitsGraphs()'
