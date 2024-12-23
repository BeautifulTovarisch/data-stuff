#!/usr/bin/env python3
#coding: utf-8

"""
Matrix Operations

This module performs basic matrix arithmetic operations. Each operation checks
the input matrices for validity, throwing an exception if the operation cannot
be performed.

TODO: Develop a 'language' that makes these operations even easier.
"""

from math import sqrt

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

# Also called the magnitude of [u].
def norm(u):
    """
    norm computes the magnitude of [u] given by:

    ||u|| = sqrt(u1^2 + u2^2 + ... + un^2)

    Input:
        u (Vector): An nx1 vector

    Output:
        The magnitude of [u]

    Examples:
        >>> norm([1, 0])
        1.0

        >>> c = norm([1, 1])
        >>> c - sqrt(2)
        0.0
    """

    return sqrt(sum([a**2 for a in u]))

def magsquare(u):
    """
    magsquare computes the square of the magnitude of [u].

    Input:
        u (Vector): An nx1 vector

    Output:
        The magnitude of [u] squared
    """
    return sum([a**2 for a in u])

def normalize(u):
    """
    normalize produces a unit vector from [u] by scaling the components of [u]
    by the reciprocal of its magnitude.

    Input:
        u (Vector): A non-zero vector

    Output:
        The unit vector obtained by normalizing [u]

    Examples:
        >>> normalize([1, 0, 0])
        [1.0, 0.0, 0.0]

        >>> normalize([3, 4, 0])
        [0.6, 0.8, 0.0]

        >>> normalize([0, 0, 0])
        Traceback (most recent call last):
            ...
        ValueError: u must be a non-zero vector
    """
    k = norm(u)

    if not k:
        raise ValueError("u must be a non-zero vector")

    return [c * 1/k for c in u]

def vadd(u, v):
    return [u[i] + v[i] for i in range(len(u))]

def vsub(u, v):
    return [u[i] - v[i] for i in range(len(u))]

def vscale(u, k):
    return [a*k for a in u]

# TODO: Document the precise operation that happens here. Should have read more
# closely.
def project(u, v):
    """
    project computes the orthogonal project of [u] onto [v] given by:

        <u, v>/||v||^2 * v

    in other words, [v] scaled by the ratio of the inner product of [u] and [v]
    to the square of the magnitude of [v].

    Input:
        u, v (Vector): Vectors in some inner product space

    Output:
        The orthognal projection of [u] onto [v].

    Examples:
    """
    dotp = _dot(u, v)
    c = dotp / magsquare(v)

    return vscale(v, c)

# TODO: Generalize to an arbitrary inner product space
def gramschmidt(basis):
    """
    gramschmidt converts [basis] into an orthogonal basis using the Gram-Schmidt
    process. The G-S algorithm can be described by the recurrence:

        v_i     = u1 if i = 1
                = u_i - sum(proj(u_i) v_k for k in 1 to i-1)

    where proj(u) is given by <u, v_k>/||v_k||^2

    NOTE: That this procedure does not normalize the resulting basis.

    Input:
        basis ([]Vector): A nonempty set of vectors forming a basis.

    Output:
        A list of vectors comprising an orthgonal basis

    Examples:
        >>> gramschmidt([])
        Traceback (most recent call last):
            ...
        ValueError: basis must be nonempty

        >>> gramschmidt([[1, 0, 1]])
        [[1, 0, 1]]

        >>> gramschmidt([[3, -5], [1, 0]])
        [[1, 0], [0.0, -5.0]]
    """
    if not basis:
        raise ValueError('basis must be nonempty')

    if len(basis) == 1:
        return basis

    # This gives us v1, v2, ..., vn to use in the computation of the ith vector
    orthobasis = gramschmidt(basis[1:])

    u = basis[0]

    # Subtract the orthogonal projection of u onto the current orthgonal basis.
    for v in [project(u, v) for v in orthobasis]:
        u = vsub(u, v)

    return orthobasis + [u]

def matprod(A, u, v):
    """
    matprod computes the matrix inner product <u, v> using the inner product
    space generated by [A]:

    Au dot Av

    Input:
        A (Matrix): An mxn matrix
        u,v (Vector): nx1 column vectors

    Output:
        The matrix inner product <u, v>

    Examples:
        >>> matprod([[1, 0], [0, 1]], [1, 2], [3, 4])
        11

        >>> matprod([[2, 1], [1, 1]], [3, 2], [1, 1])
        34

        >>> matprod([[2, 1], [1, 1]], [3, 2], [0, -1])
        -13
    """
    return _dot(matvec(A, u), matvec(A, v))

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

