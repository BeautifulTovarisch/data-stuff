#!/usr/bin/env python3
#coding: utf-8

"""
Least Squares

This program computes a best-fit linear regression through a set of n points
using the least squares method. The overall objective is to provide acceptable
estimates for the slope and intercept of a linear equation.

TODO: Explain better.

NOTE: Compare this to the technique in lintest.py, which constructs a similar
approximation.
"""

def conjectureSlope(points, xSum, ySum):
    """
    conjectureSlope approximates the slope of a linear equation given a set of
    points. This computation is used to estimate the y-intercept of the linear
    regression.

    Input:
        points [](float, float): A set of coordinates to be used to estimate a
        slope.

        xSum, ySum (float): The sum of the x and y coordinates, respectively.

    Output:
        The conjectured slope.

    Examples:
        >>> points = [
        ... (-4.0, -3.0),
        ... (-3.0, -1.0),
        ... (-2.0, -2.0),
        ... (-1.5, -0.5),
        ... (-0.5, 1.0),
        ... (1.0, 0),
        ... (2.0, 1.5),
        ... (3.5, 1.0),
        ... (4.0, 2.5)
        ... ]
        >>> xSum = sum([x for x, _ in points])
        >>> ySum = sum([y for _, y in points])
        >>> conjectureSlope(points, xSum, ySum)
        0.551931330472103
    """

    n = len(points)

    # TODO: Populate a matrix or compute multiple values at once.
    xySum = sum([x*y for x, y in points])
    xSqSum = sum([x*x for x, _ in points])
    xSumSq = xSum**2

    num = n*xySum - xSum*ySum
    denom = n*xSqSum - xSumSq

    if denom == 0:
        raise ZeroDivisonError(num, denom)

    return num/denom

# This forumula does not require the points themselves, as the previously
# computed xSum and ySum and be reused here. As a consequence, it is better to
# simply provide [n] as a parameter.
def conjectureIntercept(slope, n, xSum, ySum):
    """
    conjectureIntercept approximates the y-intercept using the slope estimated
    by [conjectureSlope].

    Input:
        slope (float): The slope estimated by the least squares method

        n: The number of points.

        xSum, ySum: The sum of the x and y coordinates, respectively.

    Output:
        The conjectured y-intercept of the points.

    Examples:
        >>> n = 9
        >>> slope = 0.551931330472103
        >>> xSum = -0.50
        >>> ySum = -0.50

        >>> conjectureIntercept(slope, n, xSum, ySum)
        -0.024892703862660945
    """

    num = ySum - (slope*xSum)

    return num/n
