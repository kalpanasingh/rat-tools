# EnergyPromptHits Coordinator
This folder contains the files needed to coordinate the EnergyPromptHits fitter.
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyPromptHits

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: InnerAV Material to use (default = lightwater_sno)

This method first runs the ProduceData.py script, which generates a root file of 1000 events.

Once this is done, the AnalyseData.py script automatically begins.

The coordination results are written in the "AnalyseData_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_PROMPT_HITS.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder
- navigate into the new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-i] and [-s] as described above.
The coordination results are written in the "AnalyseData_Output.txt" - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_PROMPT_HITS.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

The Utilities script contains the following functions that can be used to get extra information about the Nhits vs. Energy vs. Position relations:
- PlotPromptNhits(material): Returns a plot of the prompt hits distribution.
- PlotHitTimeResiduals(material): Plot the hit time residuals.
- PrintWorkingPMTs(material): Prints the number of working PMTs at the time of fit coordination.

To run these functions, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities; Utilities.[name of function](material)'

where the [name of function] is as noted above, and the "material" argument is the same as that used to produce the data.
