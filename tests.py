from mvgdepartures import Departures
from unittest import TestCase


class DeparturesTest(TestCase):
    def test_basic(self):
        departures = Departures("Marienplatz")
        assert len(departures.__str__()) != 0, "the output is empty"
