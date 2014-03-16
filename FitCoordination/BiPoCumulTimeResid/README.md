# BiPoCumulTimeResid Coordinator
There are two methods for running this coordinator:

------------------------------


1) standard method (same as other coordinators)
- navigate to one directory up from this one
- run the command:

    python fitcoordinate BiPoCumulTimeResid

  with the following possible options:

    -s = Scintillator Material (default = te_0p3_labppo_scintillator_Oct2012)
	-g = Geometry File, specified with respect to the RAT data folder: geo/[geofile] (default = geo/snoplus.geo)
    -p = Timing Profile, indicating whether Pulse Shape Discrimination is present (= PSD, default) or Not (= noPSD, alternate option)
    -i = RATDB Index, which must take the form of conecating the explicit -s and -p options (INCLUDING their possible default values), separated by '-' (default = "")
         Because this has an empty string as default, the AnalyseData.py script which uses it will exit with error if this option is NOT assigned

- this will run the Production Script (ProduceData.py) and Analysis Script (AnalyseData.py) one after the other automatically
- NOTE: the production script runs a single macro which generates 8000 electrons at 2.527MeV filling the detector
      : this takes a long time when running interactively, so it is advised to use the second method described below

------------------------------


2) short-timing method, running the Production script on a cluster system
- write the ABSOLUTE location of this folder (as a string) in the "currentLoc" field in Utilities.py
- write the ABSOLUTE location of the user's environment setup file (as a string) into the "envronLoc" field in Utilities.py
- in this folder, run the command:

    python ProduceData_ShortTime.py

  with the -s, -g and -p options as described above (but not the -i)

- once the simulation has completed (~6.5 hours), run the command:

   python AnalyseData.py

  with only the -i option as described above

------------------------------


Both of these methods will output to screen a full RATDB entry that should be placed in the CLASSIFIER_BIPO_CUMULTIMERESID.ratdb located in rat/data, replacing any existing entry with the same index.

