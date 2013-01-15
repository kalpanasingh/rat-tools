# Effective Speed Coordinator
To run use the fitcoordinate script one directory up from this. Then do:

    python fitcoordinate ScintEffectiveSpeed

Normal fit coordination options apply.

## Diagnostic scripts
This folder contains a diagnostic plotting script, to plot the EffectiveSpeed against RadialBias. To run, first coordinate then for the EffectiveSpeed v RadialBias plot:

    python DiagnosticPlotFiles.py

This method takes a pragmatic approach and finds the effective speed as that which gives the best results, determined by the speed which minimises the radial bias of 3 MeV electron events spread through the detector.

This is in comparison to the EffectiveTransit co-ordinator which finds the effective speed in the scintillator by taking measurements at several positions along a line, finding the difference in time between early hits on this axis and using this to calculate the speed.