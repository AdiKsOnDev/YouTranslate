# :movie_camera: TranslatorYouTuber

TranslatorYouTuber is a Python script that allows you to create multilingual YouTube videos by cloning the voice of the video's author and translating the video's transcript to a different language. The script then performs a voice-over using the translated script and cloned voice, enabling you to reach a broader audience by offering content in multiple languages!

## :open_file_folder: Installation

1. Go to the most recent production-ready release and install the zip with the source code
2. Ensure you have Python 3.11+ installed on your system.
3. Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

## :exclamation: Prerequisites

To use TranslatorYouTuber, you will need the following:

- An API Key for the ElevenLab's speech synthesis (See [ElevenLabs API](https://docs.elevenlabs.io/api-reference/quick-start/introduction))
- A YouTube video URL for which you want to create a multilingual version.

## :scroll: Usage

1. Run the Script:
   - Open your terminal or command prompt.
   - Execute the following command:

```bash
python main.py
```

2. Review the Output:
   - The script will process the video, clone the voice, translate the transcript, and generate the final multilingual version.
   - After completion, you will find the multilingual video file in the `videos/` directory (`Final_Video.mp4`).
   - Add background sounds, polish the video. (If you are the author of the original video and you still have the video's assets on your computer)
   - Don't forget that the voice synthesis is not able to copy original author's pacing. You will have to edit the video to make it as good as possible

3. Upload to YouTube:
   - Upload the generated `Final_Video.mp4` to your YouTube channel and publish it to reach a wider audience.

## :question: How It Works

TranslatorYouTuber utilizes ElevenLabs' voice cloning API and 'googletrans' python library to create multilingual YouTube videos. The steps involved are as follows:

1. Getting the video and Cloning the voice:
   - The script uses voice cloning technology to clone the voice of the video's author, based on the `sample.mp3` file (Original audio track from the video)

2. Transcript Translation:
   - The script leverages googletrans library to translate the script to the languages that ElevenLabs' API supports

3. Voice-Over and Video Generation:
   - The translated transcript is combined with the voice-over to create the final multilingual video, `Final_Video.mp4`.

## :medical_symbol: Contributing

Contributions to TranslatorYouTuber are welcome! If you find any issues or want to improve the script, feel free to submit a pull request. For major changes or new features, please open an issue first to discuss the proposed changes.
