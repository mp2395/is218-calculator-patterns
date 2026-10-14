import pytest

from calculator.operations import Operations


def test_add():
    assert Operations.add(5, 3) == 8
    assert Operations.add(-5, 3) == -2
    assert Operations.add(1.5, 2.5) == 4
    assert Operations.add(0, 0) == 0


def test_subtract():
    assert Operations.subtract(5, 3) == 2
    assert Operations.subtract(-5, -3) == -2
    assert Operations.subtract(2.5, 1.5) == 1
    assert Operations.subtract(0, 3) == -3


def test_multiply():
    assert Operations.multiply(5, 3) == 15
    assert Operations.multiply(-5, 3) == -15
    assert Operations.multiply(1.5, 2) == 3
    assert Operations.multiply(0, 3) == 0


def test_divide():
    assert Operations.divide(6, 3) == 2
    assert Operations.divide(-6, 3) == -2
    assert Operations.divide(7.5, 2.5) == 3
    assert Operations.divide(0, 3) == 0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Operations.divide(5, 0)