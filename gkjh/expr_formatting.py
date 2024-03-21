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

"""
Expression formatting functions as part of GKJH.

There are known bugs in this implementation.
"""

import sympy as sp
import math


def round_expr(expr, num_digits, zeros=False, evalf=False):
    def do_conversion(val):
        if val == 0:
            return 0
        length = sp.floor(sp.log(val, 10))
        tmp = val * 10**-length
        tmp = round(tmp, num_digits)
        return tmp * 10**length

    if not hasattr(expr, "xreplace"):
        return round(expr, num_digits)

    if evalf and hasattr(expr, "evalf"):
        expr = expr.evalf()

    if zeros:
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(sp.Number)})
    return expr.xreplace({n: do_conversion(n) for n in expr.atoms(sp.Number)})


def scin_expr(expr, num_digits=math.inf):
    def do_conversion(val):
        if val == 0:
            return 0
        length = sp.floor(sp.log(val, 10))
        tmp = val * 10**-length
        tmp = round(tmp, num_digits)
        return tmp * sp.UnevaluatedExpr(10) ** length

    return expr.xreplace({n: do_conversion(n) for n in expr.atoms(sp.Number)})
