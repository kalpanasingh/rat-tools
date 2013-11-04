# EnergyLookup Coordinator
To run use the fitcoordinate script one directory up from this. Then do:

    python fitcoordinate EnergyLookup

Normal fit coordination options apply.

Alternatively, to run the coordinator on a batch system using many jobs, run:

    ./ProduceData.py -s <scintMaterial> -e <energies> -x <positions>

Where energies and positions may be single or many arguments, e.g.

    ./ProduceData.py -s labppo_scintillator -e 1.0 2.0 3.0 -x 0.0 2000.0

To then produce the RATDB tables once all jobs have completed, run:

    ./AnalyseFiles.py -s <scintMaterial> -e <full list of energies> -x <full list of positions>

## Diagnostic scripts
This folder contains a diagnostic plotting script, to plot the EnergyLookup fitcoordinator performance. To run, first coordinate then for the Nhit v pos graph:

    python DiagnosticPlotFiles.py

For Nhit v energy graph

    python DiagnosticPlotFiles.py -e