import requests
from pydub import AudioSegment
import speech_recognition as sr
import logging
import io

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_audio(url):
    try:
        response = requests.get(url, stream=True)
        logging.debug(response.status_code)  # Should be 200
        response.raise_for_status()

        recognizer = sr.Recognizer()
        
        for chunk in response.iter_content(chunk_size=8192):
            audio_stream = io.BytesIO(chunk)  # Create a byte stream from the chunk
            audio_file = AudioSegment.from_file(audio_stream, format="mp3")  # Adjust the format accordingly
            audio_data = sr.AudioData(audio_file.raw_data, audio_file.frame_rate, audio_file.sample_width)
            
            try:
                text = recognizer.recognize_google(audio_data)
                logging.debug(f'Transcription: {text}')
            except sr.UnknownValueError:
                logging.error("Could not understand audio")
            except sr.RequestError as e:
                logging.error(f'Could not request results; {e}')

    except Exception as e:
        logging.error(f'Exception occurred: {e}', exc_info=True)

if __name__ == '__main__':
    AUDIO_URL = 'https://22343.live.streamtheworld.com/KINK.mp3'
    transcribe_audio(AUDIO_URL)


    # AUDIO_URL = 'https://stream.bnr.nl/bnr_mp3_128_03'
    # AUDIO_URL = 'https://24443.live.streamtheworld.com/CSPANRADIO.mp3'
    #https://24443.live.streamtheworld.com/CSPANRADIO.mp3
    