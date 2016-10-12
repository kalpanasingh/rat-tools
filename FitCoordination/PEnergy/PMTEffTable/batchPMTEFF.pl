#!/usr/bin/perl

$pol = "s";     # Desired photon polarization, s or p
for ($ipol=1; $ipol<=2; $ipol+=1) {
  if($ipol==2) { $pol = "p"; }

  for ($lambda = 200; $lambda<=800; $lambda+=10) {

     for ($angle = 0; $angle<=90; $angle+=2) {
        $filename = "pmtEff$lambda\_$angle\_$pol";
        # Write mac file:
        $command = "sed -e /FFFFFF/s/FFFFFF/$filename/ -e /WLWLWL/s/WLWLWL/$lambda/  -e /IAIAIA/s/IAIAIA/$angle/  -e /PPPPPP/s/PPPPPP/$pol/  templatePMTEff.mac > $filename.mac";
        system("$command");
        # Submit batch job:
        $command = "q ~/rat/bin/rat -l $filename.log $filename.mac";
        print "$command \n";
#        system("$command");

    }
  }
}
