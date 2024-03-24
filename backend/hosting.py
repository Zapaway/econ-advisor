from flask import Flask
from flask import request
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

def getNewsData(ticker):
	tickerNewsPage = f'https://finance.yahoo.com/quote/{ticker}/news'
	req = Request(tickerNewsPage, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(req)
	tickerHtml = page.read().decode("utf-8")
	html_data = BeautifulSoup(tickerHtml, 'html.parser')

	# Get the news articles
	articles = html_data.find_all('li', class_='stream-item  svelte-7rcxn')
	for article in articles:
		article_link = article.find('a')['href']
		article_title = article.find('span').text
		print(f"Title: {article_title} Link: {article_link}")

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

# app.run(host="0.0.0.0", debug = True)
print(getNewsData('QQQ'))