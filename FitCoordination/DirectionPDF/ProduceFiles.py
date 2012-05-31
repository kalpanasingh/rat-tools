#!/usr/bin/env python
import os, sys, string


def ProduceRunMacFile():
	"""Produces and then runs the appropriate mac files."""
	os.system( "rat Data_for_ntuple.mac" )

if __name__ == '__main__':
	ProduceRunMacFile()
