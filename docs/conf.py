"""Sphinx configuration for the open_dvm documentation.

Built with MyST-NB rather than Jupyter Book: since these docs are published
via ReadTheDocs (fundamentally a Sphinx-native build pipeline), MyST-NB --
the Sphinx extension Jupyter Book itself is built on -- gets the same
notebook-execution/rendering behavior without an extra build-system layer
on top.
"""

import open_dvm

project = "open_dvm"
copyright = "2026, Dirk van Moorselaar"
author = "Dirk van Moorselaar"
release = open_dvm.__version__
version = release

extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",  # parses numpy-style docstrings (used throughout open_dvm)
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- MyST / MyST-NB ----------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
# Notebooks are pre-executed by .github/workflows/docs-notebooks.yml (on a
# GitHub Actions runner, which has far more memory than RTD's build
# containers -- executing BDM/CTF decoding notebooks in-place on RTD OOMs
# the build) and committed into docs/tutorials/ with real output already
# embedded. RTD itself never executes anything, just renders what's there.
nb_execution_mode = "off"
# Notebook 01 (preprocessing) needs interactive ICA component selection and
# can't run headless -- it's intentionally not linked from any toctree here,
# see tutorials/index.md.

# -- autodoc / autosummary ----------------------------------------------
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}
autodoc_typehints = "description"
napoleon_numpy_docstring = True
napoleon_google_docstring = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "mne": ("https://mne.tools/stable/", None),
}

# -- HTML output ----------------------------------------------------------
html_theme = "sphinx_book_theme"
html_title = "open_dvm"
html_theme_options = {
    "repository_url": "https://github.com/dvanmoorselaar/open_dvm",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_download_button": True,
    "path_to_docs": "docs",
}
html_static_path = []
