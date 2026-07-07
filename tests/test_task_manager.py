import builtins
import pytest
from tasks.main import get_valid_input

def test_get_valid_input_returns_validated_value(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda prompt: "10")

    result = get_valid_input("Enter a number: ", int)

    assert result == 10

def test_get_valid_input_retries_until_validator_accepts(monkeypatch, capsys):
    answers = iter(["", "Title example"])

    def faked_input(prompt):
        return next(answers)

    def validate_title(title):
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    monkeypatch.setattr(builtins, "input", faked_input)

    result = get_valid_input("Enter title: ", validate_title)

    assert result == "Title example"
    assert "Error: Title cannot be empty" in capsys.readouterr().out
