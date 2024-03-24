from flask import Flask
from flask import request
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import os 
from time import sleep

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

def getJawandArticle(ticker:str):
	url = f"https://yahoo-finance127.p.rapidapi.com/news/{ticker.lower()}"
	headers = {
		"X-RapidAPI-Key": os.environ["X-RapidAPI-Key"],
		"X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers)
	data = response.json()

	articleData = []
	for key in data:
		article_url = data[key]['link']
		# get text
		article_text = ""
		req = Request(article_url, headers={'User-Agent': 'Mozilla/5.0'})
		page = urlopen(req)
		response = page.read().decode("utf-8")
		soup = BeautifulSoup(response, 'html.parser')
		paragraphs = soup.find_all('p')
		for paragraph in paragraphs:
			article_text += paragraph.text + " "
		articleData.append((article_url, article_text))
	return articleData # (url, title)

def getArticleData(ticker):
	url = f"https://yahoo-finance127.p.rapidapi.com/news/{ticker.lower()}"
	print(os.environ["X-RapidAPI-Key"])
	headers = {
		"X-RapidAPI-Key": os.environ["X-RapidAPI-Key"],
		"X-RapidAPI-Host": "yahoo-finance127.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers)
	data = response.json()
	with open(f'res/news_data/{ticker}.json', 'w') as f:
		json.dump(data, f, indent=2)

with open('res/tickers.txt', 'r') as f:
	tickers = f.read().split('\n')
	for ticker in tickers:
		getArticleData(ticker)
		sleep(5)

def getJawandStats(ticker:str):
	return_str = ""

	with open(f'res/company_info/{ticker}.json', 'r') as f:
		data = json.load(f)
		# if 'longName' and 'longBusinessSummary' in data:
			# return_str += f"{data['longName']} is a company that {data['longBusinessSummary']}."
		if 'longName' in data:
			return_str += f"{data['longName']} is a company with the following conditions: "
		if 'dividendYield' in data and 'dividendRate' in data:
			return_str += f"It has a dividend yield of {data['dividendYield']} and a dividend rate of {data['dividendRate']}. "
		if 'trailingEps' in data and 'forwardEps' in data and 'pegRatio' in data:
			return_str += f"It has a trailing EPS of {data['trailingEps']}, a forward EPS of {data['forwardEps']}, and a P/E ratio of {data['pegRatio']}. "
		if 'marketCap' in data:
			return_str += f"It has a market cap of {data['marketCap']}. "
		if 'totalDebt' in data and 'debtToEquity' in data:
			return_str += f"It has a total debt of {data['totalDebt']} and a debt to equity ratio of {data['debtToEquity']}."
	
	return return_str

# print(getJawandStats("AAPL"))
# print(getJawandStats("META"))

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
# print(getNewsData('QQQ'))