import argparse
import numpy as np
import sys

dependant: str = "y"

def generator(m: int, n: int, seed: int, spread: int) -> tuple:
  """
  Generates a csv containing a number of points with a specific n
  """ 

  np.random.seed(seed)

  slope: np.ndarray = np.random.uniform(-5, 5, n)
  x: np.ndarray = np.random.uniform(-100, 100, m * n).reshape(-1, n)
  intercept: float = np.random.uniform(-10, 10)
  noise: np.ndarray = np.random.normal(0, spread, m)
  y: np.ndarray = (x @ slope) + intercept + noise

  independant: np.ndarray = np.array(range(n))
  header: str = f"{dependant}," + f"{','.join(f"x_{x}" for x in independant)}"

  return x, y, header

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = "Generates random points",
    description = "Generates a CSV file of nD with normal noise",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument('-fi', dest = 'file_name', type = str, default = "data.csv", help = 'name of the csv file')
  parser.add_argument('-se', dest = 'seed', type = int, required = True, help = 'random seed')
  parser.add_argument('-m', dest = 'm', type = int, default = 100, help = 'number of sample points')
  parser.add_argument('-n', dest = 'n', type = int, default = 1, help = 'dimensions of the dataset')
  parser.add_argument('-sp', dest = 'spread', type = int, default = 60, help = 'noise spread')

  arguments: argparse.Namespace = parser.parse_args() 

  try:
    x, y, header = generator(m = arguments.m, n = arguments.n, seed = arguments.seed, spread = arguments.spread)
    data: np.ndarray = np.column_stack((y, x))

    np.savetxt(arguments.file_name, data, header = header, comments = "", delimiter = ",")
    print(f"Successfully generated {len(data)} points in '{arguments.file_name}'")

  except Exception as exception:
    print(f"Error: {exception}")
    sys.exit(1)
