#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:24 PM

@author: neil

Program description here

Version 0.0.0
"""

from . import constants
from . import utils
from astropy import units as u


# =============================================================================
# Define variables
# =============================================================================
runcommand = utils.runcommand
command_arguments = utils.command_arguments
STILTS = constants.STILTS


# =============================================================================
# Define functions
# =============================================================================
def tapskymatch(**kwargs):
    # define command
    command = STILTS
    command += ' tapskymatch '

    # define allowed arguments (must be in allowed or special)
    # v = aliases for command call
    # r = will throw exception if not defined
    # d = sets default value (if r = False)
    keys = dict()
    keys['tapurl'] = dict(v=['tapurl'], r=True)
    keys['taptable'] = dict(v=['taptable'], r=True)
    keys['taplon'] = dict(v=['taplon'], r=True)
    keys['taplat'] = dict(v=['taplat'], r=True)
    keys['inlon'] = dict(v=['inlon'], r=True)
    keys['inlat'] = dict(v=['inlat'], r=True)
    keys['icmd'] = dict(v=['icmd'], r=False)
    keys['ocmd'] = dict(v=['ocmd'], r=False)
    keys['sr'] = dict(v=['radius', 'error', 'sr'], r=True, u=u.deg)
    keys['in'] = dict(v=['infile', 'in'], r=True)
    keys['out'] = dict(v=['outfile', 'out'], r=True)
    keys['fixcols'] = dict(v=['fixcols'], r=False, d='dups')
    keys['suffixin'] = dict(v=['suffixin'], r=False)
    keys['suffixremote'] = dict(v=['suffixremote'], r=False)
    # write the command
    commandargs = command_arguments(keys, kwargs, 'tapskymatch')
    for key in commandargs:
        command += commandargs[key]
    # print(command)
    # run command
    runcommand(command)


def tmatch2(**kwargs):
    # define command
    command = STILTS
    command += ' tmatch2 '
    # define allowed arguments (must be in allowed or special)
    # v = aliases for command call
    # r = will throw exception if not defined
    # d = sets default value (if r = False)
    keys = dict()
    keys['in1'] = dict(v=['in1'], r=True)
    keys['in2'] = dict(v=['in2'], r=True)
    keys['matcher'] = dict(v=['matcher'], r=False, d='sky')
    keys['values1'] = dict(v=['values1'], r=True)
    keys['values2'] = dict(v=['values2'], r=True)
    keys['join'] = dict(v=['join'], r=False, d='1and2')
    keys['icmd1'] = dict(v=['icmd1'], r=False)
    keys['icmd2'] = dict(v=['icmd2'], r=False)
    keys['ocmd'] = dict(v=['ocmd'], r=False)
    keys['params'] = dict(v=['radius'], r=True, u=u.arcsec)
    keys['out'] = dict(v=['outfile', 'out'], r=True)
    keys['fixcols'] = dict(v=['fixcols'], r=False, d='dups')
    keys['suffix1'] = dict(v=['suffix1'], r=False)
    keys['suffix2'] = dict(v=['suffix2'], r=False)
    # write the command
    commandargs = command_arguments(keys, kwargs, 'tmatch2')
    for key in commandargs:
        command += commandargs[key]
    # print(command)
    # run command
    runcommand(command)
