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

import gkjh

import sympy as sp
import sympy.physics.units as units


def test_subs_basic():
    a, b, c, d = sp.symbols("a, b, c, d")

    vals = {}
    vals[a] = 5
    vals[b] = 6
    vals[c] = a + b
    vals[d] = c * 3

    ls = gkjh.lambdas.subs(vals)

    assert ls(a) == 5
    assert ls(b) == 6
    assert ls(c) == 11
    assert ls(d) == 33


def test_put_units():
    a = 5
    b = 6
    c = a + b
    d = c * 3

    assert sp.Eq(gkjh.lambdas.put_units(units.m)(a), 5 * units.m) == True
    assert (
        sp.Eq(gkjh.lambdas.put_units(units.m / units.s)(b), 6 * units.m / units.s)
        == True
    )
    assert sp.Eq(gkjh.lambdas.put_units(units.A)(c), 11 * units.A) == True
    assert sp.Eq(gkjh.lambdas.put_units(units.V)(d), 33 * units.V) == True


def test_evalf():
    a = sp.Rational(1, 5)

    ls = gkjh.lambdas.evalf()

    assert ls(a) == 0.2


def test_round_expr():
    a = sp.Rational(321, 1000)

    ls = gkjh.lambdas.round_expr(2, zeros=True)

    assert sp.Eq(ls(a), sp.Rational(32, 100))
