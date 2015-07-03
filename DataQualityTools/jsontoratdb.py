# Convert the DQ LL table in JSON format to a DQ LL table in ratdb format

import argparse
import array

from pprint import pprint

# Read the DQ LL JSON table
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="filename", help="JSON table filename", type=str, required=True)
    args = parser.parse_args()
    if args.filename is None:
        sys.stderr.write("Please supply a JSON table filename using \'-f\'")
        sys.exit(1)

    jsonfile = args.filename

    splitjson = jsonfile.split("_")

    runnumber = splitjson[1]

    print "Converting the JSON table to RATDb format for run " + str(runnumber)

    # Create the DQ LL table in ratdb format
    ratdbfile = "run_{0}_dqll.ratdb".format(runnumber)
        
    ratdbtable = open(ratdbfile,'w')

    # Open the JSON table and reads it
    jsontable = open(jsonfile,'r')
    
    beginline = jsontable.readline()

    ratdbtable.write(beginline)

    for i in range(7):

        headerstring = jsontable.readline().split(":")

        noquoteheader = headerstring[0].split("\"")

        ratdbheaderstring = "{0}:{1}".format(noquoteheader[1],headerstring[1])

        ratdbtable.write(ratdbheaderstring)

    # Timestamps need special treatment
    timestampstring = jsontable.readline().split(":")

    noquotetimestamp = timestampstring[0].split("\"")

    ratdbtimestampstring = "{0}:{1}:{2}:{3}:{4}".format(noquotetimestamp[1],timestampstring[1],timestampstring[2],timestampstring[3],timestampstring[4])

    ratdbtable.write(ratdbtimestampstring)

    returnline1 = jsontable.readline()

    ratdbtable.write(returnline1)

    for i in range(2):

        timestring = jsontable.readline().split(":")

        noquotetime = timestring[0].split("\"")

        ratdbtimestring = "{0}:{1}:{2}:{3}:{4}".format(noquotetime[1],timestring[1],timestring[2],timestring[3],timestring[4])

        ratdbtable.write(ratdbtimestring)
   
    durationstring = jsontable.readline().split(":")

    noquoteduration = durationstring[0].split("\"")

    ratdbdurationstring = "{0}:{1}".format(noquoteduration[1],durationstring[1])

    ratdbtable.write(ratdbdurationstring)

    returnline2 = jsontable.readline()

    ratdbtable.write(returnline2)

    for i in range(2):

        cratestatusstring = jsontable.readline().split(":")

        noquotecratestatus = cratestatusstring[0].split("\"")

        ratdbcratestatusstring = "{0}:{1}".format(noquotecratestatus[1],cratestatusstring[1])

        ratdbtable.write(ratdbcratestatusstring)

    returnline3 = jsontable.readline()

    ratdbtable.write(returnline3)

    for i in range(2):

        cratenominalstring = jsontable.readline().split(":")
        
        noquotecratenominal = cratenominalstring[0].split("\"")

        ratdbcratenominalstring = "{0}:{1}".format(noquotecratenominal[1],cratenominalstring[1])
        
        ratdbtable.write(ratdbcratenominalstring)

    returnline4 = jsontable.readline()

    ratdbtable.write(returnline4)

    for i in range(2):

        cratehvreadstring = jsontable.readline().split(":")
        
        noquotecratehvread = cratehvreadstring[0].split("\"")

        ratdbcratehvreadstring = "{0}:{1}".format(noquotecratehvread[1],cratehvreadstring[1])
        
        ratdbtable.write(ratdbcratehvreadstring)

    returnline5 = jsontable.readline()

    ratdbtable.write(returnline5)

    for i in range(2):

        cratecurrentreadstring = jsontable.readline().split(":")
        
        noquotecratecurrentread = cratecurrentreadstring[0].split("\"")

        ratdbcratecurrentreadstring = "{0}:{1}".format(noquotecratecurrentread[1],cratecurrentreadstring[1])
        
        ratdbtable.write(ratdbcratecurrentreadstring)

    returnline6 = jsontable.readline()

    ratdbtable.write(returnline6)

    for i in range(6):

        xl3errorstring = jsontable.readline().split(":")
        
        noquotexl3error = xl3errorstring[0].split("\"")

        ratdbxl3errorstring = "{0}:{1}".format(noquotexl3error[1],xl3errorstring[1])
        
        ratdbtable.write(ratdbxl3errorstring)

    returnline7 = jsontable.readline()

    ratdbtable.write(returnline7)

    xl3screwedstring = jsontable.readline().split(":")
        
    noquotexl3screwed = xl3screwedstring[0].split("\"")

    ratdbxl3screwedstring = "{0}:{1}".format(noquotexl3screwed[1],xl3screwedstring[1])
        
    ratdbtable.write(ratdbxl3screwedstring)

    endline = jsontable.readline()

    ratdbtable.write(endline)
   
    jsontable.close()

    ratdbtable.close()
