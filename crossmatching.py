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
    # run command
    runcommand(command)




def tmatch2(**kwargs):
    """
    keywords are:
    
    in1         string, The location of the first input table. This may take 
                one of the following forms: 
                
                - A filename.
                - A URL.
    
    in2         string, The location of the second input table. This may take 
                one of the following forms: 
                
                - A filename.
                - A URL.
                           
    matcher     string, Defines the nature of the matching that will be 
                performed. Depending on the name supplied, this may be 
                positional matching using celestial or Cartesian coordinates, 
                exact matching on the value of a string column, or other things.
                 
                must be one of the following:
                
                - sky: The sky matcher compares positions on the celestial 
                       sphere with a fixed error radius. Rows are considered 
                       to match when the two (ra, dec) positions are within 
                       max-error arcseconds of each other along a great circle. 

                    values: 
                        ra/degrees: Right Ascension 
                        dec/degrees: Declination
                    params:
                        max-error/arcsec: Maximum separation along a great circle

                - skyerr
                - skyellipse
                - sky3d
                - exact
                - 1d, 2d, ...
                - 2d_anisotropic, ...
                - 2d_cuboid, ...
                - 1d_err, 2d_err, ...
                - 2d_ellipse
                
                this changes the values that need to be set
                
    values1     string, Defines the values from table 1 which are used to 
                determine whether a match has occurred. These will typically 
                be coordinate values such as RA and Dec and perhaps some 
                per-row error values as well, though exactly what values are 
                required is determined by the kind of match as determined by 
                matcher.
                
    value2      string, Defines the values from table 2 which are used to 
                determine whether a match has occurred. These will typically 
                be coordinate values such as RA and Dec and perhaps some 
                per-row error values as well, though exactly what values are 
                required is determined by the kind of match as determined by 
                matcher.
                
    join        string, Determines which rows are included in the output table. 
                The matching algorithm determines which of the rows from the 
                first table correspond to which rows from the second. 
                This parameter determines what to do with that information. 
                Perhaps the most obvious thing is to write out a table 
                containing only rows which correspond to a row in both of the 
                two input tables. However, you may also want to see the 
                unmatched rows from one or both input tables, or rows present 
                in one table but unmatched in the other, or other possibilities.
                The options are:

                    1and2: An output row for each row represented in both input 
                            tables (INNER JOIN)
                    
                    1or2: An output row for each row represented in either or 
                            both of the input tables (FULL OUTER JOIN)
                    
                    all1: An output row for each matched or unmatched row in 
                            table 1 (LEFT OUTER JOIN)
                    
                    all2: An output row for each matched or unmatched row in 
                            table 2 (RIGHT OUTER JOIN)
                    
                    1not2: An output row only for rows which appear in the 
                            first table but are not matched in the second table
                    
                    2not1: An output row only for rows which appear in the 
                            second table but are not matched in the first table
                    
                    1xor2: An output row only for rows represented in one of 
                            the input tables but not the other one

    icmd1
    icmd2
    ocmd
    params      string, Fixed value(s) giving the parameters of the match 
                (typically an error radius). If more than one value is required, 
                the values should be separated by spaces. 
    out
    fixcols
    suffix1
    suffix2
    
    :param kwargs: 
    :return: 
    """
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
    keys['params'] = dict(v=['radius', 'params'], r=False, u=u.arcsec)
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
