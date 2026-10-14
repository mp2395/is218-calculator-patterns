# My calculator submission

## Setup, run, and test

This project requires Python 3.12 or newer.

Clone the repository and install the test tools:

```bash
git clone git@github.com:mp2395/is218-calculator-patterns.git
cd is218-calculator-patterns
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the calculator:

```bash
python -m calculator
```

Run the tests and require 100% line coverage:

```bash
python -m pytest --cov=calculator --cov-report=term-missing --cov-fail-under=100
```

## Example conversation

```text
calculator> add 5 3
8.0
calculator> subtract 5 3
2.0
calculator> multiply -2 4
-8.0
calculator> divide 7.5 2.5
3.0
calculator> divide 5 0
Cannot divide by zero
calculator> history
add 5.0 3.0 = 8.0
subtract 5.0 3.0 = 2.0
multiply -2.0 4.0 = -8.0
divide 7.5 2.5 = 3.0
calculator> exit
Goodbye!
```

Failed calculations are not saved in history. The calculator keeps
running after errors and also ends cleanly on EOF.

## Static, class, and instance methods

The methods in Operations, including add() and divide(), are static
methods because they only use the numbers passed to them. They do
not need self or cls.

Calculation.create() is a class method. It uses cls to create an
object of the concrete class that called it.

ArithmeticCalculation.execute() is an instance method because it
uses self to access that calculation's stored numbers and operation.

## Factory, Command, and Strategy

For add 5 3, the CLI reads the command and converts the operands
to numbers. It selects Operations.add from the operations dictionary.
This selected function is the Strategy.

The CLI calls ArithmeticCalculation.create() to build the calculation.
This inherited class method is the Factory.

The CLI then creates CalculateCommand and calls its execute() method.
The command runs the calculation, saves the successful result in
history, and returns the answer for the CLI to print.

HistoryCommand is another Command. Its execute() method returns
a copy of the history list.

## OOP

Encapsulation: Calculation keeps its numbers, operation, and execution
behavior together. HistoryCommand returns a copy so changing the
returned list does not change the stored history.

Abstraction: Calculation is an abstract class that requires execute().
Concrete calculations must implement that method.

Inheritance: ArithmeticCalculation inherits the constructor and
create() factory from Calculation.

Polymorphism: CalculateCommand calls execute() on a Calculation
implementation. The alternative calculation test shows that the
same command can work with a different implementation.

Composition: CalculateCommand holds a calculation object, and
the calculation holds an operation function.

## SOLID

Single responsibility: Operations handles arithmetic, calculations
store and execute values, commands coordinate actions and history,
and the CLI handles input and output.

Open/closed: Another operation can be added to Operations and
registered in the CLI dictionary without changing calculation
or command execution.

Liskov substitution: Any replacement Calculation must keep the
execute() contract by returning a numeric result or raising an
appropriate error.

Interface segregation: Calculation only requires execute() as its
abstract behavior. It does not require unrelated input, output,
or history methods.

Dependency inversion: CalculateCommand accepts the Calculation
abstraction. A calculation receives its operation function instead
of hard-coding addition.

After addition, I added subtract(), multiply(), and divide() to
Operations and registered them in the CLI dictionary.
ArithmeticCalculation.execute() stays the same because it calls
whichever operation function it receives.

## Tests and GitHub Actions

My local test run passed all 31 tests with 100% line coverage
across the calculator package.

The tests check arithmetic, decimals, negatives, zero, division
errors, factory construction, abstraction, different operations,
commands, history copies, CLI errors, continued input, exit, and EOF.

GitHub Actions runs the same test command on pushes and pull requests.
The workflow requires all tests to pass and 100% line coverage.

Actions run link:
https://github.com/mp2395/is218-calculator-patterns/actions/runs/38517604725

## Coverage exclusions

The abstract Calculation.execute() pass statement is excluded because
it declares the contract without providing calculation behavior.

The main() call in calculator/__main__.py is also excluded because
it only starts the CLI. Tests exercise main() directly and also
check the package entry point.

Both exclusions have nearby comments. Arithmetic, factory construction,
commands, history, parsing, and error handling are covered by tests.