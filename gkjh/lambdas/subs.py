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
Various pre-made static methods for use for expression formatting or subs.

This class provides various static methods for use with functions such as
display_subs_v2.

Example use:
```
import sympy as sp
from gkjh import display_vals_v2, subs_lambdas

a, b = sp.symbols("a, b")

vals = {}
vals[a] = 1
vals[b] = a + a

display_vals_v2(vals, [a, subs_lambdas.subs(vals)])
```
"""

from typing import Optional

from ..misc import (
    put_units as gkjh_put_units,
    round_expr as gkjh_round_expr,
    subs as gkjh_subs,
)


def subs(vals: dict):
    """
    Call subs with a given vals dict.

    Example use:
    ```
    import sympy.physics.units as units
    import gkjh
    from gkjh import display_vals_v2

    display_vals_v2(vals, [(a, gkjh.lambdas.subs(vals))])
    ```
    """
    return lambda x: gkjh_subs(x, vals)


def put_units(desired_unit):
    """
    Call put_units with a given unit.

    Example use:
    ```
    import sympy.physics.units as units
    import gkjh
    from gkjh import display_vals_v2

    display_vals_v2(vals, [(v, gkjh.lambdas.put_units(units.m / units.s))])
    ```
    """
    return lambda x: gkjh_put_units(x, desired_unit)


def evalf():
    """
    Call evalf on the given sympy expression.

    Can properly handle being given values that do not have an evalf function.

    Example use:
    ```
    import gkjh
    from gkjh import display_vals_v2

    display_vals_v2(vals, [(v, gkjh.lambdas.evalf())])
    ```
    """
    return lambda x: x.evalf() if "evalf" in dir(x) else x


def round_expr(figures: int, zeros: Optional[bool]):
    """
    round_expr the given sympy expression.

    Example use:
    ```
    import gkjh

    gkjh.display_vals_v2(vals, [(v, gkjh.lambdas.round_expr(3))])
    ```
    """
    return lambda x: gkjh_round_expr(x, figures, zeros)
