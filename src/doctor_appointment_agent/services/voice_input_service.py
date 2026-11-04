import sounddevice as sd


class VoiceInputService:

    def take_voice_input(self, duration=5):
        print("start recording..........")
        sample_rate = 16000
        audio = sd.rec(
            int(duration * sample_rate), samplerate=sample_rate,
            channels=1, dtype="float32")
        sd.wait()
        print("Recording completed!")
        return audio.flatten()

    def play_audio(self, audio_data, sample_rate=16000):
        print("Playing audio...")

        sd.play(audio_data, samplerate=sample_rate)

        # Wait until audio finishes playing
        sd.wait()


vs = VoiceInputService()
audio=vs.take_voice_input()
vs.play_audio(audio)