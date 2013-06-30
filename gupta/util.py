"""Utility functions for gupta event API

Functions (see docs for more details):
* millis: epoch time in milliseconds
"""

import contextlib
import sys

def millis(dt=None):
    """Return epoch time in milliseconds.

    Optionally takes a datetime parameter. Default is to return
    current epoch time in milliseconds.
    """
    if dt is None:
        dt = datetime.now()
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds() * 1000)

@contextlib.contextmanager
def nostderr():
    """Suppress output to stderr (useful in tests)"""
    savestderr = sys.stderr
    class Devnull(object):
        def write(self, _): pass
    sys.stderr = Devnull()
    yield
    sys.stderr = savestderr
