# pystilts
Native python wrapper of topcat/stilts ([http://www.star.bris.ac.uk/~mbt/stilts/](http://www.star.bris.ac.uk/~mbt/stilts/))

## 1. Installation

### 1.1 Install with pip (editable)

From the project root:

```bash
python -m pip install -U -e .
```

No `PYTHONPATH` edits are required.

### 1.2 Java/STILTS requirement

`pystilts` wraps STILTS commands, so Java + a STILTS-capable jar is still required.

You can now bootstrap this automatically:

```bash
pystilts-bootstrap
```

This downloads `topcat-full.jar` to `~/.local/share/pystilts/` (or `$XDG_DATA_HOME/pystilts/`) and updates `config.txt` with a working `STILTS_CMD`.

Alternative: download standalone STILTS jar instead:

```bash
pystilts-bootstrap --use stilts
```

You can override at runtime without editing files:

```bash
export PYSTILTS_STILTS_CMD="java -jar /path/to/topcat-full.jar -stilts"
```

If you already have STILTS on `PATH`, point `STILTS_CMD` in `config.txt` to your preferred command.

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
    * select
    * seqview
    * setparam
    * sort
    * tablename
    * tail
    * uniq
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