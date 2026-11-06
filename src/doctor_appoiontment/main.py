from services.voice_input_service import VoiceInputService
from services.speech_to_text_service import SpeechToTextService
from services.doctor_info_service import DoctorInfoService

# vs = VoiceInputService()
# audio = vs.take_voice_input()
# vs.play_audio(audio)
#
# audio2text = SpeechToTextService()
# converted_text = audio2text.convert_to_text(audio)
#
# print(converted_text)


doctor_info_service = DoctorInfoService()
print(doctor_info_service.get_all_departments())
print(doctor_info_service.get_all_doctors())
print("Application exiting............")
