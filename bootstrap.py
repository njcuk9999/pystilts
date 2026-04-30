#!/usr/bin/env python3
"""Helpers to download and configure a local STILTS/TOPCAT runtime."""

import argparse
import os
from pathlib import Path
from urllib.request import urlopen


TOPCAT_FULL_URL = "https://www.star.bristol.ac.uk/~mbt/topcat/topcat-full.jar"
STILTS_URL = "https://www.star.bristol.ac.uk/~mbt/stilts/stilts.jar"


def _default_data_dir():
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "pystilts"
    return Path.home() / ".local" / "share" / "pystilts"


def download_jar(url=TOPCAT_FULL_URL, destination=None, force=False):
    target = Path(destination) if destination else _default_data_dir()
    if target.suffix.lower() != ".jar":
        target.mkdir(parents=True, exist_ok=True)
        filename = Path(url).name or "topcat-full.jar"
        target = target / filename
    else:
        target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not force:
        return target

    with urlopen(url) as response:
        content = response.read()
    target.write_bytes(content)
    return target


def _config_path():
    return Path(__file__).resolve().parent / "config.txt"


def configure_stilts_cmd(jar_path=None, command=None):
    if command is None:
        if jar_path is None:
            raise ValueError("jar_path or command must be set")
        command = "java -jar {0} -stilts".format(Path(jar_path).resolve())

    path = _config_path()
    existing_lines = []
    if path.exists():
        existing_lines = path.read_text(encoding="utf-8").splitlines()

    out_lines = []
    found_stilts = False
    for line in existing_lines:
        stripped = line.strip()
        if stripped.startswith("STILTS_CMD") and "=" in line:
            out_lines.append("STILTS_CMD = {0}".format(command))
            found_stilts = True
        else:
            out_lines.append(line)

    if not found_stilts:
        if out_lines and out_lines[-1] != "":
            out_lines.append("")
        out_lines.append("# Define the STILTS command to use")
        out_lines.append("STILTS_CMD = {0}".format(command))

    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return command


def bootstrap_stilts(use="topcat", destination=None, force=False, configure=True):
    if use not in {"topcat", "stilts"}:
        raise ValueError("use must be one of: topcat, stilts")

    url = TOPCAT_FULL_URL if use == "topcat" else STILTS_URL
    jar_path = download_jar(url=url, destination=destination, force=force)

    if not configure:
        return jar_path

    if use == "topcat":
        command = "java -jar {0} -stilts".format(jar_path.resolve())
    else:
        command = "java -jar {0}".format(jar_path.resolve())
    configure_stilts_cmd(command=command)
    return jar_path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Download and configure STILTS/TOPCAT for pystilts")
    parser.add_argument("--use", choices=["topcat", "stilts"], default="topcat",
                        help="Select which jar to download (default: topcat)")
    parser.add_argument("--destination", default=None,
                        help="Destination directory or full .jar path")
    parser.add_argument("--force", action="store_true",
                        help="Redownload even if destination already exists")
    parser.add_argument("--no-config", action="store_true",
                        help="Do not modify config.txt after downloading")
    args = parser.parse_args(argv)

    jar = bootstrap_stilts(use=args.use,
                           destination=args.destination,
                           force=args.force,
                           configure=not args.no_config)
    print("Downloaded:", jar)


if __name__ == "__main__":
    main()

