#!/usr/bin/env python
#####################
#
# grid.py
#
# For use to upload to the grid with
# correct file naming
#
# These have a lot in common with the tools
# in the data-flow/lib folder.  A common
# (installable) set of libraries should be
# built.
#
# Author: David Auty
#         <auty@ualberta.ca>
#
#####################

import os
import sys
import re
import getpass
import subprocess

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
import urlparse

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
    
