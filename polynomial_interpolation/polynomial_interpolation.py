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

    A = [1 for _ in range(n)]
    for i in range(1, n):
        A[i] = A[i-1]*(z - xs[i-1])

    return A

# Perform the interpolation algorithm on a single point.
def _single_point(coefficients, terms):
    return sum([coefficients[i]*terms[i] for i in range(len(terms))])

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
        A list of approximations corresponding to the points in [unknown_pts].

    Examples:
    """
    n = len(known_pts)
    m = len(unknown_pts)

    soln = [0 for _ in range(m)]

    # Coefficients can be computed once and reused for subsequent approximations
    coefs = [difference_quotient(known_pts[:i+1]) for i in range(n)]

    for i in range(m):
        terms = _compute_terms([x for x, _ in known_pts], unknown_pts[i])
        soln[i] = _single_point(coefs, terms)

    return soln
