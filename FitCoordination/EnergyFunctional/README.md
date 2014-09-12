# EnergyFunctional Coordinator
This folder contains the files needed to coordinate the Functional Form Energy fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyFunctional

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = labppo_scintillator)

Note that this coordinator does not take a "-p" option.

This method first runs the ProduceData.py script, which generates 90 rootfiles (3 parameters to coordinate, each of which has 6 energies, each of which has 5 parts) of 1000 events each.  Each one takes roughly 1 to 1.5 hours to complete, depending mainly on the scintillator material being used in the simulation.  
Once this is done, the AnalyseData.py script automatically begins - this takes between 1-2 hours to complete.  
The coordination results are written in the "AnalyseData_Results_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the 90 rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 5GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete (i.e. there are 90 complete rootfiles), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b] and [-i] as described above, and it takes roughly 30 minutes to complete.  
The coordination results are written in the "AnalyseData_Results_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

Note about Multiple Coordinations with the Same Data:  
- The analysis is made up of two separate sections:
1) generating plots of H-Parameter vs. various quantities (plots are stored in the "AnalyseData_Results_PlotsForXXX.root" files)
2) fitting functions to these plots (plots are stored in the "AnalyseData_Results_ExtractXXX.root" files)    
- Once the plots in step 1) have been generated, they do not change unless the data itself also changes - therefore step 2) can be performed extremely quickly multiple times without needing to run over the data each time  
- Generation of the plots is enabled by default, but can be disabled by commenting out lines 9, 12 and 15 of the "AnalyseData.py" script  

