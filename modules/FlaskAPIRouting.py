from flask import Flask, request, jsonify
from pytube import YouTube
import modules.helperFunctions as hf
import modules.voiceCloning as vc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Routes
@app.route('/voiceover_text', methods=['POST'])
def voiceover_text():
    """ An API route just for the audio file

        Returns:
            mp3: An .mp3 file
            HTTPS code: Depending on the result
    """    
    data = request.get_json()
    text = data.get('text')
    language_code = data.get('language_code')
    language_code = language_code.lower()

    print(text, language_code)

    if not text or not language_code:
        return jsonify({"error": "Invalid request data."}), 400

    try:
        # If a language code is provided, translate the text
        with open("data/transcript.txt", "w", encoding="utf-8") as file:
                file.write(text)
        if language_code != "en":
            hf.get_translation("data/transcript.txt", "data/translated_text.txt", language_code)
            with open("data/translated_text.txt", "r", encoding="utf-8") as file:
                text = file.read()
        if language_code == "en":
            with open("data/translated_text.txt", "w", encoding="utf-8") as file:
                file.write(text)


        # Generate voiceover audio from the given text
        vc.voiceOverNoClone(text, "audios/VoiceOver.mp3")

        # Read the generated audio and send it as a response
        with open("audios/VoiceOver.mp3", "rb") as file:
            audio_data = file.read()

        return audio_data, 200, {'Content-Type': 'audio/mpeg'}
    except Exception as e:
        return jsonify({"error": f"Error generating voice audio: {e}"}), 500

@app.route('/translated_audio', methods=['POST'])
def translated_audio():
    """ An API route for the translated audio track

        Returns:
            mp3: An .mp3 file
            HTTPS code: Depending on the result
    """    
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
    Route for getting the transcript as text
"""
@app.route('/transcript_text', methods=['POST'])
def get_transcript_text():
    """ An API route for the transcript

        Returns:
            .json: A json containing the transcript
            HTTPS code: Depending on the result
    """    
    data = request.get_json()
    video_url = data['video_url']
    
    try:
        yt = YouTube(video_url)
    except Exception as e:
        return jsonify({"error": f"Connection Error: {e}"}), 400

    try:
        video_id = video_url.split('=')[1]

        hf.get_transcript_no_delay(video_id, "data/transcript.txt")

        with open("data/transcript.txt", "r", encoding="utf-8") as file:
            transcript_text = file.read()

    except Exception as e:
        return jsonify({"error": f"Error generating transcript: {e}"}), 500

    return jsonify({"transcript": transcript_text}), 200

@app.route('/translated_video_clone', methods=['POST'])
def translate_video_clone():
    """ An API route for the final, translated video with a cloned voice

        Returns:
            .mp4: A .mp4 file containing the translated and narrated video
            HTTPS code: Depending on the result
    """    
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



@app.route('/translated_video_no_clone', methods=['POST'])
def translate_video_no_clone():
    """ An API route for the final, translated video without a cloned voice

        Returns:
            .mp4: A .mp4 file containing the translated and narrated video
            HTTPS code: Depending on the result
    """    
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
            vc.voiceOverNoClone(file.read(), "audios/VoiceOver.mp3")
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