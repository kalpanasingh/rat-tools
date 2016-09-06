# PositionANN Coordinator

This folder contains the files needed to coordinate the NearAV (Angular Positions Method) fitter.

## Required libraries

There are extra requirements for this coordinator; if running for the first time then install these first.

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

## Stage 1 - produce data

Using the appropriate RAT environment:

``./fitcoordinate [options] PositionANN''

It's best to run on batch, via -b option, and run in a directory with enough space via -d option).

## Stage 2 - analyse data

In the appropriate PositionANN folder, run:

``python AnalyseData.py [options]''

This will generate RATDB tables (printed to screen and saved in a file).  Please check the score for both test betas and
alphas (printed to screen).  If these scores are not satisfactory then double check the plots generated (results_betas.pdf
and results_alphas.pdf); it may be necessary to train multiple networks with different configurations and compare results.

Options for different configurations include (require full AnalyseData.py script):

* -t [times]: number of time bins to use (default 20)
* -a [angles]: number of angle bins to use (default 20); i.e. overall 20x20 = 400 inputs

Additionally, you may rerun the neural network training with different hidden layer options:

``python position_ann.py [options]''

Where options are:

* -x [layer1]: number of nodes in hidden layer 1
* -y [layer2]: number of nodes in hidden layer 2
