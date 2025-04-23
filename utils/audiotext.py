import io
import speech_recognition as sr
from fastapi import HTTPException
from pydub import AudioSegment

class AudioToTextConverter:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def convert_audio_to_text(self, audio_bytes):
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        wav_audio = io.BytesIO()
        audio.export(wav_audio, format="wav")
        wav_audio.seek
        with sr.AudioFile(wav_audio) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                raise HTTPException(
                    status_code=400, detail="Could not understand the audio")
            except sr.RequestError:
                raise HTTPException(
                    status_code=500, detail="Could not request results from the speech recognition service")