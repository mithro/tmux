#!/usr/bin/env python3
"""Derive the Debian version for the pinned tmux snapshot.

Produces 3.8~git<YYYYMMDD>.<shortsha>-0+welland1 from the current HEAD commit
(date = commit date, so a re-pin to a newer commit re-versions deterministically).
The ~git suffix sorts BELOW an official 3.8 and ABOVE 3.7b.
"""
import argparse
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANGELOG = REPO / "debian" / "changelog"
SOURCE = "tmux"
BASE = "3.8"            # the release this snapshot precedes
REVISION = "0+welland1"
MAINTAINER = "Tim 'mithro' Ansell <me@mith.ro>"


def _git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def version():
    sha = _git("rev-parse", "--short=7", "HEAD")
    date = _git("log", "-1", "--format=%cd", "--date=format:%Y%m%d")
    return f"{BASE}~git{date}.{sha}-{REVISION}"


def write_changelog():
    date = _git("log", "-1", "--format=%cd", "--date=rfc2822")
    sha = _git("rev-parse", "HEAD")
    CHANGELOG.write_text(
        f"{SOURCE} ({version()}) unstable; urgency=medium\n\n"
        f"  * Snapshot build of upstream tmux at {sha}\n"
        f"    (next-3.8; fixes the choose-tree blank-tree bug with grouped sessions).\n\n"
        f" -- {MAINTAINER}  {date}\n"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-changelog", action="store_true")
    a = ap.parse_args()
    (write_changelog if a.write_changelog else lambda: print(version()))()
