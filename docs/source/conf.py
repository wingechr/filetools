# coding: utf-8
import sys
import os
import sphinx_rtd_theme

# insert the project's root dir first so apidoc can find the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__name__), "..", "..")))


project = "filetools"
release = "0.0.6"
version = ".".join(release.split(".")[:2])
copyright = "2019, Christian Winger"
author = "Christian Winger"
language = "en"
html_search_language = language

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme = "sphinx_rtd_theme"  # classic | bootstrap | alabaster | sphinx_rtd_theme
source_suffix = ".rst"
master_doc = "index"
templates_path = ["_templates"]
html_static_path = ["_static"]
pygments_style = "sphinx"
html_theme_options = {}
html_sidebars = {}
htmlhelp_basename = "filetoolsdoc"
todo_include_todos = True
source_encoding = "utf-8"
add_module_names = False
show_authors = True
nitpicky = False
html_use_index = True
add_function_parentheses = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
