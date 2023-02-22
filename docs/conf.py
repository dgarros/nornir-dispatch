"""Sphinx configuration."""
project = "Nornir Dispatch"
author = "Damien Garros"
copyright = "2023, Damien Garros"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
