#!usr/bin/env python
import string, os
# Author K Majumdar - 05/09/2014 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):

    # Load any parameters for running the macros on a Batch system
    batch_params = None
    if options.batch:
        batch_params = {}
    execfile(options.batch, {}, batch_params)
	
    # Load the batch submission script template
    inFile = open("Template_Submit.sh", "r")
    rawText = string.Template(inFile.read())
    inFile.close()

    outText = rawText.substitute(Preamble = "\n".join(s for s in batch_params['preamble']),
                                 Ratenv = batch_params['ratenv'],
                                 Cwd = os.environ['PWD'].replace("/.", "/"),
                                 RunCommand = "python AnalyseData.py -i " + options.index)
    outFile = open("AnalyseData_Batch_SubmitScript.sh", "w")
    outFile.write(outText)
    outFile.close()

    os.system(batch_params["submit"] + " AnalyseData_Batch_SubmitScript.sh")


import optparse
if __name__ == '__main__':
    parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
    parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
    parser.add_option("-b", type = "string", dest = "batch", help = "Run the macros in Batch mode")
    (options, args) = parser.parse_args()
    AnalyseRootFiles(options)

