# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from typing import Any, Dict

# Add source directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cfile  # noqa: E402

# -- Project information -----------------------------------------------------

project = 'cfile'
copyright = '2026, Conny Gustafsson'
author = 'Conny Gustafsson'
release = f'v{cfile.__version__}'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.mermaid',
    'myst_parser',
]

# Autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# Napoleon settings (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

exclude_patterns = [
    '_build',
    '.venv',
    'README.md',
    'requirements*.txt',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'
html_title = f"{project} {release} documentation"

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

html_js_files: list[str] = []
html_context: Dict[str, Any] = {}
