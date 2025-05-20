"""
Very small point‑reactor‑kinetics solver (6 delayed groups).
"""
import numba as nb
import numpy as np

_L = np.array([0.0124, 0.0305, 0.111, 0.301, 1.14, 3.01])  # 1/s
_B = np.array([0.00025, 0.0012, 0.0012, 0.0027, 0.0008, 0.0003])

BETA_EFF = _B.sum()
GEN_TIME = 2.0e-5  # s

@nb.njit
def _rhs(t, y, rho):
    P, C = y[0], y[1:]
    dP = (rho - BETA_EFF) / GEN_TIME * P + (_L * C).sum()
    dC = _B / GEN_TIME * P - _L * C
    out = np.empty(1 + dC.size, dtype=dC.dtype)
    out[0] = dP
    out[1:] = dC
    return out

def solve(rho_step=0.002, t_end=5.0, dt=1e-3):
    y = np.zeros(7)
    y[0] = 1.0  # Initial power P(0) = 1.0

    # Set initial delayed neutron precursor concentrations to steady-state values
    # at P=1.0, rho=0.0: Ci = Beta_i / (Lambda * Lambda_i)
    y[1:] = _B / (GEN_TIME * _L)

    ts, ps = [0.0], [1.0]
    t = 0.0
    while t < t_end:
        k1 = _rhs(t, y, rho_step)
        k2 = _rhs(t + dt / 2, y + dt / 2 * k1, rho_step)
        k3 = _rhs(t + dt / 2, y + dt / 2 * k2, rho_step)
        k4 = _rhs(t + dt, y + dt * k3, rho_step)
        y += dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        ts.append(t)
        ps.append(y[0])
    return np.asarray(ts), np.asarray(ps)