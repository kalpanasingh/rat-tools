# PositionANN Coordinator
This folder contains the files needed to coordinate the NearAV (Angular Positions Method) fitter.
Due to a requirement on ROOT-6 for part of the analysis, the coordinator must be run in two stages.

## Stage 1

Using the appropriate RAT environment:

* ./fitcoordinate [options] PositionANN (best to run on batch, via -b option, and run in a directory with enough space via -d option).
* In the appropriate PositionANN folder, run ``python AnalyseData.py [options]''

## Stage 2

Source a ROOT6 environment, ensure all required python packages are installed (see below).

* python position_ann.py [options]

This will generate RATDB tables (printed to screen and saved in a file).  Please check the score for both test betas and
alphas (printed to screen).  If these scores are not satisfactory then double check the plots generated (results_betas.pdf
and results_alphas.pdf); it may be necessary to train multiple networks with different configurations and compare results.


## Required libraries:

The following are required and can be installed via ``pip install -r requirements.txt''; use the ``--user'' flag if you do not
have root access.

* numpy
* scipy
* root_numpy
* matplotlib

Additionally scikit-learn is required, but the version installed by ``pip'' is old; instead do:

``git clone git://github.com/scikit-learn/scikit-learn.git
cd scikit-learn
python setup.py install
''

if you do not have root access then run the last command with the ``--user'' flag.