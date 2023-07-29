from elevenlabs import clone, generate, play, set_api_key
from apiKey import API_KEY

def voiceOver():
    set_api_key(API_KEY)

    voice = clone(
        name="Alex",
        description="An old American male voice with a slight hoarseness in his throat. Perfect for news", # Optional
        files=["audios/sample.mp3"],
    )

    audio = generate(text="Hi! I'm a cloned voice! I speak german, indian, british english, javascript, C, Python and rizz", voice=voice)

