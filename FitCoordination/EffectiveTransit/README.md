# EffectiveTransit Coordinator
To run use the fitcoordinate script one directory up from this. Then do:

    python fitcoordinate EffectiveTransit

Normal fit coordination options apply.

## Diagnostic scripts
This folder contains a diagnostic plotting script, to plot the EffectiveTransit fitcoordinator performance. To run, first coordinate then for the Distance v Timing plot:

    python DiagnosticPlotFiles.py

This method find the effective speed in the scintillator by taking measurements at several positions along a line, finding the difference in time between early hits on this axis and using this to calculate the speed.

This is in comparison to the ScintEffectiveSpeed co-ordinator which takes a more pragmatic approach and finds the effective speed as that which gives the best results, determined by the speed which minimises the radial bias of 3 MeV electron events spread through the detector.
