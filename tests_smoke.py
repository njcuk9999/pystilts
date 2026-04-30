#!/usr/bin/env python3
"""Simple compatibility smoke checks for command string generation."""

import importlib
import pathlib
import sys


def main():
    repo_parent = pathlib.Path(__file__).resolve().parent.parent
    if str(repo_parent) not in sys.path:
        sys.path.insert(0, str(repo_parent))

    pystilts = importlib.import_module("pystilts")

    cmd = pystilts.addcol("flux2", "flux*2")
    assert cmd.startswith("addcol"), cmd

    keep = pystilts.keepcols(["ra", "dec"])
    assert "keepcols" in keep, keep

    assert pystilts.pipelines.every(2) == "every 2"
    assert pystilts.pipelines.fixcolnames() == "fixcolnames"
    assert pystilts.select("ra > 0").startswith("select ")
    assert pystilts.seqview() == "seqview"
    assert pystilts.setparam("AUTHOR", "Neil").startswith("setparam ")
    assert pystilts.sort(["ra", "dec"], descending=True).startswith("sort -down ")
    assert pystilts.tablename("MyTable").startswith("tablename ")
    assert pystilts.tail(10) == "tail 10"
    assert pystilts.uniq(["ra", "dec"], count=True).startswith("uniq -count ")

    # Ensure crossmatch API aliases still accept historical kwargs.
    command_arguments = importlib.import_module("pystilts.utils").command_arguments
    from astropy import units as u

    keys = {
        "params": dict(v=["radius", "params"], r=False, u=u.arcsec),
    }
    args = command_arguments(keys, {"radius": 1.5}, "tmatch2")
    assert "params" in args

    print("pystilts smoke checks passed")


if __name__ == "__main__":
    main()



