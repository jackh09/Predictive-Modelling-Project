"""
This file houses the stockFetcher functions for the predictive
analysis engine. It takes a stock name as an input and outputs
a fully formatted csv file.
"""

## Libraries ##
import logging
import yfinance as yf       # fetching stock data
import pandas as pd         # formatting data calculating returns
import csv                  # turn raw data into formatted data for frontend
import os                   # select a path to save the data

## Get stock name
stockName = "^FTSE"

## check if stock is valid
def checkStockValidity(stock: str) -> bool:
    ## Set logging level to keep CLI clear
    logging.getLogger("yfinance").setLevel(logging.CRITICAL)
    try:
        info = yf.download(stock, period="5d", interval="1d", group_by="ticker", progress=False)
        return not info.empty
    except Exception:
        return False

def fetchStockData(stock: str, historyLength: int) -> None:
    ## verify valid search
    valid = checkStockValidity(stock)
    if not valid:
        ## handle false stock
        raise Exception("Stock is invalid")


    ## fetch stock data
    stockTicker = yf.Ticker(stock)
    df = stockTicker.history(
        period=f"{historyLength}d",
        interval="1d"
    )

    df = df.reset_index() # convert to pandas useable data

    df["Returns"] = df["Close"].pct_change() # adds return column to df
    df = df.dropna()                         # removes 0th row due to NaN pct change

    newdf = pd.DataFrame()               # create formatted df
    newdf["date"] = df["Date"]           # add date
    newdf["close"] = df["Close"]         # add closing prices
    newdf["returns"] = df["Returns"]     # add returns

    ## get directory path for data.csv
    srcDir = os.path.dirname(os.path.abspath(__file__)) # get the path for the src file
    rootDir = os.path.dirname(srcDir)                   # go up to root directory
    dataDir = os.path.join(rootDir, "data")             # drop down into data folder   

    if not os.path.exists(dataDir): # create the data folder if it isn't there
        os.makedirs(dataDir)

    csvDir = os.path.join(dataDir,"data.csv")

    newdf.to_csv(csvDir, index=False) # create csv file with newdf data

if __name__ == "__main__":
    fetchStockData(stockName, 500)
