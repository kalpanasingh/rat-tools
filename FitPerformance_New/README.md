# FitPerformance
This folder contains software that can be used to test the performance (bias and resolution) of the reconstruction fitters in RAT.  
The performance of up to 2 fitters can be compared simultaneously, or alternatively the performance of a single fitter can be tested on its own.  
The software is divided into separate folders according to the fitted quantities that can be tested:
- Energy
- Position
[ * more to be added * ]
Each quantity's code is used in an identical way, as described below.  

** NOTE: each quantity required A LOT of data (550 ROOTfiles each), and so this software must be run in a location with at least 30GB of free space!

-------------------------

1) Navigate into the folder corresponding to the quantity you wish to check the performance of, and open the "Template_Macro.mac" file.  
2) In the designated sections of the macro, set the fitter or fitters you wish to run, and make a note of the name(s) you give to the fitter(s).  
3) Produce the data by doing:

    python ProduceData.py [options]

with the following options:
- [-b]: Batch configuration file ... absolute location
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-l]: Load an extra .ratdb directory
- [-s]: Scintillator Material to use (default = labppo_scintillator)
- [-p]: Particle to use (default = e-)

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

4) Once all ROOTfiles are produced correctly, run the analysis script by doing:

    python AnalyseData.py [options]

with the following options:
- [-b]: Batch configuration file ... absolute location
- [-s]: Scintillator Material to use (default = labppo_scintillator)
- [--f1]: the name of the first fitter, as set in the Template_Macro.mac file from step 2)
- [--f2]: the name of second fitter if used, again as set in the Template_Macro.mac file from step 2)

** NOTE 1: the -b and -s options must be specified here, as this script is independent from the ProduceData script
** NOTE 2: note the 2 hyphens in front of the --f1 and --f2 options, as opposed to the single hyphens used with the -b and -s options

This scripts takes around 2.5 hours to run per fitter, and produces a set of results files:
- (per fitter) a ROOTfile containing plots of the (fitted - true) value of the tested quantity at each (energy / y-coordinate / z-coordinate) combination  
- (per fitter) a text file containing the raw bias and resolution for each fitter at each (energy / y-coordinate / z-coordinate) combination  
- a ROOTfile containing per-energy plots of the bias, resolution and chi-squared values against varying y and z (if 2 fitters were specified, they will be drawn on the same plot)
- a sub-folder containing a per-material folder with .png versions of the combined plots above

-------------------------

If you wish to publish the performance plots on a webspace, a script is available that will create a simple webpage for you that will display the .png images.  Run this script by doing:

    python CreateWebpages.py [options]

with the following options:
- [-s]: Scintillator Material to use (default = labppo_scintillator)
- [--f1]: the name of the first fitter, as written in the Template_Macro.mac file from step 2)
- [--f2]: the name of second fitter if one was used, again as written in the Template_Macro.mac file from step 2)
- [-v]: the version of RAT that was used to check the fitter performance

This script will create a .html file in the same folder as the .png images sub-folder is located.  

