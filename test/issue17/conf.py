import sys
import os
# viewcode extension specifically needed for this test
extensions = [
    'sphinxcontrib.bibtex',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc']
# make sure we find the module
sys.path.insert(0, os.path.abspath('.'))

source_suffix = '.rst'
exclude_patterns = ['_build']
latex_elements = {
}
texinfo_documents = [
    ('index', 'test', u'test Documentation',
     u'nobody', 'test', 'One line description of project.',
     'Miscellaneous'),
]
