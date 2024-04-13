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
Miscellaneous functions as part of GKJH.

Many unnecessary functions are currently part of this module
"""

import math
import importlib
import sys
from contextlib import contextmanager

try:
    from IPython.display import display, display_latex
except ImportError:
    display = lambda *a, **b: None
    display_latex = lambda *a, **b: None

import sympy as sp
from sympy.physics import units

from .expr_formatting import round_expr


def package_versions(
    packages=["gkjh", "python", "sympy", "matplotlib", "pandas"],
    header_and_footer=True,
    fatal=False,
) -> str:
    """
    package_versions provides a list of the given package versions.

    Provides a list of versions of the provided package list for reproducibility
    reference (defaulting to those included with gkjh).
    """

    tr = []
    if header_and_footer:
        tr = ["== GKJH: Gary Kim Jupyter Helpers =="]

    if "python" in packages:
        tr.append(f'"python=={sys.version}"')

    if "gkjh" in packages:
        package = importlib.import_module("gkjh")
        if hasattr(package, "__version__"):
            tr.append(f'"gkjh=={package.__version__}"')
        else:
            tr.append(f'"gjkh==unknown"')

    packages = sorted(packages)
    for package_name in packages:
        if package_name == "gkjh" or package_name == "python":
            continue

        if fatal:
            try:
                package = importlib.import_module(package_name)
            except:
                pass

        package = importlib.import_module(package_name)

        if hasattr(package, "__version__"):
            tr.append(f'"{package_name}=={package.__version__}"')
        else:
            tr.append(f'"{package_name}==unknown"')

    if header_and_footer:
        tr.append("====================================")

    return "\n".join(tr)


def pd_num(num, make_scin=False):
    tmp = sp.Number(num)
    if not make_scin:
        return tmp
    return scin_expr(tmp, make_scin)


def match_by_function(tfunc, vals):
    for k, _ in vals.items():
        if k.func == tfunc:
            return k
    return None


def subs(expr, vals, recurse=math.inf):
    if "subs" not in dir(expr):
        return expr
    current_index = 0
    n_expr = expr
    while True:
        expr = n_expr
        n_expr = expr.subs(vals)
        if n_expr == expr or current_index >= recurse:
            return n_expr
        for x in n_expr.atoms(sp.Function):
            if not all((isinstance(z, sp.Symbol) for z in x.args)):
                t_func = match_by_function(x.func, vals)
                if t_func is None:
                    continue
                tmp = vals[t_func].subs(dict(zip(t_func.args, x.args)))
                n_expr = n_expr.subs(x, tmp)
        current_index += 1


def subs_vals(vals: dict) -> dict:
    """subs_vals runs subs(v, vals) for all values in vals."""
    return {k: subs(v, vals) for k, v in vals.items()}


def phasor2sympy(magnitude, angle):
    return magnitude * (
        sp.cos(angle * sp.pi / 180) + sp.I * sp.sin(angle * sp.pi / 180)
    )


def sympy2phasor(value, round_value):
    mag = abs(value)
    ang = sp.arg(value) * 180 / sp.pi

    if hasattr(mag, "evalf"):
        mag = mag.evalf()

    if hasattr(ang, "evalf"):
        ang = ang.evalf()

    return {"magnitude": round(mag, round_value), "angle": round(ang, round_value)}


def sphasor2str(value, round_value):
    return (
        str(float(round(abs(value).evalf(), round_value)))
        + "⦟"
        + str(
            round_expr((sp.arg(value) * 180 / sp.pi).evalf(), round_value, zeros=True)
        )
    )


def sphasor2euler(value):
    return abs(value) * sp.exp(sp.Mul(sp.I, sp.arg(value)))


def put_units(eqn, units):
    return sp.Mul(eqn, units, evaluate=False)


def strip_units(expr):
    au = expr.atoms(units.quantities.Quantity)
    tmp = expr
    for u in au:
        tmp = tmp.subs(u, 1)
    return tmp


def get_units(expr):
    tmp = expr.subs({n: 1 for n in expr.args if not n.has(units.quantities.Quantity)})
    tmp = tmp.xreplace({n: sp.Integer(round(n, 0)) for n in tmp.atoms(sp.Number)})
    return tmp


def clean_units(expr):
    us = get_units(expr)
    nums = strip_units(expr)
    return put_units(nums, us)


def display_eqns(eqns):
    display("===== System of equations =====")
    for e in eqns:
        display(e)
    display("===== END =====")


def display_vals(vals, to_display=False):
    if isinstance(to_display, bool) and to_display == False:
        to_display = list(vals.keys())

    if not isinstance(to_display, (list)):
        to_display = [to_display]

    for su in to_display:
        if isinstance(su, (tuple)):
            if len(su) == 3:
                display(
                    sp.Eq(
                        su[0], units.convert_to(vals[su[0]] * su[1], su[2]).simplify()
                    )
                )
                continue
            if len(su) == 2:
                display(sp.Eq(su[0], put_units(vals[su[0]], su[1])))
                continue
        display(sp.Eq(su, vals[su]))


def display_vals_v2(vals, to_display=False):
    if isinstance(to_display, bool) and to_display == False:
        to_display = list(vals.keys())

    if not isinstance(to_display, (list)):
        to_display = [to_display]

    for su in to_display:
        if isinstance(su, (tuple)):
            if len(su) >= 2:
                display(sp.Eq(su[0], su[1](vals[su[0]]), evaluate=False))
                continue
        display(sp.Eq(su, vals[su], evaluate=False))


def display_knowns(vals, to_display=False):
    display("===== Knowns =====")
    display_vals(vals, to_display)
    display("===== END =====")


def display_boxed(eqn):
    display_latex(r"$$\boxed{" + sp.latex(eqn) + r"}$$")


def circuit_series(*args):
    return sum(args)


def circuit_parallel(*args):
    val = sp.Number(0)
    for a in args:
        val += a**-1
    return val**-1


@contextmanager
def short_assign(l):
    """
    For use as a managed resource to temporarily shorten a variable.


    Example use:
    ```
    import gkjh

    with gkjh.short_assign(gkjh.lambdas) as l:
        l.subs(vals)
        ...
    ```
    """
    yield l
