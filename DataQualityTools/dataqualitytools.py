"""dataqualitytools.py
This code has some tools to access the ORCA run and configuration 
documents for the data-quality (DQ) low-level (LL) checks. 
Work in progress: 
- does not read the XL3 error and screwed messages (from run Log files)
- does not read the slow control database yet
- does not read the PIE database yet

Author: Gersende Prior
        <gersende@lip.pt>

Inspired by chstools.py script from Freija Descamps
"""

import getpass
import argparse
import httplib
import json
import sys
import dateutil
import pytz
import datetime

from pprint import pprint

db_server = 'couch.snopl.us'

def get_configuration_document_from_db(runnumber, db_username, db_password):
    """Function to retrieve the ORCA configuration document
    from the snoplus database.
    :param: The run-number (int).
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA configuration data for the specified runnumber.
    """
    # Contact the snoplus ORCA database to retrieve the configuration file
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewConfigDocByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {}'.format(auth.encode('base64'))
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
    
def get_run_document_from_db(runnumber, db_username, db_password):
    """Function to retrieve the ORCA runconfiguration document
    from the snoplus database.
    :param: The run-number (int).
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA run document for the specified runnumber.
    """
    # Contact the snoplus ORCA database to retrieve the run document
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewRunTypeByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {}'.format(auth.encode('base64'))
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
    :returns: true if run document properly filled, false otherwise
    """

    timeok = 'false'

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
        timeok = 'false'
        return timeok
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
        timeok = 'true'

    if not (timeendstring or timestampendstring):
        table.write('end_time: "no end-of-run time information in the run document"\n')
        timeok = 'false'
        return timeok
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
        timeok = 'true'

    if timeok:
        timestampdiff = timestampendstring - timestampstartstring

        duration = "\"duration_seconds\": {0},\n".format(int(round(timestampdiff)))
        table.write(duration)

        table.write("\n")

    return timeok

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
    table.write('"type": "DATAQUALITY_LOWLEVEL",\n')
    table.write('"version": 1,\n')
    table.write('"index": "",\n')
    
    runrange = "\"run_range\": [{0},{1}],\n".format(runnumber,runnumber)
    table.write(runrange)
    
    table.write('"pass": 0,\n')
    table.write('"production": false,\n')
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
