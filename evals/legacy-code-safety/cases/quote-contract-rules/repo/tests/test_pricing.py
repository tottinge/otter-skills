import unittest
from types import SimpleNamespace
from pricing import quote


class PriceTest(unittest.TestCase):
    def test_quote(self):
        offer = SimpleNamespace(eligible="no", rate=0.1)
        self.assertGreater(quote(100, "customer", lambda _: offer), 0)