def trans(A):
    """
    trans computes the transpose of [A].

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
        >>> trans(A)
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
    T = trans(A)

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

        >>> A = [
        ... [6, -2, 4],
        ... [0, 1, 3],
        ... [7, 7, 5]
        ... ]
        >>> v = [4, 3, 5]
        >>> matvec(A, v)
        [38, 18, 74]
    """

    # Since row and column vectors are represented the same way, we compare
    # against the 'columns'
    check_dim(A, [v], lambda _, b, _2, d: b == d)

    return [_dot(row, v) for row in A]

def classic_multiply(A, B):
    """
    classic_mulitply performs a cache-unfriendly, O(n^3) matrix multiplication
    using the standard triple-loop with no intelligent tricks.

    Input:
        A (Matrix): An mxn matrix
        B (Matrix): An nxl matrix

    Output:
        The mxl matrix obtained via matrix multiplication of [A] and [B].

    Examples:
        >>> A = [
        ... [1, 2],
        ... [2, 1],
        ... ]
        >>> B = [
        ... [1, 0],
        ... [0, 1],
        ... ]
        >>> classic_multiply(A, B)
        [[1, 2], [2, 1]]

        >>> A = [
        ... [3, 1],
        ... [2, 1]
        ... ]
        >>> classic_multiply(classic_multiply(A, A), A)
        [[41, 15], [30, 11]]
    """

    check_dim(A, B, lambda _, b, c, _2: b == c)

    m = len(A)
    n = len(A[0])
    l = len(B[0])

    # Output matrix is mxl
    C = [[0 for _ in range(l)] for _ in range(m)]

    for i in range(m):
        entry = 0
        for k in range(l):
            for j in range(n):
                C[i][k] += A[i][j] * B[j][k]

    return C

# TODO: This procedure is horribly wrong for certain inputs. Review later.
def rc_multiply(A, B):
    """
    rc_multiply performs the matrix multiplication AB by row-column partitions:

        A = [c1 c2 c3 ... cn]
        B = [r1 r2 r3 ... rn]

    and computing the matrix summation:

        c1r1 + c2r2 + ... cnrn

    Input:
        A (Matrix): An mxn matrix
        B (Matrix): An nxl matrix

    Output:
        The mxl matrix obtained via matrix multiplication of [A] and [B].

    Examples:
        >>> A = [
        ... [1, 2],
        ... [2, 1],
        ... ]
        >>> B = [
        ... [1, 0],
        ... [0, 1],
        ... ]
        >>> rc_multiply(A, B)
        [[1, 2], [2, 1]]

        >>> A = [
        ... [3, 1],
        ... [2, 1]
        ... ]
        >>> rc_multiply(rc_multiply(A, A), A)
        [[41, 15], [30, 11]]
    """

    check_dim(A, B, lambda _, b, c, _2: b == c)

    # Easier to iterate over columns of [A].
    aT = trans(A)

    r = len(A)
    c = len(B[0])

    C = [[0 for _ in range(c)] for _ in range(r)]

    # This approach screams parallelizable.
    for i in range(r):
        # Form a linear combination of the rows of B with coefficients given by
        # the columns of A.
        partial = [[a * b for b in B[i]] for a in aT[i]]

        C = mat_add(C, partial)

    return C

def normaleqn(A, b):
    """
    normaleqn returns an augmented matrix representing the normal equation
    associated with [A]x = [b]. The resulting matrix is typically then solved
    to find least squares solutions.

    Input
        A (Matrix): An mxn matrix
        b (Vector): An mx1 vector

    Output:
        An mxm matrix augmented with an mx1 vector encoding a linear system.

    Examples:
        >>> normaleqn([[1, -1], [2, 3], [4, 5]], [2, -1, 5])
        [[21, 25, 20], [25, 35, 20]]

        >>> normaleqn([[2, -1, 0], [3, 1, 2], [-1, 4, 5], [1, 2, 4]], [-1, 0, 1, 2])
        [[15, -1, 5, -1], [-1, 22, 30, 9], [5, 30, 45, 13]]
    """

    T = trans(A)
    mat = classic_multiply(T, A)
    vec = matvec(T, b)

    # Augment TA with the corresponding element in Tb
    return [mat[i] + [vec[i]] for i in range(len(vec))]
