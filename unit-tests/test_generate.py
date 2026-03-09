import unittest

import sys
sys.path.append('app')
from app.generate import formatLinks

class TestGenerate(unittest.TestCase):

    def test_formatLinks_emptyList(self):
        """Should return empty string when links list is empty"""
        result = formatLinks([])
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
