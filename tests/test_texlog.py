import unittest
from src.texlog import texlog
class TestSection(unittest.TestCase):
    def test_init(self):
        section = texlog.Section('filename')
