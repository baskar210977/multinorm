"""Tests for multinorm, using pyest.
"""
import pytest
from numpy.testing import assert_allclose
from multinorm import MultiNorm


@pytest.fixture()
def mn():
    """A simple test case."""
    mean = [10, 20, 30]
    covariance = [[1, 0, 0], [0, 4, 0], [0, 0, 9]]
    names = ["a", "b", "c"]
    return MultiNorm(mean, covariance, names)


def test_init():
    mn = MultiNorm(names=["a", "b"])
    assert mn.names == ["a", "b"]

    mn = MultiNorm(mean=[1, 2])
    assert mn.names == ["par_0", "par_1"]

    mn = MultiNorm(cov=[[1, 0], [0, 1]])
    assert mn.names == ["par_0", "par_1"]

    mn = MultiNorm(names=["a"])
    assert mn.mean.shape == (1,)
    assert mn.cov.shape == (1, 1)

    # Bad input should give good error
    with pytest.raises(ValueError):
        MultiNorm()

    with pytest.raises(ValueError):
        MultiNorm(mean=[0, 0, 0], names=["a", "b"])

    # TODO: check more bad inputs, like wrong order or such


def test_init_parnames():
    mn = MultiNorm([0, 0], [[0, 0], [0, 0]])
    assert mn.names == ["par_0", "par_1"]


def test_repr(mn):
    assert repr(mn) == "MultiNorm(n=3)"


def test_str(mn):
    assert "MultiNorm" in str(mn)


def test_from_err():
    mean = [10, 20, 30]
    err = [1, 2, 3]
    names = ["a", "b", "c"]
    mn = MultiNorm.from_err(mean, err, names)
    assert_allclose(mn.mean, mean)
    assert_allclose(mn.err, err)
    assert mn.names == names


def test_from_points():
    points = [
        (10, 20, 30),
    ]
    names = ["a", "b", "c"]
    mn = MultiNorm.from_points(points, names)


def test_from_product():
    mn1 = MultiNorm(mean=[0, 0], names=["a", "b"])
    mn2 = MultiNorm(mean=[2, 4], names=["a", "b"])

    mn = MultiNorm.from_product([mn1, mn2])

    assert mn.names == ["a", "b"]
    assert_allclose(mn.mean, [1, 2])
    assert_allclose(mn.cov, [[0.5, 0], [0, 0.5]])


def test_marginal(mn):
    mn2 = mn.marginal([0, 2])
    assert mn2.names == ["a", "c"]
    assert_allclose(mn2.mean, [10, 30])
    assert_allclose(mn2.err, [1, 3])


def test_conditional(mn):
    mn2 = mn.conditional(1, 20)
    assert mn2.names == ["a", "c"]
    assert_allclose(mn2.mean, [10, 30])
    assert_allclose(mn2.err, [1, 3])


def test_pdf(mn):
    res = mn.pdf([[10, 20, 30]])
    assert_allclose(res, 0.010582272655706831)


def test_logpdf(mn):
    res = mn.logpdf([[10, 20, 30]])
    assert_allclose(res, -4.548575068842073)


def test_sample(mn):
    res = mn.sample(size=1, random_state=0)
    assert_allclose(res, [10.978738, 20.800314, 35.292157])


def test_to_matplotlib_ellipse(mn):
    ellipse = mn.marginal(["a", "b"]).to_matplotlib_ellipse()
    assert_allclose(ellipse.center, (10, 20))
    assert_allclose(ellipse.width, 2)
    assert_allclose(ellipse.height, 4)
    # TODO: change to a test case where `angle` is nonzero and well defined.
    assert_allclose(ellipse.angle, 0)
