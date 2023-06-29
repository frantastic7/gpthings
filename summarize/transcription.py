#!/usr/bin/env python3

import whisper
import sys
import openai
import os
from dotenv import load_dotenv

load_dotenv()

#Sizes of english models, can use multilingual if necesary, just change the main prompt.
sizes = {"t": "tiny.en", "b": "base.en", "s": "small.en", "m": "medium.en", "l": "large"}


#Api keys, loaded in from a .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

#Gets the audio file from the command line
#TODO make it download videos directly
audio = sys.argv[1]
#Gets size and loads appropriate model based on user input
size = sizes.get(sys.argv[2])
model = whisper.load_model(size)

result = model.transcribe(audio)

transcript = result["text"]

role = "You will be given the transcript of an audio file. Your job is to summarise it concisely and write a few short note/talking points about the transcript. \n"

summary = openai.Completion.create (

    engine = "text-davinci-003",
    prompt = role + transcript,
    max_tokens =  512,
    n=1,
    temperature = 0.3

)

print(summary.choices[0].text.strip())