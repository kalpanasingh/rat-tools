# EnergyFunctional Coordinator
This folder contains the files needed to coordinate the Functional Form Energy fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyFunctional

Normal fit coordination options apply (-g, -s, -i, -d), but do not specify a particle type using "-p" - this coordinator does not take that option.

This method first runs the ProduceData.py script, which generates 90 rootfiles (3 parameters to coordinate, each of which has 6 energies, each of which has 5 parts) of 1000 events each.  Each one takes roughly 1 to 1.5 hours to complete, depending mainly on the scintillator material being used in the simulation.  
Once this is done, the AnalyseData.py script automatically begins - this takes between 1-2 hours to complete.  
The coordination results are written in the "AnalyseData_Results_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the 90 rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) time-saving method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 10GB of free disk-space, and write the ABSOLUTE value of this new location (as a string) to the "currentLoc" field in Utilities.py
- write the ABSOLUTE location (as a string) of the user's environment setup file into the "envronLoc" field in Utilities.py
- navigate into the folder copy, and run the command:

    python ProduceData_ShortTime.py [options]

Normal options for ONLY the production script apply (-g, -s), but do not specify a particle type using "-p" - this coordinator does not take that option.  
This production script generates the same 90 rootfiles as the standard method, but runs them in parallel, cutting the required time for the whole production script. 
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a set of batch scripts.

** NOTE: Batch commands in "ProduceData_ShortTime.py" are currently given as "qsub ... " - this may not work on all systems.  If this is the case, please replace "qsub" with the equivalent batch command.

- once the production script is complete (i.e. there are 90 complete rootfiles), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in the copied folder, run the command:

    python AnalyseData_ShortTime.py [options]

Normal options for the analysis script ONLY apply (-i), and it takes roughly 30 minutes to complete.  
The coordination results are written in the "AnalyseData_Results_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.  

** NOTE: Batch commands in "AnalyseData_ShortTime.py" are currently given as "qsub ... " - this may not work on all systems.  If this is the case, please replace "qsub" with the equivalent batch command.

-------------------------

Note about Multiple Coordinations with the Same Data:  
- The analysis is made up of two separate sections: 1) generating plots of H-Parameter vs. various quantities ("AnalyseData_Results_PlotsForXXX.root"), and 2) fitting functions to these plots ("AnalyseData_Results_ExtractXXX.root")    
- Once the plots in 1) have been generated, they do not change unless the data itself also changes - therefore step 2) can be performed extremely quickly multiple times without needing to run over the data each time  
- Regeneration of the plots is enabled by default, but can be disabled by commenting out lines 24, 43 and 70 of the "AnalyseData.py" script  

