# BiPoLikelihoodDiff Coordinator

BEFORE RUNNING THIS COORDINATOR, please make sure you have "turned off" the alpha-decay branch of the Bismuth isotope(s) you wish to coordinate.
To do this, edit the Decay0Backg.ratdb file as follows:

- in the entry for the Bismuth isotope(s): "Bi212" and/or "Bi214"
- in the "ProbDecay" field
- set the first number in the square brackets to 0.0


There are two methods for running this coordinator:


------------------------------


1) standard method (same as other coordinators)
- navigate to one directory up from this one
- run the command:

    python fitcoordinate BiPoLikelihoodDiff

  with the following possible options:

    -s = Scintillator Material (default = te_0p3_labppo_scintillator_Oct2012)
	-g = Geometry File, specified with respect to the RAT data folder: geo/[geofile] (default = geo/snoplus.geo)
    -p = Combined Isotope-Timing, indicating which Isotope ('212' or '214') and if Pulse Shape Discrimination is present ('PSD') or Not ('noPSD') (default = "")
	     Both parts of this option must be explicitly assigned, and separated by a '-' (e.g. "212-PSD" or "214-noPSD")
         Because this has an empty string as default, the ProduceData.py script which uses it will exit with error if this option is NOT assigned
    -i = RATDB Index, which must take the form of conecating the explicit -s and -p options (INCLUDING their possible default values), separated by '-' (default = "")
         Because this has an empty string as default, the AnalyseData.py script which uses it will exit with error if this option is NOT assigned

- this will run the Production Script (ProduceData.py) and Analysis Script (AnalyseData.py) one after the other automatically
- NOTE: the production script runs 3 macros which generates 5000 electrons at 2.527MeV, 5000 Bi-Beta decays and 5000 Po-Alpha decays all filling the detector
      : this takes a long time when running interactively, so it is advised to use the second method described below

------------------------------


2) short-timing method, running the Production script on a cluster system
- write the ABSOLUTE location of this folder (as a string) in the "currentLoc" field in Utilities.py
- write the ABSOLUTE location of the user's environment setup file (as a string) into the "envronLoc" field in Utilities.py
- in this folder, run the command:

    python ProduceData_ShortTime.py

  with the -s, -g and -p options as described above (but not the -i)

- once this has completed (~3 hours), run the command:

   python AnalyseData.py

  with only the -i option as described above

------------------------------


Both of these methods will output to screen a full RATDB entry that should be placed in the CLASSIFIER_BIPO_LIKELIHOODDIFF.ratdb located in rat/data, replacing any existing entry with the same index.

