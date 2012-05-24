#!usr/bin/env python
import string, UnseededUtilities
# Author K Majumdar - 11/05/2012 <Krishanu.Majumdar@physics.ox.ac.uk>


def AnalyseRootFiles(options):
	# returns the tail fraction value optimised for minimum overlap between alpha and electron tail/total PMTs ratio distributions
	minlap = 10**9
	minfrac = 1000.0

	for tailfrac in UnseededUtilities.TailFracs:
		Histogram1 = UnseededUtilities.ProduceRatioHistogram(UnseededUtilities.Particles[0] + ".root", tailfrac)
		Histogram2 = UnseededUtilities.ProduceRatioHistogram(UnseededUtilities.Particles[1] + ".root", tailfrac)
		overlap = UnseededUtilities.BhattacharyaCoeff(Histogram1, Histogram2)

		del Histogram1
		del Histogram2

		if overlap < minlap:
			minlap = overlap
			minfrac = tailfrac

	print "\n"
	print "Please place the text below into the database file: CLASSIFIER_ALPHA_UNSEEDED.ratdb located in rat/data, replacing the existing corresponding text."
	print "tail_fraction: %.2fd," % minfrac
	print "\n"


import optparse
if __name__ == '__main__':
	parser = optparse.OptionParser(usage = "usage: %prog [options] target", version = "%prog 1.0")
	parser.add_option("-i", type = "string", dest = "index", help = "RATDB index to place result.", default = "")
	(options, args) = parser.parse_args()
	AnalyseRootFiles(options)
