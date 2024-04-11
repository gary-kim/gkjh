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


def test_chaining():
    a, b, c, d, e, f = sp.symbols("a, b, c, d, e, f")

    vals = {}
    vals[a] = 5
    vals[b] = 6
    vals[c] = a + b
    vals[d] = c * 3
    vals[e] = d / 66
    vals[f] = e / 234

    ls = gkjh.lambdas.chaining(
        gkjh.lambdas.subs(vals),
        gkjh.lambdas.put_units(units.m),
        gkjh.lambdas.evalf(),
        gkjh.lambdas.round_expr(3, zeros=True),
    )

    assert sp.Eq(ls(a), 5 * units.m)
    assert sp.Eq(ls(b), 6 * units.m)
    assert sp.Eq(ls(c), 11 * units.m)
    assert sp.Eq(ls(d), 33 * units.m)
    assert sp.Eq(ls(e), 0.5 * units.m)
    assert sp.Eq(ls(f), sp.Rational(2, 1000) * units.m)
