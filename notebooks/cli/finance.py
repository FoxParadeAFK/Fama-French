import argparse
import sys
from pandas import DataFrame
import yfinance as yf

def download(tickers: str) -> DataFrame:
  """
  Fetch and save as a CSV a specific tickers information
  """
  ticker: yf.Ticker = yf.Ticker(tickers)
  data: DataFrame = ticker.history(period = "max")

  if data.empty:
    print(f"Resulting ticker {tickers} created empty dataset")
    data: DataFrame = DataFrame([])

  return data

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog = "Download yFinance dataset",
    description = "Download CSV file for a specific ticker from Yahoo Finance",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
  )

  parser.add_argument('-ti', dest = 'ticker', type = str, required = True, help = 'name of ticker')
  parser.add_argument('-fi', dest = 'file_name', type = str, required = True, help = 'name of file the csv')

  arguments: argparse.Namespace = parser.parse_args() 

  try:
    data: DataFrame = download(arguments.ticker)
    data.to_csv(arguments.file_name)
  
  except Exception as exception:
    print(f"Error: {exception}")
    sys.exit(1)