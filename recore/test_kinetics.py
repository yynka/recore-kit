import numpy as np
import pytest
from recore import kinetics

def test_solve_default():
    ts, ps = kinetics.solve()
    # Check output types
    assert isinstance(ts, np.ndarray)
    assert isinstance(ps, np.ndarray)
    # Check output shapes
    assert ts.shape == ps.shape
    # Check initial conditions
    assert np.isclose(ts[0], 0.0)
    assert np.isclose(ps[0], 1.0)
    # Check that time increases
    assert np.all(np.diff(ts) > 0)
    # Check that power is always positive
    assert np.all(ps > 0)

@pytest.mark.parametrize("rho_step", [0.0, 0.001, 0.005])
def test_solve_rho_step(rho_step):
    ts, ps = kinetics.solve(rho_step=rho_step)
    assert ts.shape == ps.shape
    assert np.isclose(ts[0], 0.0)
    assert np.isclose(ps[0], 1.0)
    assert np.all(ps > 0)

def test_solve_conserves_power_at_zero_rho():
    ts, ps = kinetics.solve(rho_step=0.0, t_end=5.0, dt=1e-3)
    # Power should remain close to 1.0 for all times
    assert np.allclose(ps, 1.0, atol=1e-2) 