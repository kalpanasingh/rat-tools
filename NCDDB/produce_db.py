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
from math import fabs
    
x_old = [ 5438.8,  505.4, -494.1, -5434.0, -5439.5, -493.0, 492.4, 5438.2, 4490.1, 2502.6, -2488.8, -4491.2, -4500.3, -2498.0, 2508.4, 4495.4, 3500.0, -3495.4, -3503.5, 3500.4, 4500.6, 1507.1, -1491.6, -4498.6, -4499.6, -1515.7, 1495.1, 4497.7, 4496.1, 460.7, -496.6, -4492.4, -4493.8, -509.1, 499.9, 4494.6, 3488.4, 2504.9, -2494.9, -3489.1, -3501.3, -2498.4, 2497.3, 3490.6, 3495.8, 1506.1, -1492.0, -3492.9, -3496.5, -1422.9, 1501.1, 3495.5, 2436.7, -2430.7, -2464.7, 2421.8, 3414.8, 499.8, -491.6, -3408.2, -3414.6, -524.9, 448.4, 3411.0, 2502.3, 1517.7, -1485.9, -2490.5, -2516.5, -1523.7, 1485.9, 2499.3, 2502.7, 520.1, -488.5, -2503.1, -2507.1, -517.7, 488.5, 2504.6, 1489.1, -1497.2, -1515.0, 1495.8, 1504.3, 482.1, -494.6, -1506.2, -1507.9, -489.8, 476.4, 1504.1, 500.0, -500.0, -500.0, 500.0 ]

y_old = [ 486.1, 5446.6, 5445.8, 502.1, -495.2, -5408.4, -5443.7, -495.8, 2492.6, 4498.5, 4505.9, 2499.8, -2491.6, -4497.9, -4489.1, -2501.6, 3500.0, 3504.2, -3496.1, -3507.7, 1496.7, 4502.7, 4500.0, 1503.1, -1490.4, -4495.4, -4505.5, -1504.6, 495.4, 4507.1, 4507.1, 502.1, -492.3, -4498.5, -4503.0, -504.2, 2502.1, 3500.9, 3500.2, 2505.1, -2497.1, -3496.1, -3503.8, -2508.3, 1497.7, 3500.4, 3504.0, 1501.8, -1494.4, -3533.2, -3499.3, -1502.6, 2446.1, 2449.4, -2418.6, -2454.8, 486.4, 3414.2, 3413.8, 519.7, -473.0, -3410.2, -3425.8, -509.4, 1517.1, 2502.1, 2517.7, 1535.6, -1484.9, -2496.5, -2525.2, -1525.2, 501.1, 2511.6, 2514.8, 517.2, -481.9, -2504.6, -2515.0, -509.9, 1499.3, 1516.1, -1494.2, -1521.9, 507.0, 1517.5, 1509.2, 503.7, -489.7, -1513.4, -1516.9, -511.9, 500.0, 500.0, -500.0, -500.0 ]

z_old = [ -2479.9, -2476.1, -2477.5, -2481.6, -2480.1, -2547.2, -2477.3, -2482.3, -3098.7, -3094.1, -3098.3, -3102.8, -3100.2, -3099.8, -3095.1, -3096.5, -3396.2, -3398.1, -3397.1, -3397.9, -3678.4, -3679.7, -3683.2, -3682.2, -3686.7, -3682.8, -3683.4, -3682.9, -3944.8, -3942.7, -3943.9, -3949.0, -3947.6, -3942.8, -3939.4, -3945.9, -4189.2, -4185.8, -4191.2, -4195.8, -4191.7, -4188.4, -4191.5, -4192.6, -4642.0, -4641.0, -4646.7, -4645.2, -4644.2, -4642.0, -4645.9, -4645.0, -4913.5, -4914.8, -4913.2, -4916.5, -4915.9, -4915.0, -4916.1, -4917.1, -4917.4, -4915.2, -4911.9, -4916.2, -5244.1, -5244.0, -5245.6, -5244.4, -5246.5, -5245.0, -5242.1, -5243.2, -5435.9, -5430.0, -5431.5, -5434.2, -5435.6, -5433.5, -5431.4, -5434.2, -5621.3, -5614.6, -5615.7, -5613.4, -5791.7, -5790.4, -5791.5, -5791.5, -5792.3, -5790.8, -5791.0, -5791.3, -5960.0, -5960.0, -5960.0, -5960.0 ]

ncd_db = {} # Dict for ratdb (yaml) output
ncd_db["x"] = []
ncd_db["y"] = []
ncd_db["z"] = []
ncd_db["u"] = []
ncd_db["v"] = []
ncd_db["w"] = []

ncd_file = csv.reader(open("ncd_positions.csv", "r"))
index = 0
for ncd in ncd_file:
    x = float(ncd[4]) * 10.0 # cm to mm
    y = float(ncd[5]) * 10.0
    z = float(ncd[6]) * 10.0
    if ncd[0] == "D3":
        y = 4500.0
    elif ncd[0] == "N1" or ncd[0] == "N2" or ncd[0] =="N3" or ncd[0] =="N4":
        x, y, z = x * 100.0, y * 100.0, z * 100.0

    if fabs(x - x_old[index]) > 0.1:
        print "x differs", ncd[0], x, x_old[index]
    if fabs(y - y_old[index]) > 0.1:
        print "y differs", ncd[0], y, y_old[index]
    if fabs(z - z_old[index]) > 0.1:
        print "z differs", ncd[0], z, z_old[index]
    index += 1
    pos = numpy.array([x, y, z])
    pos = 6005.3 * pos / numpy.linalg.norm(pos)
    print numpy.linalg.norm(pos)
    dir = -pos / numpy.linalg.norm(pos) # Want to point inwards
    pos += 28.6 * dir # Measured position is the centre of the top face, rat uses centre of the object
    ncd_db["x"].append(float("%.2f" % pos[0])) # Dodgy way to ensure 2 decimal places in yaml dump, with knowledge of type
    ncd_db["y"].append(float("%.2f" % pos[1]))
    ncd_db["z"].append(float("%.2f" % pos[2]))
    ncd_db["u"].append(float("%.2f" % dir[0])) 
    ncd_db["v"].append(float("%.2f" % dir[1]))
    ncd_db["w"].append(float("%.2f" % dir[2]))

print  yaml.dump(ncd_db).replace("]", "],")
