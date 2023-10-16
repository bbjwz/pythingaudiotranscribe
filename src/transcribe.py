import os
import requests
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_audio(url):
    response = requests.get(url, stream=True, timeout=(5, 10))  # 5 seconds to connect, 10 seconds to read
    logging.debug(response.status_code)  # Should be 200
    logging.debug(f'Content-Length: {response.headers.get("Content-Length")}')
    logging.debug(f'Content-Type: {response.headers.get("Content-Type")}')
    logging.debug(f'Accept-Ranges: {response.headers.get("Accept-Ranges")}')
    response.raise_for_status()

    try:
        with open('audio_stream.wav', 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                logging.debug(f"First chunk: {chunk[:100]}")  # Log the first 100 bytes of the first chunk
                file.write(chunk)
    except Exception as e:
        logging.error(f"Exception while writing file: {e}")

    logging.debug(f'File size: {os.path.getsize("audio_stream.wav")} bytes')  # Debug Step 2
    
    print("It gets here")
    audio_file = AudioSegment.from_wav('audio_stream.wav')
    print("Audiosegment found?")

    azure_key = os.environ.get('AZURE_KEY')
    print(f"Key: {azure_key}")
    if not azure_key:
        raise ValueError("AZURE_KEY environment variable is not set.")
    
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region="westeurope")
    audio_config = speechsdk.audio.AudioConfig(filename='audio_stream.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    logging.debug('Initializing Speech Recognizer')
    logging.debug('Starting transcription')
    result = speech_recognizer.recognize_once()
    logging.debug('Transcription result received')
    logging.debug(f'Result: {result}')
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Transcription: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

if __name__ == '__main__':
    AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    transcribe_audio(AUDIO_URL)


    # AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    # AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    # AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    # https://24443.live.streamtheworld.com/CSPANRADIO.mp3
    