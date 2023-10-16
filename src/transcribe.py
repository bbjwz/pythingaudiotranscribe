import os
import requests
from pydub import AudioSegment
import speech_recognition as sr
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_audio(url):
    try:
        response = requests.get(url, stream=True)
        logging.debug(response.status_code)  # Should be 200
        response.raise_for_status()
        logging.debug(f'Expected content length: {response.headers.get("Content-Length")}')

        logging.debug('Starting to write audio data to file')
        with open('audio_stream.mp3', 'wb') as file:
            for chunk in response.iter_content(chunk_size=2048):
             file.write(chunk)
        logging.debug('Finished writing audio data to file')

        logging.debug(f'File size: {os.path.getsize("audio_stream.mp3")} bytes')  # Debug Step 2

        audio_file = AudioSegment.from_mp3('audio_stream.mp3')
        logging.debug(audio_file)  # Debug Step 3

        audio_data = sr.AudioData(audio_file.raw_data, audio_file.frame_rate, audio_file.sample_width)
        logging.debug(audio_data)  # Debug Step 4

        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio_data)
        logging.debug(f'Transcription: {text}')

    except sr.UnknownValueError:
        logging.error("Could not understand audio")

    except sr.RequestError as e:
        logging.error(f'Could not request results; {e}')

    except Exception as e:
        logging.error(f'Exception occurred: {e}')
        logging.error("Exception", exc_info=True)  # This will log the full exception traceback

if __name__ == '__main__':
    AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    transcribe_audio(AUDIO_URL)
