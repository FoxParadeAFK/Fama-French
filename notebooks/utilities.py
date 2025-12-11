from typing import Any
import argparse
import numpy as np

dependant: str = "y"
independant: list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]

def generator(file_name: str, count: int = 100, dimension: int = 2) -> Any:
  """
  Generates a csv containing a number of points with a specific dimension
  """
  if (dimension := dimension - 1) < 1:
    raise ValueError(f"Cannot generate a random data of dimensions {dimension}D. Valid dimensions >=2D must be given")

  if not file_name.endswith(".csv"):
    raise ValueError(f"File name {file_name} is invalid. Ensure it ends with .csv")

  slope: np.ndarray = np.random.uniform(-5, 5, dimension)
  x: np.ndarray = np.random.uniform(-100, 100, count * dimension).reshape(-1, dimension)
  intercept: float = np.random.uniform(-10, 10)
  noise: np.ndarray = np.random.normal(0, 60, count)
  y: np.ndarray = (x @ slope) + intercept + noise

  data: np.ndarray = np.column_stack((y, x))
  header: str = f"{dependant}, {", ".join(independant[:dimension])}"

  np.savetxt(file_name, data, header = header)
  print(f"Successfully generated {len(y)} points in '{file_name}'")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = "Generates random points",
    description = "Generates a CSV file of dimension nD with normal noise",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument(
    '-f', '--file_name',
    type = str,
    required = True,
    help = 'Name of the csv file'
  )

  parser.add_argument(
    '-c', '--count',
    type = int,
    default = 100,
    help = 'Number of sample points'
  )

  parser.add_argument(
    '-d', '--dimension',
    type = int,
    default = 2,
    help = 'Dimensions of the datasets'
  )

  arguments: argparse.Namespace = parser.parse_args()
  generator(file_name = arguments.file_name, count = arguments.count, dimension = arguments.dimension)