"""lintest

   A simple program that accepts a list of data points and computes the slope
   between successive pairs of points.
"""

import os.path

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

  return [computeSlope(points[i], points[i+1]) for i in range(n-1)]
