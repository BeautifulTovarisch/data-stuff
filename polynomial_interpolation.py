#!/usr/bin/env python3
#coding: utf-8

"""
Polynomial Interpolation

This program constructs an interpolating polynomial used to approximate some
function at a point z. The general algorithm works by computing the difference
quotients between n-1 interpolating points.
"""

def difference_quotient(points):
    """
    difference_quotient computes the pairwise difference quotients given a set
    of points x1, x2, ... and their corresponding values. The algorithm used is
    a straightforward divide-and-conquer routine.

    Input:
        points [](float, float): A list of tuples corresponding to the known
        values of some function.

    Output:
        The difference quotient obtained by computing the pairwise difference
        quotients of each x_i, x_j in points and then combining each result.

    Examples:
        >>> difference_quotient([(0, 1), (4, 3)])
        0.5

        >>> difference_quotient([(0, 1), (4, 3), (5, 2)])
        -0.4
    """
    if not points:
        raise ValueError("points must not be empty")

    n = len(points)

    if n == 1:
        return points[0][1]

    mid = n//2

    left = points[:n-1]
    right = points[1:n]

    # We only care about the value of f(x) here
    lquot = difference_quotient(left)
    rquot = difference_quotient(right)

    a, _ = points[0]
    b, _ = points[n-1]

    # The denominator is always the endpoints of the current interval.
    dquot = (rquot - lquot) / (b - a)

    return dquot

# Output an array A, such that A[i] = the product of (z-x_0)(z-x_1)...(z-x_i)
# These form the terms of the linear combination used in the interpolate proc.
def _compute_terms(xs, z):
    n = len(xs)

    A = [1 for _ in range(n+1)]
    for i in range(1, n+1):
        A[i] = A[i-1]*(z - xs[i-1])

    return A

# Perform the interpolation algorithm on a single point.
def _single_point(coefficients, terms):
    return sum([c*t for c in coefficients for t in terms])

def interpolate(known_pts, unknown_pts):
    """
    interpolate approximates the value of a function f at each z in [zs] using
    polynomial interpolation.

    Input:
        known_pts [](float, float): A list of tuples associating the points
        x for which f is known and the corresponding value of f(x).

        unknown_pts ([]float): The desired points at which f(z) is to be
        approximated

    Output:
        A list of real numbers corresponding to the points given in [zs].

    Examples:
        # >>> xs = [-3.0, -2.0, 2.0, 2.0]
        # >>> ys = [-5.0, -1.1, 1.9, 4.8]
        # >>> zs = [-2.5, 0, 2.5]
        # >>> interp_recur(list(zip(xs, ys)), zs)
        # [-2.694, 0.8000, 3.044]
    """

    n = len(known_pts)

    coefs = [difference_quotient(known_pts[:i+1]) for i in range(n)]

    for z in unknown_pts:
        terms = _compute_terms([x for x, _ in known_pts], z)
        print(_single_point(coefs, terms))

    return []
