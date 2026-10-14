import pytest

from calculator.calculation import Calculation, ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def test_successful_command():
    history = []

    calculation = ArithmeticCalculation.create(
        5, 3, Operations.add
    )

    command = CalculateCommand(calculation, history, "add")

    assert command.execute() == 8
    assert history == ["add 5 3 = 8"]


def test_history_order():
    history = []

    first = ArithmeticCalculation.create(
        5, 3, Operations.add
    )
    second = ArithmeticCalculation.create(
        6, 3, Operations.divide
    )

    CalculateCommand(first, history, "add").execute()
    CalculateCommand(second, history, "divide").execute()

    assert HistoryCommand(history).execute() == [
        "add 5 3 = 8",
        "divide 6 3 = 2.0"
    ]


def test_failed_command():
    history = ["add 1 1 = 2"]

    calculation = ArithmeticCalculation.create(
        5, 0, Operations.divide
    )

    command = CalculateCommand(calculation, history, "divide")

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        command.execute()

    assert history == ["add 1 1 = 2"]


def test_empty_history():
    assert HistoryCommand([]).execute() == []


def test_history_copy():
    history = ["add 1 1 = 2"]

    result = HistoryCommand(history).execute()

    assert result == history
    assert result is not history

    result.append("another calculation")
    result.remove("add 1 1 = 2")

    assert history == ["add 1 1 = 2"]


def test_different_calculation_implementation():
    class AlternativeCalculation(Calculation):

        def execute(self):
            return self.operation(self.a, self.b) + 1

    history = []

    calculation = AlternativeCalculation.create(
        2, 3, Operations.add
    )

    command = CalculateCommand(
        calculation, history, "adjusted_add"
    )

    assert command.execute() == 6
    assert history == ["adjusted_add 2 3 = 6"]