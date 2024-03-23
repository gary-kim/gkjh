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

from gkjh import subs, subs_vals

import sympy as sp


def test_wing_lift():
    C_D, v, h, w, a, rho, C_L, D, LD_ratio = sp.symbols(
        "C_D, v, h, w, a, rho, C_L, D, LD_ratio"
    )

    vals = {}
    vals[C_D] = sp.Rational(31, 1000)
    vals[rho] = sp.Rational(1927, 1e6)  # slug / ft^3
    vals[v] = 115  # mph
    vals[h] = 7000  # ft
    vals[w] = 1500  # lbf
    vals[a] = 157  # ft^2
    vals[LD_ratio] = w / D

    vals[D] = sp.Rational(1, 2) * rho * v**2 * a * C_D

    eqn = sp.Eq(w, sp.Rational(1, 2) * rho * v**2 * a * C_L)

    vals[C_L] = sp.solve(subs(eqn, vals), C_L, dict=True)[0][C_L]

    vals = subs_vals(vals)

    assert sp.Eq(vals[C_D], sp.Rational(31, 1000))
    assert sp.Eq(vals[rho], sp.Rational(1927, 1000000))
    assert vals[v] == 115
    assert vals[h] == 7000
    assert vals[w] == 1500
    assert vals[a] == 157
    assert sp.Eq(vals[LD_ratio], sp.Rational(120000000000, 4961337061))
    assert sp.Eq(vals[D], sp.Rational(4961337061, 80000000))
    assert sp.Eq(vals[C_L], sp.Rational(120000000, 160043131))
