#!/usr/bin/env python
#####################
#
# list_generator
#
# Generates lists of production or
# processed data (full RAT format or
# ntuples) for download.
#
# Author: Matt Mottram
#         <m.mottram@sussex.ac.uk>
#
#####################

import os
import sys
import database
import grid
import utilities
try:
    import json
except:
    raise ImportError("json not available; python version needs to be 2.7+")
    

# Copy type will be set to SURL if lcg-utils or gfal are not available
copy_type = "GUID"
server_list = []
# The first allowed type will ALWAYS be the default
allowed_file_types = ["ntuple", "ratds", "soc"]


def get_module_list_version(data_type, rat_version=None):
    """Get a list of available modules.
    """
    rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                         reduce=True, group=True, group_level=3,
                         startkey=[data_type], endkey=[data_type,{}])
    module_list = []
    for row in rows:
        if rat_version and row["key"][2] != unicode(rat_version):
            continue
        module_list.append(row["key"][1])
    return module_list


def get_module_list_label(data_type, label=None):
    """Get a list of available modules.                                                                                                            
    """
    rows = database.view("_design/proddata/_view/data_by_label",
                         reduce=True, group=True, group_level=3,
                         startkey=[data_type], endkey=[data_type,{}])
    module_list = []
    for row in rows:
        if label and row["key"][0]!=unicode(label):
            continue
        module_list.append(row["key"][1])
    return module_list


def get_list_by_module_version(data_type, module, rat_version, run_range):
    """Get a list of files for the settings given.
    """
    names = []
    sizes = []
    guids = []
    adlers = []
    rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                   startkey = [data_type, module, rat_version],
                   endkey = [data_type, module, rat_version, {}],
                   reduce=False)
    for row in rows:
        if copy_type=="GUID":
            if not row["value"][2] or row["value"][2]=="":
                print "Cannot get file %s, no GUID" % (row["value"][0])
                continue
        else:
            if len(row["value"][4])==0 or row["value"][4]=="":
                print "Cannot get file %s, no SURL" % row["value"][0]
                continue
        # Run range is after pass in the key, have to filter here rather than on server
        if run_range:
            if row["key"][4] < run_range[0] or row["key"][4] > run_range[1]:
                continue
        names.append(row["value"][0])
        sizes.append(row["value"][1])
        if copy_type=="GUID":
            guids.append(row["value"][2])
        else:
            guids.append(grid.get_closest_copy(server_list, row["value"][4]))
        adlers.append(row["value"][5])
    return names, sizes, guids, adlers


def get_list_by_label_module(data_type, label, module, run_range):
    """Get a list of files for the settings given

    If no module give, return all modules.
    """
    names = []
    sizes = []
    guids = []
    adlers = []
    startkey = [data_type, label, module]
    endkey = [data_type, label, module, {}]
    if run_range:        
        startkey = [data_type, label, module, run_range[0]]
        endkey = [data_type, label, module, run_range[1]+1] # range inclusive    
    rows = database.view("_design/proddata/_view/data_by_label",
                   startkey=startkey, endkey=endkey, reduce=False)
    for row in rows:
        if copy_type=="GUID":
            if not row["value"][1] or row["value"][1]=="":
                print "Cannot get file %s, no GUID" % (row["value"][0])
                continue
        else:
            if len(row["value"][4])==0 or row["value"][4]=="":
                print "Cannot get file %s, no SURL" % row["value"][0]
                continue
        names.append(row["value"][0])
        if copy_type=="GUID":
            guids.append(row["value"][1])
        else:
            guids.append(grid.get_closest_copy(server_list, row["value"][4]))
        adlers.append(row["value"][2])
        sizes.append(row["value"][3])
    return names, sizes, guids, adlers


def get_labels(data_type, module=None):
    """Get a list of all labels available

    Specify a module to see versions associated with that module.
    """
    labels = set()
    if module is None:
        # List any labels
        rows = database.view("_design/proddata/_view/data_by_label",
                             reduce=True, group_level=3,
                             startkey=[data_type], endkey=[data_type, {}])
        for row in rows:
            labels.add(row["key"][1])
    elif type(module)==list and len(module)==1:
        # List labels only for a given module
        rows = database.view("_design/proddata/_view/data_by_label",
                             reduce=True, group_level=3,
                             startkey=[data_type], endkey=[data_type, {}])
        for row in rows:
            if str(row["key"][2])==module[0]:
                labels.add(row["key"][1])
    else:
        raise Exception("Must only provide one module name.")
    return labels


def get_versions(data_type, module=None):
    """Get a list of all versions available.

    Specify a module to see versions associated with that module.
    """
    versions = set()
    if module is None:
        # List all RAT versions
        rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                             reduce=True, group_level=3,
                             startkey=[data_type], endkey=[data_type, {}])
        for row in rows:
            versions.add(row["key"][2])
    elif type(module)==list and len(module)==1:
        # List only versions for a given module
        rows = database.view("_design/proddata/_view/%s_by_mod_pass_sr",
                             reduce=True, group_level=3,
                             startkey=[data_type], endkey=[data_type, {}])
        for row in rows:
            if str(row["key"][1])==module[0]:
                versions.add(row["key"][2])
    else:
        raise Exception("Must only provide one module name.")
    return versions


