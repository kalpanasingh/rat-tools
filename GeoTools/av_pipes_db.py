#!/usr/bin/env python
#
# produce_db.py
#
# Outputs each acrylic pipe in ratdb format.
#
# Author P G Jones - 2013-11-27 <p.g.jones@qmul.ac.uk> : First revision
#        N Barros  - 2015-06-24 <nfbarros@hep.upenn.edu> : Added new DB fields
#                                                          Generate tables with line breaks
####################################################################################################
import math
import yaml
from collections import OrderedDict

start_z = 12705.00
neck_r = 25.5 * 25.4 # Inches to mm
av_r = 6005.0
boss_z = 5700.0
gap = 5.0 # Safety margin

pipe1 = {"name" : "1",
         "theta" : -29.5,
         "od" : 1.875,
         "id" : 1.375,
         "z" : 9800.0}
pipe2 = {"name" : "2",
         "theta" : -22.0,
         "od" : 1.875,
         "id" : 1.375,
         "z" : 5600.0}
pipe3 =  {"name" : "3",
          "theta" : -14.5,
          "od" : 1.875,
          "id" : 1.375,
          "phi" : [13.0, 20.0, 37.5, 53.0]}
pipe4 =  {"name" : "4",
          "theta" : -7.0,
          "od" : 1.875,
          "id" : 1.375,
          "phi" : [15.0, 22.0, 39.5, 55.0, 72.5, 90.0, 107.5]}
pipe5 =  {"name" : "labs",
          "theta" : 2.5,
          "od" : 3.5,
          "id" : 2.75,
          "phi" : [15.0, 22.0, 39.5, 55.0, 72.5, 90.0, 107.5, 125.0, 142.5, 160.0, 177.5, 180.0]}
pipe6 =  {"name" : "6",
          "theta" : 12.0,
          "od" : 1.875,
          "id" : 1.375,
          "phi" : [13.0, 20.0, 37.5, 53.0, 70.5, 86.0, 105.5, 123.0, 140.5, 158.0]}
pipe7 =  {"name" : "labr",
          "theta" : 21.5,
          "od" : 3.5,
          "id" : 2.75,
          "z" : 6100.0}

def output_pipe(pipe):
    global start_z, neck_r, av_r, boss_z, gap
    db = OrderedDict([("type" , '"SOLID"'),
                      ("index" , '"av_pipe-%s"' % pipe["name"]),
                      ("version", 1),
                      ("solid" , '"avPipe"'),
                      ("run_range" , "[0, 0]"),
                      ("pass" , 0),
                      ("production" , "false"),
                      ("timestamp",'""'),
                      ("comment" , '""'),
                      ("r_min" , pipe["id"] * 25.4 / 2.0),
                      ("r_max" , pipe["od"] * 25.4 / 2.0)])
    if "z" in pipe:
        x = [math.sin(math.radians(pipe["theta"])) * neck_r] * 2
        y = [math.cos(math.radians(pipe["theta"])) * neck_r] * 2
        z = [start_z, pipe["z"]]
    else:
        x = [math.sin(math.radians(pipe["theta"])) * neck_r] * 2
        y = [math.cos(math.radians(pipe["theta"])) * neck_r] * 2
        z = [start_z, boss_z, boss_z]
        x.append(math.sin(math.radians(pipe["theta"])) * math.sin(math.radians(8.0)) * (av_r - pipe["od"] * 25.4 - gap))
        y.append(math.cos(math.radians(pipe["theta"])) * math.sin(math.radians(8.0)) * (av_r - pipe["od"] * 25.4 - gap))
        for phi in pipe["phi"]:
            x.append(math.sin(math.radians(pipe["theta"])) * math.sin(math.radians(phi)) * (av_r - pipe["od"] * 25.4 - gap))
            y.append(math.cos(math.radians(pipe["theta"])) * math.sin(math.radians(phi)) * (av_r - pipe["od"] * 25.4 - gap))
            z.append(math.cos(math.radians(phi)) * (av_r - pipe["od"] * 25.4 - gap))
            db["x"] = x
            db["y"] = y
            db["z"] = z
            # Manual print
            print "{"
            for key,value in db.iteritems():
                print key+": "+str(value)+","
            print "}"

output_pipe(pipe1)
output_pipe(pipe2)
output_pipe(pipe3)
output_pipe(pipe4)
output_pipe(pipe5)
output_pipe(pipe6)
output_pipe(pipe7)
