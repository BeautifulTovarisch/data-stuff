"""lintest

  Functions which provide helpful computations when determining whether a data
  set might be approxiately modeled as a linear function.
"""

import os.path

def slope(a, b):
  """slope is the slope of the line passing through points a and b.

    Parameters:
      a, b (float, float): Tuples whose elements correspond to the x and y
      values of the points a and b, respectively.

    Output:
      The slope of the line passing through a and b

    Raises:
      ZeroDivisionError: if a[0] = b[0]

    Example:
      >>> slope((11, 68), (11.25, 85))
      68.0
  """

  if a[0] == b[0]:
    raise ZeroDivisionError(a, b)

  return (a[1] - b[1]) / (a[0] - b[0])

def readPoints(filename, header=False):
  """
  readPoints attempts to parse [filename] and produce a list of ordered pairs.
  [filename] should be a gnuplot-style text file with optional labels as the
  first line.

  NOTE: For now I only care about single-variable functions, but this should
  generalize to multivariate data as well.

  Parameters:
    filename (string): The path to a file containing data columns representing
    points. The file should be structured as follows:

    XLABEL  YLABEL  # (OPTIONAL)
    x1      y1
    x2      y2
    x3      y3
    ...     ...

    where each column is separated by whitespace. This corresponds to the
    format expected by gnuplot.

    See: http://www.gnuplot.info/docs_4.2/node101.html

    header (boolean): If header is True, then the first line containing the
    optional data labels will be skipped. This program does not make use of the
    x and y labels.

  Output:
    A list of ordered pairs whose x-values correspond to the first column and
    whose y-values correspond to the second column.

  Raises:
    FileNotFoundError: If [filename] does not exist.
    TODO: More validation?
  """
  def parseLine(line):
    d = line.split()

    return (float(d[0]), float(d[1]))

  if not os.path.exists(filename):
    raise FileNotFoundError(filename)

  with open(filename, 'r') as data:
    lines = list(data)[1:] if header else list(data)

    return [parseLine(line) for line in lines]

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

  return [slope(points[i], points[i+1]) for i in range(n-1)]

def yIntercept(point, m):
  """yIntercept computes the vertical intercept b in the eqn
     y = mx + b given a [point] and slope [m].

    Parameters:
      point (float, float): A tuple representing a point in the plane.
      m (float): The slope of line

    Output:
      The point (0, b) that intercepts the y-axis.

    Example:
      Suppose we are given points (1, 2) and (6, 3). Then,

      >>> m = slope((1, 2), (6, 3))
      >>> yIntercept((1, 2), m)
      1.8
  """
  x, y = point

  return y - m * x

def conjectureSlope(slopes):
  """conjectureSlope is the average of a list of slopes through successive points.

    Parameters:
      slopes ([]float): A list of slopes between successive points p_i, p_i+1

    Output:
      The arithmetic mean of the slopes. If slopes is empty, then 0 is returned

    Example:
      >>> conjectureSlope([
      ... 68.0,
      ... 64.0,
      ... 64.0,
      ... 68.0
      ... ])
      66.0

      >>> conjectureSlope([])
      0
  """
  if not slopes:
    return 0

  return sum(slopes) / len(slopes)

def conjectureIntercept(points, conjecturedSlope):
    """conjectureIntercept computes the y-intercept for each point p in [points]
       and returns the arithmetic mean

      Parameters:
        points ([](float, float)): A list of points in the plane
        conjecturedSlope (float): The average of pairwise slopes computed from
        a sequence of successive points.

      Output:
        The arithmetic mean of the y-intercepts of each point in [points].

      Example:
        >>> m = conjectureSlope([
        ... 68.0,
        ... 64.0,
        ... 64.0,
        ... 68.0
        ... ])
        >>> conjectureIntercept([
        ...  (11, 68),
        ...  (11.25, 85),
        ...  (11.5, 101),
        ...  (11.75, 117),
        ...  (12.75, 185)
        ... ], m)
        -657.7
    """

    return sum([yIntercept(p, conjecturedSlope) for p in points]) / len(points)
