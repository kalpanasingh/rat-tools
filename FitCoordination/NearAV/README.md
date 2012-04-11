# NearAV Coordinator
To run use the fitcoordinate script one directory up from this. Then do:

    python fitcoordinate NearAV

Normal fit coordination options apply.

## Diagnostic scripts
This folder contains a diagnostic plotting script, to plot the NearAV fitcoordinator performance. To run, first coordinate then for pure timing (see the TIR gap)

    python DiagnosticPlotFiles.py

For the averaged ratio for a certain window choice (220, 250):

    python DiagnosticPlotFiles.py -a 220.0 250.0

For all the ratios (not averaged) then:

    python DiagnosticPlotFiles.py 220.0 250.0