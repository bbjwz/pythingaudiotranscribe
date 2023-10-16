import os
import requests
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk

def transcribe_audio(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open('audio_stream.wav', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    audio_file = AudioSegment.from_wav('audio_stream.wav')
    
    azure_key = os.environ.get('AZURE_KEY')
    if not azure_key:
        raise ValueError("AZURE_KEY environment variable is not set.")
    
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region="your-region")
    audio_config = speechsdk.audio.AudioConfig(filename='audio_stream.wav')
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

if __name__ == '__main__':
    AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    transcribe_audio(AUDIO_URL)


    # AUDIO_URL = 'https://stream06.dotpoint.nl:8004/stream'
    # AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    # AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    # https://24443.live.streamtheworld.com/CSPANRADIO.mp3
    