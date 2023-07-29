import youtube_transcript_api
from helperFunctions import *

link = input("Paste the link to the video you want to translate: ")
id = link.split()

installVideo(link)
extract_audio("videos/Original_Video", "audios/Original_Audio.mp3")