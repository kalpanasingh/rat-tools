"""dqlltools.py
This code has some tools to access the ORCA run and configuration 
documents for the data-quality (DQ) low-level (LL) checks. 
Work in progress: 
- does not read the XL3 error and screwed messages (from run Log files)
- does not read the slow control database yet
- does not read the PIE database yet

Author: Gersende Prior
        <gersende@lip.pt>

Inspired by runtools.py script from Freija Descamps
"""

import getpass
import argparse
import httplib
import json
import sys
import dateutil
import pytz
import datetime
import os

from pprint import pprint

def get_configuration_document_from_db(runnumber, db_server, db_username, db_password):
    """Function to retrieve the ORCA configuration document
    from the snoplus database.
    :param: The run-number (string).
    :param: the servername for the snoplus database (string)
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA configuration data for the specified runnumber.
    """
    # Contact the snoplus ORCA database to retrieve the configuration file
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewConfigDocByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {0}'.format(auth.encode('base64'))
    # New python versions (=>2.7.10) do not like newlines in the HTTP headers,  
    # see http://bugs.python.org/issue22928
    request_headers['Authorization'] = request_headers['Authorization'].rstrip()
    connection = httplib.HTTPConnection(db_server)
    connection.request('GET', request_url, headers=request_headers)
    try:
        data = json.loads(connection.getresponse().read())
    except ValueError, e:
        sys.stderr.write("Failed to contact database, try again\n")
        sys.exit(1)
    rows = data['rows']
    # Check if there is data available for this run
    if len(rows) == 0:
        sys.stderr.write("No ORCA configuration file for this run\n")
        sys.exit(1)
    return data
    
def get_run_document_from_db(runnumber, db_server, db_username, db_password):
    """Function to retrieve the ORCA run document
    from the snoplus database.
    :param: The run-number (string).
    :param: The servername for the snoplus database (string).
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA run document for the specified runnumber.
    """
    # Contact the snoplus ORCA database to retrieve the run document
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewRunTypeByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {0}'.format(auth.encode('base64'))
    # New python versions (=>2.7.10) do not like newlines in the HTTP headers,	
    # see http://bugs.python.org/issue22928
    request_headers['Authorization'] = request_headers['Authorization'].rstrip()
    connection = httplib.HTTPConnection(db_server)
    connection.request('GET', request_url, headers=request_headers)
    try:
        data = json.loads(connection.getresponse().read())
    except ValueError, e:
        sys.stderr.write("Failed to contact database, try again\n")
        sys.exit(1)
    rows = data['rows']
    # Check if there is data available for this run
    if len(rows) == 0:
        sys.stderr.write("No ORCA run document for this run\n")
        sys.exit(1)
    return data

