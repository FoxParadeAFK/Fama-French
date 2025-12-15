from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import seaborn as sb

class Metrics():
  @classmethod
  def mean_squared(cls, error: np.ndarray | int, m: int):
    """
    Calculates the mean squared error
    """
    if isinstance(error, np.ndarray):
      return ((error.T @ error) * (1 / m)).item()

    return (error * error) * (1 / m)

  @classmethod
  def root_mean_squared(cls, error: np.ndarray | int, m: int):
    """
    Calculates the root mean squared error
    """
    return np.sqrt(cls.mean_squared(error, m))

  @classmethod
  def r_squared(cls, squared_error: np.ndarray, variance: np.ndarray):
    """
    Calculates the root mean squared error
    """
    return (1 - ((squared_error.T @ squared_error) / (variance.T @ variance))).item()

def metric_visualise(metrics: dict, height: float = 2.5):
  row: int = len(metrics)
  column: int = 1
  figsize = row * height, 1 * height

  figure: Figure = plt.figure(figsize = figsize)
  
  for header, index in zip(metrics.keys(), range(1, row + 1)):
    axes = figure.add_subplot(column, row, index)
    axes.plot(metrics[header], c = "red", linewidth = 1)  

  figure.tight_layout()
  figure.savefig("test.png")