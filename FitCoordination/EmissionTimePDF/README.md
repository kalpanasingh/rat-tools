# EmissionTimePDF Coordinator
This folder contains the files needed to coordinate the EmissionTimePDF fitter.  

To run this coordinator:
- navigate to one directory up from this, and then do:

    python fitcoordinate [options] EmissionTimePDF

The following fit coordination options apply:
- [-d]: A location in which to run the scripts, e.g. on a data disk (default = [empty])
- [-g]: Geometry File to use ... location relative to rat/data/ (default = geo/snoplus.geo)
- [-i]: RATDB index to place result (default = [empty])
- [-l]: Load an extra .ratdb directory
- [-p]: Particle type to use ... see generator documentation for available particles (default = 'e-')
- [-s]: Scintillator Material to use (default = labppo_scintillator)

This first runs the ProduceData.py script, which generates a rootfile containing 20 events at 3MeV.  
Once this is done, the AnalyseData.py script automatically begins.  
The coordination results are written to screen - there will be a complete RATDB entry that should be placed in the ET1D.ratdb located in rat/data, replacing any existing entry with the same index.  

-------------------------

The Analysis script contains the following function that can be used to get extra information about the emission times PDF:  
- PlotPDF(): draw the PDF plot  

To run this function, first run the full coordinator as described above, and then do the following:

    python -c 'import AnalyseData.py; AnalyseData.PlotPDF()'

