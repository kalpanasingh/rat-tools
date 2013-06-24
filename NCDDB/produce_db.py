#!/usr/bin/env python
#
# produce_db.py
#
# Outputs NCD positions and directions from the csv file in ratdb format.
#
# Author P G Jones - 21/06/2013 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import csv
import numpy
import yaml

ncd_db = {} # Dict for ratdb (yaml) output
ncd_db["x"] = []
ncd_db["y"] = []
ncd_db["z"] = []
ncd_db["u"] = []
ncd_db["v"] = []
ncd_db["w"] = []

ncd_file = csv.reader(open("ncd_positions.csv", "r"))
for ncd in ncd_file:
    ncd_db["x"].append(float(ncd[4]))
    ncd_db["y"].append(float(ncd[5]))
    ncd_db["z"].append(float(ncd[6]))
    pos = numpy.array([float(ncd[4]), float(ncd[5]), float(ncd[6])])
    dir = -pos / numpy.linalg.norm(pos) # Want to point inwards
    ncd_db["u"].append(float("%.2f" % dir[0])) # Dodgy way to ensure 2 decimal places in yaml dump, with knowledge of type
    ncd_db["v"].append(float("%.2f" % dir[1]))
    ncd_db["w"].append(float("%.2f" % dir[2]))

print  yaml.dump(ncd_db).replace("]", "],")
    
