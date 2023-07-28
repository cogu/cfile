"""
The cfile package
"""

from cfile.factory import CFactory
from cfile.writer import Writer
from cfile.style import StyleOptions, BreakBeforeBraces, Alignment

__all__ = ["CFactory",
           "Writer",
           "StyleOptions",
           "BreakBeforeBraces",
           "Alignment"
           ]
