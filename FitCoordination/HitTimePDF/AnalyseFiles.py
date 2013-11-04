#!/usr/bin/env python
import os, sys, string, ROOT, rat

def AnalyseFiles(options):
    if options.scintMaterial=="lightwater_sno":
        os.system("root 'water_command.cpp(\"%s\",%d)'" % (options.scintMaterial, options.runs))
    else:
        os.system("root 'root_command.cpp(\"%s\",%d)'" % (options.scintMaterial, options.runs))


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version="%prog 1.0")
    parser.add_option("-s", type="string", dest="scintMaterial", help="Scintillator material.", default="labppo_scintillator")
    parser.add_option("-r", type="int", dest="runs", help="Total number of runs", default=1)
    (options, args) = parser.parse_args()
    AnalyseFiles(options)
