# pystilts
Native python wrapper of topcat/stilts ([http://www.star.bris.ac.uk/~mbt/stilts/](http://www.star.bris.ac.uk/~mbt/stilts/))

## 1. Installation

### 1.1 Setup

Make sure pystilts folder is on python path

* with bash
    ```
    export PYTHONPATH = "~/bin/python-scripts/"
    ```
    Or 
    ```
    export PYTHONPATH = "${PATH}:~/bin/python-scripts/"
    ```
* with tcsh
 
    ```
    setenv PYTHONPATH ~/bin/python-scripts/
    ```
    Or 
    ```
    setenv PYTHONPATH ${PATH}:~/bin/python-scripts/
    ```

where pystilts folder is in the directory
```
~/bin/python-scripts/
```
### 1.2 Setting up the config file

You MUST set up the config file to point to STILTS

i.e. the line that reads:

```commandline
# Define the STILTS command to use
STILTS_CMD = java -jar /home/neil/bin/topcat/topcat-full.jar -stilts
```
must link to your topcat jar

If you do not have topcat get it from here: [http://www.star.bristol.ac.uk/~mbt/topcat/#install](http://www.star.bristol.ac.uk/~mbt/topcat/#install)

If you are able to run STILTS from the command line you are able to run this python module. (Note the STILTS command for windows/mac may not be the same form as above).

## 2. Documentation

This python module follows all documentation from [http://www.star.bristol.ac.uk/~mbt/stilts/sun256/sun256.html#MatchEngine](http://www.star.bristol.ac.uk/~mbt/stilts/sun256/sun256.html#MatchEngine).
All variables and function forms should be close to that describied in the link above.

Currently supported functions are:

* Table Pipelines (used via tpipe)
    * addcols (custom command - loop around addcol)
    * addcol
    * addresolve
    * addskycoords
    * assert_  (custom command - assert in STILTS)
    * badval
    * cache
    * check
    * colmeta
    * delcol
    * delcols (custom command - delcol in STILTS)
    * every
    * fixcolnames
    * head
    * keepcol
    * keepcols (custom command - loop around keepcol)
    * progress
    * random
    * randomview
    * renamecol 
    * renamecols (custom command - loop around renamecol)
    * repeat 
    * replacecol
    * replacecols(custom command - loop around replacecol)
    * replaceval
    * rowrange
    * updatemeta (custom command - custom form of meta function in STILTS)

* Commands
    * tapskymatch
    * tmatch2
    * tpipe

* Other
    * clean (runs a suit of cleaning commands from STILTS)

## 3. Examples

##### Combine two files on a 1 arcsec cross-match in RA and DEC columns
* 'table1.fits' and 'table2.fits' must have columns 'ra' and 'dec'

```python

import pystilts

filename1 = 'table1.fits'
filename2 = 'table2.fits'
filename3 = 'table3.fits'

pystilts.tmatch2(in1=filename1, in2=filename2, out=filename3,
                 matcher='sky', values1='ra dec', values2='ra dec',
                 join='1and2', radius='1')
```

##### Crossmatching with an online table via TAP

* 'table1.fits' must have columns 'ra' and 'dec'
* Here we crossmatch with PPMXL (Roeser et al. 2011), keep only the 'ra' and 'dec' columns from 'table1.fits', name all columns from ppmxl with a suffix of '_ppmxl' and then rename table1.fits 'ra' and 'dec' columns to 'ra_table1', 'dec_table1'

```python
from pystilts import tapskymatch
from pystilts import keepcols, renamecols

filename = 'table1.fits'
outfile = 'table2.fits'
name = 'ppmxl'
tapurl = "http://dc.zah.uni-heidelberg.de/tap"
taptable = "ppmxl.main"
taplong = 'raj2000'
taplat = 'dej2000'
crossmatch = 3
nra1, ndec1 = 'ra', 'dec'
nra2, ndec2 = 'ra_table1', 'dec_table1'
# Run sky match via TAP
tapskymatch(tapurl=tapurl, taptable=taptable,
            taplon=taplong, taplat=taplat,
            infile=filename, inlon=nra1, inlat=ndec1,
            radius=crossmatch, outfile=outfile,
            icmd=keepcols([nra1, ndec1]), fixcols='all', suffixin='',
            suffixremote='_{0}'.format(name))
# Rename table1.fits ra and dec columns
renamecols(outfile, [nra1, ndec1], [nra2, ndec2])
```