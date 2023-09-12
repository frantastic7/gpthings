# Summary

Are you tired of YouTube videos being plagued with double ads? Annoyed by them being stretched out with meaningless jabber just to meet ad requirements?  

Summary is the solution! A 10 minute video condensed into a 30 second highly informative summary with AI voiceover. (Takes about 2 minutes to download, transcribe,summariez and generate the voiceover of a 10 minute video -- the script will nofity you when the voiceover is ready to be played!!)  

Whisper + GPT3 powered tool used to transcribe and summarize youtube videos.
Using youtube-dl to download the videos.  

Youtube-dl has a bug as of writing this code. Big thanks to Jared Thomas (https://www.youtube.com/watch?v=Ghe058HpmMk) for providing a hot fix.  

Use "-a" if you want the an AI generated voice to read the summary for you. 

For the AI voiceover I used the elevenlabs.io API (https://beta.elevenlabs.io). Feel free to modify the voice, all of the models are provided in the models.json file.

# Enviorment variables 

Set up a .env file as such :  

```env
OPENAI_API_KEY=your_openai_api_key
FMP_API_KEY=your_fmp_api_key
ALPHA_VANTAGE_API_KEY=your_av_api_key
XI_LABS_API=your_xilabs_api_key
```  
