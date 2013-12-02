#!/usr/bin/env python
#####################
#
# grid.py
#
# Some basic functions for interaction
# with grid tools.
#
# These have a lot in common with the tools
# in the data-flow/lib folder.  A common
# (installable) set of libraries should be
# built.
#
# Author: Matt Mottram
#         <m.mottram@sussex.ac.uk>
#
#####################

import os
import sys
import re
import subprocess


def execute(command, *args):
    '''Simple command execution.
    '''
    cmdArgs = []
    for arg in args:
        if type(arg) == list:
            cmdArgs += arg
        else:
            cmdArgs += [arg]
    rtc, out, err = execute_command(command, cmdArgs)
    return rtc, out, err


def execute_command(command, args, env=None, cwd=None, verbose=False, debug=False):
    '''Command execution
    '''
    shellCommand = [command] + args
    if verbose:
        print shellCommand
    useEnv = os.environ # Default to current environment
    if env is not None:
        for key in env:
            useEnv[key] = env[key]
    if cwd is None:
        cwd = os.getcwd()
    for i, arg in enumerate(args):
        if type(arg) is unicode:
            args[i] = ucToStr(arg)
    if debug:
        print 'cmd', shellCommand
        print 'cwd', cwd
        print 'ls', os.listdir(cwd)
        print 'env', useEnv
    process = subprocess.Popen(args = shellCommand, env = useEnv, cwd = cwd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    output = ""
    error = ""
    if verbose:
        for line in iter(process.stdout.readline, ""):
            sys.stdout.write('\n' + line[:-1])
            sys.stdout.flush()
            output += '\n' + line[:-1]
        process.wait()
    else:
        output, error = process.communicate()
    output = output.split('\n')#want lists
    error = error.split('\n')#will always have a '' as last element, unless :
    if output[len(output)-1] == '':
        del output[-1]
    if error[len(error)-1] == '':
        del error[-1]
    return process.returncode, output, error #don't always fail on returncode!=0

##############################################################
# Certificate commands

def proxy_check(*args):
    '''Check a proxy with whatever args.
    '''
    command = 'voms-proxy-info'
    rtc, out, err = execute(command, *args)
    return rtc, out, err


def proxy_time():
    '''Check the lifetime of a proxy
    '''
    rtc, out, err = proxy_check('-timeleft')
    tleft = 0
    if not rtc:
        tleft = int(out[0])
    return tleft


def proxy_roles():
    '''Check the role attribute of a proxy.
    '''
    rtc, out, err = proxy_check('-fqan')
    roles = []
    if rtc:
        #attr will be something like:
        #/snoplus.snolab.ca/Role=NULL/Capability=NULL
        pattern = re.compile(r'''[/](?P<vo>\S*)[/](?P<r>\S*)[=](?P<role>\S*)[/](?P<c>\S*)[=](?P<cap>\S*)''')
        for line in out:
            search = pattern.search(line)
            roles += [search.group('role')]
    return roles

##############################################################
# Data management commands

def copy(url, local, timeout=None):
    '''Copy a file listed at a LFN/SURL to a local filename/path
    '''
    if timeout is None:
        rtc, out, err = execute('lcg-cp', url, local)
    else:
        rtc, out, err = execute('lcg-cp', '--sendreceive-timeout', str(timeout), url, local)
    if rtc:
        raise Exception('Unable to copy %s to %s'%(url, local))

def list_reps(guid):
    """Get the SURLS of a file.
    """
    rtc, out, err = execute("lcg-lr", guid)
    if rtc:
        raise Exception('Cannot find replicas for %s' % (guid))
    return out
