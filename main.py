from helperFunctions import *
from pytube import extract
from voiceCloning import voiceOver

url = input("Paste the link to the video you want to translate: ")
id = extract.video_id(url)

installVideo(url)
get_transcript(id, "data/transcript.txt")
extract_audio("videos/Original_Video", "audios/sample.mp3")

get_translation("data/transcript.txt", "data/translated_transcript.txt", "fr")

with open("data/translated_transcript.txt", "r") as file:
    voiceOver(file.read(1500), "audios/VoiceOver.mp3")

replace_audio("videos/Original_Video", "audios/VoiceOver.mp3", "videos/Final_Video.mp4")