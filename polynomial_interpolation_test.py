#!/usr/env/bin python3
#coding: utf-8

import unittest

from polynomial_interpolation import difference_quotient

class TestDifferenceQuotient(unittest.TestCase):
    def test_standard(self):
        self.assertEqual(difference_quotient([(0, 1), (4, 3)]), 0.5)
        self.assertEqual(difference_quotient([(0, 1), (4, 3), (5, 2)]), 0.5)
