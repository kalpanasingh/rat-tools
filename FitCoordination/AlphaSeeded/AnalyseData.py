#!usr/bin/env python
import string, SeededUtilities
# Author K Majumdar - 14/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):
	# returns the lower (t1) and upper (t2) limits of the prompt time residuals range, optimised for minimum overlap between alpha and electron prompt/total PMTs ratio distributions
	minlap = 10**9
	mint1 = 500.0
	mint2 = 500.0

	for t1 in range(-10, 10, 2):
		for t2 in range(20, 200, 2):
			Histogram1 = SeededUtilities.ProduceRatioHistogram(SeededUtilities.Particles[0] + ".root", t1, t2)
			Histogram2 = SeededUtilities.ProduceRatioHistogram(SeededUtilities.Particles[1] + ".root", t1, t2)
			overlap = SeededUtilities.BhattacharyaCoeff(Histogram1, Histogram2)

			del Histogram1
			del Histogram2

			if overlap < minlap:
				minlap = overlap
				mint1 = t1
				mint2 = t2

	print "\n"
	print "Please place the text below into the database file: CLASSIFIER_ALPHA_SEEDED.ratdb located in rat/data, replacing the existing corresponding text."
	print "t1: %.2fd," % mint1
	print "t2: %.2fd," % mint2
	print "\n"


import optparse
if __name__ == '__main__':
	parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
	parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
	(options, args) = parser.parse_args()
	AnalyseRootFiles(options)
