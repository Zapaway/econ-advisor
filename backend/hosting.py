from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/getTickers')
def getTickers():
	risk = request.args['risk']
	timeframe = request.args['timeframe']
	data = json.load(open('res/all_stocks.json', 'r'))
	valid_tickers = []
	for ticker in data:
		ticker_data = data[ticker]
		if risk in ticker_data['risk'] and timeframe in ticker_data['timeframe']:
			valid_tickers.append(ticker)
	return valid_tickers

app.run(host="0.0.0.0", debug = True)