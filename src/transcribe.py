import os
import requests
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_chunk(chunk_data):
    # Save chunk data to file
    with open('audio_chunk.wav', 'wb') as file:
        file.write(chunk_data)

    # Transcribe the audio chunk
    azure_key = os.environ.get('AZURE_KEY')
    if not azure_key:
        raise ValueError("AZURE_KEY environment variable is not set.")
    
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region="westeurope")
    audio_config = speechsdk.audio.AudioConfig(filename='audio_chunk.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Transcription: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

def process_stream(url, chunk_duration=10):
    # Calculate chunk size in bytes given the chunk_duration in seconds
    # Assuming a bitrate of 128kbps for the stream, adjust if needed.
    chunk_size = int(128 * 1024 * chunk_duration / 8) 

    while True:
        response = requests.get(url, stream=True, timeout=(5, 30))
        chunk_data = b""
        for data in response.iter_content(chunk_size=chunk_size):
            chunk_data += data
            if len(chunk_data) >= chunk_size:
                break
        
        # Transcribe this chunk
        transcribe_chunk(chunk_data)

if __name__ == '__main__':
    AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    process_stream(AUDIO_URL)

    # AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    # AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    # AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    # https://24443.live.streamtheworld.com/CSPANRADIO.mp3
    