"""
The cfile package
"""

from cfile.factory import CFactory
from cfile.writer import Writer
from cfile.style import StyleOptions, BreakBeforeBraces, Alignment, PPDirectiveIndent

__version__ = "0.5.0"

__all__ = ["__version__",
           "CFactory",
           "Writer",
           "StyleOptions",
           "BreakBeforeBraces",
           "Alignment",
           "PPDirectiveIndent",
           ]
