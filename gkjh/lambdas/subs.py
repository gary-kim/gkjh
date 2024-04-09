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
from ..misc import display_vals_v2, subs_lambdas

a, b = sp.symbols("a, b")

vals = {}
vals[a] = 1
vals[b] = a + a

display_vals_v2(vals, [a, subs_lambdas.subs(vals)])
```
"""

from ..misc import subs as gkjh_subs


def subs(vals: dict):
    """
    Call subs with a given vals dict.

    Example use:
    ```
    display_vals_v2(vals, [a, subs_lambdas.subs(vals)])
    ```
    """
    return lambda x: gkjh_subs(x, vals)
