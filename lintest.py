"""lintest

   A simple program that accepts a list of data points and computes the slope
   between successive pairs of points.

   TODO: Have this read in files in the 'gnuplot' (tsv) format
   TODO: Good candidate for doc tests
"""

def computeSlope(a, b):
  """computeSlope is the slope of the line passing through points a and b.

    Parameters:
      a, b (float, float): Tuples whose elements correspond to the x and y
      values of the points a and b, respectively.

    Output:
      The slope of the line passing through a and b

    Raises:
      ZeroDivisionError: if a[0] = b[0]

    Example:
      >>> computeSlope((11, 68), (11.25, 85))
      68.0
  """

  if a[0] == b[0]:
    raise ZeroDivisionError(a, b)

  return (a[1] - b[1]) / (a[0] - b[0])

def slopes(points):
  """
    slopes computes the pairwise slopes between adjacent [points].

    Parameters:
      points ([](float, float)): A list of points.

      NOTE: Points are not sorted according to their x-coordinates, and as such
      the slopes between points are naively computed.

    Output:
      A list whose entry [i] is the slope between points[i] and points[i+1]

    Example:
      >>> slopes([
      ...  (11, 68),
      ...  (11.25, 85),
      ...  (11.5, 101),
      ...  (11.75, 117),
      ...  (12.75, 185)
      ... ])
      [68.0, 64.0, 64.0, 68.0]
  """

  n = len(points)

  return [computeSlope(points[i], points[i+1]) for i in range(n-1)]
