from elevenlabs import clone, generate, play, set_api_key, save
from apiKey import API_KEY

def voiceOver(transcript, output_file):
    set_api_key(API_KEY)

    print("Generating a Voice Over...")

    voice = clone(
        name="YouTuber",
        files=["audios/sample.mp3"],
        model='eleven_multilingual_v1'
    )


    audio = generate(text=transcript, voice=voice)

    save(audio, output_file)