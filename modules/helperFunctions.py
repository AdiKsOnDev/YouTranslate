from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator

def get_transcript_no_delay(video_id:str, file_name:str):
    """ Function will get the transcript of a video and write it down
        in "transcript.txt" WITHOUT adding any delays

        Arguments:
            video_id --> String containing the ID for a YouTube video
        
        No return type
    """
    print("Getting the transcript...")

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    with open(file_name, "w", encoding= "utf-8") as file:
        for i in range(len(transcript)):
            subtitle = transcript[i]
            text = subtitle["text"]
            file.write(text)
            file.write("\n")

def get_transcript(video_id:str, file_name:str):
    """ Function will get the transcript of a video and write it down
        in "transcript.txt"

        Arguments:
            video_id --> String containing the ID for a YouTube video
        
        No return type
    """
    print("Getting the transcript...")

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    with open(file_name, "w", encoding= "utf-8") as file:
        x = transcript[0].get("start")
        x = int(x/0.04)
        file.write("uh")
        file.write(x*".")
        file.write("\n")
        for i in range(len(transcript)):
            subtitle = transcript[i]
            text = subtitle["text"]
            file.write(text)
            
            # Calculate time difference between this subtitle and the next one
            if i < len(transcript) - 1:
                current_end_time = subtitle["start"] + subtitle["duration"]
                next_start_time = transcript[i + 1]["start"]
                time_diff =  current_end_time - next_start_time 
                
                # Calculate the number of full stops (0.1 second per full stop)
                num_full_stops = int(time_diff / 0.1)

                if(num_full_stops > 27):
                    print("adding a delay of ", num_full_stops, " seconds")
                    file.write("." * int(num_full_stops/2))
            
            file.write("\n")

    
def installVideo(link:str):
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

        return 0
    except Exception as e:
        print(f"!!ERROR!! {e}")
        return 1

def extract_audio(input_file:str, output_file:str):
    """ Function for extracting the audio from a video.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
        
        No return type
    """
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(output_file, codec='mp3')

def replace_audio(input_file:str, audio_replacement_file:str, output_file:str):
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

def get_translation(input_file:str, output_file:str, language:str):
    """ Function for translating a text.  

        Arguments:
            input_file --> Path to the input file
            output_file --> Path to the output file
            language --> The language that you need to translate the text to
        
        No return type
    """
    translator = Translator()

    with open(input_file, "r", encoding="utf-8") as file:
        translation = translator.translate(file.read(), dest=language)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(translation.text)