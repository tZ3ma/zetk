"""Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
 -- Path setup --------------------------------------------------------------
If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))
"""
import typing

# from zettelkasten import __version__
# -- Project information -----------------------------------------------------

project = "zettelkasten"
copyright = "2021, tZE"
author = "tZE"

# # The full version, including alpha/beta/rc tags
# release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",  # enable docstring documentation
    "sphinx.ext.napoleon",  # enable numpy style docstring syntax
    "sphinx.ext.intersphinx",  # allow :mod: references to interlinked docs
    "sphinx.ext.viewcode",  # enable source links
    "sphinx.ext.autosummary",  # create linked tables for documented attributes
    "sphinx_paramlinks",  # enable :paramref: cross referencing
    "sphinx_click",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: typing.List[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"
# html_theme = "furo"
html_theme = "sphinx_rtd_theme"

# html_theme_options = {
#     # "canonical_url": "https://www.pypsa.org/doc",
#     # "display_version": True,
#     # "sticky_navigation": True,
#     # "style_nav_header_background": "#009682",
# }
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
