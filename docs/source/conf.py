# coding: utf-8
import sys
import os

# insert the project's root dir first so apidoc can find the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

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

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True

# mathjax
mathjax_path = "mathjax/MathJax.js"  # relative to _static

# extend template
html_css_files = [
    "mystyle.css",
]

html_js_files = [
    "mathjaxConfig.js",
]
