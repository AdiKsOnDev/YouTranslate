from flask import Flask, request, jsonify

from pytube import YouTube
from helperFunctions import *
from voiceCloning import *

app = Flask(__name__)

@app.route('/translated_audio', methods=['POST'])
def translated_audio():
    """ An API route that sends back the audio track

        Returns:
            bytes: The .mp3 file
            response: The HTTPS response code (Depending on the outcome)
    """    
    data = request.get_json()
    video_url = data['video_url']
    language_code = data['language_code']

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

@app.route('/translated_with_video', methods=['POST'])
def translated_with_video():
    """ An API route for the final video with the translated audio track

    Returns:
        bytes: The .mp4 file
        response: The HTTPS response code (Depending on the outcome)
    """    
    data = request.get_json()
    video_url = data['video_url']
    language_code = data['language_code']

    try:
        yt = YouTube(video_url)
    except Exception as e:
        return jsonify({"error": f"Connection Error: {e}"}), 400

    try:
        yt.streams.filter(
            progressive=True, 
            file_extension="mp4"
        ).first().download(
            output_path="videos", 
            filename="Original_Video"
        )
        video_id = yt.video_id

        get_transcript(video_id, "data/transcript.txt")
        get_translation("data/transcript.txt", "data/translated_transcript.txt", language_code)
        extract_audio("videos/Original_Video", "audios/sample.mp3")

        with open("data/translated_transcript.txt", "r") as file:
            voiceOver(file.read(), "audios/VoiceOver.mp3")
            delete_cloned_voice()

        replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4")
    except Exception as e:
        return jsonify({"Error": f"Error translating and creating video: {e}"}), 500

    # Read the final video and send it as a response
    with open("videos/Final_Video.mp4", "rb") as file:
        video_data = file.read()

    return video_data, 200, {'Content-Type': 'video/mp4'}


if __name__ == '__main__':
    app.run(debug=True)
