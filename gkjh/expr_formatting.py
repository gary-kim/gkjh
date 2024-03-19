import sympy as sp
import math


def round_expr(expr, num_digits, zeros=False, evalf=False):
    def do_conversion(val):
        if val == 0:
            return 0
        length = sp.floor(sp.log(val, 10))
        tmp = val * 10 ** -length
        tmp = round(tmp, num_digits)
        return tmp * 10 ** length

    if not hasattr(expr, 'xreplace'):
        return round(expr, num_digits)

    if evalf and hasattr(expr, 'evalf'):
        expr = expr.evalf()


    if zeros:
        return expr.xreplace(
            {n: round(n, num_digits) for n in expr.atoms(sp.Number)}
        )
    return expr.xreplace({n: do_conversion(n) for n in expr.atoms(sp.Number)})


def scin_expr(expr, num_digits=math.inf):
    def do_conversion(val):
        if val == 0:
            return 0
        length = sp.floor(sp.log(val, 10))
        tmp = val * 10 ** -length
        tmp = round(tmp, num_digits)
        return tmp * sp.UnevaluatedExpr(10) ** length

    return expr.xreplace({n: do_conversion(n) for n in expr.atoms(sp.Number)})
