from flask import Flask, request, jsonify
from pytube import YouTube
import helperFunctions as hf
import voiceCloning as vc
app = Flask(__name__)


# API Routes
"""
    Mini-Route for just audio
"""
@app.route('/translated_audio', methods=['POST'])
def translated_audio():
    data = request.get_json()
    video_url = data['video_url']
    language_code = data['language_code']
    try:
        yt = YouTube(video_url)
    except Exception as e:
        return jsonify({"error": f"Connection Error: {e}"}), 400
    try:

        video_id = video_url.split('=')[1]
        hf.get_transcript(video_id, "data/transcript.txt")
        hf.get_translation("data/transcript.txt", "data/translated_transcript.txt", language_code)

        with open("data/translated_transcript.txt", "r",  encoding="utf-8") as file:
            vc.voiceOverNoClone(file.read(), "audios/VoiceOver.mp3")

    except Exception as e:
        return jsonify({"error": f"Error generating voice audio: {e}"}), 500
    # Read the generated audio and send it as a response
    with open("audios/VoiceOver.mp3", "rb") as file:
        audio_data = file.read()
    return audio_data, 200, {'Content-Type': 'audio/mpeg'}
"""
    complete route with video
"""
@app.route('/translated_video', methods=['POST'])
def translate_video():
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
        hf.get_transcript(video_id, "data/transcript.txt")
        hf.get_translation("data/transcript.txt", "data/translated_transcript.txt", language_code)
        hf.extract_audio("videos/Original_Video", "audios/sample.mp3")

        with open("data/translated_transcript.txt", "r") as file:
            vc.voiceOver(file.read(), "audios/VoiceOver.mp3")
            vc.delete_cloned_voice()

        hf.replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4")
    except Exception as e:
        return jsonify({"error": f"Error translating and creating video: {e}"}), 500

    # Read the final video and send it as a response
    with open("videos/Final_Video.mp4", "rb") as file:
        video_data = file.read()
    return video_data, 200, {'Content-Type': 'video/mp4'}
if __name__ == '__main__':
    app.run(debug=True)