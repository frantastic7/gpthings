#!/usr/bin/env python3

#NOT FINANCAL ADVICE

import openai
import requests 
import sys
import json
from dotenv import dotenv_values

env_values = dotenv_values(".env")


#OpenAI API key
openai.api_key = env_values.get("OPENAI_API_KEY")

#AlphaVantage API key (price data)
AVapiKey = env_values.get("ALPHA_VANTAGE_API_KEY")

#FinancialModelingPrep API (balance sheet and company data)
apiFMP = env_values.get("FMP_API_KEY")


#Symbol for the company you wanna check, needs to be in caps for API calls, eg. AAPL 
symbol = sys.argv[1].upper()

#Defines amount of tokens for the output, modify as needed. 4k/16k max depending on your api choice
toks = {"s":128,"m":256,"l":512}


role = """
    You are an analyst at a top investment firm. You will recieve data about a company, including its balance sheet and recent price data, along with trading volume. You primrary task is to assest the companys financials and provide an verdict on the company stock. Verdict options include : ["HOLD","BUY","SELL","SHORT"]. Also provide a volatility raiting : ["Low","Medium","High","Extreme"].

    The format of your answers should be as such:

    Analysis : short analysis about the company, financials and a prediciton about future prices
    Volatility raiting : eg. Low
    Verdict : eg. BUY


    ! IMPORTANT ! 
    Always finish the message with : "Please remember, I am just a bot, this is not financial advice."
    ! IMPORTANT !

    Be sure to maximize the allowed tokens.


"""


price_data = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AVapiKey}'

balance_data = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=120&apikey={apiFMP}'

price_data_json = requests.get(price_data)
balance_data_json = requests.get(balance_data)

if price_data_json.status_code == 200:
    prices = price_data_json.json()
else:
    print('no work :( 1', price_data_json.status_code)

if balance_data_json.status_code == 200 : 
    balance_sheet = balance_data_json.json()
else :
    print('no work :( 2', balance_data_json.status_code)


evaluation = openai.Completion.create (

    engine = "text-davinci-003",
    prompt = role + "\n" + json.dumps(balance_sheet) + "\n" + json.dumps(prices),
    max_tokens = int(toks.get(sys.argv[2])),
    n=1,
    temperature = 0.5

)


print (evaluation.choices[0].text.strip())