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

# The following is needed to access the available TELLIETools in rat-tools
if "RATTOOLS" in os.environ:
    sys.path.insert(0, os.path.join(os.environ.get("RATTOOLS"), 'TELLIETools'))
    import telliedbTools
else:
    print "tellie2rat: please set RATTOOLS environment variable"
    sys.exit()

def file_check(filename):
    """Function to check the tellierun info
    :param: The name of the temporary file (string).
    :returns: Nothing so far.
    """
    # First make sure it is not empty
    if os.path.getsize(filename) == 0:
        raise RuntimeError("File size is zero")
    # Second, check to make sure it is all ASCII
    # Do this by reading in the lines of the file
    # and try to decode as ascii
    with open(filename, 'r') as f:
        for line in f:
            print line.decode('ascii')
    # Other checks can be added here

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
    data = telliedbTools.get_tellie_run_doc(args.runnumber,
                                            args.telliedb_server,
                                            args.telliedb_username,
                                            args.telliedb_password)

    # Check if this run has old file type - if so, convert to
    # ratdb compatible.
    if int(data['version']) == 0:
        rat_format = telliedbTools.reformat_run_doc(data)
    else: 
        rat_format = data

    # Create a temp. file to hold the tellie_run.ratdb content
    with tempfile.NamedTemporaryFile() as tempf:
        telliedbTools.write_doc_to_file(rat_format, tempf.name)
        tempf.flush()
        # Do some checks on this file to make sure it can be uploaded
        try:
            file_check(tempf.name)
        except RuntimeError, e:
            print "tellie2rat run {}: {}".format(args.runnumber, e)
            return 1
        except UnicodeDecodeError:
            print ("tellie2rat run {}: non-ASCII characters present "
                   "in file").format(args.runnumber)
            return 2
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
            return 3
    # Done! 
    return 0

if __name__ == '__main__':
    print sys.exit(main())
