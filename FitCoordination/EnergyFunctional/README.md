# EnergyFunctional Coordinator
This folder contains the files needed to coordinate the Functional Form Energy fitter.  The following files should be found here:
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyFunctional

Normal fit coordination options apply (-g, -s, -i, -d), but do not specify a particle type using "-p" - this coordinator does not take that option.

This method first runs the ProduceData.py script, which generates 90 rootfiles (3 parameters to coordinate, each of which has 6 energies, each of which has 5 parts) of 1000 events each.  Each one takes roughly 2-3 hours to complete.  
Once this is done, the AnalyseData.py script automatically begins - this takes between 20 and 30 minutes to complete.  
The coordination results are displayed in your terminal - after any warning messages (which can be ignored unless they are actually errors), there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.

** NOTE: the standard method of coordination takes upwards of 4 days to complete, since the 90 rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) time-saving method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 1GB of free disk-space, and write the ABSOLUTE value of this new location (as a string) to the "currentLoc" field in Utilities.py
- write the ABSOLUTE location (as strings) of the user's environment setup file into the "envrnLoc" field in Utilities.py
- navigate into the folder copy, and run the command:

    python ProduceData_ShortTime.py [options]

Normal options for the production script apply (-g, -s), but do not specify a particle type using "-p" - this coordinator does not take that option.  
This production script generates the same 90 rootfiles as the standard method, but runs them in parallel, cutting the required time for the whole production script. 
The command above must be run in an interactive session, not through a batch script, since the production script itself creates and runs a set of batch scripts.

** NOTE: Batch commands in "ProduceData_ShortTime.py" are currently given as "qsub ... " - this may not work on all systems.  If this is the case, please replace "qsub" with the equivalent batch command.

- once the production script is complete (i.e. there are 90 complete rootfiles), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in the copied folder, run the command:

    python AnalyseData_ShortTime.py [options]

Normal options for the analysis script apply (-i), and it takes roughly 10 minutes to complete.  
The coordination results are displayed in the batch log-file associated with the "SubmitAnalysisScript.sh" file - at the end, there will be a complete RATDB entry that should be placed in the FIT_ENERGY_FUNCTIONAL.ratdb located in rat/data, replacing any existing entry with the same index.

