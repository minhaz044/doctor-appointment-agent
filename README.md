# 🩺 Voice AI Medical Receptionist

> A voice-powered AI receptionist that talks to patients, figures out which
> department they need, finds the right doctor, checks the schedule, and books
> the appointment — all using natural spoken conversation.

---

## Table of Contents

1. [The Story](#-the-story)
2. [The Idea](#-the-idea)
3. [What You'll Build](#-what-youll-build)
4. [Architecture](#-architecture)
5. [Project Structure](#-project-structure)
6. [Prerequisites](#-prerequisites)
7. [Step-by-Step Tutorial](#-step-by-step-tutorial)
   - [Step 0 — Project Setup](#step-0--project-setup)
   - [Step 1 — Sample Data](#step-1--sample-data)
   - [Step 2 — The Data Layer (DoctorInfoService)](#step-2--the-data-layer-doctorinfoservice)
   - [Step 3 — Doctor Tools](#step-3--doctor-tools)
   - [Step 4 — Appointment & Utility Tools](#step-4--appointment--utility-tools)
   - [Step 5 — LLM Models](#step-5--llm-models)
   - [Step 6 — The Answer Domain Model](#step-6--the-answer-domain-model)
   - [Step 7 — The System Prompt](#step-7--the-system-prompt)
   - [Step 8 — Voice Input Service](#step-8--voice-input-service)
   - [Step 9 — Speech-to-Text Service](#step-9--speech-to-text-service)
   - [Step 10 — Text-to-Speech Service](#step-10--text-to-speech-service)
   - [Step 11 — Build the Agent](#step-11--build-the-agent)
   - [Step 12 — The Conversation Loop](#step-12--the-conversation-loop)
   - [Step 13 — Run It](#step-13--run-it)
8. [How a Booking Flows](#-how-a-booking-flows)
9. [Where It Can Go Next](#-where-it-can-go-next)

---

## 📖 The Story

A few days ago, I was looking for a doctor's appointment for my wife. It was
around **8:30 PM**, she wasn't feeling well, and I just needed one thing — a
consultation slot for the next morning.

So I called the hospital reception.

The phone rang. And rang. And rang. **Nobody picked up.**

No one should have to sit on hold at 8:30 PM just to book a slot that a machine
could hand out in 30 seconds. And here's the thing: the information I needed —
which department, which doctor, what times are free — was all sitting in a
database. The only thing missing was a human to *listen* to me and *click* the
right buttons.

That "human" is exactly what a modern AI agent is good at: **listen → understand
→ call the right tool → confirm.** So I built it.

---

## 💡 The Idea

Instead of a rigid phone menu ("Press 1 for Cardiology…"), we give the patient a
**voice agent** that:

- **Listens** to what the patient says (symptoms, a doctor's name, a request).
- **Reasons** about what to do next (which department? which doctor? which slot?).
- **Calls tools** to fetch real data from our system.
- **Books** the appointment and confirms it in natural language.

The patient just talks. The agent does the rest.

---

## 🎯 What You'll Build

A CLI voice assistant with five moving parts:

| Part | Responsibility | Tech |
|------|----------------|------|
| **Voice Input** | Record the patient's speech | `sounddevice`, `numpy` |
| **Speech-to-Text** | Turn the recording into text | OpenAI audio API |
| **Agent** | Decide what to do, call tools | LangGraph `create_agent` + LLM |
| **Tools + Data** | Look up departments/doctors, book | LangChain `@tool` + JSON data |
| **Text-to-Speech** | Speak the reply back | OpenAI TTS |

The agent is the brain. Everything else is either an **ear** (voice in), a
**mouth** (voice out), or a **hand** (tools that touch data).

---

## 🏗 Architecture

Here's the whole system at a glance:

```
                     ┌───────────────────────────────────────────────┐
                     │        VOICE AI MEDICAL RECEPTIONIST          │
                     └───────────────────────────────────────────────┘

   🎤 Patient talks
        │
        ▼
 ┌───────────────┐  raw audio   ┌──────────────────┐   text    ┌─────────────────┐
 │ Voice Input   │ ───────────► │ Speech-to-Text   │ ────────► │  LangGraph      │
 │ sounddevice   │              │ (OpenAI Whisper) │           │  Agent  (LLM)   │
 └───────────────┘              └──────────────────┘           └────────┬────────┘
                                                                        │
                                                         decides & calls │ tools
                                                                        ▼
                                                     ┌───────────────────────────────┐
                                                     │            Tools              │
                                                     │  • departments by symptom     │
                                                     │  • doctors by department       │
                                                     │  • doctor details + schedule   │
                                                     │  • create appointment          │
                                                     │  • today's date & time         │
                                                     └───────────────┬───────────────┘
                                                                     │ reads
                                                                     ▼
                                                     ┌───────────────────────────────┐
                                                     │      DoctorInfoService        │
                                                     │  departments.json             │
                                                     │  doctors.json                 │
                                                     └───────────────────────────────┘

   🔈 Agent reply ──► prints text ──► (optional Text-to-Speech) ──► speaks back
```

And the **conversation loop** looks like this:

```
   ┌───────────────────────────────────────────────────────────────┐
   │                                                               │
   ▼                                                               │
 Record voice ─► Transcribe ─► Agent reasons ─► calls tools ─► Reply
   ▲                                                          │
   │                    conversation still open?              │
   └──────────────────────────── yes ─────────────────────────┘
                              │ no
                              ▼
                          Booked ✅ end
```

---

## 📁 Project Structure

```
voice-ai-medical-receptionist/
├── pyproject.toml
├── .env                          # API keys (not committed)
├── README.md
└── src/
    ├── resources/
    │   └── data/
    │       ├── departments.json   # 20 departments + their symptoms
    │       └── doctors.json       # 50 doctors + schedules
    └── doctor_appointment/
        ├── main.py                # entry point + conversation loop
        ├── domain/
        │   └── answer.py          # structured LLM response model
        ├── models/
        │   └── llm_models.py      # the LLM(s) we use
        ├── prompt/
        │   └── appointment_system_prompt.py
        ├── services/
        │   ├── doctor_info_service.py   # reads the JSON data
        │   ├── voice_input_service.py   # records microphone
        │   ├── speech_to_text_service.py
        │   └── text_to_speech_service.py
        └── tools/
            ├── doctor_info_tools.py     # @tool wrappers over the service
            ├── appointment_tools.py     # @tool to book
            └── utility_tools.py         # @tool for today's date
```

---

## ✅ Prerequisites

- **Python 3.13+**
- **[uv](https://github.com/astral-sh/uv)** (or plain `pip`)
- A working **microphone**
- API keys for **OpenAI** (Whisper + TTS) and **Google Gemini** (or OpenAI) for the LLM

---

## 🧭 Step-by-Step Tutorial

### Step 0 — Project Setup

Create the project and install dependencies. We need an audio stack
(`sounddevice`, `soundfile`, `numpy`), an LLM stack (`langchain`, `langgraph`,
provider SDKs), and `python-dotenv` for config.

```bash
uv init voice-ai-medical-receptionist
cd voice-ai-medical-receptionist
```

`pyproject.toml`:

```toml
[project]
name = "voice-ai-medical-receptionist"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "openai",
    "python-dotenv",
    "sounddevice",
    "soundfile",
    "numpy",
    "langchain",
    "langgraph",
    "langchain_google_genai",
    "langchain_openai",
]
```

Create a `.env` file (never commit this):

```dotenv
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

> **Why separate services?** Each concern (voice, speech, LLM, data) lives on its
> own so we can swap any one of them without touching the others. Want a
> different STT provider? Replace one file.

---

### Step 1 — Sample Data

Our "database" is two JSON files. This keeps the demo self-contained — no real
DB required. Real systems would replace these with an API or SQL, but the
**shape** stays the same.

`src/resources/data/departments.json` — a department has an id, a name, and
associated symptoms:

```json
[
  {
    "department_id": 1,
    "department_name": "Cardiology",
    "symptoms": ["Chest pain", "Shortness of breath", "Heart palpitations", "Irregular heartbeat"]
  },
  {
    "department_id": 6,
    "department_name": "Gastroenterology",
    "symptoms": ["Stomach pain", "Acidity", "Heartburn", "Diarrhea", "Constipation"]
  }
]
```

`src/resources/data/doctors.json` — a doctor has a name, the departments they
belong to, specializations, and their weekly schedule:

```json
[
  {
    "doctor_id": 101,
    "doctor_name": "Dr. Ahmed Rahman",
    "department_ids": [1, 2],
    "specializations": ["Cardiology", "Internal Medicine"],
    "available_schedule": [
      {
        "day": "Saturday",
        "consultation_hours": {
          "Morning": { "start_time": "09:00 AM", "end_time": "01:00 PM" }
        }
      },
      {
        "day": "Monday",
        "consultation_hours": {
          "Evening": { "start_time": "05:00 PM", "end_time": "08:00 PM" }
        }
      }
    ]
  }
]
```

📌 Note the two important links: a doctor lists `department_ids`, and a department
lists `symptoms`. That's what lets the agent go **symptom → department → doctor**.

---

### Step 2 — The Data Layer (DoctorInfoService)

Tools shouldn't read raw files. We wrap the data in a small service with clear
methods and simple in-memory caching.

`src/doctor_appointment/services/doctor_info_service.py`:

```python
import json
import re
from pathlib import Path


class DoctorInfoService:

    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        self._data_dir = project_root / "resources" / "data"
        self._departments = None
        self._doctors = None

    def _load_json(self, filename: str):
        file_path = self._data_dir / filename
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_all_departments(self):
        if self._departments is None:
            self._departments = self._load_json("departments.json")
        return self._departments

    def get_all_doctors(self):
        if self._doctors is None:
            self._doctors = self._load_json("doctors.json")
        return self._doctors

    def get_department_by_symptom(self, symptoms: list[str]):
        departments = self.get_all_departments()
        matched = []
        for department in departments:
            for symptom in department["symptoms"]:
                if symptom in symptoms:
                    matched.append(department)
                    break
        return matched

    def get_doctors_by_department(self, department_id: int = 0):
        doctors = self.get_all_doctors()
        if department_id == 0:
            return doctors
        return [d for d in doctors if department_id in d["department_ids"]]

    def get_doctor_details(self, doctor_id: int):
        for doctor in self.get_all_doctors():
            if doctor["doctor_id"] == doctor_id:
                return doctor
        return {"error": "Doctor not found"}

    def get_doctor_details_by_name(self, doctor_name: str):
        pattern = re.compile(re.escape(doctor_name.strip()), re.IGNORECASE)
        return [d for d in self.get_all_doctors() if pattern.search(d["doctor_name"])]
```

✅ Plain Python, easy to test, and the file loads happen only once thanks to the
`if ... is None` cache.

---

### Step 3 — Doctor Tools

Now we expose the service to the LLM as **tools**. In LangChain, a tool is just a
function with a `@tool` decorator — the **docstring is the prompt**, so the model
knows *when* and *how* to call it.

`src/doctor_appointment/tools/doctor_info_tools.py`:

```python
from langchain.tools import tool
from services.doctor_info_service import DoctorInfoService

_info_service = DoctorInfoService()


@tool
def get_all_medicine_department_list_with_symptom():
    """Find all medical departments with their symptoms.
    Args: No argument required.
    Return all departments with details."""
    return _info_service.get_all_departments()


@tool
def get_doctors_list_by_department_id(department_id: int):
    """Retrieve doctors belonging to a specific department.
    Args: department_id (int).
    Return all doctors in that department."""
    return _info_service.get_doctors_by_department(department_id)


@tool
def get_doctor_details_and_schedule_info_by_doctor_id(doctor_id: int):
    """Retrieve a doctor's profile and available consultation schedule using the doctor's unique ID.
    Args: doctor_id (int)."""
    return _info_service.get_doctor_details(doctor_id)


@tool
def get_doctor_details_by_name(doctor_name: str):
    """Find doctors by name using case-insensitive matching.
    Args: doctor_name (str). Use 3+ characters for a good match."""
    return _info_service.get_doctor_details_by_name(doctor_name)
```

> 💡 **Tip:** Tool descriptions are the single most important lever for reliable
> agents. Be explicit about arguments and what the tool returns — vague
> docstrings are the #1 cause of a confused agent.

---

### Step 4 — Appointment & Utility Tools

Two more tools: one to **create** the appointment (a stub here — swap in a real
DB write later) and one so the agent can reason about **today's date**.

`src/doctor_appointment/tools/appointment_tools.py`:

```python
from langchain.tools import tool


@tool
def create_an_appointment(doctor_id: int, date: str, time: str):
    """Create a doctor's appointment on a particular date and time.
    Args:
        doctor_id - the doctor you want to take appointment with
        date - the date the patient will consult the doctor
        time - the time the patient will consult the doctor
    Return: confirmation text."""
    return (
        f"Confirmation: Your appointment is successfully scheduled on "
        f"{date} at {time}. Please note, your serial number is 10."
    )
```

`src/doctor_appointment/tools/utility_tools.py`:

```python
@tool
def get_today_date_and_time():
    """Return today's date, time, and weekday name."""
    return "Today is 01 November 2026, Sunday, Current time: 10:35"
```

> In production, use `datetime.now()` here. It's stubbed so the agent has a
> deterministic grounding for reasoning about "tomorrow" or "next Saturday".

---

### Step 5 — LLM Models

Keep model creation in one place so you can switch providers freely.

`src/doctor_appointment/models/llm_models.py`:

```python
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Use valid model identifiers for your provider.
_gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
_openai_llm = ChatOpenAI(model="gpt-4.1-mini")

llm = _openai_llm   # swap providers by changing this one line
```

> The original project also defines a Gemini fallback — pick whichever model you
> have keys for and can afford. Tool-calling quality matters more than raw
> intelligence here.

---

### Step 6 — The Answer Domain Model

We want the agent's final response to be **structured**, not just free text. A
Pydantic model gives us two things: the spoken answer, and a boolean telling the
loop whether the conversation is **finished** or should continue.

`src/doctor_appointment/domain/answer.py`:

```python
from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(description="The reply to give the patient")
    conversation: bool = Field(
        default=True,
        description=(
            "True if the conversation should continue; "
            "False once the appointment has been booked."
        ),
    )
```

This is the **termination signal** for our loop — the agent decides when the job
is done.

---

### Step 7 — The System Prompt

The prompt defines the agent's personality and — crucially — its **step-by-step
goal chain**: symptom → department → doctor → schedule → booking.

`src/doctor_appointment/prompt/appointment_system_prompt.py`:

```python
APPOINTMENT_SYSTEM_PROMPT = """
You are a highly efficient, empathetic, and professional Medical Assistant voice AI.
Your goal is to help patients find the right department or doctor, check schedules,
and guide them toward booking an appointment based on their symptoms or requests.
Your replies will be read aloud, so keep them voice-friendly.

CORE GOAL: find a doctor and book an appointment for the patient.

Patient Problem => department
department      => doctor list
doctor list     => specific doctor
specific doctor => date and time the patient wants
date_time       => appointment creation

At each step, if something is found, proceed to the next step, always keeping the
end goal (booking an appointment) in mind.

RULES:
- Tone: empathetic, polite, clear, reassuring.
- Respond in the patient's language (Bengali or English).
- Do not diagnose. Rely strictly on tool results.
- If symptoms are vague, ask a gentle follow-up before calling tools.
- Suggest at most 2 doctors at a time, conversationally — don't dump a big list.
- Present names, specialties, and available slots as clean bullet points.
"""
```

---

### Step 8 — Voice Input Service

This records audio from the mic using a callback that appends chunks, then
concatenates them into one NumPy array.

`src/doctor_appointment/services/voice_input_service.py`:

```python
import sounddevice as sd
import numpy as np


class VoiceInputService:

    def __init__(self):
        self._sample_rate = 16000
        self._audio_chunks = []

    def _callback(self, indata, frames, time, status):
        print(".", end=" ")
        self._audio_chunks.append(indata.copy())

    def take_voice_input(self):
        input("Press Enter to start recording")
        print("Recording...")
        self._audio_chunks = []
        stream = sd.InputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        stream.start()
        input("Press Enter to stop")
        stream.stop()
        print("Recording finished.")
        return np.concatenate(self._audio_chunks, axis=0)

    def play_audio(self, audio_data):
        sd.play(audio_data, samplerate=self._sample_rate)
        sd.wait()
```

> **Why 16 kHz mono?** It's exactly what Whisper wants, so no resampling needed.

---

### Step 9 — Speech-to-Text Service

We take the NumPy audio, write it into an in-memory WAV buffer, and send it to
OpenAI's transcription API.

`src/doctor_appointment/services/speech_to_text_service.py`:

```python
import io
import soundfile as sf
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SpeechToTextService:

    def __init__(self):
        self._client = OpenAI()

    def convert_to_text(self, audio):
        print("Converting audio to text...")
        buffer = io.BytesIO()
        sf.write(buffer, audio, 16000, format="WAV")
        buffer.seek(0)

        transcript = self._client.audio.transcriptions.create(
            model="whisper-1",
            file=("recording.wav", buffer, "audio/wav"),
        )
        return transcript.text.strip()
```

> Using an **in-memory buffer** avoids writing temp files to disk on every turn.

---

### Step 10 — Text-to-Speech Service

Finally, the "mouth". This one isn't strictly required to close the loop, but it
turns the assistant into a real voice agent.

`src/doctor_appointment/services/text_to_speech_service.py`:

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class TextToSpeechService:

    def __init__(self):
        self._client = OpenAI()

    def convert_to_audio(self, text: str, output_filename: str = "output.mp3"):
        print("Converting text to audio...")
        response = self._client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file(output_filename)
        return output_filename
```

> **To make the assistant speak**, call this with the agent's `answer` and play
> the resulting file. (The reference `main.py` prints the reply; wiring TTS in is
> a one-line addition — see Step 12.)

---

### Step 11 — Build the Agent

This is where it all clicks together. `create_agent` gives us an LLM that can use
our tools. We pass:

- the **model**,
- the **system prompt**,
- the **tools**,
- a **checkpointer** (so it remembers the conversation across turns), and
- **`response_format=Answer`** (so we get structured output we can loop on).

`src/doctor_appointment/main.py` (part 1):

```python
from uuid import uuid4
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from models.llm_models import llm
from prompt.appointment_system_prompt import APPOINTMENT_SYSTEM_PROMPT
from domain.answer import Answer
from tools.doctor_info_tools import (
    get_all_medicine_department_list_with_symptom,
    get_doctors_list_by_department_id,
    get_doctor_details_and_schedule_info_by_doctor_id,
    get_doctor_details_by_name,
)
from tools.appointment_tools import create_an_appointment
from tools.utility_tools import get_today_date_and_time

appointment_agent = create_agent(
    name="Doctor appointment agent",
    model=llm,
    system_prompt=APPOINTMENT_SYSTEM_PROMPT,
    tools=[
        get_all_medicine_department_list_with_symptom,
        get_doctors_list_by_department_id,
        get_doctor_details_and_schedule_info_by_doctor_id,
        get_doctor_details_by_name,
        create_an_appointment,
        get_today_date_and_time,
    ],
    checkpointer=InMemorySaver(),
    response_format=Answer,
)
```

> 🔑 **Two details that matter:**
> 1. **`InMemorySaver`** — without it, the agent forgets everything between turns.
> 2. **`response_format=Answer`** — the agent must return `{answer, conversation}`,
>    so we can reliably detect when the booking is done.

---

### Step 12 — The Conversation Loop

Now we wire the ear (voice in), the brain (agent), and prepare the mouth (voice
out) into a loop that runs until the agent says the conversation is over.

`src/doctor_appointment/main.py` (part 2):

```python
from langchain_core.messages import HumanMessage
from services.voice_input_service import VoiceInputService
from services.speech_to_text_service import SpeechToTextService

vs = VoiceInputService()
stt = SpeechToTextService()


def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    audio = vs.take_voice_input()
    question = stt.convert_to_text(audio)
    print(f"Patient: {question}")

    conversation = True
    while conversation:
        response = appointment_agent.invoke(
            {"messages": HumanMessage(content=question)},
            config=config,
        )
        answer = response["structured_response"]
        print(f"AI: {answer.answer}")

        # Optional: speak the reply back
        # from services.text_to_speech_service import TextToSpeechService
        # TextToSpeechService().convert_to_audio(answer.answer)
        # ...then play "output.mp3"

        conversation = answer.conversation
        if conversation:
            audio = vs.take_voice_input()
            question = stt.convert_to_text(audio)
            print(f"Patient: {question}")


if __name__ == "__main__":
    run_conversation()
    print("Session ended. Take care!")
```

The `thread_id` key is what lets the checkpointer keep the context of *this*
patient's call.

---

### Step 13 — Run It

```bash
uv run python src/doctor_appointment/main.py
```

A real session might look like this:

```
Press Enter to start recording
Recording...
Patient: my wife has had severe stomach pain for two days
AI: I understand — that sounds uncomfortable. Based on the symptoms,
    the Gastroenterology department is the best fit. Would you like me
    to show the available doctors?
Press Enter to start recording
Patient: yes please
AI: Here are two doctors available:
    • Dr. Rezaul Islam — Gastroenterology, Sat 9:00 AM–12:00 PM
    • Dr. Anisur Rahman — Gastroenterology, Sat 10:00 AM–1:00 PM
    Which one would you like?
Patient: Dr. Rezaul Islam, tomorrow morning
AI: Perfect. Dr. Rezaul Islam is available today. Shall I book you in
    for tomorrow at 9:00 AM?
Patient: yes
AI: Done! Your appointment with Dr. Rezaul Islam is confirmed for tomorrow
    at 9:00 AM. Your serial number is 10.
Session ended. Take care!
```

🎉 An appointment booked at 8:30 PM, with no one on the other end of the line.

---

## 🔁 How a Booking Flows

The agent walks a decision chain, calling a tool at each step:

```
  🗣  "stomach pain for 2 days"
        │
        ▼
  ┌─────────────────────────────────────────────┐
  │ get_all_medicine_department_list_with_symptom│  → Gastroenterology
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────────────┐
  │ get_doctors_list_by_department_id(6)         │  → [Dr. Rezaul, Dr. Anisur, ...]
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────────────┐
  │ get_doctor_details_and_schedule_info_by_id   │  → slot: Sat 9:00 AM–12:00 PM
  └─────────────────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────────────────┐
  │ create_an_appointment(107, "2026-11-07", ...)│  → confirmed ✅
  └─────────────────────────────────────────────┘
        │
        ▼
   Answer(conversation=False)  → loop ends
```

---

## 🚀 Where It Can Go Next

This is a working foundation, not the finish line. Some natural upgrades:

- **Streaming voice** — replace push-to-talk with real-time VAD so it feels like a phone call.
- **Real backend** — swap `DoctorInfoService` JSON reads for a database or clinic API.
- **Real STT/TTS options** — try local models (Whisper.cpp, Piper) to cut API costs.
- **Persistent memory** — replace `InMemorySaver` with a DB checkpointer for cross-call context.
- **SMS/WhatsApp confirmation** — send the confirmation to the patient's phone.
- **Guardrails** — add a max-turn limit and a hand-off-to-human path for emergencies.
- **Tests** — the data layer and tools are pure functions; they're easy to unit test.

The core lesson is simple: **let the LLM reason, keep the data in tools, and
constrain the output with a schema.** That pattern builds agents that actually
finish the job.

---

<p align="center"><i>Built because nobody should wait on hold at 8:30 PM to book a doctor.</i></p>
