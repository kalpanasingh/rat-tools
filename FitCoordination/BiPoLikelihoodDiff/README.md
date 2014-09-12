# BiPoLikelihoodDiff Coordinator

BEFORE RUNNING THIS COORDINATOR, please make sure you have "turned off" the alpha-decay branch of the Bismuth isotope(s) you wish to coordinate.
To do this, edit the Decay0Backg.ratdb file as follows:

- in the entry for the Bismuth isotope(s): "Bi212" and/or "Bi214"
- in the "ProbDecay" field
- set the first number in the square brackets to 0.0

This folder contains the files needed to coordinate the BiPo (Log-Likelihood Difference Method) classifier.  
There are two methods for running this coordinator:

-------------------------


1) standard method, which is the same as other coordinators:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] BiPoLikelihoodDiff

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: REQUIRED Isotope, either '212' or '214' (default = [empty]).  Note that the coordinator will exit automatically if this options is not specified at all.
- [-s]: Scintillator Material to use (default = te_0p3_labppo_scintillator_bisMSB_Dec2013)

This method first runs the ProduceData.py script, which generates 3 rootfiles of 5000 events: electrons at 2.527MeV, Bi-Beta decays, and Po-Alpha decays, all filling the detector.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index.  

------------------------------


2) batch method, which needs to be invoked differently from the standard method:
- in this folder, run the command:

    python ProduceData.py [options]

The options for this script are: [-g], [-l], [-p] and [-s] as specified above, as well as:
- [-b]: Batch configuration file ... absolute location

There already exists a basic "batch.config" file in the "FitCoordination" folder.  However, users may specify their own configuration using that file as a template, and then provide the filename of their new configuration file here.  

- once the production script is complete, the analysis script will NOT begin automatically - it must be run by the user.  To do this, while still in this folder, run the command:

    python AnalyseData.py [options]

The only applicable options for this script are [-b], [-i] and [-p] as described above.  
Note that the analysis script also requires an explicit [-p] to be set - it will exit if this is not done.    
The coordination results are written to the Batch logfile - there will be a complete RATDB entry that should be placed in the CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

