# pylint: disable=missing-docstring
import main


def test_one():
    assert main.one() is True


def test_two():
    assert main.two() == "string"
