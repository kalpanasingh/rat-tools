##Definitions 

PMT face - the approximate circle formed by the outer edges of the petals of
	the PMT concentrator.

PMT effectiveness or response - the probability that a photon incident on
	or crossing the PMT face will produce a photoelectron in the PMT

##General info
PEnergy uses a 3-dimensional table of PMT effectiveness as function of photon
wavelength, incidence angle, and polarization at the PMT face.  It is currently
input to the program in the simplest possible form, as a C-style array in the
code file itself.

Generation of the table is a two-step process involving a set of special RAT
simulation runs (one run for each polarization, wavelength, and incidence
angle), followed by execution of a program to tabulate the results and write
the table in the format appropriate for copying it into array "pmtRsp" in the
PEnergy.cc code file.

The file templatePMTEFF.mac is a template used by the batchPMTEFF.pl perl
script to creating RAT mac files for the simulation runs.

The perl script batchPMTEFF.pl generates the RAT mac files and submits 
the simulation runs to a batch queue.

Creation of the table is done with the C++ program, makePMTEffTable.cc.

##Recommended procedure
   - Copy the files in this directory into a working directory
   - Modify batchPMTEFF.pl, as necessary to adapt it to the RAT installation
     and batch queue on the local system
   - Execute batchPMTEff.pl.  Because of the large number of runs (5612), 
     you may want to submit them in smaller batches, which would involve
     modifying and running the batch script a number of times.
   - Move the mac files, the output log files, and the output
     pmtEff...ntuple.root files into a separate directory
   - Compile the program makePMTEffTable with scons (which uses file
     SConstruct)
   - Examine one of the simulation log files to find the number of PMTs that
     were simulated as on-line,  written in the line beginning with
     "GenPMTEff:  Number of tubes on-line = ".
   - Execute makePMTEffTable with the command 
       ``./makePMTEffTable.exe  nOnLine  outputDir  c  > outFile``
     where nOnLine is the number of on-line PMTs and outputDir is the
     directory containing the the ...ntuple.root simulation output files.
   - Replace the pmtRsp table in PEnergy.cc with the contents of outFile.
  
##Additional Info
   The special event generator GenPMTEff is used in the RAT simulation runs to
   generate events initiated with one photon, directed outward, at the face of
   each on-line PMT.  Code has been added to EventBuilderProc to extract and
   save the required information from the event track bank.  This section of
   code is activated by the command line "/rat/procset countpe  1" in the
   template mac file.

   The file NO\_PMT\_VARIATION.ratdb is input to the simulation runs to ensure
   that all the PMTs have the same response.  The file NTUPLE\_custom.ratdb
   defines the output ROOT ntuple from the simulation runs.

   The default number of events in each simulation run is 500 (set in
   templatePTMEFF.mac).  This may be overkill, since the number of actual
   photon detection trials in each event is equal to the number of on-line
   PMTs, resulting in 4,500,000 detection trials in each run if 9000 PMTs are
   on-line.  The maximum PMT effectiveness for the 3-d PMT model as of December
   2014 was about 0.18.  For an effectiveness of say 0.1 with 500 events in a
   simulation run, the statistical uncertainty would be about 0.15%.
   Adjustment for the number of events per run is done automatically in
   makePMTEffTable.

   The makePMTEffTable program has a third command-line argument, in addition
   to the number of PMTs on-line in the RAT simulation runs and the directory
   in which the RAT simulation output files are located.  It is a string that
   specifies what kind(s) of output is desired.  Any combination of the
   following three options is allowed:

      c -- write outputs in form for copying into the RAT PEnergy.cc file

      r -- write outputs at each wavelength/polarization as a function of
           incidence angle, with the values normalized to one at
           perpendicular incidence

      p -- Write results for use as input to a plotting routine:
           for a given polarization and wavelength, pairs of
           incidence angle and probability values; and for a given
           polarization and incidence angle, pairs of wavelength and
           probability values.


