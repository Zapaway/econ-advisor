from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration



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

	# Finally, we can print the generated summary
	return (tokenizer.decode(output[0], skip_special_tokens=True))
	# Generated Output: Saudi bank to pay a 3.5% premium to Samba share price. Gulf region’s third-largest lender will have total assets of $220 billion


from flask import Flask
app = Flask(__name__)
# @app.route("/")
# def home():
# 	return "Dog"
@app.route("/summarize")
def summarize():
	return summarizeText("I shit my pants last night. This resulted in an estimated loss of $5.2 bn. Investors are devastated. The projected revenue drop is $2 mn over the next year.")


summarizer_model_name = "human-centered-summarization/financial-summarization-pegasus"
summarizer_tokenizer = PegasusTokenizer.from_pretrained(summarizer_model_name)
summarizer_model = PegasusForConditionalGeneration.from_pretrained(summarizer_model_name)



app.run(host="0.0.0.0", debug = True)