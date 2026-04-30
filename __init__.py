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
from . import bootstrap
from importlib import metadata
import os

__author__ = "Neil Cook"
__email__ = 'neil.james.cook@gmail.com'
try:
    from ._version import version as __version__
except Exception:
    try:
        __version__ = metadata.version('pystilts')
    except metadata.PackageNotFoundError:
        __version__ = '0.1.0'
__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
__all__ = ['addcols', 'addcol',
           'delcol', 'delcols',
           'keepcol', 'keepcols',
           'renamecol', 'renamecols',
           'replacecol', 'replacecols',
           'tpipe', 'updatemeta',
           'tapskymatch', 'tmatch2',
           'clean', 'bootstrap_stilts',
           'select', 'seqview', 'setparam',
           'sort', 'tablename', 'tail', 'uniq']


# =============================================================================
# Pipeline functions
# =============================================================================
addcols = pipelines.addcols
addcol = pipelines.addcol
addresolve = pipelines.addresolve
addskycoords = pipelines.addskycoords
assert_ = pipelines.assert_
badval = pipelines.badval
cache = pipelines.cache
check = pipelines.check
# clearparams = pipelines.clearparams
colmeta = pipelines.colmeta
delcol = pipelines.delcols
delcols = pipelines.delcols
every = pipelines.every
# explodeall = pipelines.explodeall
# explodecols = pipelines.explodecols
fixcolnames = pipelines.fixcolnames
head = pipelines.head
keepcol = pipelines.keepcols
keepcols = pipelines.keepcols
# meta = pipelines.meta
progress = pipelines.progress
random = pipelines.random
randomview = pipelines.randomview
renamecol = pipelines.renamecol
renamecols = pipelines.renamecols
repeat = pipelines.repeat
replacecol = pipelines.replacecol
replacecols = pipelines.replacecols
replaceval = pipelines.replaceval
rowrange = pipelines.rowrange
select = pipelines.select
seqview = pipelines.seqview
setparam = pipelines.setparam
sort = pipelines.sort
# sorthead = pipelines.sorthead
# stats = pipelines.stats
# tablename = pipelines.tablename
tablename = pipelines.tablename
tail = pipelines.tail
# transpose = pipelines.transpose
uniq = pipelines.uniq
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
bootstrap_stilts = bootstrap.bootstrap_stilts
