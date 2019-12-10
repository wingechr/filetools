# coding: utf-8


project = "filetools"
release = "0.0.6"
version = ".".join(release.split(".")[:2])
copyright = "2019, Christian Winger"
author = "Christian Winger"
language = "en"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon"
]

source_suffix = ".rst"
master_doc = "index"
templates_path = ["_templates"]
html_static_path = ["_static"]
pygments_style = None
html_theme = "alabaster"
html_theme_options = {}
html_sidebars = {}
htmlhelp_basename = "filetoolsdoc"
todo_include_todos = True
