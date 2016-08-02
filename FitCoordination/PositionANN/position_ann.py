'''
position_ann.py: train and test neural networks for the PositionANN method

Requires inputs generated from RAT files using FillTree.cc prior to running.
Also requires the use of ROOT 6, therefore cannot be run within the normal
RAT infrastructure without changes; better to run FillTree within the RAT
environment, then in a clean environment (with access to ROOT-6, rootpy,
numpy, and scikit_learn) run position_ann.
'''
import os

import numpy as np

from ROOT import TFile, TTree
from root_numpy import root2array, rec2array

from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib

import matplotlib.pyplot as plt

_radius_scale = 6000.0 # Can change cuts, always scale by ~AV radius


def load_data(filename, use_mc=False, cut_data=False):
    '''Load ROOT TTrees, return numpy arrays
    '''
    # Get the number of branches (+1 for radius, 2 for each array entry)
    tf = TFile(filename, "read")
    n_branches = len(tf.Get("tree").GetListOfBranches())
    n_inputs = (n_branches - 1) / 2
    # Open the files and transform branches to numpy arrays
    if use_mc is True:
        branches_in = ["hitPatternMC_{0}".format(i) for i in range(n_inputs)]
    else:
        branches_in = ["hitPatternFit_{0}".format(i) for i in range(n_inputs)]
    print "MAX:", max(branches_in), branches_in[-1]
    branches_out = ["radius"]
    # root2array converts ROOT tree entries into numpy array (branches still in lists)
    ann_inputs = root2array(filename, "tree", branches_in)
    ann_output = root2array(filename, "tree", branches_out)
    # rec2array converts the list entries to an array for each record
    data_in = rec2array(ann_inputs)
    data_out = rec2array(ann_output)
    if cut_data is True:
        # Remove samples at z > 7m
        upper_neck = data_out < 7000
        print upper_neck
        data_out = data_out[upper_neck]
        data_in = data_in[upper_neck]
    # Normalise radius (even though this is a regression problem
    # feature scaling still makes a big difference for the ANN)
    data_out = data_out / _radius_scale # On the order of the AV radius
    return data_in, data_out


_training_cut = None
def train_ann(input_data, output_mlp, **kwargs):
    '''Train an ANN with setup according to the kwargs
    '''
    if not os.path.exists(os.path.dirname(output_mlp)):
        os.makedirs(os.path.dirname(output_mlp))
    ann_inputs, ann_output = load_data(input_data, use_mc = True)
    if _training_cut is not None:
        ann_inputs = ann_inputs[_training_cut[0]:_training_cut[1]]
        ann_output = ann_output[_training_cut[0]:_training_cut[1]]
    print "training with", len(ann_inputs), "samples"
    # Create the MLP, train it, then save to the output file
    # In order to read back in and apply to test data
    mlp = MLPRegressor(**kwargs)
    mlp.fit(ann_inputs, ann_output)
    joblib.dump(mlp, output_mlp) # This will create a number of .pkl_xx.npy files


def test_ann(input_data, input_mlp, draw=False, use_mc=True, cut_data=True, plotname="results.pdf"):
    '''Test the ANN on data, return the score (sum((pred - true)^2))
    By default ignore anything above 7 m
    '''
    ann_inputs, ann_output = load_data(input_data, use_mc = use_mc, cut_data = cut_data)
    mlp = joblib.load(input_mlp)

    predictions = mlp.predict(ann_inputs)
    try:
        fig, ax = plt.subplots()
    except:
        print "Note - cannot draw, no X server access"
    else:
        plot = ax.scatter(ann_output*_radius_scale, predictions*_radius_scale)
        ax.set_xlabel("True radius [mm]")
        ax.set_ylabel("Predicted radius [mm]")
        ax.set_xlim(-1000, 9000)
        ax.set_ylim(-1000, 9000)
        ax.grid()
        if draw is True:
            fig.show()
            raw_input("RTN to continue")
        else:
            fig.savefig(plotname, format='pdf')

    return mlp.score(ann_inputs, ann_output) # No weighting applied


