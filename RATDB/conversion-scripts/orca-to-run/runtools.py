"""runtools.py
This code has some tools to access the run info from orcadb
and to create the run.ratdb file
for the specified runnumber.

Author: Freija Descamps
         <fbdescamps@lbl.gov>
"""

import httplib
import json
import sys
import datetime


def get_run_document_from_db(runnumber, db_server, db_username, db_password):
    """Function to retrieve the ORCA run document
    from the snoplus database.
    :param: The run-number (string).
    :param: The username for the snoplus database (string).
    :param: The password for the snoplus database (string).
    :returns: The ORCA run document for specified run-number.
    """
    # Contact the snoplus ORCA database to retrieve the run configuration file
    # for the requested run
    auth = db_username + ":" + db_password
    request_url = '/orca/_design/OrcaViews/_view/viewRunTypeByRunNumber?descending=true&include_docs=true&startkey=%s&endkey=%s' % (runnumber, runnumber)
    request_headers = {'Content-type': "application/json"}
    request_headers['Authorization'] = 'Basic {}'.format(auth.encode('base64'))
    # New python versions (=>2.7.10) do not like newlines in the HTTP headers,
    # see http://bugs.python.org/issue22928
    request_headers['Authorization'] = request_headers['Authorization'].rstrip()
    connection = httplib.HTTPConnection(db_server)
    connection.request('GET', request_url, headers=request_headers)
    try:
        data = json.loads(connection.getresponse().read())
    except ValueError:
        sys.stderr.write("Failed to contact database, try again\n")
        sys.exit(1)
    rows = data['rows']
    # Check if there is data available for this run
    if len(rows) == 0:
        sys.stderr.write("No ORCA data for this run\n")
        sys.exit(1)
    return data


def write_run_document_to_file(runnumber, data, outfilename=None):
    """Function that writes out the RUN.ratdb file
    :param: runnumber: The run-number (string).
    :param: data: The ORCA run document data
    :param: outfilename: The name for the outputfile (optional)
    :returns: None.
    """
    if outfilename is None:
        outfilename = "RUN_%i.ratdb" % (runnumber)
    runtype = data['rows'][0]['doc']['run_type']
    starttime = data['rows'][0]['doc']['timestamp_start']
    endtime = data['rows'][0]['doc']['timestamp_end']
    runrange = [runnumber, runnumber]
    ratdb_content = {
        'type': 'RUN',
        'version': 1,
        'pass': 0,
        'run_range': runrange,
        'comment': '',
        'timestamp': '',
        'production': 'true',
        'run_type': runtype,
        'starttime': starttime,
        'endtime': endtime
    }
    with open(outfilename, 'w') as f:
        json.dump(ratdb_content, f, sort_keys=True,
                  indent=4, separators=(',', ': '))
