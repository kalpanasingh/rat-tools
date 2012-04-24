# Tools to manage the RAT PMTINFO & PANELINFO files
Allows conversion from Noel's PMT DB format into the PMTINFO and PANELINFO files (JSON).

## PyYAML & JSON.Minify
The RATDB files are not strict json, rather they are more like YAML with comments. Therefore the included JSON.minify file removes the quotes, and PyYAML parses the result. PyYAML must be separately installed from http://pyyaml.org .

## Convert Noel's to RAT
To convert Noel's csv format to RATDB use the ConvertNoelToPMTINFO.py script:
    python ConvertNoelToPMTINFO.py [Path to Noel csv file] [Path to PANELINFO.ratdb] [Index]
It will parse the csv file and output a new format PMTINFO file. The PMTINFO expects to have the PMT directions, which come from the PANELINFO for panel PMTs and from the position for OWL PMTs (point outwards), for other PMT types it is irrelevant.

## Produce PANELINFO.ratdb
This will hopefully not need to be run again, but if it does just run:
    python ProducePanelInfo.py [Path to old style PMTINFO.ratdb]
It will parse the old style PMTINFO (releases < 3.0) and produce a PANELINFO.ratdb file.
