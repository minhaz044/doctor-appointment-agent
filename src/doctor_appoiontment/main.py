from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from domian.answer import Answer
from services.voice_input_service import VoiceInputService
from services.speech_to_text_service import SpeechToTextService
from services.text_to_speech_service import TextToSpeechService
from langchain.agents import create_agent
from models.llm_models import llm
from prompt.appiontment_system_prompt import APPOINTMENT_SYSTEM_PROMPT
from uuid import uuid4
from tools.doctor_info_tools import (
    get_all_medicine_department_list_with_symptom,
    get_doctors_list,
    get_doctors_list_by_department_id,
    get_doctor_details_by_name,
    get_doctor_details_and_schedule_info_by_doctor_id
)
from tools.appiontment_tools import create_an_appointment
from tools.utility_tools import get_today_date_and_time

appointment_agent = create_agent(
    name="Doctor appointment agent",
    model=llm,
    system_prompt=APPOINTMENT_SYSTEM_PROMPT,
    tools=[get_all_medicine_department_list_with_symptom,
           get_doctors_list,
           get_doctors_list_by_department_id,
           get_doctor_details_by_name,
           get_doctor_details_and_schedule_info_by_doctor_id,
           create_an_appointment,
           get_today_date_and_time],
    checkpointer=InMemorySaver(),
    response_format=Answer
)

vs = VoiceInputService()
audio2text = SpeechToTextService()
text2audio = TextToSpeechService()


def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    audio = vs.take_voice_input()
    # vs.play_audio(audio)
    converted_text = audio2text.convert_to_text(audio)
    print(converted_text)

    conversation = True

    while conversation:
        question = HumanMessage(content=converted_text)
        response = appointment_agent.invoke({"messages": question}, config=config)
        structured_response = response["structured_response"]
        print(f"Ai Response : {structured_response.answer}")

        text2audio.convert_to_audio_play(structured_response.answer)

        conversation = structured_response.conversation

        if conversation:
            audio = vs.take_voice_input()
            converted_text = audio2text.convert_to_text(audio)
            print(converted_text)


run_conversation()

print("Application exiting............")
