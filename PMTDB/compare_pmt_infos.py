#!/usr/bin/env python
import yaml # Needs installing
import sys
import numpy
from minify_json import json_minify # In this directory


with open("data/PMTINFO_rat3.ratdb", "r") as original_file:
    rat_original = yaml.load(json_minify(original_file.read(), False))

with open("data/snoman_phil.ratdb", "r") as snoman_file:
    snoman = yaml.load(json_minify(snoman_file.read(), False))

with open("data/snoman.ratdb", "r") as snoman_file:
    rat_snoman = yaml.load(json_minify(snoman_file.read(), False))

with open("data/airfill2.ratdb", "r") as airfill2_file:
    airfill2 = yaml.load(json_minify(airfill2_file.read(), False))

with open("data/airfill3.ratdb", "r") as airfill3_file:
    airfill3 = yaml.load(json_minify(airfill3_file.read(), False))

# Correct snoman cm to mm
for lcn in range(0, len(snoman["pmt_type"])):
    snoman["x"][lcn] = snoman["x"][lcn] * 10.0
    snoman["y"][lcn] = snoman["y"][lcn] * 10.0
    snoman["z"][lcn] = snoman["z"][lcn] * 10.0


def compare(info1, info2):
    
    for lcn in range(0, len(info1["pmt_type"])):
        differs = False
        if info2["type"][lcn] != info1["type"][lcn]:
            differs = True
        if info2["panelnumber"][lcn] != info1["panelnumber"][lcn]:
            differs = True
        position1 = numpy.array([info1["x"][lcn], info1["y"][lcn], info1["z"][lcn]])
        position2 = numpy.array([info2["x"][lcn], info2["y"][lcn], info2["z"][lcn]])
        max_offset = 1.0
        if numpy.linalg.norm(position1 - position2) > max_offset:
            differs = True
        if differs:
            print lcn, "&", info1["type"][lcn], "&", info2["type"][lcn], "&", info1["panelnumber"][lcn], "&", info2["panelnumber"][lcn], "&",
            print position1, "&", position2


#compare(snoman, rat_original)
#compare(rat_original, rat_snoman)
print "Comparison between rat_snoman and airfill2"
compare(rat_snoman, airfill2)
print "Comparison between airfill2 and airfill3"
compare(airfill2, airfill3)
