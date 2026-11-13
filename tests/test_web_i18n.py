"""web/index.html's translations: the page's text all comes from EN, every language has every
string of it, with the same HTML tags and {placeholders} as the English, and is listed in the
language menu."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

pytestmark = pytest.mark.nam   # upstream NAM A2 Lite: skipped unless -m names nam (conftest.py)

PAGE = (Path(__file__).resolve().parent.parent / "web/index.html").read_text()


class _Page(HTMLParser):
    """The body before the scripts: each data-i18n element's inner HTML, the data-i18n-label keys,
    and the text outside them (but inside no translate="no" element)."""
    VOID = {"input", "br", "meta", "link", "img", "source", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack, self.inner, self.labels, self.loose = [], {}, [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for e in self.stack:
            e[2].append(self.get_starttag_text())
        if "data-i18n-label" in a:
            self.labels.append(a["data-i18n-label"])
        if tag not in self.VOID:
            self.stack.append([tag, a.get("data-i18n"), [], a.get("translate") == "no"])

    def handle_endtag(self, tag):
        e = self.stack.pop()
        if e[1]:
            self.inner[e[1]] = "".join(e[2])
        for x in self.stack:
            x[2].append(f"</{tag}>")

    def handle_data(self, d):
        for e in self.stack:
            e[2].append(d)
        if not any(e[1] or e[3] for e in self.stack):
            self.loose.append(d)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")


def _page():
    p = _Page()
    body = PAGE.index("<body>")
    p.feed(PAGE[body:PAGE.index("<script", body)])
    return p


BODY = _page()
EN_TEXT = PAGE.split("// EN-BEGIN\nvar EN = ")[1].split(";\n// EN-END")[0]
EN = json.loads(EN_TEXT)
LANGS_TEXT = PAGE.split("// LANGS-BEGIN\nvar LANGS = ")[1].split(";\n// LANGS-END")[0]
LANGS = json.loads(LANGS_TEXT)
NAMES = re.findall(r"(\w+): \"", PAGE.split("var LANG_NAMES = {")[1].split("};")[0])


def tags(s):
    return sorted(re.findall(r"<[^>]+>", s))


def placeholders(s):
    return sorted(re.findall(r"\{\w+\}", s))


def test_translations_have_one_string_a_line():
    """So PRs editing different strings don't conflict: EN and LANGS as json.dumps(..., ensure_ascii=False, indent=2) writes them."""
    assert EN_TEXT == json.dumps(EN, ensure_ascii=False, indent=2), \
        "EN is not one string a line: rewrite it with json.dumps(EN, ensure_ascii=False, indent=2)"
    assert LANGS_TEXT == json.dumps(LANGS, ensure_ascii=False, indent=2), \
        "LANGS is not one string a line: rewrite it with json.dumps(LANGS, ensure_ascii=False, indent=2)"


def test_page_text_comes_from_en():
    """English lives in EN, not the HTML: each data-i18n element is empty and named in EN, and so is each data-i18n-label."""
    assert {k: v for k, v in BODY.inner.items() if v.strip()} == {}, "text in a data-i18n element: move it to EN"
    assert sorted(set(BODY.inner) - set(EN)) == [], "data-i18n keys missing from EN"
    assert sorted(set(BODY.labels) - set(EN)) == [], "data-i18n-label keys missing from EN"


def test_no_words_outside_translations():
    """Text outside data-i18n is only numbers and symbols, or names marked translate="no" (the HX Stomp's knob labels)."""
    words = [d.strip() for d in BODY.loose if re.search(r"[^\W\d_]", d)]
    assert words == [], "page text outside data-i18n: give it a key in EN"


def test_menu_lists_every_language():
    assert NAMES[0] == "en" and sorted(NAMES[1:]) == sorted(LANGS) and len(NAMES) == 10


@pytest.mark.parametrize("lang", sorted(LANGS))
def test_language_matches_english(lang):
    t = LANGS[lang]
    assert sorted(t) == sorted(EN), "missing or extra keys"
    assert [k for k in EN if tags(t[k]) != tags(EN[k])] == [], "HTML tags differ"
    assert [k for k in EN if placeholders(t[k]) != placeholders(EN[k])] == [], "placeholders differ"
    assert [k for k in EN if not t[k].strip()] == [], "empty strings"
