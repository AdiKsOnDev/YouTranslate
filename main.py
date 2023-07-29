from helperFunctions import *
from pytube import extract
from voiceCloning import *

url = input("Paste the link to the video you want to translate: ")
id = extract.video_id(url)

installVideo(url)
get_transcript(id, "data/transcript.txt") # Get the video's transcript to translate it to a different language
extract_audio("videos/Original_Video", "audios/sample.mp3") # Extract the audio to use it as a sample for voice cloning
get_translation("data/transcript.txt", "data/translated_transcript.txt", "de") # Translate the transcript for recording a voice over for it

with open("data/translated_transcript.txt", "r") as file:
    voiceOver(file.read(300), "audios/VoiceOver.mp3")
    delete_cloned_voice()

replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4") # Combine the final recording with the original video