def predict_ann(input_data, input_mlp, draw=False, use_mc=True, cut_data=True):
    '''Test the ANN on data, return the score (sum((pred - true)^2))
    By default ignore anything above 7 m
    '''
    ann_inputs, ann_output = load_data(input_data, use_mc = use_mc, cut_data = cut_data)
    mlp = joblib.load(input_mlp)
    predictions = mlp.predict(ann_inputs)
    return (ann_output - predictions)*_radius_scale


def write_line(f, line):
    '''Write to file and to screen, add line endings for the file'''
    f.write('{0}\n'.format(line))


def save_ratdb(input_mlp, output_ratdb, output_index, n_dots, n_times):
    '''Save the ANN parameters to a ratdb format file
    '''
    mlp = joblib.load(input_mlp)
    with open(output_ratdb, 'wb') as f:
        write_line(f, '{')
        write_line(f, '"type": "FIT_POSITION_ANN",')
        write_line(f, '"index": "{0}",'.format(output_index))
        write_line(f, '"version": 1,')
        write_line(f, '"pass": 0,')
        write_line(f, '"comment": "",')
        write_line(f, '"run_range": [0, 0],')
        write_line(f, '"timestamp": "",')
        weight_layers = []
        bias_layers = []
        for weight_layer in mlp.coefs_:
            weight_layers.append([])
            for weight_i in weight_layer:
                weight_layers[-1].append([weight_io for weight_io in weight_i])
        for bias_layer in mlp.intercepts_:
            bias_layers.append([bias for bias in bias_layer])
        write_line(f, '"weights": {0},'.format(str(weight_layers)))
        write_line(f, '"biases": {0},'.format(str(bias_layers)))
        write_line(f, '"nDots": {0},'.format(n_dots))
        write_line(f, '"dotLow": -1.0,')
        write_line(f, '"dotHigh": 1.0,')
        write_line(f, '"nTimes": {0},'.format(n_times))
        write_line(f, '"timeLow": -10.0,')
        write_line(f, '"timeHigh": 90.0,')
        write_line(f, '"radiusScale": {0},'.format(_radius_scale))
        write_line(f, '}')


import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type = int, dest = "times", help = "Timing bins", default = 20)
    parser.add_argument("-a", type = int, dest = "angles", help = "Angular bins", default = 20)
    parser.add_argument("-h1", type = int, dest = "h1", help = "Hidden layer 1 nodes", default = 20)
    parser.add_argument("-h2", type = int, dest = "h2", help = "Hidden layer 2 nodes", default = 5)
    parser.add_argument("-r", type = str, dest = "ratdb", help = "RATDB filename", default = "FIT_POSITION_ANN_COORD.ratdb")
    parser.add_argument("-i", type = str, dest = "index", help = "RATDB index (material)")
    (args) = parser.parse_args()

    mlp_filename = "mlps/mlp_t_{t}_a_{a}_h1_{h1}_h2_{h2}.pkl".format(t = args.times, a = args.angles,
                                                                     h1 = args.h1, h2 = args.h2)
    train_filename = "training_tree_{0}_{1}.root".format(args.times, args.angles)
    betas_filename = "crossval_tree_{0}_{1}.root".format(args.times, args.angles)
    alphas_filename = "alphas_tree_{0}_{1}.root".format(args.times, args.angles)

    train_ann(train_filename, mlp_filename, hidden_layer_sizes = (args.h1, args.h2),
              tol = 1e-30, verbose = True, max_iter = 500)
    # Always print the quality, only test on < 7m and using the estimated direction
    score_betas = test_ann(betas_filename, mlp_filename, use_mc = False, cut_data = True, plotname = 'results_betas.pdf')
    score_alphas = test_ann(alphas_filename, mlp_filename, use_mc = False, cut_data = True, plotname = 'results_alphas.pdf')
    print "ANN score on betas (should be above 0.99):", score_betas
    print "ANN score on alphas (should be above 0.90):", score_alphas
    
    # Print to file
    save_ratdb(mlp_filename, args.ratdb, args.index, args.angles, args.times)
    print "RATDB saved in", args.ratdb
