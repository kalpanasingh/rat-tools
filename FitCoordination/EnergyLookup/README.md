# EnergyLookup Coordinator
This folder contains the files needed to coordinate the EnergyLookup fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyLookup

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates a set of rootfiles (one for each energy/position combination) of 500 events each.  Each one takes roughly 1 to 1.5 hours to complete, depending mainly on the scintillator material being used in the simulation.  
Once this is done, the AnalyseData.py script automatically begins - this takes between 1-2 hours to complete.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 5GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

This production script generates the same rootfiles as the standard method, but runs them in parallel, cutting the required time for the whole production script.  
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a set of batch scripts.

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-i] and [-s] as described above, and it takes roughly 30 minutes to complete.  
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

The Utilities script contains the following functions that can be used to get extra information about the Nhits vs. Energy vs. Position relations:  
- PlotNHitsPerPosition(material): return a set of Nhits vs. Position plots (one for each Energy)  
- PlotNHitsPerEnergy(material): return a set of Nhits vs. Energy plots (one for each Position)  

To run these functions, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities.py; Utilities.[name of function](material)'

where the [name of function] is as noted above, and the "material" argument is the same as that used to produce the data.

