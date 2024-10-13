#!/usr/bin/env python3
#coding: utf-8

"""
Eliminator

This program provides a basic interactive session for performing elementary row
operations on a given matrix. Each input performs one operation (for now) on an
input matrix and prints the result of the operation. Three row operations are
allowed:

    1. Swap row i with row j        (i != j)
    2. Scale row i by constant c    (c != 0)
    3. Scale row i and add to row j (i != j)

While a more sophsticated program could simply perform all of these operations
until the matrix was in row echelon form, the purpose of this tool is to teach
the principles of elimination while avoiding the tedious arithmetic ordinarily
done by hand.

NOTE: For all operations, rows are indexed starting at 1.
"""

# TODO: find a nice way to build CLI tools

# TODO: Consider updating to return T/F instead of throwing.
def check_row(i, maxRow):
    if i < 1 or i > maxRow:
        msg = f'invalid row: {i}. rows must be between 1 and {maxRow}'
        raise IndexError(msg)

# Print the rows of A
def printm(A):
    for row in A:
        for entry in row:
            print(entry, end='\t')

        print()

def scale(A, i, c):
    """
    scale performs scalar multiplication on row [i] in [A].

    Input:
        A ([][]int): An m x n matrix with integer entries.
        i (int): The row to be scaled
        c (int): A nonzero scalar

    Raises:
        IndexError: If [i] is invalid
        ValueError: if [c] == 0

    Examples:
        >>> A = []
        >>> scale(A, 0, 0)
        Traceback (most recent call last):
            ...
        ValueError: scalar must not equal 0

        >>> A = [[1, 2, 3]]
        >>> scale(A, 0, 10)
        Traceback (most recent call last):
            ...
        IndexError: invalid row: 0. rows must be between 1 and 1

        >>> scale(A, 2, 10)
        Traceback (most recent call last):
            ...
        IndexError: invalid row: 2. rows must be between 1 and 1

        >>> scale(A, 1, 5)
        >>> A
        [[5, 10, 15]]

        >>> A = [
        ... [3, 1, 2],
        ... [-1, 2, -1],
        ... [7, -3, 4],
        ... [0, 0, 0]
        ... ]
        >>> scale(A, 1, 2)
        >>> A
        [[6, 2, 4], [-1, 2, -1], [7, -3, 4], [0, 0, 0]]

        >>> scale(A, 3, 1/2)
        >>> A[2]
        [3.5, -1.5, 2.0]
    """
    if not c:
        raise ValueError('scalar must not equal 0')

    check_row(i, len(A))

    A[i-1] = [c*a for a in A[i-1]]

def combine(A, i, j, c):
    """
    combine scales row [i] of [A] and adds the resulting vector to row [j]. Row
    [i] is not updated.

    Input
        A ([][]int): An m x n matrix of integers
        i (int): The row to be scaled and added
        j (int): The row to be updated

    Raises:
        IndexError: if [i] or [j] is invalid
        Exception: if [i] == [j]

        ValueError: if [c] == 0

    Examples:
        >>> A = [
        ... [1, 2, -5, 3, 6, 14],
        ... [0, 0, -2, 0, 7, 12],
        ... [2, 4, -5, 6, -5, -1] # Eliminate leading coefficient in this row
        ... ]
        >>> combine(A, 1, 3, -2)
        >>> A
        [[1, 2, -5, 3, 6, 14], [0, 0, -2, 0, 7, 12], [0, 0, 5, 0, -17, -29]]
    """
    if not c:
        raise ValueError('scalar must not equal 0')

    n = len(A)

    check_row(i, n)
    check_row(j, n)

    # scale row [i]
    vec = [c*a for a in A[i-1]]

    A[j-1] = [vec[col]+A[j-1][col] for col in range(len(vec))]

