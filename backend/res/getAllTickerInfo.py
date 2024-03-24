# go through all tickers and store info in a json file
import json
import yfinance as yf

with open('tickers.txt', 'r') as infile:
    tickers = infile.read().splitlines()
    for ticker in tickers:
        tickerInfo = yf.Ticker(ticker).info
        with open(f'company_info/{ticker}.json', 'w') as outfile:
            json.dump(tickerInfo, outfile, indent=4)