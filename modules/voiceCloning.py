from elevenlabs import clone, generate, set_api_key, save, Voices, Voice
from dotenv import dotenv_values
from os import listdir, system

import requests

if not '.env' in listdir('.'):
    api_key = input("Please input your api key: ")
    system(f'echo "API_KEY={str(api_key)}" > .env')
else:
    config = dotenv_values(".env")
    api_key = config['API_KEY']

def voiceOverNoClone(transcript:str, output_file:str):
    """ Function for recording the translated audio track.  

        Arguments:
            transcript --> The transcript to be used for voice-over
            output_file --> Path to the output file
        
        No return type
    """
    set_api_key(api_key)

    print("Generating a Voice Over...")

    


    audio = generate(text=transcript)

    save(audio, output_file)
    
def voiceOver(transcript:str, output_file:str):
    """ Function for recording the translated audio track.  

        Arguments:
            transcript --> The transcript to be used for voice-over
            output_file --> Path to the output file
        
        No return type
    """
    set_api_key(api_key)

    print("Generating a Voice Over...")

    voice = clone(
        name="YouTuber",
        files=["audios/sample.mp3"],
        model='eleven_multilingual_v1'
    )


    audio = generate(text=transcript, voice=voice)

    save(audio, output_file)

def delete_cloned_voice():
    """ Function for deleting the voice template form ElevenLabs API

        No Arguments
    
        No return type
    """    
    HEADERS = {
        "Accept": "application/json",
        "xi-api-key": api_key
    }

    voices = Voices.from_api()
    URL = f"https://api.elevenlabs.io/v1/voices/{voices[0].voice_id}"
    
    response = requests.delete(URL, headers=HEADERS)

    print(response)