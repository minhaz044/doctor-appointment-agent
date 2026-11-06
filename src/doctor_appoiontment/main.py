from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from services.voice_input_service import VoiceInputService
from services.speech_to_text_service import SpeechToTextService
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

appointment_agent = create_agent(
    name="Doctor appointment agent",
    model=llm,
    system_prompt=APPOINTMENT_SYSTEM_PROMPT,
    tools=[get_all_medicine_department_list_with_symptom,
           get_doctors_list,
           get_doctors_list_by_department_id,
           get_doctor_details_by_name,
           get_doctor_details_and_schedule_info_by_doctor_id],
    checkpointer=InMemorySaver()
)

vs = VoiceInputService()
audio = vs.take_voice_input()
vs.play_audio(audio)

audio2text = SpeechToTextService()
converted_text = audio2text.convert_to_text(audio)

print(converted_text)

config = {"configurable": {"thread_id": str(uuid4())}}

question = HumanMessage(content=converted_text)
conversation = True

response = appointment_agent.invoke({"messages": question}, config=config)

print(response)
# print(response.text)

print("Application exiting............")
