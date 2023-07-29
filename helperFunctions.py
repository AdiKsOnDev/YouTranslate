from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, AudioFileClip


""" Function will get the transcript of a video and write it down
    in "transcript.txt"

    Arguments:
        video_id --> String containing the ID for a YouTube video
    
    No return type
"""
def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    with open("data/transcript.txt", "w") as file:
        for subtitle in transcript:
            file.write(subtitle.get("text") + "\n")

def installVideo(link):
    SAVE_PATH = "videos"

    try:  
        yt = YouTube(link) 
    except Exception as e: 
        print(f"Connection Error {e}")
        raise e

    try:
        print("Installing the video...")

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
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_file, codec='mp3')

def replace_audio(input_video_file, audio_replacement_file,output_video_file):
    video_clip = VideoFileClip(input_video_file)
    audio_replacement_clip = AudioFileClip(audio_replacement_file)

    video_clip = video_clip.set_audio(audio_replacement_clip)
    video_clip.write_videofile(output_video_file, codec='libx264')



