import os
import requests
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import logging
import io

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_chunk(chunk_data):
    # Convert MP3 data to WAV format
    audio_chunk = AudioSegment.from_mp3(io.BytesIO(chunk_data))
    audio_chunk.export("audio_chunk.wav", format="wav")
    
    azure_key = os.environ.get('AZURE_KEY')
    if not azure_key:
        raise ValueError("AZURE_KEY environment variable is not set.")
    
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region="westeurope")
    
    # Setting the language to Dutch
    speech_config.speech_recognition_language = 'nl-NL'

    # Enabling audio logging
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EnableAudioLogging, "true")

    audio_config = speechsdk.audio.AudioConfig(filename='audio_chunk.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    logging.debug('Starting transcription')
    result = speech_recognizer.recognize_once()
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

def process_stream(url):
    response = requests.get(url, stream=True, timeout=(5, 10))
    response.raise_for_status()

    chunk_size = 32768  # 32KB
    chunk_data = b""
    for chunk in response.iter_content(chunk_size=chunk_size):
        chunk_data += chunk
        if len(chunk_data) > chunk_size * 20:  
            transcribe_chunk(chunk_data)
            chunk_data = b""

if __name__ == '__main__':
    AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    process_stream(AUDIO_URL)


    # AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    # AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    # AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    # https://24443.live.streamtheworld.com/CSPANRADIO.mp3
    