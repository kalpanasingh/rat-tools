'''tellie2rat.py
This is a script to run near-line, 
it will create and upload a tellie_run
file for the spcified run to the specified
ratdb.

Author: Ed Leming <e.leming@sussex.ac.uk>
'''

import argparse
import sys
import subprocess
import tempfile
import os
import couchdb
import json 

# The following is needed to access the available chstools in rat-tools
#if "RATTOOLS" in os.environ:
#    sys.path.insert(0, os.path.join(os.environ.get("RATTOOLS"), 'TELLIETools'))
#    import telliedbTools
#else:
#    print "tellie2rat: please set RATTOOLS environment variable"
#    sys.exit()


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

def create_rat_run_doc(doc, pass_no=0):
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
        outfilename = 'tellie_run_%i.js' % (doc['run_range'][0])
    with open(outfilename, 'w+') as json_file:
        try:
            json_file.write(json.dumps(doc))
        except:
            raise Exception('Problem writing to file')
        json_file.close()

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="runnumber", help="Run number",
                        type=int, required=True)
    parser.add_argument('-t', dest='telliedb_server',
                        help='URL to CouchDB telliedb server',
                        default='couch.snopl.us')
    parser.add_argument("-u", dest="telliedb_username",
                        help="telliedb Username",
                        type=str, required=True)
    parser.add_argument("-p", dest="telliedb_password",
                        help="telliedb Password",
                        type=str, required=True)
    parser.add_argument('-s', dest='ratdb_server',
                        help='URL to CouchDB ratdb server',
                        #default='http://couch.snopl.us')
                        default='http://localhost:5984/')
    parser.add_argument('-d', dest='ratdb_name',
                        help='Name of ratdb database on server',
                        default='ratdb')
    args = parser.parse_args()
    
    # Get run_doc from telliedb and generate rat-formatted version
    data = get_tellie_run_doc(args.runnumber,
                              args.telliedb_server,
                              args.telliedb_username,
                              args.telliedb_password)
    rat_format = create_rat_run_doc(data)
    
    # Create a temp. file to hold the tellie_run.ratdb content
    with tempfile.NamedTemporaryFile() as tempf:
        write_doc_to_file(rat_format, tempf.name)
        tempf.flush()
    try:
        # Run the command to upload the table to the specified
        # ratdb location
        command = ["ratdb", "upload", "-s", args.ratdb_server, "-d",
                   args.ratdb_name, tempf.name]
        print command
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        print ("tellie2rat run {}: there was a problem uploading "
               "the file").format(args.runnumber)
        return 1
    # Done! 
    return 0

if __name__ == '__main__':
    print sys.exit(main())
