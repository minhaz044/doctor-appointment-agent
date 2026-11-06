from langchain.tools import tool
from services.doctor_info_service import DoctorInfoService
from typing import List

_info_service = DoctorInfoService()


@tool
def get_all_medicine_department_list_with_symptom():
    """
        Find All medical departments list.
        Args:  No Argument required
        Return All department  with details.
    """
    return _info_service.get_all_departments()


# @tool
# def get_department_searched_by_symptom(symptoms: List[str]):
#     """
#     Find relevant medical departments based on the patient's symptoms list.
#     Args:
#         Take a list of symptoms
#     Return matching department IDs and names and symptoms details.
#     """
#     return _info_service.get_department_by_symptom(symptoms)


@tool
def get_doctors_list():
    """
    Retrieve doctors belonging to a specific department
    Args:
        No param needed
    Return all doctor list
    """
    return _info_service.get_doctors_by_department(0)


@tool
def get_doctors_list_by_department_id(department_id: int):
    """
    Retrieve doctors belonging to a specific department
    Args:
        Take department_id as param,
    Return all teh doctor slist of that department.
    """
    return _info_service.get_doctors_by_department(department_id)


@tool
def get_doctor_details_and_schedule_info_by_doctor_id(doctor_id: int):
    """
    Retrieve a doctor's profile and available consultation schedule
    Args:
        take doctor id as param
    using the doctor's unique ID.
    """
    return _info_service.get_doctor_details(doctor_id)


@tool
def get_doctor_details_by_name(doctor_name: str):
    """
    Find doctors by name using case-insensitive regular expression matching.
    Args:
        take the doctor name as param ,and match pattern , So small name better result , but 3+ char beer
    Find doctor list by name using case-insensitive regular expression matching.
    """
    return _info_service.get_doctor_details_by_name(doctor_name)
