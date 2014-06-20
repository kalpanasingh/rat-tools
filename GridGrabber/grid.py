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
import getpass
import subprocess


def check_environment():
    '''Ensure grid environment variables are set
    '''
    global _env
    for check in _checks:
        if check not in os.environ:
            print "WARNING: %s not set in shell environment (to: %s)" % (check, _checks[check])
            _env[check] = _checks[check]


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


def execute_command(command, args, inputs=[], env=None, cwd=None):
    '''Command execution
    '''
    shellCommand = [command] + args
    useEnv = os.environ # Default to current environment
    if env is not None:
        for key in env:
            useEnv[key] = env[key]
    if cwd is None:
        cwd = os.getcwd()
    for i, arg in enumerate(args):
        if type(arg) is unicode:
            args[i] = ucToStr(arg)
    process = subprocess.Popen(args = shellCommand, env = useEnv, cwd = cwd,
                               stdout = subprocess.PIPE, stderr = subprocess.PIPE,
                               stdin = subprocess.PIPE, shell = False)
    for i in inputs:
        process.stdin.write(i)
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


def proxy_create():
    '''Create a snoplus proxy
    '''
    command = 'voms-proxy-init'
    args = ['--voms', 'snoplus.snolab.ca']
    pswd = getpass.getpass("Grid password: ")
    inputs = [pswd + "\n"] # Need return char?
    rtc, out, err = execute_command(command, args, inputs)
    return rtc


##############################################################
# Data management commands

def copy(url, local, timeout=None):
    '''Copy a file listed at a LFN/SURL to a local filename/path.

    URL can also be a guid (requires correct format)
    Timeout is the time for the FULL transfer (lcg-cp defaults to 3600)
    '''
    if timeout is None:
        rtc, out, err = execute('lcg-cp', url, local)
    else:
        rtc, out, err = execute('lcg-cp', '--sendreceive-timeout', str(timeout), url, local)
    if rtc:
        raise Exception('Unable to copy %s to %s\nError: %s'%(url, local, err))

def list_reps(guid):
    """Get the SURLS of a file.
    """
    rtc, out, err = execute("lcg-lr", guid)
    if rtc:
        raise Exception('Cannot find replicas for %s' % (guid))
    return out


# Check environment variables
_env = {}
_checks = {"LFC_HOST": "lfc.gridpp.rl.ac.uk",
           "LCG_GFAL_INFOSYS": "lcgbdii.gridpp.rl.ac.uk:2170"}
check_environment()
