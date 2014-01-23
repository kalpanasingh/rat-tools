#!/usr/bin/env python
#
# internal_db.py
#
# Outputs the internal rope block passing/end points
#
# Author P G Jones - 2013-11-25 <p.g.jones@qmul.ac.uk> : First revision
####################################################################################################
import math

neck_radial_pos = 27.5 * 25.4 # 27.5" to mm
av_radius = 6005.0
top_z = av_radius + 6700.0 # Approx ~
boss_z = 5500.0 # Also approx
rope_radius = 0.1 * 25.4 / 2.0
gap = 0.1

x_pos = [0] * 6
y_pos = [neck_radial_pos, neck_radial_pos]
z_pos = [top_z, boss_z]

y_pos.append(math.sin(math.radians(45.0)) * (av_radius - rope_radius - gap))
z_pos.append(math.cos(math.radians(45.0)) * (av_radius - rope_radius - gap))

y_pos.append(math.sin(math.radians(80.0)) * (av_radius - rope_radius - gap))
z_pos.append(math.cos(math.radians(80.0)) * (av_radius - rope_radius - gap))

y_pos.extend([neck_radial_pos - rope_radius - gap, neck_radial_pos - rope_radius - gap])
z_pos.extend([boss_z, top_z])

print "[",
for x in x_pos:
    print "%4.2f," % float(x),
print "],\n[",
for y in y_pos:
    print "%4.2f," % float(y),
print "],\n[",
for z in z_pos:
    print "%4.2f," % float(z),
print "],"
