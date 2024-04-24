#!/usr/env/bin python3
#coding: utf-8

import unittest

from polynomial_interpolation import interpolate, difference_quotient

class TestDifferenceQuotient(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(difference_quotient([(0, 1), (4, 3)]), 0.5)
        self.assertEqual(difference_quotient([(0, 1), (4, 3), (5, 2)]), -0.3)

    def test_approx(self):
        self.assertAlmostEqual(difference_quotient([(-3.0, -5.0), (-2.0, -1.1), (2.0, 1.9), (3.0, 4.8)]), 0.1767, places=4)

class TestInterpolate(unittest.TestCase):
    # some kind of unknown cubic function, or close to it
    def test_cubic(self):
        points = [
            (-3.0, -5.0),
            (-2.0, -1.1),
            (2.0, 1.9),
            (3.0, 4.8)
        ]

        zs = [-2.5, 0.0, 2.5]

        interpolate(points, zs)
