#!/usr/bin/env python3
"""Derive the Debian version for the pinned tmux snapshot.

Produces 3.8~git<YYYYMMDD>.<shortsha>-0+welland1 from the pinned UPSTREAM_COMMIT
(date = commit date, so a re-pin to a newer commit re-versions deterministically).
This is independent of HEAD, so packaging commits layered on top do not change
the version.
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
# pinned upstream tmux commit (next-3.8); the version tracks THIS, not packaging HEAD
UPSTREAM_COMMIT = "5ed5e36"


def _git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def version():
    sha = _git("rev-parse", "--short=7", UPSTREAM_COMMIT)
    date = _git("log", "-1", "--format=%cd", "--date=format:%Y%m%d", UPSTREAM_COMMIT)
    return f"{BASE}~git{date}.{sha}-{REVISION}"


def write_changelog():
    date = _git("log", "-1", "--format=%cd", "--date=rfc2822", UPSTREAM_COMMIT)
    sha = _git("rev-parse", UPSTREAM_COMMIT)
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
