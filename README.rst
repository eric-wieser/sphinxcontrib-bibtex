sphinxcontrib-bibtex
====================

|ci| |codecov| |version| |license|

Sphinx extension for BibTeX style citations.

Overview
--------

The bibtex extension allows `BibTeX <http://www.bibtex.org/>`_
citations to be inserted into documentation generated by
`Sphinx <https://www.sphinx-doc.org/en/master/>`_, via
a ``bibliography`` directive,
along with ``:cite:p:`` and ``:cite:t:`` roles.
These work similarly to LaTeX's ``thebibliography`` environment
and the ``\citet`` and ``\citep`` commands.

For formatting, the extension relies on
`pybtex <https://pybtex.org/>`_
written by Andrey Golovizin.
The extension is inspired by Matthew Brett's
`bibstuff.sphinxext.bibref <https://github.com/matthew-brett/bibstuff>`_
and Weston Nielson's
`sphinx-natbib <https://github.com/mcmtroffaes/sphinxcontrib-bibtex/blob/develop/test/natbib.py>`_.

* Download: https://pypi.org/project/sphinxcontrib-bibtex/#files

* Documentation: https://sphinxcontrib-bibtex.readthedocs.io/en/latest/

* Development: https://github.com/mcmtroffaes/sphinxcontrib-bibtex/

.. |ci| image:: https://github.com/mcmtroffaes/sphinxcontrib-bibtex/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/mcmtroffaes/sphinxcontrib-bibtex/actions/workflows/python-package.yml
    :alt: ci

.. |codecov| image:: https://codecov.io/gh/mcmtroffaes/sphinxcontrib-bibtex/branch/develop/graph/badge.svg
    :target: https://app.codecov.io/gh/mcmtroffaes/sphinxcontrib-bibtex
    :alt: codecov

.. |version| image:: https://img.shields.io/pypi/v/sphinxcontrib-bibtex.svg
    :target: https://pypi.org/project/sphinxcontrib-bibtex/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/sphinxcontrib-bibtex.svg
    :target: https://pypi.org/project/sphinxcontrib-bibtex/
    :alt: license

Installation
------------

Install the module with ``pip install sphinxcontrib-bibtex``, or from
source using ``pip install -e .``. Then add:

.. code-block:: python

   extensions = ['sphinxcontrib.bibtex']
   bibtex_bibfiles = ['refs.bib']

to your project's Sphinx configuration file ``conf.py``.

Installation with ``python setup.py install`` is discouraged due to potential
issues with the sphinxcontrib namespace.

Minimal Example
---------------

In your project's documentation, you can use
``:cite:t:`` for textual citation references,
``:cite:p:`` for parenthetical citation references,
and ``.. bibliography::`` for inserting the bibliography.
For `example <https://github.com/mcmtroffaes/sphinxcontrib-bibtex/tree/develop/test/roots/test-debug_minimal_example>`_:

.. code-block:: rest

   See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
   Non-standard analysis is fun :cite:p:`1987:nelson`.

   .. bibliography::

where ``refs.bib`` would contain an entry::

   @Book{1987:nelson,
     author = {Edward Nelson},
     title = {Radically Elementary Probability Theory},
     publisher = {Princeton University Press},
     year = {1987}
   }

In the default style, this will get rendered as:

See Nelson [Nel87a]_ for an introduction to non-standard analysis.
Non-standard analysis is fun [Nel87a]_.

.. [Nel87a] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.

Citations in sphinx are resolved globally across all documents.
Typically, you have a single ``bibliography`` directive across
your entire project which collects all citations.
Advanced use cases with multiple ``bibliography`` directives
across your project are also supported, but some care
needs to be taken from your end to avoid duplicate citations.

In contrast, footnotes in sphinx are resolved locally per document.
To achieve local bibliographies per document, you can use citations
represented by footnotes as follows:

.. code-block:: rest

   See :footcite:t:`1987:nelson` for an introduction to non-standard analysis.
   Non-standard analysis is fun :footcite:p:`1987:nelson`.

   .. footbibliography::

which will get rendered as:

See Nelson [#Nel87b]_ for an introduction to non-standard analysis.
Non-standard analysis is fun [#Nel87b]_.

.. [#Nel87b] Edward Nelson. *Radically Elementary Probability Theory*. Princeton University Press, 1987.

Typically, you have a single ``footbibliography`` directive
at the bottom of each document that has footnote citations.
Advanced use cases with multiple ``footbibliography`` directives
per document are also supported. Since everything is local,
there is no concern with duplicate citations when using footnotes.
