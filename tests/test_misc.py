# Copyright (C) 2024 Gary Kim <gary@garykim.dev>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

import sympy as sp
import sympy.physics.units as units
import gkjh

from gkjh import (
    phasor2sympy,
    subs,
    get_units,
    strip_units,
    clean_units,
    package_versions,
    put_units,
)


def test_package_versions():
    assert package_versions() != ""


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


def test_phasor2sympy():
    a, b, c = sp.symbols("a, b, c")

    vals = {}
    vals[a] = 10
    vals[b] = sp.Rational(45, 2)
    vals[c] = phasor2sympy(a, b * 2)

    assert subs(a, vals) == 10
    assert sp.Eq(subs(b, vals), sp.Rational(45, 2), evaluate=True)
    assert sp.Eq(subs(c, vals), 10 / sp.sqrt(2) + sp.I / sp.sqrt(2) * 10, evaluate=True)


def test_units():
    a, b, c, d = sp.symbols("a, b, c, d")

    vals = {}
    vals[a] = 3 * units.meters
    vals[b] = 4 * units.s
    vals[c] = 5 * units.s
    vals[d] = a / b / c

    assert sp.Eq(strip_units(subs(d, vals)), sp.Rational(3, 4 * 5))
    assert sp.Eq(get_units(subs(d, vals)), units.meters / units.s**2)
    assert sp.Eq(
        put_units(strip_units(subs(d, vals)), units.meters),
        sp.Rational(3, 4 * 5) * units.meters,
    )


def test_subs_with_number():
    assert subs(10, {}) == 10
    assert subs(-10, {}) == -10


def test_clean_units():
    val_a = 10 * units.s / units.m
    val_b = -30.3 * units.m / units.s**2

    assert sp.Eq(clean_units(val_a), val_a)
    assert sp.Eq(clean_units(val_b), val_b)


def test_short_assign():
    a, b, c, d, e, f = sp.symbols("a, b, c, d, e, f")

    vals = {}
    vals[a] = 5
    vals[b] = 6
    vals[c] = a + b
    vals[d] = c * 3
    vals[e] = d / 66
    vals[f] = e / 234

    with gkjh.short_assign(gkjh.lambdas) as l:
        ls = l.chaining(
            l.subs(vals),
            l.put_units(units.m),
            l.evalf(),
            l.round_expr(3, zeros=True),
        )

    assert sp.Eq(ls(a), 5 * units.m)
    assert sp.Eq(ls(b), 6 * units.m)
    assert sp.Eq(ls(c), 11 * units.m)
    assert sp.Eq(ls(d), 33 * units.m)
    assert sp.Eq(ls(e), 0.5 * units.m)
    assert sp.Eq(ls(f), sp.Rational(2, 1000) * units.m)
