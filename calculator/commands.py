from calculator.calculation import Calculation


class CalculateCommand:

    def __init__(
        self,
        calculation: Calculation,
        history,
        command_name
    ):
        self.calculation = calculation
        self._history = history
        self.command_name = command_name

    def execute(self):
        # Calculate first so errors do not enter history.
        result = self.calculation.execute()

        entry = (
            f"{self.command_name} "
            f"{self.calculation.a} "
            f"{self.calculation.b} = {result}"
        )

        self._history.append(entry)

        return result


class HistoryCommand:

    def __init__(self, history):
        self._history = history

    def execute(self):
        # Return a copy to protect the stored list.
        return self._history.copy()