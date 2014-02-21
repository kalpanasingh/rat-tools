#!/usr/bin/env python
#
# hold_down_ropes_db.py
#
# Outputs hold down rope positions in ratdb format
# Output is in ratdb format.
#
# Author P G Jones - 2014-02-21 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import math
import yaml
import numpy

db = {"rope_x" : [], "rope_y" : [], "rope_z" : [], "sling_position" : []}

# Positions as documented
rope_x = [6077.5, 4546.1, -4323.6, -5780.0]
rope_y = [0.0, 0.0, 1404.8, 1878.0]
rope_z = [0.0, 4033.4, 4033.4, 0.0]

sling_pos = [4323.6, -1404.8, 4033.4]

av_radius = 6060.4
rope_radius = 19.812

for x, y, z in zip(rope_x, rope_y, rope_z):
    pos = numpy.array( [x, y, z] )
    pos *= (av_radius + rope_radius) / numpy.linalg.norm(pos)
    db["rope_x"].append(float("%.2f" % pos[0]))
    db["rope_y"].append(float("%.2f" % pos[1]))
    db["rope_z"].append(float("%.2f" % pos[2]))

# Add Start anchor, FIXED Z
db["rope_x"] = [db["rope_x"][0]] + db["rope_x"]
db["rope_y"] = [db["rope_y"][0]] + db["rope_y"]
db["rope_z"] = [-12000.0] + db["rope_z"]
# Add end anchor, FIXED Z
db["rope_x"].append(db["rope_x"][-1])
db["rope_y"].append(db["rope_y"][-1])
db["rope_z"].append(-12000.0)

pos = numpy.array(sling_pos)
pos = pos * (av_radius + rope_radius) / numpy.linalg.norm(pos)
db["sling_position"].append(float("%.2f" % pos[0]))
db["sling_position"].append(float("%.2f" % pos[1]))
db["sling_position"].append(float("%.2f" % pos[2]))

print "Ropes:"
print  yaml.dump(db).replace("]", "],")
