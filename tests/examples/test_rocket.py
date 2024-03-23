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

from gkjh import subs

import sympy as sp


def test_rocket_launch():
    mach_exit, mach_2, m_payload, m_rocket, T_t, P_inf, mratio, m_dot = sp.symbols(
        "mach_exit, mach_2, m_payload, m_rocket, T_t, P_inf, mratio, m_dot"
    )
    D_max, R, k, P_t, phi, M_1, f_thrust, g, m_fuel, payload_mf = sp.symbols(
        "D_max, R, k, P_t, phi, M_1, f_thrust, g, m_fuel, payload_mf"
    )

    vals = {}

    # Knowns/Directly Givens
    vals[mach_exit] = 4
    vals[mach_2] = 1
    vals[m_payload] = 907  # kg
    vals[g] = sp.Rational(981, 100)
    vals[T_t] = 3839  # K
    vals[P_inf] = 1  # atm
    vals[R] = 924
    vals[k] = sp.Rational(13, 10)
    vals[phi] = 2
    vals[payload_mf] = sp.Rational(1, 100)

    A_throat, A_exit, D_hat_e, D_e, m_dot, c_p, d_exit = sp.symbols(
        "A_throat, A_exit, D_hat_e, D_e m_dot, c_p, d_exit"
    )
    T_1, T_2, T_3, P_1, P_2, P_3, mach_1, d_throat = sp.symbols(
        "T_1, T_2, T_3, P_1, P_2, P_3, mach_1, d_throat"
    )

    # Derived
    vals[m_rocket] = m_payload * payload_mf**-1  # kg
    vals[m_fuel] = m_rocket - m_payload  # kg
    vals[f_thrust] = vals[m_rocket] * g

    vals[c_p] = R * k / (k - 1)

    # Temperatures
    vals[T_1] = (1 / (1 + (k - 1) / 2 * mach_1**2)) * T_t
    vals[T_2] = (1 / (1 + (k - 1) / 2 * mach_2**2)) * T_t
    vals[T_3] = (1 / (1 + (k - 1) / 2 * mach_exit**2)) * T_t

    # Pressures
    vals[P_3] = P_inf
    vals[P_t] = (T_3 / T_t) ** (-c_p / R) * P_3
    vals[P_1] = (T_1 / T_t) ** (c_p / R)
    vals[P_2] = (T_2 / T_t) ** (c_p / R)

    # Mass Flow Function
    vals[D_max] = (2 / (k + 1)) ** ((k + 1) / (2 * (k - 1)))
    vals[D_e] = (P_3 / P_t) * sp.sqrt(T_t / T_3) * mach_exit
    vals[D_hat_e] = D_e / D_max

    # Throat area
    vals[A_throat] = f_thrust / (
        k * mach_exit**2 * (P_3 / P_t) * D_hat_e**-1 * (P_t * 101325)
    )
    vals[d_throat] = sp.sqrt(A_throat / sp.pi) * 2

    # Exit area
    A_ratio, v_exit, A_exit, rho_exit = sp.symbols("A_ratio, v_exit, A_exit, rho_exit")
    vals[A_ratio] = D_hat_e**-1
    vals[A_exit] = A_ratio * A_throat
    vals[d_exit] = sp.sqrt(A_exit / sp.pi) * 2

    # Mass flow rate of propellant
    vals[m_dot] = sp.sqrt(k / R) * D_e * (P_t * 101325) * A_exit / sp.sqrt(T_t)

    # Density at exit
    vals[rho_exit] = (P_3 * 101325) / (R * T_3)

    # Exit velocity
    vals[v_exit] = m_dot / (rho_exit * A_exit)

    # Specific Impulse Equations
    impulse, specific_impulse, t_burn = sp.symbols("impulse, sp, t_burn")
    vals[impulse] = sp.sqrt(T_3 / T_t) * mach_exit
    vals[specific_impulse] = sp.sqrt(k * R * T_t) / g * impulse
    vals[t_burn] = m_fuel / m_dot

    vals = {k: subs(v, vals) for k, v in vals.items()}

    assert vals[mach_exit] == 4
    assert vals[mach_2] == 1
    assert vals[m_payload] == 907
    assert sp.Eq(vals[g], sp.Rational(981, 100))
    assert vals[T_t] == 3839
    assert vals[P_inf] == 1
    assert vals[R] == 924
    assert sp.Eq(vals[k], sp.Rational(13, 10))
    assert vals[phi] == 2
    assert sp.Eq(vals[payload_mf], sp.Rational(1, 100))
    assert vals[m_rocket] == 90700
    assert vals[m_fuel] == 89793
    assert vals[f_thrust] == 889767
    assert vals[c_p] == 4004
    assert sp.Eq(vals[T_1], 3839 / (3 * mach_1**2 / 20 + 1))
    assert sp.Eq(vals[T_2], sp.Rational(76780, 23))
    assert sp.Eq(vals[T_3], sp.Rational(19195, 17))
    assert vals[P_3] == 1
    assert sp.Eq(
        vals[P_t], 83521 * 17 ** sp.Rational(1, 3) * 5 ** sp.Rational(2, 3) / 3125
    )
    assert sp.Eq(vals[P_1], (1 / (3 * mach_1**2 / 20 + 1)) ** sp.Rational(13, 3))
    assert sp.Eq(
        vals[P_2], 160000 * 20 ** sp.Rational(1, 3) * 23 ** sp.Rational(2, 3) / 6436343
    )
    assert sp.Eq(
        vals[D_max],
        16000
        * 2 ** sp.Rational(2, 3)
        * 23 ** sp.Rational(1, 6)
        * 5 ** sp.Rational(5, 6)
        / 279841,
    )
    assert sp.Eq(
        vals[D_e], 500 * 17 ** sp.Rational(1, 6) * 5 ** sp.Rational(5, 6) / 83521
    )
    assert sp.Eq(
        vals[D_hat_e],
        12167
        * 17 ** sp.Rational(1, 6)
        * 2 ** sp.Rational(1, 3)
        * 23 ** sp.Rational(5, 6)
        / 5345344,
    )
    assert sp.Eq(
        vals[A_throat],
        3608598363
        * 17 ** sp.Rational(1, 6)
        * 2 ** sp.Rational(1, 3)
        * 23 ** sp.Rational(5, 6)
        / 3755211066880,
    )
    assert sp.Eq(
        vals[d_throat],
        23
        * 17 ** sp.Rational(1, 12)
        * 2 ** sp.Rational(2, 3)
        * 23 ** sp.Rational(11, 12)
        * sp.sqrt(26044963035)
        / (406056560 * sp.sqrt(sp.pi)),
    )
    assert sp.Eq(
        vals[A_ratio],
        157216
        * 17 ** sp.Rational(5, 6)
        * 2 ** sp.Rational(2, 3)
        * 23 ** sp.Rational(1, 6)
        / 279841,
    )
    assert sp.Eq(vals[A_exit], sp.Rational(296589, 702520))
    assert sp.Eq(vals[d_exit], sp.sqrt(52089926070) / (175630 * sp.sqrt(sp.pi)))
    assert sp.Eq(vals[m_dot], 296589 * sp.sqrt(3239418) / 2794792)
    assert sp.Eq(vals[rho_exit], sp.Rational(16405, 168916))
    assert sp.Eq(vals[v_exit], 44 * sp.sqrt(3239418) / 17)
    assert sp.Eq(vals[impulse], 4 * sp.sqrt(85) / 17)
    assert sp.Eq(vals[specific_impulse], 4400 * sp.sqrt(3239418) / 16677)
    assert sp.Eq(vals[t_burn], 484 * sp.sqrt(3239418) / 1853)
