from elevenlabs import clone, generate, set_api_key, save, Voices, Voice
from apiKey import API_KEY

import requests

def voiceOver(transcript:str, output_file:str):
    """ Function for recording the translated audio track.  

        Arguments:
            transcript --> The transcript to be used for voice-over
            output_file --> Path to the output file
        
        No return type
    """
    set_api_key(API_KEY)

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
        "xi-api-key": API_KEY
    }

    voices = Voices.from_api()
    URL = f"https://api.elevenlabs.io/v1/voices/{voices[0].voice_id}"
    
    response = requests.delete(URL, headers=HEADERS)

    print(response)