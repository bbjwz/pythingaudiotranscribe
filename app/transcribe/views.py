import requests
from pydub import AudioSegment
import speech_recognition as sr
from django.http import JsonResponse
from django.views import View

class TranscribeAudioView(View):

    def get(self, request, *args, **kwargs):
        url = request.GET.get('url')
        if not url:
            return JsonResponse({'error': 'URL parameter is required'}, status=400)
        
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
            return JsonResponse({'transcription': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Could not understand audio'}, status=400)
        except sr.RequestError as e:
            return JsonResponse({'error': f'Could not request results; {e}'}, status=500)
