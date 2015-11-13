# EnergyRSP Coordinator (Part 2)
This folder contains the files needed to coordinate part 2 of the EnergyRSP fitter.  
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyRSP-Part2

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-s]: InnerAV Material to use (default = lightwater_sno)

This method first runs the ProduceData.py script, which generates a set of rootfiles (by reading in the root files created for each energy in part 1).

Once this is done, the AnalyseData.py script automatically begins - this takes several hours to complete.

The coordination results are written in the "AnalyseData_Output.txt" file - there will be a table that needs to be copied to the corresponding index in FIT_ENERGY_RSP.ratdb located in rat/data, replacing any existing table with the same name.  

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 30GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-l], and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-i] and [-s] as described above, and it takes roughly 1 hour to complete.

The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_RSP.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

The Utilities script contains the following functions that can be used to get extra information about the fitter:
- PlotMeanPredictedNCerenkovVsEnergy(material): return a predicted NCerenkov vs. Energy plot
- PlotPredictedNCerenkovPerEnergy(material): return a set of predicted NCerenkov distribution plots (one for each Energy)

To run these functions, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities; Utilities.[name of function](material)'

where the [name of function] is as noted above, and the "material" argument is the same as that used to produce the data.
