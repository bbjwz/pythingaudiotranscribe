import os
import requests
from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(url):
    response = requests.get(url, stream=True)
    print(response.status_code)  # Should be 200
    response.raise_for_status()

    with open('audio_stream.mp3', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f'File size: {os.path.getsize("audio_stream.mp3")} bytes')  # Debug Step 2

    audio_file = AudioSegment.from_mp3('audio_stream.mp3')
    print(audio_file)  # Debug Step 3

    audio_data = sr.AudioData(audio_file.raw_data, audio_file.frame_rate, audio_file.sample_width)
    print(audio_data)  # Debug Step 4

    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data)
        print(f'Transcription: {text}')
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f'Could not request results; {e}')

if __name__ == '__main__':
    AUDIO_URL = 'https://25703.live.streamtheworld.com/BNR_NIEUWSRADIO.mp3?dist=nederlandfm'
    transcribe_audio(AUDIO_URL)
