#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02/06/17 at 2:20 PM

@author: neil

Program description here

Version 0.0.0
"""

from . import crossmatching
from . import pipelines
from . import utils
import os

__author__ = "Neil Cook"
__email__ = 'neil.james.cook@gmail.com'
__version__ = '0.1'
__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
__all__ = ['addcols', 'addcol',
           'delcol', 'delcols',
           'keepcol', 'keepcols',
           'renamecol', 'renamecols',
           'replacecol', 'replacecols',
           'tpipe', 'updatemeta',
           'tapskymatch', 'tmatch2',
           'clean']


# =============================================================================
# Pipeline functions
# =============================================================================
# Add columns
addcols = pipelines.addcols
addcol = pipelines.addcol
# Delete columns
delcol = pipelines.delcols
delcols = pipelines.delcols
# Keep columns
keepcol = pipelines.keepcols
keepcols = pipelines.keepcols
# Rename columns
renamecol = pipelines.renamecol
renamecols = pipelines.renamecols
# Replace columns
replacecol = pipelines.replacecol
replacecols = pipelines.replacecols
#tpipe
tpipe = pipelines.tpipe
# Update column meta data
updatemeta = pipelines.updatemetadata

# =============================================================================
# Crossmatching functions
# =============================================================================
tapskymatch = crossmatching.tapskymatch
tmatch2 = crossmatching.tmatch2


# =============================================================================
# Utility functions
# =============================================================================
clean = utils.clean_file