# fbrelation documentation build configuration file, created by
# sphinx-quickstart on Sat May 11 00:26:57 2013.

import sys, os

autodoc_member_order = 'bysource'
autodoc_default_flags = ['special-members', 'private-members']

def skip_member_handler(app, what, name, obj, skip, options):
    if 'special-members' in options:
        return name.startswith('__') and name.endswith('__') and name not in ('__init__', '__contains__', '__getitem__', '__str__')
    return False

def setup(app):
    app.connect('autodoc-skip-member', skip_member_handler)

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'fbrelation'
copyright = u'2013, Alex Forsythe'

version = ''
release = ''

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

add_module_names = False

pygments_style = 'sphinx'
html_theme = 'sphinxdoc'
html_theme_options = {}
html_static_path = []
html_domain_indices = False
html_use_index = False
htmlhelp_basename = 'fbrelationdoc'

latex_elements = {}
latex_documents = [
  ('index', 'rel.tex', u'fbrelation Documentation',
   u'Alex Forsythe', 'manual'),
]

man_pages = [
    ('index', 'fbrelation', u'fbrelation Documentation',
     [u'Alex Forsythe'], 1)
]

texinfo_documents = [
  ('index', 'fbrelation', u'fbrelation Documentation',
   u'Alex Forsythe', 'fbrelation', 'A simple declarative language for creating MotionBuilder relation constraints.',
   'Miscellaneous'),
]

epub_title = u'fbrelation'
epub_author = u'Alex Forsythe'
epub_publisher = u'Alex Forsythe'
epub_copyright = u'2013, Alex Forsythe'
