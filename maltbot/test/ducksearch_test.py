# pylint: disable=missing-docstring
import ducksearch


def test_ifeellucky_duckduckgo_should_return_result():
    assert ducksearch.ifeellucky("duckduckgo") is not None


def test_beer_junglehaze_should_return_result():
    assert ducksearch.beer("jungle haze") is not None


def test_beer_baileys_should_return_none():
    assert ducksearch.beer("baileys") is None
