#!/usr/bin/env python3
#coding: utf-8

"""
Matrix Operations

This module performs basic matrix arithmetic operations. Each operation checks
the input matrices for validity, throwing an exception if the operation cannot
be performed.

TODO: Develop another 'language' that makes these operations even easier.
"""

def check_dim(A, B, fn):
    if not A or not B:
        raise ValueError("Both matrices must be defined")

    rowA, colA = len(A), len(A[0])
    rowB, colB = len(B), len(B[0])

    if not fn(rowA, colA, rowB, colB):
        msg = f'invalid dimensions for A: {rowA}x{colA} B: {rowB}x{colB}'

        raise ValueError(msg)

# Compute the dot product of A * B
def _dot(A, B):
    return sum([A[i]*B[i] for i in range(len(A))])

def mat_scale(A, c):
    """
    mat_scale scales the entries in [A] by constant [c].

    Input:
        A (Matrix): A matrix with integer entries

    Output:
        The matrix obtained by multiplying each entry of [A] by [c].

    Examples:
        >>> A = [
        ... [1, 0, 2],
        ... [3, 9, -3],
        ... [4, 6, 11]
        ... ]
        >>> mat_scale(A, 2)
        [[2, 0, 4], [6, 18, -6], [8, 12, 22]]

        >>> A = [
        ... [3, 0],
        ... [-1, 2],
        ... [1, 1]
        ... ]
        >>> mat_scale(A, 5)
        [[15, 0], [-5, 10], [5, 5]]

        >>> A = [
        ... [1, 4, 2],
        ... [3, 1, 5],
        ... ]
        >>> mat_scale(A, -7)
        [[-7, -28, -14], [-21, -7, -35]]
    """
    if not A:
        return A

    return [[entry * c for entry in row] for row in A]

def mat_add(A, B):
    """
    mat_add computes [A] + [B], that is, the sum of the entries of [A] and the
    corresponding entries of [B].

    Input:
        A, B (Matrix): Matrices of the same dimension

    Output:
        The matrix given by the operation [A] + [B].

    Raises:
        ValueError: if the dimensions of [A] and [B] are different.

    Examples:
        >>> A = [
        ... [1, 5, 2],
        ... [-1, 0, 1],
        ... [3, 2, 4]
        ... ]
        >>> B = [
        ... [6, 1, 3],
        ... [-1, 1, 2],
        ... [4, 1, 3]
        ... ]
        >>> mat_add(A, B)
        [[7, 6, 5], [-2, 1, 3], [7, 3, 7]]
    """

    # Must have equal dimensions
    check_dim(A, B, lambda a, b, c, d: a == c and b == d)

    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def mat_sub(A, B):
    """
    mat_add computes [A] - [B], that is, the difference of the entries of [A]
    and the corresponding entries of [B].

    Input:
        A, B (Matrix): Matrices of the same dimension

    Output:
        The matrix given by the operation [A] - [B].

    Raises:
        ValueError: if the dimensions of [A] and [B] are different.

    Examples:
        >>> A = [
        ... [8, -2],
        ... [0, 4]
        ... ]
        >>> mat_sub(A, A)
        [[0, 0], [0, 0]]

        >>> A = [
        ... [1, 5, 2],
        ... [-1, 0, 1],
        ... [3, 2, 4]
        ... ]
        >>> B = [
        ... [6, 1, 3],
        ... [-1, 1, 2],
        ... [4, 1, 3]
        ... ]
        >>> mat_sub(A, B)
        [[-5, 4, -1], [0, -1, -1], [-1, 1, 1]]

        >>> A = [
        ... [8, -2],
        ... [0, 4]
        ... ]
        >>> B = [
        ... [1, 4, 2],
        ... [3, 1, 5]
        ... ]
        >>> mat_sub(A, B)
        Traceback (most recent call last):
            ...
        ValueError: invalid dimensions for A: 2x2 B: 2x3
    """

    # Must have equal dimensions
    check_dim(A, B, lambda a, b, c, d: a == c and b == d)

    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def tr(A):
    """
    tr computes the transpose of [A].

    Input:
        A (Matrix): A matrix with integer entries

    Output:
        The transpose of [A].

    Examples:
        >>> A = [
        ... [3, 0],
        ... [-1, 2],
        ... [1, 1]
        ... ]
        >>> tr(A)
        [[3, -1, 1], [0, 2, 1]]
    """
    if not A:
        return A

    return [[A[col][row] for col in range(len(A))] for row in range(len(A[0]))]

def vecmat(v, A):
    """
    vecmat computes the multiplication of vector [v] by matrix [A]. [v] must be
    a row vector with length equal to the number of columns in [A].

    Input:
        v (Vector): A row vector with length equal to the columns of [A]
        A (Matrix): An mxn matrix

    Output:
        A row vector equal in length to [v] obtained by the product [v]x[A].

    Examples:
        >>> v = [3, -2, 7]
        >>> A = [
        ... [6, -2, 4],
        ... [0, 1, 3],
        ... [7, 7, 5]
        ... ]
        >>> vecmat(v, A)
        [67, 41, 41]

        >>> v = [0, 4, 9]
        >>> A = [
        ... [6, -2, 4],
        ... [0, 1, 3],
        ... [7, 7, 5]
        ... ]
        >>> vecmat(v, A)
        [63, 67, 57]
    """

    check_dim([v], A, lambda _, b, c, _2: b == c)

    # TODO: Awful. Refactor later to avoid this step.
    T = tr(A)

    return [_dot(v, row) for row in T]

def matvec(A, v):
    """
    matvec computes the product [A]x[v], where [v] is a column vector with size
    equal to the number of columns of [A].

    NOTE: That a column vector has identical representation to a row vector.

    Input:
        A (Matrix): An mxn matrix with integer entries
        v (Vector): A column vector with length equal to the columns of [A]

    Output:
        A column vector equal in length to [v] obtained by the product [A]x[v].

    Examples:
        >>> A = [
        ... [3, -2, 7],
        ... [6, 5, 4],
        ... [0, 4, 9]
        ... ]
        >>> v = [-2, 1, 7]
        >>> matvec(A, v)
        [41, 21, 67]

        >>> A = [
        ... [6, -2, 4],
        ... [0, 1, 3],
        ... [7, 7, 5]
        ... ]
        >>> v = [3, 6, 0]
        >>> matvec(A, v)
        [6, 6, 63]
    """

    # Since row and column vectors are represented the same way, we compare
    # against the 'columns'
    check_dim(A, [v], lambda _, b, _2, d: b == d)

    return [_dot(row, v) for row in A]
