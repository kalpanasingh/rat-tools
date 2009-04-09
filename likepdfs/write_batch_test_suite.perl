#! /usr/bin/perl -w

# This perl script generates macro and submission scripts for running RAT simulations on the Oxford CPU cluster.
# Adapt to a different site by changing the directory settings at the top.
# The jobs are designed to test the FitLike processors. 
# Generate sets of electron events at different energies, both isotropically and at
# fixed radial positions. 

# choose statistics for each job
$stats = 500;

# These are environment variables for your system
$env_file = ".snoplusenv";
$env_dir = "/home/wilson/";
# inputs (this script writes the mac and scr files which go in these directories
$mac_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/TestSuite/macs/";
$scr_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/TestSuite/scripts/";
# where is the PDF rootfile?
$pdf_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/ratdb/";
$pdf_file = "FitLikePDFNtuple.root";
# fitlike db file
$db_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/ratdb/";
$db_file = "FIT_LIKE.ratdb";
# optics db file
$op_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/ratdb/";
$op_file = "labppo_OPTICS.ratdb";
# output directories
$root_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/TestSuite/rootfiles/";
$out_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/TestSuite/outfiles/";
$log_dir = "/data/dblchooz/wilson/RAT/fitter_PDFs/TestSuite/logfiles/";

# one file to submit all the jobs (edit commands depending on queue system)
open(SUBFILE,">submit_TS.scr\n");

# firstly set of isotropic e- events at 5 different kinetic energies 
	@energy = (1.0, 2.0, 3.0, 4.0, 5.0, 1.3, 2.4, 3.6, 4.7);
	foreach $E (@energy){                
		$name = "TS_tidy_labppo_$E"."MeV_iso_$stats";
    	$mac_file = "$name".".mac";
    	$root_file = "$name".".root";
    	$out_file = "$name".".out";
    	$log_file = "$name".".log";
    	$scr_file = "$name"."_batch.scr";
    	print "$name - $stats isotropic events with kinetic energy $E MeV\n";
    	open(MACFILE,">$mac_dir$mac_file\n");                          
			print MACFILE "/glg4debug/glg4param omit_muon_processes  1.0\n";
        	print MACFILE "/glg4debug/glg4param omit_hadronic_processes  1.0\n";
        	print MACFILE "/rat/db/set DETECTOR geo_file \"geo/snoplus.geo\"\n";
			print MACFILE "/rat/db/load $db_file\n";
			print MACFILE "/rat/db/load $op_file\n";
        	print MACFILE "/rat/db/set GEO[scint] material \"labppo_scintillator\"\n";
        	print MACFILE "/rat/db/set DAQ nhit_thresh 15.0\n";
			print MACFILE "/rat/db/set FIT_LIKE histogram_filename \"$pdf_file\"\n"; 
        	print MACFILE "/run/initialize\n";
        	print MACFILE "/rat/proc frontend\n";
        	print MACFILE "/rat/proc trigger\n";
        	print MACFILE "/rat/proc eventbuilder\n";
        	print MACFILE "/rat/proc count\n";
        	$nup = $stats/20;
        	print MACFILE "/rat/procset update $nup\n";
        	print MACFILE "/rat/proc fitcentroid\n";
        	print MACFILE "/rat/proc fitlikepos\n";
        	print MACFILE "/rat/proc fitlikeenergy\n";
        	print MACFILE "/rat/proc QPDFitter\n";
        	print MACFILE "/rat/proc outroot\n";
        	print MACFILE "/rat/procset file \"$root_file\"\n";
        	print MACFILE "/generator/add combo gun:fill\n";
        	print MACFILE "/generator/vtx/set e- 0 0 0 $E\n";
        	print MACFILE "/generator/pos/set 0 0 0 \n";
        	print MACFILE "/generator/rate/set 1\n";
        	print MACFILE "/run/beamOn $stats\n";
        	print MACFILE "exit\n";                
		close(MACFILE);    	
		open(SCRFILE,">$scr_dir$scr_file\n");
        	print SCRFILE "#!/bin/csh \ncd \$TMPDIR\n";
        	print SCRFILE "cp $pdf_dir$pdf_file .\n";
        	print SCRFILE "cp $db_dir$db_file .\n";
        	print SCRFILE "cp $op_dir$op_file .\n";
        	print SCRFILE "cp $env_dir$env_file .\n";
        	print SCRFILE "source $env_file\n";
        	print SCRFILE "cp $mac_dir$mac_file .\n";
        	print SCRFILE "rat < $mac_file > $out_file\n";
        	print SCRFILE "cp $out_file $out_dir\n";
        	print SCRFILE "cp rat.log $log_dir$log_file\n";
        	print SCRFILE "cp $root_file $root_dir\n";
        	print SCRFILE "echo  Job $name Done\n";
		close(SCRFILE);
		print SUBFILE "qsub $scr_dir$scr_file\n";
	}	
