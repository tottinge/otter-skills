import unittest
import bootstrap
from catalog import catalog_key


class CatalogTest(unittest.TestCase):
    def test_key_prefix(self):
        self.assertTrue(catalog_key("abc").startswith("item:"))