def write_db_times(table,data):
    """Write in table run start and end times and duration
    :params: The ORCA run document data for the run processed
    :returns: run duration in sec if ok if not any of the -999/-99/-9
    """

    duration = -999

    # Define Sudbury time zone
    sudburytimezone = pytz.timezone('US/Eastern')

    monthname = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    monthid = ('01','02','03','04','05','06','07','08','09','10','11','12')

    rows = data['rows']

    for value in rows:

        timestartstring = value['doc']['sudbury_time_start']

        timeendstring = value['doc']['sudbury_time_end']

        timestampstartstring = value['doc']['timestamp_start']
        
        timestampendstring = value['doc']['timestamp_end']

    if not (timestartstring or timestampstartstring):
        table.write('start_time: "no start-of-run time information in the run document"\n')
        duration = -9
        return duration
    else:

        # Put the start time in correct format
        timestartsplit = timestartstring.split(" ")

        startyear = timestartsplit[3]

        for i in range(0,12):
            if monthname[i] == timestartsplit[2]:
                startmonth = monthid[i]

        startday = timestartsplit[1]

        starthour = timestartsplit[4]

        starttimezone = timestartsplit[5]

        # Create an ISO 8601 compliant string for startdate
        timestampstart = "{0}-{1}-{2}T{3}{4}".format(startyear,startmonth,startday,starthour,starttimezone)

        # Convert the string to a datetime object
        timestampstart_obj = dateutil.parser.parse(timestampstart)

        # If there was no time zone information in the string, assume it's UTC
        if timestampstart_obj.tzinfo is None:
            timestampstart_obj = (pytz.timezone('UTC')).localize(timestampstart_obj)

        starttime =  timestampstart_obj.astimezone(sudburytimezone).isoformat()
        start_time = "\"start_time\": \"{0}\",\n".format(starttime)
        table.write(start_time)

    if not (timeendstring or timestampendstring):
        table.write('end_time: "no end-of-run time information in the run document"\n')
        duration = -99
        return duration
    else:

        # Put the end time in correct format
        timeendsplit = timeendstring.split(" ")

        endyear = timestartsplit[3]

        for i in range(0,12):
            if monthname[i] == timeendsplit[2]:
                endmonth = monthid[i]

        endday = timeendsplit[1]

        endhour = timeendsplit[4]

        endtimezone = timeendsplit[5]

        # Create an ISO 8601 compliant string for enddate
        timestampend = "{0}-{1}-{2}T{3}{4}".format(endyear,endmonth,endday,endhour,endtimezone)

        # Convert the string to a datetime object
        timestampend_obj = dateutil.parser.parse(timestampend)

        # If there was no time zone information in the string, assume it's UTC
        if timestampend_obj.tzinfo is None:
            timestampend_obj = (pytz.timezone('UTC')).localize(timestampend_obj)

        endtime = timestampend_obj.astimezone(sudburytimezone).isoformat()
        end_time = "\"end_time\": \"{0}\",\n".format(endtime)
        table.write(end_time)

    timestampdiff = timestampendstring - timestampstartstring

    duration = int(round(timestampdiff))

    duration_sec = "\"duration_seconds\": {0},\n".format(int(round(timestampdiff)))
    table.write(duration_sec)

    table.write("\n")

    return duration

def create_hv_status_a(data):
    """Retrieve the crate HV status (ON/OFF) from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_status_a: the boolean array of crate HV status (ON = true, OFF= false) for power supply A
    """

    hv_status_a = ['false' for i in range(19)]

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']

        for crate in range(0,19):

            status = xl3s.get(str(crate))['hv_status_a']

            if status == "OFF":
                hv_status_a[crate] = 'false'

            if status == "ON":
                hv_status_a[crate] = 'true'

    return hv_status_a

def create_hv_status_b(data):
    """Retrieve the crate 16 HV status (ON/OFF) from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_status_b: crate 16 HV status in boolean (OFF = false, ON = true) for power supply B
    """

    hv_status_b = 'false'

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']

        status = xl3s.get(str(16))['hv_status_b']

        if status == "OFF":
            hv_status_b = 'false'

        if status == "ON":
            hv_status_b = 'true'

    return hv_status_b

def create_hv_nominal_a(data):
    """Retrieve the crate HV nominal value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_nominal_a: the array of crate HV nominal values for power supply A
    """
    
    hv_nominal_a = [0 for i in range(19)]

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']

        for crate in range(0,19):

            hv_nominal_a[crate] = xl3s.get(str(crate))['hv_nominal_a']

    return hv_nominal_a

def create_hv_nominal_b(data):
    """Retrieve the crate 16 HV nominal value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_nominal_b: crate 16 HV nominal values for power supply B
    """
    
    hv_nominal_b = 0

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']

        hv_nominal_b = xl3s.get(str(16))['hv_nominal_b']

    return hv_nominal_b

def create_hv_read_value_a(data):
    """Retrieve the crate HV read value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_nominal_a: the array of crate HV read values for power supply A
    """
    
    hv_read_value_a = [0 for i in range(19)]

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']
        
        for crate in range(0,19):
            
            hv_read_value_a[crate] = xl3s.get(str(crate))['hv_voltage_read_value_a']

    return hv_read_value_a

def create_hv_read_value_b(data):
    """Retrieve the crate 16 HV read value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: hv_nominal_a: crate 16 HV read values for power supply B
    """
    
    hv_read_value_b = 0

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']
        
        hv_read_value_b = xl3s.get(str(16))['hv_voltage_read_value_b']

    return hv_read_value_b

