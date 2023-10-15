import requests
from pydub import AudioSegment
import speech_recognition as sr

def transcribe_audio(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open('audio_stream.wav', 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    audio_file = AudioSegment.from_wav('audio_stream.wav')
    audio_data = sr.AudioData(audio_file.raw_data, audio_file.frame_rate, audio_file.sample_width)

    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio_data)
        print(f'Transcription: {text}')
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f'Could not request results; {e}')

if __name__ == '__main__':
    AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    transcribe_audio(AUDIO_URL)
