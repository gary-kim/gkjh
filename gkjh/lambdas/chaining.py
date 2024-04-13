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

from contextlib import contextmanager


class chaining:
    """
    Class for chaining lambda functions, mostly used for display_vals_v2.

    This class intentionally lacks support for lambdas with more than one
    argument.

    Example use:
    ```
    import sympy as sp
    from gkjh import display_vals_v2
    from gkjh.lambdas import subs, put_units

    a, b = sp.symbols("a, b")

    vals = {}
    vals[a] = 1
    vals[b] = a + a

    display_vals_v2(vals, [(a, chaining(subs(vals), put_units(units.m)))])
    ```
    """

    def __init__(self, *funcs, **kwargs):
        funcs = list(funcs)
        if not all([callable(func) for func in funcs]):
            raise ValueError("All given funcs must be callable")
        self.funcs = funcs

    def __call__(self, args):
        tr = args
        for func in self.funcs:
            tr = func(tr)
        return tr
