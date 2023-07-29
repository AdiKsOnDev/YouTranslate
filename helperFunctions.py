from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator


def get_transcript(video_id, file_name):
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

def installVideo(link):
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

def extract_audio(input_file, output_file):
    """ Function for extracting the audio from a video.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
        
        No return type
    """
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_file, codec='mp3')

def replace_audio(input_file, audio_replacement_file, output_file):
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

def get_translation(input_file, output_file, language):
    """ Function for translating a text.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
            language --> The language that you need to translate the text to
        
        No return type
    """
    translator = Translator()

    with open(input_file, "r") as file:
        translation = translator.translate(file.read(), dest=language)

    with open(output_file, "w") as file:
        file.write(translation.text)