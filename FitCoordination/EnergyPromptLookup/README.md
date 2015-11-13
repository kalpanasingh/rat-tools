# EnergyPromptLookup Coordinator
This folder contains the files needed to coordinate the EnergyPromptLookup fitter.
There are two methods for running the coordinator:

-------------------------

1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EnergyPromptLookup

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: InnerAV Material to use (default = lightwater_sno)

This method first runs the ProduceData.py script, which generates a set of rootfiles (one for each energy/position combination) of 1000 events each.

Once this is done, the AnalyseData.py script automatically begins - this takes about 1hour 30 mins to complete.

The coordination results are written in the "AnalyseData_Output.txt" file - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_PROMPT_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index.

** NOTE: the standard method of coordination takes upwards of 3 days to complete, since the rootfiles are generated one after the other, so it is strongly advised that the user perform the coordination on a batch system using the 2nd method below.

-------------------------

2) batch method, which needs to be invoked differently from the standard method:
- copy this entire folder to a location with around 9GB of free disk-space
- navigate into this new folder, and run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.

- once the production script is complete (i.e. all rootfiles have been generated), the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-i] and [-s] as described above, and it takes roughly 1 hour 30 minutes to complete.
The coordination results are written in the "AnalyseData_Output.txt" - there will be a complete RATDB entry that should be placed in the FIT_ENERGY_PROMPT_LOOKUP.ratdb located in rat/data, replacing any existing entry with the same index.

-------------------------

The Utilities script contains the following functions that can be used to get extra information about the Nhits vs. Energy vs. Position relations:
- PlotMeanPromptNhitsPerEnergy(material): Returns a mean prompt Nhits vs Energy plot for events at the centre of the detector. This is the graphical form of the table that the EnergyPromptLookup fitter uses to map from prompt Nhits to energy.
- PlotPromptNhitsPerEnergy(material): Returns a set of prompt Nhits histograms (one for each energy).
- PlotPositionDirectionScaleFactor(material): Returns a plot of the scale factor that the EnergyPromptLookup fitter uses. The scale factor scales the prompt Nhits for an event, with a particular radius (and direction in the case of scintillator material), to what would have been expected had the event occurred at the centre of the detector.
- PlotHitTimeResiduals(material): Plots the hit time residuals.
- PrintWorkingPMTs(material): Prints the number of working PMTs at the time of fit coordination.

To run these functions, first run the ProduceData script as described above, and then do the following:

    python -c 'import Utilities; Utilities.[name of function](material)'

where the [name of function] is as noted above, and the "material" argument is the same as that used to produce the data.
