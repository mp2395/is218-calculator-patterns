import runpy

from calculator.cli import main


def run_calculator(monkeypatch, capsys, commands):
    commands = iter(commands)

    def fake_input(prompt):
        try:
            return next(commands)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)

    main()

    return capsys.readouterr().out


def test_successful_operations(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        [
            "add 5 3",
            "subtract 5 3",
            "multiply -2 4",
            "divide 7.5 2.5",
            "add -2.5 1",
            "exit"
        ]
    )

    lines = output.splitlines()

    assert "8.0" in lines
    assert "2.0" in lines
    assert "-8.0" in lines
    assert "3.0" in lines
    assert "-1.5" in lines
    assert "Goodbye!" in output


def test_errors_and_continuation(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        [
            "something",
            "add",
            "subtract 5",
            "multiply 1 2 3",
            "add apple 2",
            "add 2 apple",
            "divide 5 0",
            "history extra",
            "exit extra",
            "add 1 2",
            "exit"
        ]
    )

    assert "Unknown command." in output
    assert "Usage: add <number> <number>" in output
    assert "Usage: subtract <number> <number>" in output
    assert "Usage: multiply <number> <number>" in output
    assert "Invalid numbers." in output
    assert "Cannot divide by zero" in output
    assert "Usage: history" in output
    assert "Usage: exit" in output
    assert "3.0" in output.splitlines()
    assert "Goodbye!" in output


def test_empty_history(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["history", "exit"]
    )

    assert "History is empty." in output


def test_successful_history_only(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        [
            "add 5 3",
            "divide 5 0",
            "subtract 10 4",
            "history",
            "exit"
        ]
    )

    entries = []

    for line in output.splitlines():
        if " = " in line:
            entries.append(line)

    assert entries == [
        "add 5.0 3.0 = 8.0",
        "subtract 10.0 4.0 = 6.0"
    ]


def test_blank_input(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        ["", "   ", "add 1 2", "exit"]
    )

    assert "3.0" in output.splitlines()
    assert "Unknown command." not in output


def test_exit(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch,
        capsys,
        ["exit", "add 50 50"]
    )

    assert "Goodbye!" in output
    assert "100.0" not in output.splitlines()


def test_eof(monkeypatch, capsys):
    output = run_calculator(monkeypatch, capsys, [])

    assert "Goodbye!" in output


def test_eof_after_calculation(monkeypatch, capsys):
    output = run_calculator(
        monkeypatch, capsys, ["add 2 3"]
    )

    assert "5.0" in output.splitlines()
    assert "Goodbye!" in output


def test_package_entry_point(monkeypatch, capsys):
    def fake_input(prompt):
        return "exit"

    monkeypatch.setattr("builtins.input", fake_input)

    runpy.run_module("calculator", run_name="__main__")

    output = capsys.readouterr().out

    assert "Welcome to the calculator!" in output
    assert "Goodbye!" in output