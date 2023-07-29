from flask import Flask, request, jsonify
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator
from elevenlabs import clone, generate, set_api_key, save, Voices, Voice
import requests
from apiKey import API_KEY

app = Flask(__name__)

def get_transcript(video_id: str, file_name: str):
    """ Function will get the transcript of a video and write it down
        in "transcript.txt"

        Arguments:
            video_id --> String containing the ID for a YouTube video
        
        No return type
    """
    print("Getting the transcript...")

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    with open(file_name, "w") as file:
        for subtitle in transcript:
            file.write(subtitle.get("text") + "\n")

def installVideo(link: str):
    """ Function will install a video using the passed link

        Arguments:
            link --> String containing the link for a YouTube video
        
        No return type
    """
    SAVE_PATH = "videos"

    try:  
        yt = YouTube(link) 
    except Exception as e: 
        print(f"Connection Error {e}")
        raise e

    try:
        print("Installing the video...")

        # Filter out the .mp4 files from the youtube response and download the video
        yt.streams.filter(
            progressive = True,
            file_extension = "mp4"
        ).first().download(
            output_path = SAVE_PATH, 
            filename = "Original_Video"
        )
    except Exception as e:
        print(f"!!ERROR!! {e}")

def extract_audio(input_file: str, output_file: str):
    """ Function for extracting the audio from a video.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
        
        No return type
    """
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_file, codec='mp3')

def replace_audio(input_file: str, audio_replacement_file: str, output_file: str):
    """ Function for replacing the audio track in a video with a new one.  

        Arguments:
            input_file --> Path to the input file
            audio_replacament_file --> Path to the audio file that needs to be used in a video
            output_file --> Path to the output file
        
        No return type
    """
    video_clip = VideoFileClip(input_file)
    audio_replacement_clip = AudioFileClip(audio_replacement_file)
    video_clip = video_clip.set_audio(audio_replacement_clip)

    video_clip.write_videofile(output_file, codec='libx264')

def get_translation(input_file: str, output_file: str, language: str):
    """ Function for translating a text.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
            language --> The language that you need to translate the text to
        
        No return type
    """
    translator = Translator()

    with open(input_file, "r", encoding="utf-8") as file:  # Specify the encoding here
        translation = translator.translate(file.read(), dest=language)

    with open(output_file, "w", encoding="utf-8") as file:  # Specify the encoding here
        file.write(translation.text)


def voiceOver(transcript: str, output_file: str):
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


# API Routes
"""
    Mini-Route for just audio
"""
@app.route('/translated_voice_audio', methods=['POST'])
def translated_voice_audio():
    data = request.get_json()
    video_url = data['video_url']
    language_code = data['language_code']

    try:
        yt = YouTube(video_url)
    except Exception as e:
        return jsonify({"error": f"Connection Error: {e}"}), 400

    try:
        
        video_id = video_url.split('=')[1]
        get_transcript(video_id, "data/transcript.txt")
        get_translation("data/transcript.txt", "data/translated_transcript.txt", language_code)

        with open("data/translated_transcript.txt", "r",  encoding="utf-8") as file:
            voiceOver(file.read(), "audios/VoiceOver.mp3")
            delete_cloned_voice()

    except Exception as e:
        return jsonify({"error": f"Error generating voice audio: {e}"}), 500

    # Read the generated audio and send it as a response
    with open("audios/VoiceOver.mp3", "rb") as file:
        audio_data = file.read()

    return audio_data, 200, {'Content-Type': 'audio/mpeg'}


"""
    complete route with video
"""
@app.route('/translated_with_video', methods=['POST'])
def translate_and_video():
    data = request.get_json()
    video_url = data['video_url']
    language_code = data['language_code']

    try:
        yt = YouTube(video_url)
    except Exception as e:
        return jsonify({"error": f"Connection Error: {e}"}), 400

    try:
        yt.streams.filter(progressive=True, file_extension="mp4").first().download(output_path="videos", filename="Original_Video")
        video_id = yt.video_id
        get_transcript(video_id, "data/transcript.txt")
        get_translation("data/transcript.txt", "data/translated_transcript.txt", language_code)
        extract_audio("videos/Original_Video", "audios/sample.mp3")

        with open("data/translated_transcript.txt", "r") as file:
            voiceOver(file.read(), "audios/VoiceOver.mp3")
            delete_cloned_voice()

        replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4")
    except Exception as e:
        return jsonify({"error": f"Error translating and creating video: {e}"}), 500

    # Read the final video and send it as a response
    with open("videos/Final_Video.mp4", "rb") as file:
        video_data = file.read()

    return video_data, 200, {'Content-Type': 'video/mp4'}


if __name__ == '__main__':
    app.run(debug=True)
