import common
import dataclasses
import pytest
import re
import sphinxcontrib.bibtex.plugin

from sphinxcontrib.bibtex.domain import BibtexDomain
from typing import cast

from sphinxcontrib.bibtex.style.referencing import \
    BracketStyle, PersonStyle
from sphinxcontrib.bibtex.style.referencing.author_year import \
    AuthorYearReferenceStyle


@pytest.mark.sphinx('html', testroot='citation_not_found')
def test_citation_not_found(app, warning):
    app.build()
    assert 'could not find bibtex key "nosuchkey1"' in warning.getvalue()
    assert 'could not find bibtex key "nosuchkey2"' in warning.getvalue()


# test mixing of ``:cite:`` and ``[]_`` (issue 2)
@pytest.mark.sphinx('html', testroot='citation_mixed')
def test_citation_mixed(app, warning):
    app.build()
    assert not warning.getvalue()
    domain = cast(BibtexDomain, app.env.get_domain('cite'))
    assert len(domain.citation_refs) == 1
    citation_ref = domain.citation_refs.pop()
    assert citation_ref.keys == ['Test']
    assert citation_ref.docname == 'adoc1'
    assert len(domain.citations) == 1
    citation = domain.citations.pop()
    assert citation.formatted_entry.label == '1'


@pytest.mark.sphinx('html', testroot='citation_multiple_keys')
def test_citation_multiple_keys(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    cits = {match.group('label')
            for match in common.html_citations().finditer(output)}
    citrefs = {match.group('label')
               for match in common.html_citation_refs().finditer(output)}
    assert {"App", "Bra"} == cits == citrefs


# see issue 85
@pytest.mark.sphinx('html', testroot='citation_no_author_no_key')
def test_citation_no_author_no_key(app, warning):
    app.build()
    assert not warning.getvalue()


# test cites spanning multiple lines (issue 205)
@pytest.mark.sphinx('html', testroot='citation_whitespace')
def test_citation_whitespace(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.html").read_text()
    # ensure Man09 is cited
    assert len(common.html_citation_refs(label='Fir').findall(output)) == 1
    assert len(common.html_citation_refs(label='Sec').findall(output)) == 1


# test document not in toctree (issue 228)
@pytest.mark.sphinx('pseudoxml', testroot='citation_from_orphan')
def test_citation_from_orphan(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('html', testroot='citation_roles')
def test_citation_roles_label(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx(
    'html', testroot='citation_roles',
    confoverrides={'bibtex_reference_style': 'author_year'})
def test_citation_roles_authoryear(app, warning):
    app.build()
    assert not warning.getvalue()


@pytest.mark.sphinx('pseudoxml', testroot='debug_bibtex_citation',
                    confoverrides={'bibtex_reference_style': 'non_existing'})
def test_citation_style_invalid(make_app, app_params):
    args, kwargs = app_params
    with pytest.raises(ImportError, match='plugin .*non_existing not found'):
        make_app(*args, **kwargs)


@dataclasses.dataclass
class CustomReferenceStyle(AuthorYearReferenceStyle):
    bracket: BracketStyle = BracketStyle(
        left='(',
        right=')',
        sep='; ',
        sep2='; ',
        last_sep='; ',
    )
    person: PersonStyle = PersonStyle(
        style='last',
        abbreviate=False,
        sep=' & ',
        sep2=None,
        last_sep=None,
        other=' et al',
    )
    author_year_sep = ', '


sphinxcontrib.bibtex.plugin.register_plugin(
    'sphinxcontrib.bibtex.style.referencing',
    'xxx_custom_xxx', CustomReferenceStyle)


@pytest.mark.sphinx('text', testroot='citation_roles',
                    confoverrides={
                        'bibtex_reference_style': 'xxx_custom_xxx'})
def test_citation_style_custom(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    tests = [
        ("p",           " (de Du et al, 2003) "),
        ("ps",          " (de Du & Em & Fa, 2003) "),
        ("t",           " de Du et al (2003) "),
        ("ts",          " de Du & Em & Fa (2003) "),
        ("ct",          " De Du et al (2003) "),
        ("cts",         " De Du & Em & Fa (2003) "),
        ("labelpar",    " (dDEF03) "),
        ("label",       " dDEF03 "),
        ("yearpar",     " (2003) "),
        ("year",        " 2003 "),
        ("authorpar",   " (de Du et al) "),
        ("authorpars",  " (de Du & Em & Fa) "),
        ("cauthorpar",  " (De Du et al) "),
        ("cauthorpars", " (De Du & Em & Fa) "),
        ("author",      " de Du et al "),
        ("authors",     " de Du & Em & Fa "),
        ("cauthor",     " De Du et al "),
        ("cauthors",    " De Du & Em & Fa "),
        ("p",           " (al Ap, 2001; Be & Ci, 2002) "),
        ("ps",          " (al Ap, 2001; Be & Ci, 2002) "),
        ("t",           " al Ap (2001); Be & Ci (2002) "),
        ("ts",          " al Ap (2001); Be & Ci (2002) "),
        ("ct",          " Al Ap (2001); Be & Ci (2002) "),
        ("cts",         " Al Ap (2001); Be & Ci (2002) "),
        ("labelpar",    " (aA01; BC02) "),
        ("label",       " aA01; BC02 "),
        ("yearpar",     " (2001; 2002) "),
        ("year",        " 2001; 2002 "),
        ("authorpar",   " (al Ap; Be & Ci) "),
        ("authorpars",  " (al Ap; Be & Ci) "),
        ("cauthorpar",  " (Al Ap; Be & Ci) "),
        ("cauthorpars", " (Al Ap; Be & Ci) "),
        ("author",      " al Ap; Be & Ci "),
        ("authors",     " al Ap; Be & Ci "),
        ("cauthor",     " Al Ap; Be & Ci "),
        ("cauthors",    " Al Ap; Be & Ci "),
    ]
    for role, text in tests:
        escaped_text = re.escape(text)
        pattern = f'":cite:{role}:".*{escaped_text}'
        assert re.search(pattern, output) is not None


@pytest.mark.sphinx('text', testroot='citation_style_round_brackets')
def test_citation_style_round_brackets(app, warning):
    app.build()
    assert not warning.getvalue()
    output = (app.outdir / "index.txt").read_text()
    assert "(Evensen, 2003)" in output
    assert "Evensen (2003)" in output
