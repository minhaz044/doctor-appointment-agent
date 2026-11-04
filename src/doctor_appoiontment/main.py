from services.voice_input_service import VoiceInputService
from services.speech_to_text_service import SpeechToTextService

vs = VoiceInputService()
audio = vs.take_voice_input()
vs.play_audio(audio)

audio2text = SpeechToTextService()
converted_text = audio2text.convert_to_text(audio)

print(converted_text)
print("Application exiting............")
