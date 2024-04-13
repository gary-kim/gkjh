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


from importlib.metadata import version, PackageNotFoundError
from .expr_formatting import round_expr, scin_expr
from .misc import (
    subs,
    phasor2sympy,
    sympy2phasor,
    sphasor2str,
    sphasor2euler,
    put_units,
    strip_units,
    get_units,
    clean_units,
    display_eqns,
    display_vals,
    display_vals_v2,
    display_knowns,
    display_boxed,
    circuit_series,
    circuit_parallel,
    pd_num,
    subs_vals,
    package_versions,
    short_assign,
)
from . import lambdas

try:
    __version__ = version("gkjh")
except PackageNotFoundError:
    # package is not installed
    pass
