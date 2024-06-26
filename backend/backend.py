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
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def getBlurb(
	ticker:str,
    investor:str,
	stats:str,
	articleSummary: str, longName: str) -> str:
	global genModel
	parameters = {
		"temperature": 0.2,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 512,  # Token limit determines the maximum amount of text output.
        "top_p": 0.85,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }
	prompt = f'''{articleSummary} 
				{stats} 
				Given a {investor} who might want to invest in {longName}, describe the benefits and risks of investing in this stock. 
				Give your answer in paragraph form.
				Make your answer as simple as possible, try explaining to someone with little to no background in investing.'''
	print(f"Prompt: {prompt}")
	model = genModel
	response = model.predict(
		prompt,
		**parameters,
	)
	print(f"Response from Model: {response.text}")
	return response.text


def summarizeText(text_to_summarize, MAX_OUTPUT_TOKENS=128):
	# Let's load the model and the tokenizer 
	 # If you want to use the Tensorflow model 
	                                                                    # just replace with TFPegasusForConditionalGeneration
	global summarizer_model, summarizer_tokenizer
	model, tokenizer = summarizer_model, summarizer_tokenizer

	# Some text to summarize here
	#text_to_summarize = "National Commercial Bank (NCB), Saudi Arabia’s largest lender by assets, agreed to buy rival Samba Financial Group for $15 billion in the biggest banking takeover this year.NCB will pay 28.45 riyals ($7.58) for each Samba share, according to a statement on Sunday, valuing it at about 55.7 billion riyals. NCB will offer 0.739 new shares for each Samba share, at the lower end of the 0.736-0.787 ratio the banks set when they signed an initial framework agreement in June.The offer is a 3.5% premium to Samba’s Oct. 8 closing price of 27.50 riyals and about 24% higher than the level the shares traded at before the talks were made public. Bloomberg News first reported the merger discussions.The new bank will have total assets of more than $220 billion, creating the Gulf region’s third-largest lender. The entity’s $46 billion market capitalization nearly matches that of Qatar National Bank QPSC, which is still the Middle East’s biggest lender with about $268 billion of assets."

	# Tokenize our text
	# If you want to run the code in Tensorflow, please remember to return the particular tensors as simply as using return_tensors = 'tf'
	input_ids = tokenizer(text_to_summarize, return_tensors="pt", truncation = True, max_length=480).input_ids

	# Generate the output (Here, we use beam search but you can also use any other strategy you like)
	output = model.generate(
	    input_ids, 
	    max_length=MAX_OUTPUT_TOKENS, 
	    num_beams=5, 
	    early_stopping=True
	)

	# sentiment_pipeline = pipeline("text-classification")  #Pretty much all we need but still experimenting with it
	# sentiment_result = sentiment_pipeline(article_body)

	# Finally, we can print the generated summary
	return tokenizer.decode(output[0], skip_special_tokens=True)#, sentiment_result)[0]
	# Generated Output: Saudi bank to pay a 3.5% premium to Samba share price. Gulf region’s third-largest lender will have total assets of $220 billion

def getJawandArticle(ticker:str):
	with open(f'res/news_data/{ticker}.json', 'r') as f:
		data = json.load(f)
		
	articleData = []
	for idx, key in enumerate(data):
		if idx > 2:
			break
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
def combineArticles(articles):
	articleStr = ""
	urls = []
	n = len(articles)
	for (url, text) in articles:
		urls.append(url)
		articleStr += summarizeText(text, 450 //n)
	return articleStr, urls
from flask import Flask
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# @app.route("/")
# def home():
# 	return "Dog"

@app.route("/blurb")
@cross_origin()
def blurb():
	ticker = request.args["ticker"]
	risk = request.args["risk"]
	print(f"Received ticker {ticker}")
	timeframe = request.args["timeframe"]
	investor = f"investor with {risk} risk and over a {timeframe} timeframe"
	articleTuples = getJawandArticle(ticker)
	stats = getJawandStats(ticker)
	summArticle, links = combineArticles(articleTuples)
	generatedBlurb = getBlurb(ticker, investor, stats, summArticle, request.args["name"])
	return [generatedBlurb, links]


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
			valid_tickers.append({
				"ticker": ticker,
				"name": ticker_data['name']
			})
	return valid_tickers
	

summarizer_model_name = "human-centered-summarization/financial-summarization-pegasus"
summarizer_tokenizer = PegasusTokenizer.from_pretrained(summarizer_model_name)
summarizer_model = PegasusForConditionalGeneration.from_pretrained(summarizer_model_name)
vertexai.init(project="esoteric-quanta-418207", location="us-east4")
genModel = TextGenerationModel.from_pretrained("text-bison@002")
app.run(host="0.0.0.0", debug = True)