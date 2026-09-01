#!/usr/bin/env python3
"""Shim: the loop-line lint lives with the skill (skills/loopify/scripts/loop_line_lint.py) so an
installed copy of the skill carries it. This path is kept for the documented command
`python3 evals/loop_line_lint.py "<line>"` and for tests/test_manifests.py."""
import os
import runpy
import sys

_TARGET = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "skills", "loopify", "scripts", "loop_line_lint.py")
sys.path.insert(0, os.path.dirname(_TARGET))
from loop_line_lint import lint_loop_line, MAX_CHARS, DAILY_PHRASES  # noqa: E402,F401

if __name__ == "__main__":
    sys.argv[0] = _TARGET
    runpy.run_path(_TARGET, run_name="__main__")
