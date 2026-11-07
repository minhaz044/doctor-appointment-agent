import io

from openai import OpenAI
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf

load_dotenv()


class TextToSpeechService:

    def __init__(self):
        self._client = OpenAI()

    def _convert_to_audio(self, text):
        print("Converting text to audio........")

        response = self._client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            response_format="wav"
        )

        audio_buffer = io.BytesIO(response.content)

        return audio_buffer

    def _play_audio(self, audio_data):
        print("Playing audio...")
        audio_data.seek(0)
        data, sample_rate = sf.read(
            audio_data,
            dtype="float32"
        )
        sd.play(data, samplerate=sample_rate)
        sd.wait()

    def convert_to_audio_play(self, text):
        self._play_audio(self._convert_to_audio(text))
