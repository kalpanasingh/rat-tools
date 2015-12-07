# EnergyRThetaFunctional
This folder contains the files needed to coordinate the EnergyRThetaFunctional fitter.
There are two methods for running the coordinator (second method recommended):

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    ./fitcoordinate [options] EnergyRThetaFunctional

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This method first runs the ProduceData.py script, which generates a set of rootfiles (one for each energy/position) of 1000 events each.
Once this is done, the AnalyseData.py script automatically begins.
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_RTHETA_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- Run the fitcoordinate function as above with a -b option to run on a batch farm (and with an extra -d option if you need to produce data in a different location with extra disk space):

    ./fitcoordinate -b [batch.config] -d [destination] EnergyRThetaFunctional

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location
- [-d]: Destination of output files.

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder (or, if -d was used, in the folder [destination]/EnergyRThetaFunctional), run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-i] and [-s] as described above.
The coordination results will be printed to screen, there will be a complete RATDB entry that should be placed in the FIT_ENERGY_RTHETA_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

The Utilities script contains the following functions that can be used to get extra information about the H vs Energy relationship:  
- CompareMaps(material): plot a comparison of H vs energy from the functional form to the simulated data.

To run these functions, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities.py; Utilities.[name of function](material)'

where the [name of function] is as noted above, and the "material" argument is the same as that used to produce the data.

