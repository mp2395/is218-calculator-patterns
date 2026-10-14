import pytest

from calculator.calculation import Calculation, ArithmeticCalculation
from calculator.operations import Operations


def test_factory():
    calculation = ArithmeticCalculation.create(
        5, 3, Operations.add
    )

    assert isinstance(calculation, ArithmeticCalculation)
    assert isinstance(calculation, Calculation)
    assert calculation.a == 5
    assert calculation.b == 3
    assert calculation.operation is Operations.add
    assert calculation.execute() == 8


def test_abstract_class():
    with pytest.raises(TypeError):
        Calculation(5, 3, Operations.add)


def test_different_operations():
    addition = ArithmeticCalculation.create(
        6, 3, Operations.add
    )
    subtraction = ArithmeticCalculation.create(
        6, 3, Operations.subtract
    )
    multiplication = ArithmeticCalculation.create(
        6, 3, Operations.multiply
    )
    division = ArithmeticCalculation.create(
        6, 3, Operations.divide
    )

    assert addition.execute() == 9
    assert subtraction.execute() == 3
    assert multiplication.execute() == 18
    assert division.execute() == 2


def test_calculation_error():
    calculation = ArithmeticCalculation.create(
        5, 0, Operations.divide
    )

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.execute()