# Now do 2MeV events at different fixed radii (on X axis)
	@XPos = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 0.25, 1.25, 2.25, 3.25, 4.25, 5.25);	
	foreach $x (@XPos){ 
        $name = "TS_sep_labppo_2MeV_X$x"."m_$stats";
        $mac_file = "$name".".mac";
        $root_file = "$name".".root";
        $out_file = "$name".".out";
        $log_file = "$name".".log";
        $scr_file = "$name"."_batch.scr";
        $mypos = $x*1000.;
        print "$name - $stats 2MeV events at X = $mypos mm\n";	
    	open(MACFILE,">$mac_dir$mac_file\n");                          
			print MACFILE "/glg4debug/glg4param omit_muon_processes  1.0\n";
        	print MACFILE "/glg4debug/glg4param omit_hadronic_processes  1.0\n";
        	print MACFILE "/rat/db/set DETECTOR geo_file \"geo/snoplus.geo\"\n";
			print MACFILE "/rat/db/load $db_file\n";
			print MACFILE "/rat/db/load $op_file\n";
        	print MACFILE "/rat/db/set GEO[scint] material \"labppo_scintillator\"\n";
			print MACFILE "/rat/db/set DAQ nhit_thresh 15.0\n";
			print MACFILE "/rat/db/set FIT_LIKE histogram_filename \"$pdf_file\"\n"; 
        	print MACFILE "/run/initialize\n";
        	print MACFILE "/rat/proc frontend\n";
        	print MACFILE "/rat/proc trigger\n";
        	print MACFILE "/rat/proc eventbuilder\n";
        	print MACFILE "/rat/proc count\n";
        	$nup = $stats/20;
        	print MACFILE "/rat/procset update $nup\n";
        	print MACFILE "/rat/proc fitcentroid\n";
        	print MACFILE "/rat/proc QPDFitter\n";
        	print MACFILE "/rat/proc fitchitime\n";
        	print MACFILE "/rat/proc fitlikepos\n";
        	print MACFILE "/rat/proc fitlikeenergy\n";
        	print MACFILE "/rat/proc outroot\n";
        	print MACFILE "/rat/procset file \"$root_file\"\n";
        	print MACFILE "/generator/add combo gun:point\n";
        	print MACFILE "/generator/vtx/set e- 0 0 0 2.0\n";
        	print MACFILE "/generator/pos/set $x 0 0 \n";
        	print MACFILE "/generator/rate/set 1\n";
        	print MACFILE "/run/beamOn $stats\n";
        	print MACFILE "exit\n";                
		close(MACFILE);    	
		open(SCRFILE,">$scr_dir$scr_file\n");
        	print SCRFILE "#!/bin/csh \ncd \$TMPDIR\n";
        	print SCRFILE "cp $pdf_dir$pdf_file .\n";
        	print SCRFILE "cp $db_dir$db_file .\n";
        	print SCRFILE "cp $op_dir$op_file .\n";
        	print SCRFILE "cp $env_dir$env_file .\n";
        	print SCRFILE "source $env_file\n";
        	print SCRFILE "cp $mac_dir$mac_file .\n";
        	print SCRFILE "rat < $mac_file > $out_file\n";
        	print SCRFILE "cp $out_file $out_dir\n";
        	print SCRFILE "cp rat.log $log_dir$log_file\n";
        	print SCRFILE "cp $root_file $root_dir\n";
        	print SCRFILE "echo  Job $name Done\n";
		close(SCRFILE);
		print SUBFILE "qsub $scr_dir$scr_file\n";		
	}               	
	
close(SUBFILE);  
$command = "chmod u+x submit_TS.scr\n";   
system($command);
