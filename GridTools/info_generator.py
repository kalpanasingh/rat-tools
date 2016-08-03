#!/usr/bin/env python
#####################
#
# info_generator.py
#
# Generates lists with supplementary
# information (e.g. number of sim entries)
# that is useful for analysis (esp. ntuples)
#
# Author: Matt Mottram
#         <m.mottram@qmul.ac.uk>
#
#####################

import os
import sys
import database
import list_generator as lg

allowed_fields = sorted(['sim_entries', 'z', 'rate', 'day'])

def get_fields_from_doc(doc, sub_run, fields):
    '''Return a list (same ordering as fields passed in)
    of values for the document.
    '''
    values = [None for f in fields]
    for i, f in enumerate(fields):
        if f=='sim_entries':
            try:
                val = doc['files'][sub_run]['sim_entries']
            except KeyError:
                val = None
        else:
            try:
                val = doc['files'][sub_run]['extras'][f]
            except:
                val = None
        values[i] = val
    return values


def generate_info_by_label(label, data_type, modules, run_range, fields):
    '''Generates file information by production labels
    '''
    names = []
    info = [[] for f in fields]
    output_list = []
    for i, module in enumerate(modules):

        print "Generating lists, %d of %d" % (i, len(modules))
        startkey = [data_type, label, module]
        endkey = [data_type, label, module]
        if run_range:
            startkey.append(run_range[0])
            endkey.append(run_range[1]+1)
        else:
            # No need to change the startkey
            endkey.append({})
        rows = database.view("_design/proddata/_view/data_by_label",
                             reduce = False, include_docs = True,
                             startkey = startkey, endkey=endkey)
        for row in rows:
            # We only want the sub run from the key...
            sub_run = row['key'][-1]
            name = row['value'][0]
            values = get_fields_from_doc(row['doc'], sub_run, fields)
            output_list.append([name]+values)
    return output_list


def generate_info_by_version(version, data_type, modules, run_range, fields):
    '''Generates file information by production labels
    '''
    names = []
    info = [[] for f in fields]
    output_list = []
    for i, module in enumerate(modules):

        print "Generating lists, %d of %d" % (i, len(modules))
        startkey = [data_type, module, version]
        endkey = [data_type, module, version]
        if run_range:
            startkey.append(run_range[0])
            endkey.append(run_range[1]+1)
        else:
            # No need to change the startkey
            endkey.append({})
        rows = database.view("_design/proddata/_view/data_by_mod_pass_sr",
                             reduce = False, include_docs = True,
                             startkey = startkey, endkey=endkey)
        for row in rows:
            # We only want the sub run from the key...
            sub_run = row['key'][-1]
            name = row['value'][0]
            values = get_fields_from_doc(row['doc'], sub_run, fields)
            output_list.append([name]+values)
    return output_list


def generate_info(parser):
    
    args = parser.parse_args()

    if args.file_type not in lg.allowed_file_types:
        print "Unknown filetype, allowed types are:"
        print ", ".join(f for f in lg.allowed_file_types)
        sys.exit()

    for field in args.fields:
        if field not in allowed_fields:
            print "Unknown field, allowed values are:"
            print ", ".join(f for f in allowed_fields)
            sys.exit()

    if args.list_fields:
        print "ALLOWED FIELDS:"
        print ", ".join(f for f in allowed_fields)
        sys.exit()

    if not args.module:
        parser.print_help()
        print "Require a module argument"
        sys.exit()

    # For each module requested, get files in the range
    # and list information for each file (NA if missing)
    database.connect_db(args.db_server, args.db_port, args.db_name)

    if args.label:
        file_info = generate_info_by_label(args.label, args.file_type, args.module,
                               args.run_range, args.fields)
    elif args.version:
        file_info = generate_info_by_version(args.version, args.file_type, args.module,
                                             args.run_range, args.fields)
    else:
        parser.print_help()
        print "Incorrect usage; see help above"
        sys.exit()

    # Save the information to disk
    with open(args.output, 'w') as f:
        f.write('%s\n' % '\t'.join(field for field in (['name'] + args.fields)))
        for line in file_info:
            f.write('%s\n' % '\t'.join(str(val) for val in line))
    print "Saved information for %s files" % len(file_info)
