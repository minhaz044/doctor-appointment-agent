from langchain.tools import tool


@tool
def create_an_appointment(doctor_id: int, date: str, time: str):
    """
    Create a doctor's appointment on a particular date and time
    Args :
        doctor_id - the doctor you want to take appointment
        date - the date patient will like to consult the doctor
        time -  what time patient will take the consultation of the doctor
    Return a Successfully appointment taken or Rejected due to allocation filled for today
    """
    return f"Confirmation: Your appointment is successfully scheduled on {date} at {time}. Please note, your serial number is 10."
