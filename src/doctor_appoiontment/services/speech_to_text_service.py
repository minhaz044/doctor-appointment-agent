import io
import soundfile as sf

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SpeechToTextService:

    def __init__(self):
        self._client = OpenAI()

    def convert_to_text(self, audio):
        print("Converting audio to text........")

        buffer = io.BytesIO()
        sf.write(buffer, audio, 16000, format="WAV")
        buffer.seek(0)

        transcript = self._client.audio.transcriptions.create(
            model="gpt-transcribe",
            file=("recording.wav", buffer, "audio/wav"),
            languages=["en"]
        )

        return transcript.text.strip()