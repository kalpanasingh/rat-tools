# NearAVAngular Coordinator
This folder contains the files needed to coordinate the NearAV-Angular fitter.  The following files should be found here:

- AnalyseData.py
- AnalyseData_Short.py
- Coordinate.cpp
- fitcoordinate.config
- ProduceData.py
- ProduceData_Short.py
- README.md
- Template_Coordinate.sh
- Template_Macro.mac
- Template_Submit.sh
- Utilities.py

Any other files that are present SHOULD BE DELETED, since they will interfere with the running of the coordinator.

There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] NearAVAngular

Normal fit coordination options apply (-g, -s, -d), but do not specify a particle type using "-p" - this coordinator does not take that option.  
This method first runs the ProduceData.py script, which generates 8 rootfiles (1 for each of the radius values given in Utilities.py) of 5000 events each.  Each one takes roughly 8-9 hours to complete.  
Once this is done, the AnalyseData.py script automatically begins, which runs the Coordination function found in Coordinate.cpp.  This takes around 17-18 hours.  
** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the 8 rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system.

-------------------------

2) time-saving method, which needs to be invoked differently from the standard method:
- copy this folder to a location with enough space to hold 8 rootfiles of ~3Gb each, and write the ABSOLUTE value of this new location (as a string) to the "currentLoc" field in Utilities.py
- write the ABSOLUTE locations (as strings) of the user's RAT folder and environment setup file into the "ratLoc" and "envrnLoc" fields respectively
- navigate into the folder copy, and run the command:

    python ProduceData_Short.py [options]

Normal options for the production script apply (-g, -s), but do not specify a particle type using "-p" - this coordinator does not take that option.  
This production script generates the same 8 rootfiles as the standard method, but runs them in parallel, cutting the required time for the whole production script to around 8-9 hours in total.  
The user SHOULD NOT run this command on a batch system, since the script itself creates and runs a set of batch commands - the command above must be run in an interactive session.

** NOTE: Batch commands in "ProduceData_Short.py" are currently given as "qsub ... " - this may not work on all systems.  If this is the case, please replace "qsub" with the equivalent batch command.

- once the production script is complete (i.e. there are 8 complete rootfiles), the analysis script will not begin automatically - it must be run by the user.  To do this, while in the folder copy run the command:

    python AnalyseData_Short.py

This analysis script takes no options, and takes the same time to run as in the standard method.  
The AnalyseData_Short script (like the ProduceData_Short script) generates and then runs a batch script, so must be invoked interactively.

** NOTE: Batch commands in "AnalyseData_Short.py" are currently given as "qsub ... " - this may not work on all systems.  If this is the case, please replace "qsub" with the equivalent batch command.

-------------------------

Both methods output the coordinated values to a textfile, "Coordinate_Results.txt".  The progress of the analysis script can be monitored via this text file as the script is being run.  
Once complete, the final section of text in this file should be copy-pasted into the NearAV_Angular fitter's RATDB file located in the rat/data folder: FIT_NEAR_AV_ANGULAR.ratdb .
