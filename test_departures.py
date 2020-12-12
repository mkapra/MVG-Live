import pytest
from mvgdepartures import Departures


def test_basic():
    departures = Departures("Marienplatz")
    assert len(departures.__str__()) != 0, "the output is empty"