def create_current_read_value_a(data):
    """Retrieve the crate current read value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: current_read_value_a: the array of crate current read values for power supply A
    """
    
    current_read_value_a = [0 for i in range(19)]

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']
        
    for crate in range(0,19):
            
        current_read_value_a[crate] = xl3s.get(str(crate))['hv_current_read_value_a']

    return current_read_value_a

def create_current_read_value_b(data):
    """Retrieve the crate 16 current read value from the orca runconfiguration document
    :param: The ORCA run configuration data for the run processed
    :returns: current_read_value_b: crate 16 current read values for power supply B
    """
    
    current_read_value_b = 0

    rows = data['rows']

    for value in rows:

        xl3s = value['doc']['xl3s']
        
    current_read_value_b = xl3s.get(str(16))['hv_current_read_value_b']

    return current_read_value_b

def write_db_header(table,runnumber):
    """Write the database table header lines
    :param: database file pointer
    """

    table.write('{\n')
    table.write('"type": "DQLL",\n')
    table.write('"version": 1,\n')
    table.write('"index": "",\n')
    
    runrange = "\"run_range\": [{0},{1}],\n".format(runnumber,runnumber)
    table.write(runrange)
    
    table.write('"pass": 0,\n')
    table.write('"production": true,\n')
    table.write('"comment": "",\n')

    currentdatetime = datetime.datetime.now()

    # If there is no time zone information in the string, assume it's the local computer timezone
    if currentdatetime.tzinfo is None:
        currentdatetime = (pytz.timezone('Europe/Lisbon')).localize(currentdatetime)

        # Define Sudbury time zone
        sudburytimezone = pytz.timezone('US/Eastern')

        timestamp = "\"timestamp\": \"{0}\",\n".format(currentdatetime.astimezone(sudburytimezone).isoformat())
        table.write(timestamp)

        table.write("\n")

def write_db_footer(table,runnumber):
    """Write the database table footer lines
    :param: table database file pointer
    :param: runnumber the run number processed
    """
    
    table.write('}\n')

def file_jsoncheck(filename):
    """Function to check that file is JSON format and number of lines is correct
    :param: The name of the JSON file (string)
    :returns: boolean true if JSON
    """
    with open(filename, 'r') as jsontable:
        try:
            json_object = json.load(jsontable)
        except ValueError, e:
            return False

    # DQLL.json number of lines should be 35
    # Will change with table version
    nlines = 35
        
    with open(filename, 'r') as f:
         l = [x for x in f.readlines()]
         # Default number of lines should be 35
         if len(l) != nlines:
             print "Number of lines in DQLL.json is not default {} but {}".format(nlines, len(l))
             return False

    return True

def json_to_ratdb(local_dir,filename):
    """Function to convert the JSON table to the ratdb format
    :param: The local directory where to put the ratdb tables (string)
    :param: The name of the file to convert (string)
    :returns: nothing
    """ 
    ratdbdir = local_dir

    jsonfile = filename

    splitjson = jsonfile.split("_")

    runnumber = splitjson[1]

    print "Converting the JSON table to RATDb format for run " + str(runnumber)

    # Create the DQ LL table in ratdb format
    ratdbfile = "{0}run_{1}_dqll.ratdb".format(ratdbdir,runnumber)
        
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

    ratdbtimestampstring = "{0}:{1}:{2}:{3}:{4}".format(noquotetimestamp[1], timestampstring[1],
                                                                             timestampstring[2], 
                                                                             timestampstring[3],
                                                                             timestampstring[4])

    ratdbtable.write(ratdbtimestampstring)

    returnline1 = jsontable.readline()

    ratdbtable.write(returnline1)

    for i in range(2):

        timestring = jsontable.readline().split(":")

        noquotetime = timestring[0].split("\"")

        ratdbtimestring = "{0}:{1}:{2}:{3}:{4}".format(noquotetime[1], timestring[1],
                                                                       timestring[2],
                                                                       timestring[3],
                                                                       timestring[4])

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



