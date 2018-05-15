# -*- coding: utf-8 -*-
# =============================================================================
# Switch-Else
# =============================================================================
class Switch:
    def __init__(self, value):
        self._val = value

    def __enter__(self):
        return self

    def __exit__(self, swt_type, value, traceback):  # Allows traceback to occur
        return False

    def __call__(self, *mconds):
        return self._val in mconds