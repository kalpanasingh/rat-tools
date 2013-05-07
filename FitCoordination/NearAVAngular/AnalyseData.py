#!/usr/bin/env python
import os, sys, string, ROOT, rat


def AnalyseFiles():
  ROOT.gROOT.ProcessLine(".L Coordinate.cpp+")
  ROOT.Coordination("electrons_5000mm.root", "electrons_5300mm.root", "electrons_5400mm.root", "electrons_5500mm.root", "electrons_5600mm.root", "electrons_5700mm.root", "electrons_5800mm.root", "electrons_5900mm.root")
  ROOT.gROOT.ProcessLine(".q")


if __name__ == '__main__':
	AnalyseFiles()
