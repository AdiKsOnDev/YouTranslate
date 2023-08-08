# TranslatorYoutube-API Documentation

## Introduction
This API documentation provides details about the endpoints available in the application. 
The API allows users 2 routes, one of which returns the a translated voiceover of a YouTube video 
and the other which clones the voice in the YouTube video, layers it over the video and returns the new video

## Base URL
The base URL for all API endpoints is `[http://127.0.0.1:5000]` when running the application locally with Flask.

## Endpoints

### `POST /translated_audio`
An API route that translates the audio track of a YouTube video and returns the translated audio in MP3 format.

#### Request Body
The request body should be a JSON object with the following parameters:

- `video_url` (string, required): The URL of the YouTube video for which the audio needs to be translated.
- `language_code` (string, required): The language code for the desired translation language (e.g., 'en' for English, 'fr' for French,
-  'de' for German, 'pl' for Polish, 'es' for Spanish, 'it' for Italian, 'pt' for Portuguese, 'hi' for Hindi.

#### Response
- `200 OK`: If the translation is successful, the API will respond with the translated audio in MP3 format.
- `500 Internal Server Error`: If an error occurs during the translation process, the API will respond with an error message.

### `POST /translated_with_video`
An API route that clones the voice used in a YouTube video,  translates the cloned audio track of a YouTube video, creates a new video with the translated cloned audio track, and returns the final video in MP4 format.

#### Request Body
The request body should be a JSON object with the following parameters:

- `video_url` (string, required): The URL of the YouTube video for which the audio needs to be translated and video created.
- `language_code` (string, required): The language code for the desired translation language (e.g., 'en' for English, 'fr' for French).

#### Response
- `200 OK`: If the translation and video creation are successful, the API will respond with the final video in MP4 format.
- `400 Bad Request`: If the YouTube video URL is invalid or cannot be accessed, the API will respond with an error message.
- `500 Internal Server Error`: If an error occurs during the translation and video creation process, the API will respond with an error message.

## Running the Application
To run the application, execute the following command:

```bash
python FlaskAPIRouting.py
```


The application will be hosted locally on `http://127.0.0.1:5000`, and you can use the endpoints as described above.
