from faster_whisper import WhisperModel


class SpeechToTextService:
    def __init__(self):
        self._model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
            cpu_threads=4,
            num_workers=2
        )

    def convert_to_text(self, audio):
        print("Converting audio to text........")
        segments, info = self._model.transcribe(audio, beam_size=3, vad_filter=True, language="en")
        text = " ".join(segment.text for segment in segments)
        return text.strip()