def swap(A, i, j):
    """
    swap exchanges row [i] in [A] with row [j].

    Input
        A ([][]int): An m x n matrix of integers
        i,j (int): Row numbers to be exchanged. Rows are indexed beginning at 1

    Raises:
        IndexError: if [i] or [j] is invalid
        Exception: if [i] == [j]

    Examples:
        >>> A = []
        >>> swap(A, 1, 1)
        Traceback (most recent call last):
            ...
        Exception: cannot exchange row with itself

        >>> A = []
        >>> swap(A, 0, 1)
        Traceback (most recent call last):
            ...
        IndexError: invalid row: 0. rows must be between 1 and 0

        >>> A = [
        ... [1, 2, 3]
        ... ]
        >>> swap(A, 1, 2)
        Traceback (most recent call last):
            ...
        IndexError: invalid row: 2. rows must be between 1 and 1

        >>> A = [
        ... [1, 2, 3],
        ... [4, 5, 6],
        ... [7, 8, 9]
        ... ]

        >>> swap(A, 1, 2)
        >>> A
        [[4, 5, 6], [1, 2, 3], [7, 8, 9]]

        >>> swap(A, 2, 3)
        >>> A
        [[4, 5, 6], [7, 8, 9], [1, 2, 3]]
    """
    if i == j:
        # No reason to throw this except to reinforce the rules of elimination
        raise Exception("cannot exchange row with itself")

    n = len(A)

    # Reminds me of old-school assert statements
    check_row(i, n)
    check_row(j, n)

    # Account for row indexing
    i -= 1
    j -= 1

    A[i], A[j] = A[j], A[i]

def reduce(A):
    """
    reduce performs elementary row operations on [A] until it is in row-echelon
    form.

    TODO: This is a fairly confusing function with seemingly endless edge cases.
    I should review a proper implementation and compare my approach.

    Input:
        A (Matrix): An mxn matrix

    Output:
        A reduced to row-echelon form

    Examples:
        >>> reduce([[0, 0], [0, 0]])
        [[0, 0], [0, 0]]

        >>> reduce([[1, 0], [0, 1]])
        [[1, 0], [0, 1]]

        >>> reduce([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
        [[1, 0, 0], [0, 0, 1], [0, 0, 0]]

        >>> reduce([[4, -4], [-2, 2]])
        [[1, -1], [0, 0]]

        >>> reduce([[4, 0, 1], [-2, 1, 0], [-2, 0, 1]])
        [[1, 0, 0.25], [0, 1, 0.5], [0, 0, 1]]

        >>> reduce([[1, 0], [0, 0], [0, -1], [2, 0]])
        [[1, 0], [0, 1], [0, 0], [0, 0]]

        >>> reduce([[0, 0, 0, 1], [1, 0, 1, 0]])
        [[1, 0, 1, 0], [0, 0, 0, 1]]

        >>> reduce([[1, -3, 3], [3, -5, 3], [6, -6, 4]])
        [[1, -3, 3], [0, 1, -1.5], [0, 0, 1]]
    """
    def place_pivot(A, pidx, i):
        # Find the index of the next pivot, if any
        for j in range(i, len(A)):
            if A[j][i]:
                A[pidx],A[j] = A[j],A[pidx]
                break

        return A[pidx][i]

    B = [[col for col in row] for row in A]

    rows = len(A)
    cols = len(A[0])

    # We can only ever produce at most [rank] pivot rows
    maxrank = min(rows, cols)

    # Algorithm:
    #   Locate pivot if A[i][i] is 0, moving such occurrences to the bottom
    #       If there is no such row, skip
    #   Eliminate rows using combine()
    #   Repeat until all pivots are located or remaining rows are all zero.
    pidx = 0
    for i in range(maxrank):
        pivot = place_pivot(B, pidx, i)
        if not pivot:
            continue

        pidx += 1
        B[i] = [1/pivot*b for b in B[i]]
        B[i] = [int(b) if b.is_integer() else b for b in B[i]]

        for j in range(i+1, rows):
            if not B[j][i]:
                continue

            p = B[j][i]
            for k in range(i, cols):
                entry = -p*B[i][k] + B[j][k]

                B[j][k] = int(entry) if entry.is_integer() else entry

    return B

if __name__ == "__main__":
    print()
    # TODO:
    #   Parse input matrix
    #   Design commands
    #   Parse commands and evaluate (simple "repl")
    #   Handle CTRL+C (optional)
