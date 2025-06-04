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
