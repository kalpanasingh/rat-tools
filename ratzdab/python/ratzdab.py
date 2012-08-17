'''Python interface to libratzdab, wrapped using CINT and PyROOT.

Provides:

    `ratzdab.zdabfile(filename)`:
        A `ratzdab::zdabfile` ZDAB file interface object

    `ratzdab.dispatch(hostname, block=True)`:
        A `ratzdab::dispatch` ZDAB dispatcher interface object

    `ratzdab.pack.*`:
        Packing functions from `ratzdab::pack`

    `ratzdab.unpack.*`:
        Unpacking functions from `ratzdab::unpack`

SNO struct types are available in `ratzdab.ROOT` and RAT ROOT types are found
in `ratzdab.ROOT.RAT`.
'''

from os.path import dirname, join
from rat import ROOT
ROOT.gROOT.SetBatch(True)

libpath = join(dirname(dirname(__file__)), 'lib')
ROOT.gROOT.ProcessLine('.L %s/ratzdab_root.so' % libpath)

# more convenient scope
zdabfile = ROOT.ratzdab.zdabfile
dispatch = ROOT.ratzdab.dispatch
pack = ROOT.ratzdab.pack
unpack = ROOT.ratzdab.unpack

