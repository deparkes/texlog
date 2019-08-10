import unittest
from freezegun import freeze_time


from datetime import datetime
import pytest
from src.texlog import texlog

FAKE_TIME = datetime(2020, 12, 25, 17, 5, 55)

class TestSection(unittest.TestCase):
    def test_init(self):
        section = texlog.Section('filename')

    @freeze_time("2019-08-09 21:55")
    def test_get_data_no_data(self):
        section = texlog.Section('filename')
        headers, values = section.get_data()
        self.assertEqual(headers, ['Date'])
        self.assertEqual(values, ['2019-08-09 21:55'])

    @freeze_time("2019-08-09 21:55")
    def test_get_data_with_data(self):
        section = texlog.Section('filename')
        section.data = ['heading1,:data1', 'heading2,:data2']
        headers, values = section.get_data()
        self.assertEqual(headers, ['Date', 'heading1', 'heading2'])
        self.assertEqual(values, ['2019-08-09 21:55', 'data1', 'data2'])