#!/usr/bin/env python3

import youtube_dl
import whisper
import openai
import os
from sys import argv, platform
import subprocess
from dotenv import load_dotenv
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

load_dotenv()

MAX_TOKENS = 4096

#Api keys, loaded in from a .env file

openai.api_key = os.getenv('OPENAI_API_KEY')

xi_api_key = os.getenv('XI_LABS_API')

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

def play_audio (file):
    pygame.init()
    pygame.mixer.init() 

    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except pygame.error as err:
        print (f'Error playing audio: {str(err)}')
    
    pygame.mixer.quit()
    pygame.quit()
 

#Downloads YouTube file into script directory

url = input ('YouTube video link : ')

title = get_title(url)
audio_download(url)
output = title + '_summary.txt'

#Loads whisper model, 'base.en' works fine for a large percentage of cases
model = whisper.load_model('base.en')

#Loads the audio file for Whisper to transcibe
audio_file = f'{title}.mp3'

result = model.transcribe(audio_file)

transcript = result['text']

#Preprompt for GPT. Modify as needed.

role = 'You will be given the transcript of an audio file. Your job is to summarise it concisely and write a few short note/talking points about the transcript. Please use at least half of the provided the provided tokens \n'

#assuming we cut the content by 60% in a summary, from 120-150 wpm, we go down to around 48-60, which would equate to about 70 per minute of audio max.

toks = int (1.2 * get_seconds(url))

if toks > MAX_TOKENS :
    toks = MAX_TOKENS



if len(argv) > 1 and argv[1] == '-a':
    toks = 180

    summary = openai.Completion.create (

    engine = 'text-davinci-003',
    prompt = role + transcript,
    max_tokens =  toks,
    n=1,
    temperature = 0.7

)
    import requests

    user_input = summary.choices[0].text.strip()
    CHUNK_SIZE = 1024

    #Change it to your liking, all the base voices by ELEVEN LABS can be found in the models.json file
    voice_ID = 'TxGEqnHWrfWFTfGW9XjX'
    voice_url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_ID}'

    headers = {
        'Accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        'xi-api-key':f'{xi_api_key}'
    }

    data = {
        'text': f'{user_input}',
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
           'stability': 0.5,
           'similarity_boost': 0.5
        }
    }

    response = requests.post(voice_url, json=data, headers=headers)

    summary_file = title + '_summary.mp3'
    


    with open (summary_file, 'wb') as audio_new :
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                audio_new.write(chunk)
    with open (output, 'w') as summary_text :
        summary_text.write(summary.choices[0].text.strip())

    if platform.startswith('win'):

        subprocess.run(['powershell', '-Command', 'New-BurntToastNotification -Text "Summary ready to play"'])

    elif platform.startswith('darwin'):

        subprocess.run(['osascript', '-e', 'display notification "Summary ready to play" with title "Summary finished"'])

    elif platform.startswith('linux'):

        subprocess.run(['notify-send', 'Summary ready to play']) 

    play = input ("Press enter to play summary audio file.")

    play_audio(summary_file)

else:

    summary = openai.Completion.create (

        engine = 'text-davinci-003',
        prompt = role + transcript,
        max_tokens =  toks,
        n=1,
        temperature = 0.7

    )
    
    print (f'Summary of {title} :\n')
    print(summary.choices[0].text.strip())

    with open (output, 'w') as summary_text :
        summary_text.write(summary.choices[0].text.strip())

    if platform.startswith('win'):

        subprocess.run(['powershell', '-Command', 'New-BurntToastNotification -Text "Summary finished"'])

    elif platform.startswith('darwin'):

        subprocess.run(['osascript', '-e', 'display notification "Summary ready" with title "Summary finished"'])

    elif platform.startswith('linux'):

        subprocess.run(['notify-send', 'Summary finished']) 

    
    