def get_modules(data_type, label=None, version=None):
    """Get a list of all modules available

    Only one of label or version can be specified (or neither).
    """
    if label is not None and version is not None:
        raise Exception("May only specify label OR version")
    modules = set()
    if label is not None:
        # Only modules for a given label
        rows = database.view("_design/proddata/_view/data_by_label" % (data_type),
                             reduce=True, group_level=3, startkey=[data_type, label],
                             endkey=[data_type, label, {}])
        for row in rows:
            modules.add(row["key"][2])
    elif version is not None:
        # Only modules for a given RAT version
        rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                             reduce=True, group_level=3, startkey=[data_type],
                             endkey=[data_type, {}])
        for row in rows:
            if str(row["key"][2])==version:
                modules.add(row["key"][1])
    else:
        # Any and all modules
        rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                             reduce=True, group_level=2,
                             startkey=[data_type], endkey=[data_type, {}])
        for row in rows:
            modules.add(row["key"][1])
    return modules


def get_response(host, url, username=None, password=None):
    headers = {}
    if username is not None and password is not None:
        auth_string = base64.encodestring('%s:%s' % (username, password))[:-1]
        headers['Authorization'] = 'Basic %s' % auth_string
    connection = httplib.HTTPConnection(host, port=5984)
    try:
        connection.request('GET', url, headers=headers)
        response = connection.getresponse()
    except httplib.HTTPException as e:
        sys.stderr.write('Error accessing the requested db query: %s' % str(e))
        sys.exit(20)
    return response.read()


def generate_list_by_label(label, data_type, module, run_range):
    """Generate the file list by production labels
    """
    names = []
    sizes = []
    guids = []
    adlers = []
    if not module:
        module = get_module_list_label(data_type)
    print module
    for i, mod in enumerate(module):
        print "Generating file lists, %d of %d" % (i, len(module))
        n, s, g, a = get_list_by_label_module(data_type, label, mod, run_range)
        names += n
        sizes += s
        guids += g
        adlers += a
    if len(names)==0:
        print "No files for label %s, modules %s" % (label, module)
        sys.exit()
    return names, sizes, guids, adlers


def generate_list_by_version(version, data_type, module, run_range):
    """Generate the file list by rat version
    """
    # Now loop through each module and get the file lists
    if not module:
        module = get_module_list_version(data_type, version)
    if len(module)==0:
        print "No modules for rat %s" % version
        sys.exit()
    names = []
    sizes = []
    guids = []
    adlers = []
    for i, mod in enumerate(module):
        print "Generating file lists, %d of %d" % (i, len(module))
        n, s, g, a= get_list_by_module_version(data_type, mod, version, run_range)
        names += n
        sizes += s
        guids += g
        adlers += a
    if len(names)==0:
        print "No files for version %s, modules %s" % (version, module)
        sys.exit()
    return names, sizes, guids, adlers


def generate_list(parser):
    '''Main function called by both production_list and processing_list
    '''
    global copy_type, server_list
    args = parser.parse_args()

    if args.file_type not in allowed_file_types:
        print "Unknown filetype, allowed types are:"
        print ", ".join(f for f in allowed_file_types)
        sys.exit()

    # First, check that no help commands are requested
    if args.list_labels:
        database.connect_db(args.db_server, args.db_port, args.db_name)
        for l in sorted(get_labels(args.file_type, args.module)):
            print l
        sys.exit()
    if args.list_versions:
        database.connect_db(args.db_server, args.db_port, args.db_name)
        for v in sorted(get_versions(args.file_type, args.module)):
            print v
        sys.exit()
    if args.list_modules:
        database.connect_db(args.db_server, args.db_port, args.db_name)
        for m in sorted(get_modules(args.file_type, args.label, args.version)):
            print m
        sys.exit()

    # Check that the output file is OK
    if os.path.exists(args.output):
        overwrite = raw_input("%s exists, overwrite [y/N]?: " % args.output)
        if overwrite!="y" and overwrite!="Y":
            print "Specify another filename"
            sys.exit()

    # Connect to the database
    database.connect_db(args.db_server, args.db_port, args.db_name)

    # If there is a run range, need exactly two arguments
    if args.run_range:
        if len(args.run_range)!=2:
            print "Require two arguments for run range (lower upper)"
            sys.exit()

    if grid.copy == grid.srm_copy:
        # Use SRMs to copy from 
        copy_type = "SURL"
        server_list = grid.get_server_preferences()

    # Now handle either rat version or labelled data
    if args.label:
        names, sizes, guids, adlers = generate_list_by_label(args.label, args.file_type, args.module, args.run_range)   
    elif args.version:
        names, sizes, guids, adlers = generate_list_by_version(args.version, args.file_type, args.module, args.run_range)   
    else:
        parser.print_help()
        print "Incorrect usage; see help above"
        sys.exit()    

    # And write the output file
    utilities.write_grabber_file(args.output, copy_type, names, sizes, guids, adlers)
