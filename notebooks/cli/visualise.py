import argparse
from typing import Iterable
from matplotlib import pyplot as plt
from pandas import DataFrame, read_csv
import seaborn

pairplot_congfig: dict = {
  "kind": "reg",
  "height": 2.5,
  "line": { "color": "red", "linewidth": 1 },
  "scatter": { "s": 3, "color": "green" }
}
def pairplot(data: DataFrame, file_name: str):
  """
  Generates and save a pairplot of the dataframe
  """
  x: Iterable[str] = data.columns
  y: str = "y"

  pairplot: seaborn.PairGrid = seaborn.pairplot(data = data, y_vars = y, x_vars = x, kind = pairplot_congfig["kind"], height = pairplot_congfig["height"], 
                                                plot_kws = { "line_kws": pairplot_congfig["line"], "scatter_kws": pairplot_congfig["scatter"]})
  pairplot.savefig(file_name)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = "Explore dataset",
    description = "Generate images of explored datasets",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument('-da', dest = 'data_set', type = str, required = True, help = 'path to dataset')
  parser.add_argument('-fi', dest = 'file_name', type = str, required = True, help = 'name of images')

  arguments: argparse.Namespace = parser.parse_args() 

  data: DataFrame = read_csv(arguments.data_set)

  pairplot(data, arguments.file_name)