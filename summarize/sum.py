#!/usr/bin/env python3

import youtube_dl
import whisper
import sys
import openai
import os
from dotenv import load_dotenv

load_dotenv()


#Api keys, loaded in from a .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

#YT-DL download audio function

def audio_download(url) :
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(options) as ytdl:
        info = ytdl.extract_info(url, download=False)
        title = info['title']
        ytdl.download([url])
    return title

#YT-DL get title function, separate for ease of modifications
def get_title (url) :
    options = {
        'format':'best',
        'quiet':True,
        'no_warnings':True,
    }
    with youtube_dl.YoutubeDL(options) as ytdl :
        info = ytdl.extract_info(url, download=False)
        video_title = info.get('title','')
    return video_title


def get_seconds (url) :
    options = {
        'format':'best',
        'quiet':True,
        'no_warnings':True,
    }
    with youtube_dl.YoutubeDL(options) as ytdl :
        info = ytdl.extract_info(url, download=False)
        length = info['duration']
    return length



#Downloads YouTube file into script directory

url = input ("YouTube video link : ")

title = get_title(url)
audio_download(url)


#Loads whisper model, "base.en" works fine for a large percentage of cases
model = whisper.load_model("base.en")

#Loads the audio file for Whisper to transcibe
audio_file = f'{title}.mp3'

result = model.transcribe(audio_file)

transcript = result["text"]

#Preprompt for GPT. Modify as needed.

role = "You will be given the transcript of an audio file. Your job is to summarise it concisely and write a few short note/talking points about the transcript. \n"

#assuming we cut the content by 60% in a summary, from 120-150 wpm, we go down to around 48-60, which would equate to about 70 per minute of audio max.

toks = int (1.2 * get_seconds(url))


summary = openai.Completion.create (

    engine = "text-davinci-003",
    prompt = role + transcript,
    max_tokens =  toks,
    n=1,
    temperature = 0.3

)


print (f'Summary of {title} :\n')
print(summary.choices[0].text.strip())
print(toks)