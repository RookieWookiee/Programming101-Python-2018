import unittest
from unittest.mock import Mock, patch, mock_open
from performance import performance
import os
import time

class TestPerf(unittest.TestCase):
    def test_happy_path(self):
        file_mock = mock_open()
        with patch('builtins.open', file_mock), \
                patch('time.time') as time_mock, \
                patch('performance.datetime') as dt_mock:
            dt_mock.now.return_value = 1
            time_mock.side_effect = [1, 2]
            with performance('test, doesnt matter'):
                time.sleep(0.01)

        handle = file_mock()
        handle.write.assert_called_with('1. Execution time: 1\n')
