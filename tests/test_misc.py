import pytest

import sympy as sp

from gkjh.misc import subs


def test_subs_basic():
    a, b, c, d = sp.symbols("a, b, c, d")

    vals = {}
    vals[a] = 5
    vals[b] = 6
    vals[c] = a + b
    vals[d] = c * 3

    assert subs(a, vals) == 5
    assert subs(b, vals) == 6
    assert subs(c, vals) == 11
    assert subs(d, vals) == 33


def test_subs_with_fns():
    a, b, c = sp.symbols("a, b, c")

    d = sp.Function("d")(a)

    vals = {}
    vals[a] = 5
    vals[b] = 4
    vals[c] = d * 5
    vals[d] = a * 4

    assert subs(a, vals) == 5
    assert subs(b, vals) == 4
    assert subs(c, vals) == 100
    assert subs(d, vals) == 20


def test_subs_with_fns_and_known():
    a, b, c, e = sp.symbols("a, b, c, e")

    d = sp.Function("d")(a)

    vals = {}
    vals[b] = 4
    vals[c] = d * 5
    vals[d] = a * 4
    vals[e] = d.subs(a, 3)

    assert subs(b, vals) == 4
    assert sp.Eq(subs(c, vals), 20 * a, evaluate=True)
    assert sp.Eq(subs(d, vals), 4 * a, evaluate=True)
    assert subs(e, vals) == 12
