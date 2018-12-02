# pylint: disable=missing-docstring
import pytest
import ducksearch


@pytest.mark.skip(reason="no way of currently testing this")
def test_ifeellucky_duckduckgo_should_return_result():
    assert ducksearch.ifeellucky("duckduckgo") is not None


@pytest.mark.skip(reason="no way of currently testing this")
def test_beer_junglehaze_should_return_result():
    assert ducksearch.beer("jungle haze") is not None


@pytest.mark.skip(reason="no way of currently testing this")
def test_beer_parishilton_should_return_none():
    assert ducksearch.beer("paris hilton") is None


def test_ifeellucky_multiple_calls_should():
    for i in range(100):
        print("pass", i)
        result = ducksearch.ifeellucky("beer")
        assert result is not None
