import sounddevice as sd
import numpy as np


class VoiceInputService:

    def __init__(self):
        self._sample_rate = 16000
        self._audio_chunks = []

    def _callback(self, indata, frames, time, status):
        print(".",end=" ")
        self._audio_chunks.append(indata.copy())

    def take_voice_input(self):
        input("Press any key to start")

        print("start recording..........")
        self._audio_chunks = []
        stream = sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback
        )
        stream.start()
        input("Please Enter to Stop")
        stream.stop()

        print("Recording completed........")
        audio = np.concatenate(self._audio_chunks, axis=0)
        return audio

    def play_audio(self, audio_data):
        print("Playing audio...")

        sd.play(audio_data, samplerate=self._sample_rate)
        sd.wait()
