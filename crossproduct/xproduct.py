#!/usr/bin/env python3
#coding:utf-8

"""
Cross Product

This program accepts two comma separated vectors in R3 and computes their cross
product.

usage: ./xproduct v1 v2

The formula for the cross products of vectors u and v is given by:

    u x v = (u2v3 - u3v2, u3v1 - u1v3, u1v2 - u2v1)

or in determinant form:

    |u2 u3|  |u3 u1|  |u1 u2|
    |v2 v3|, |v3 v1|, |v1 v2|
"""

import sys

def xproduct(u, v):
    """
    xproduct computes the cross product u x v.

    Input:
        u, v ([3]Number): Two vectors in R3

    Output:
        A vector w = u x v in R3

    Examples:
        >>> xproduct([1, 2, -2], [3, 0, 1])
        [2, -7, -6]
    """
    # Extremely straightforward constant time operations
    c1 = u[1]*v[2] - u[2]*v[1]
    c2 = u[2]*v[0] - u[0]*v[2]
    c3 = u[0]*v[1] - u[1]*v[0]

    return [c1, c2, c3]

# Accepts a comma-separated list of numbers and produces a vector in list form
# Strings are parsed as floats and then converted to integers if possible.
def _parse_vector(vecstring):
    """
    >>> parse_vector("1,2,3")
    """
    v = [float(s) for s in vecstring.split(',')]

    return [int(f) for f in v if f.is_integer()]

# Converts a vector of the form [v1, v2, ..., vn] to a string of the form:
# (v1, v2, ..., vn)
def _vstr(v):
    return f'({",".join([str(i) for i in v])})'

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f'usage: {sys.argv[0]} v1 v2')

        exit(1)

    u = _parse_vector(sys.argv[1])
    v = _parse_vector(sys.argv[2])

    # TODO: Find a more elegant output.
    print(f'{_vstr(u)} x {_vstr(v)} = {_vstr(xproduct(u, v))}')


