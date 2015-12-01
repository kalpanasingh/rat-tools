'''telliedbTools.py 
This code has some tools to convert files available 
on the telliedb to be ratdb compatible. This is 
required in a number of cases as ratdb now requires
documents to be selectable by run number, not time

Author: Ed Leming <e.leming@sussex.ac.uk>
Date  : 1/12/2015
'''

import couchdb
import json
import sys 
import os

def get_tellie_run_doc(runnumber, servername, usrname, password):
    '''Function to retrive specific run doc from the
    telliedb.
    :param: The run number requested.
    :returns: A dictionary of the requested doc's fields.
    '''
    login_str = 'http://%s:%s@%s' % (usrname, password, servername)
    telliedb = couchdb.Server(login_str)['telliedb']
    for row in telliedb.view('_design/runs/_view/run_by_number'):
        if int(row.key) == runnumber:
            return telliedb.get(row.id)
    raise Exception('TELLIE run doc %i doesn\'t exist' % (runnumber))

def reformat_run_doc(doc, pass_no=0):
    '''Fuction to updated a telliedb run doc (passed in dictionary form) to be 
    compatiple with standard ratdb format.
    :param: A dictionary containing all the doc fields.
    :param: A pass number to be applied [defaults to 0].
    :returns: A dictionary with updated doc fields.
    '''
    # Make run_range and del old 'run' field
    run_range = [doc['run'], doc['run']]
    del doc['run']
    # Update doc
    doc['run_range'] = run_range
    doc['pass'] = pass_no
    doc['version'] = int(doc['version'])
    doc['production'] = True
    if not 'comment' in doc:
        doc['comment'] = ''
    return doc

def write_doc_to_file(doc, outfilename=None):
    '''Write a .json document from dictionary.
    :param: A dictionary containing all the doc fields.
    :param: The name of the file to be written.
    :returns: None.
    '''
    if outfilename is None:
        outfilename = 'tellie_run_%i' % (doc['run_range'][0])
    with open(outfilename, 'w+') as json_file:
        try:
            json_file.write(json.dumps(doc))
        except:
            raise Exception('Problem writing to file')
        json_file.close()
