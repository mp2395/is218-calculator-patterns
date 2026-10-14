from calculator.operations import Operations
from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand


def main():
    # Operation functions are the arithmetic strategies.
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide
    }

    history = []

    print("Welcome to the calculator!")
    print("Commands: add, subtract, multiply, divide, history, exit")

    while True:
        try:
            user_input = input("calculator> ")
        except EOFError:
            print("Goodbye!")
            break

        parts = user_input.split()

        if len(parts) == 0:
            continue

        command_name = parts[0].lower()

        if command_name == "exit":
            if len(parts) != 1:
                print("Usage: exit")
                continue

            print("Goodbye!")
            break

        if command_name == "history":
            if len(parts) != 1:
                print("Usage: history")
                continue

            history_command = HistoryCommand(history)
            entries = history_command.execute()

            if len(entries) == 0:
                print("History is empty.")
            else:
                for entry in entries:
                    print(entry)

            continue

        if command_name not in operations:
            print(
                "Unknown command. Use add, subtract, multiply, "
                "divide, history, or exit."
            )
            continue

        if len(parts) != 3:
            print(f"Usage: {command_name} <number> <number>")
            continue

        try:
            a = float(parts[1])
            b = float(parts[2])
        except ValueError:
            print("Invalid numbers. Enter two numeric values.")
            continue

        # Read input -> select operation -> create calculation ->
        # execute command -> print answer.
        operation = operations[command_name]

        calculation = ArithmeticCalculation.create(
            a,
            b,
            operation
        )

        command = CalculateCommand(
            calculation,
            history,
            command_name
        )

        try:
            result = command.execute()
        except ValueError as error:
            print(error)
            continue

        print(result)