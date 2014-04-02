#!/usr/bin/env python
#
# belly_ropes_db.py
#
# Outputs Belly plate positions and rool from the approximate positions in 17-702-F-6499-02_Rev_01.
# Output is in ratdb format.
# Remember the PSUP North is the y-axis and there is a plate on the x axis
#
# Author P G Jones - 21/06/2013 <p.g.jones@qmul.ac.uk> : First revision
# Author P G Jones - 2014-03-31 <p.g.jones@qmul.ac.uk> : Correct axis understanding.
####################################################################################################
import math
import yaml

initial_offset_to_x = 0.0#1.55
separation = 36
rotational_positions = [initial_offset_to_x + angle for angle in range(0, 360, separation)] 
print rotational_positions
rope_radial_pos = 6030.0

db = { "x" : [], "y" : [], "z" : [], "roll" : [] }

for rotation in rotational_positions:
    z = 0.0 # Centre is that of the torus bit, which is at z=0
    x = math.cos(math.radians(rotation)) * rope_radial_pos
    y = math.sin(math.radians(rotation)) * rope_radial_pos
    roll = rotation
    db["x"].append(float("%.2f" % x))
    db["y"].append(float("%.2f" % y))
    db["z"].append(float("%.2f" % z))
    db["roll"].append(float("%.2f" % (roll)))

print "Ropes:"
print  yaml.dump(db).replace("]", "],")

db = {}
plate_radial_pos = 6032.5
db = { "x" : [], "y" : [], "z" : [], "roll" : [] }
for rotation in rotational_positions:
    z = 0.0 
    x = math.cos(math.radians(rotation)) * plate_radial_pos
    y = math.sin(math.radians(rotation)) * plate_radial_pos
    roll = rotation
    db["x"].append(float("%.2f" % x))
    db["y"].append(float("%.2f" % y))
    db["z"].append(float("%.2f" % z))
    db["roll"].append(float("%.2f" % ((roll))))

print "Plates:"
print  yaml.dump(db).replace("]", "],")
