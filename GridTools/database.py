#!/usr/bin/env python
#####################
#
# database.py
#
# Methods for db access.
#
# Author: Matt Mottram
#         <m.mottram@sussex.ac.uk>
#
#####################

import getpass
import urlparse
import urllib
import httplib
import base64
import json
import sys

_db_name = None # db name
_db_user = None # db user
_db_pswd = None # db password
_db_host = None # db host
_db_port = None # db port
_db_url = None # db url


def connect_db(db_server, db_port, db_name):
    """Open up the database connection.
    """
    global _db_name, _db_user, _db_pswd, _db_host, _db_url, _db_port
    _db_user = raw_input("[%s] Username: " % db_server)
    _db_pswd = getpass.getpass("[%s] Password: " % db_server)
    _db_name = "%s" % (db_name)
    _db_host = "%s" % (db_server)
    if db_port:
        _db_port = "%s" % (db_port)
    db_http = "http" # For now
    if not db_port:
        _db_url = "%s://%s" % (db_http, db_server)
    else:
        _db_url = "%s://%s:%s" % (db_http, db_server, db_port)


def view(view_name, **kwargs):
    global _db_name, _db_user, _db_pswd, _db_url
    query_opts = {}    
    for name, value in kwargs.items():
        value = json.dumps(value)
        query_opts[name] = value
    query_string = urllib.urlencode(query_opts, True)
    if len(query_opts):
        query_url = "%s/%s/%s?%s" % (_db_url, _db_name, view_name, query_string)
    else:
        query_url = "%s/%s/%s" % (_db_host, _db_name, view_name)
    response = get_response(_db_host, query_url, _db_user, _db_pswd)
    # Now map these to rows
    try:
        data = json.loads(response)
    except ValueError, e:
        # Don't bother parsing whole html response, just look for the response code
        if "401 Authorization Required" in response:
            print "Failed to contact database, incorrect credentials supplied?"
            sys.exit()
        else:
            raise Exception("Unknown respose from database:\n%s" % response)
    try:
        return data["rows"]
    except KeyError, e:
        sys.stderr.write("DB view error, response: %s\tquery: %s" % (response, query_url))
        raise


def get_response(host, url, username=None, password=None):
    headers = {}
    if username is not None and password is not None:
        auth_string = base64.encodestring('%s:%s' % (username, password))[:-1]
        headers['Authorization'] = 'Basic %s' % auth_string
    if _db_port is not None:
        connection = httplib.HTTPConnection(host, port=_db_port)
    else:
        connection = httplib.HTTPConnection(host)
    try:
        connection.request('GET', url, headers=headers)
        response = connection.getresponse()
    except httplib.HTTPException as e:
        sys.stderr.write('Error accessing the requested db query: %s' % str(e))
        sys.exit(20)
    return response.read()
