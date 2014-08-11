#!/usr/bin/env python
import os, sys, string, ROOT, rat

def AnalyseFiles(options):
    if options.scintMaterial=="lightwater_sno":
        os.system("root 'water_command.cpp(\"%s\",%d)'" % (options.scintMaterial, options.runs))
    else:
        os.system("root 'root_command.cpp(\"%s\",%d,%.2f)'" % (options.scintMaterial, options.runs, options.velocity))


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-r", type="int", dest="runs", help="Total number of runs", default=1)
    parser.add_option("-v", type="float", dest="velocity", help="Use an updated group velocity", default=-999)
    (options, args) = parser.parse_args()
    AnalyseFiles(options)
