from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
import predictionguard as pg
from sentence_transformers import SentenceTransformer
import streamlit as st
from transformers import pipeline
from flask import request
from flask_cors import CORS, cross_origin
import json
import vertexai
from vertexai.language_models import TextGenerationModel
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def getBlurb(
	ticker:str,
    investor:str,
	stats:str,
	articleSummary: str) -> str:
	global genModel
	parameters = {
		"temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }
	model = genModel
	response = model.predict(
		f'''{articleSummary} {stats} Explain why a {investor} would might want to invest in {ticker}. Describe the benefits and risks.''',
		**parameters,
	)
	print(f"Response from Model: {response.text}")
	return response.text


def summarizeText(text_to_summarize):
	MAX_OUTPUT_TOKENS = 64
	# Let's load the model and the tokenizer 
	 # If you want to use the Tensorflow model 
	                                                                    # just replace with TFPegasusForConditionalGeneration
	global summarizer_model, summarizer_tokenizer
	model, tokenizer = summarizer_model, summarizer_tokenizer

	# Some text to summarize here
	#text_to_summarize = "National Commercial Bank (NCB), Saudi Arabia’s largest lender by assets, agreed to buy rival Samba Financial Group for $15 billion in the biggest banking takeover this year.NCB will pay 28.45 riyals ($7.58) for each Samba share, according to a statement on Sunday, valuing it at about 55.7 billion riyals. NCB will offer 0.739 new shares for each Samba share, at the lower end of the 0.736-0.787 ratio the banks set when they signed an initial framework agreement in June.The offer is a 3.5% premium to Samba’s Oct. 8 closing price of 27.50 riyals and about 24% higher than the level the shares traded at before the talks were made public. Bloomberg News first reported the merger discussions.The new bank will have total assets of more than $220 billion, creating the Gulf region’s third-largest lender. The entity’s $46 billion market capitalization nearly matches that of Qatar National Bank QPSC, which is still the Middle East’s biggest lender with about $268 billion of assets."

	# Tokenize our text
	# If you want to run the code in Tensorflow, please remember to return the particular tensors as simply as using return_tensors = 'tf'
	input_ids = tokenizer(text_to_summarize, return_tensors="pt").input_ids

	# Generate the output (Here, we use beam search but you can also use any other strategy you like)
	output = model.generate(
	    input_ids, 
	    max_length=MAX_OUTPUT_TOKENS, 
	    num_beams=5, 
	    early_stopping=True
	)

	sentiment_pipeline = pipeline("text-classification")  #Pretty much all we need but still experimenting with it
	sentiment_result = sentiment_pipeline(article_body)

	# Finally, we can print the generated summary
	return (tokenizer.decode(output[0], skip_special_tokens=True), sentiment_result)
	# Generated Output: Saudi bank to pay a 3.5% premium to Samba share price. Gulf region’s third-largest lender will have total assets of $220 billion

def getJawandArticle(ticker:str):
	import requests
	import os 

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

from flask import Flask
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# @app.route("/")
# def home():
# 	return "Dog"
article_body = "I shit my pants last night. This resulted in an estimated loss of $5.2 bn. Investors are devastated. The projected revenue drop is $2 mn over the next year."
ticker_fact_sheet = "Annual Dividend Yield: 6% ($13/share); EPS: -$0.02"

@app.route("/blurb")
@cross_origin()
def blurb():
	ticker = request.args["ticker"]
	risk = request.args["risk"]
	timeframe = request.args["timeframe"]
	investor = f"investor with risk {risk} and timeframe {timeframe}"
	article = getJawandArticle(ticker)
	stats = getJawandStats(ticker)
	summArticle = summarizeText(article)
	return getBlurb(ticker, investor, stats, summArticle)


@app.route('/getTickers')
@cross_origin()
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
	

summarizer_model_name = "human-centered-summarization/financial-summarization-pegasus"
summarizer_tokenizer = PegasusTokenizer.from_pretrained(summarizer_model_name)
summarizer_model = PegasusForConditionalGeneration.from_pretrained(summarizer_model_name)
vertexai.init(project=1, location="us-east4")
genModel = TextGenerationModel.from_pretrained("text-bison@002")
app.run(host="0.0.0.0", debug = True)