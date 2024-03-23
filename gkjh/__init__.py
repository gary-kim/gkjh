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
)

try:
    __version__ = version("package-name")
except PackageNotFoundError:
    # package is not installed
    pass
