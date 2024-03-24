# analyze the tickers and classify into short/mid/long terms and low/medium/high risk

import json 
import yfinance as yf

ticker_info = {}

with open('tickers.txt') as infile:
    tickers = infile.read().splitlines()
    for ticker in tickers:
        tickerInfo = yf.Ticker(ticker).info
        try:
            beta = tickerInfo['beta']
            if beta < 1:
                risk = 'low'
            elif beta < 1.3:
                risk = 'medium'
            else:
                risk = 'high'
            earnings = tickerInfo['forwardPE']
            if earnings < 15:
                term = 'short'
            elif earnings < 25:
                term = 'mid'
            else:
                term = 'long'

            ticker_info[ticker] = {
                'name': tickerInfo['longName'],
                'risk': [risk],
                'timeframe': [term]
            }
        except Exception as e:
            print(f"Error: {e}")

with open('all_stocks.json', 'w') as outfile:
    json.dump(ticker_info, outfile, indent=4)