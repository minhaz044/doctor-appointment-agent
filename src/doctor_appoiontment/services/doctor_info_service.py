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
        matched_departments = []

        for department in departments:
            for department_symptom in department["symptoms"]:
                if department_symptom in symptoms:
                    matched_departments.append(department)
                    break

        return matched_departments

    def get_doctors_by_department(self, department_id: int = 0):
        """    Retrieve doctors belonging to a specific department.        """

        doctors = self.get_all_doctors()
        if department_id == 0:
            return doctors

        return [
            doctor
            for doctor in doctors
            if department_id in doctor["department_ids"]
        ]

    def get_doctor_details(self, doctor_id: int):
        """   Retrieve a doctor's profile and available consultation schedule       """
        doctors = self.get_all_doctors()

        for doctor in doctors:
            if doctor["doctor_id"] == doctor_id:
                return doctor

        return {"error": "Doctor not found"}

    def get_doctor_details_by_name(self, doctor_name: str):
        """
        Find doctors by name using case-insensitive matching.
        """
        pattern = re.compile(re.escape(doctor_name.strip()), re.IGNORECASE)

        doctors = self.get_all_doctors()

        return [
            doctor
            for doctor in doctors
            if pattern.search(doctor["doctor_name"])
        ]
