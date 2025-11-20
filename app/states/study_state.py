import reflex as rx
from typing import Optional
import datetime
import uuid
import os
import logging
from supabase import create_client, Client
from app.models import Study
from app.states.auth_state import AuthState


class StudyState(rx.State):
    title: str = ""
    description: str = ""
    study_image: str = ""
    experiment_type: str = "Computer Based"
    sample_size: int = 0
    compensation: str = ""
    psychological_health_type: str = "No Preference"
    age_range_min: int = 18
    age_range_max: int = 99
    gender_requirement: str = "Any"
    custom_criteria: str = ""
    procedure_description: str = ""
    location_type: str = "Online"
    physical_location: str = ""
    duration: str = ""
    contact_info: str = ""
    is_open: bool = True
    editing_study_id: str = ""
    form_error: str = ""

    @property
    def _supabase_client(self) -> Client | None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)

    def _sync_study_to_supabase(self, study: Study):
        client = self._supabase_client
        if not client:
            return
        try:
            client.table("experiments").upsert(study).execute()
            logging.info(f"Synced study {study['id']} to Supabase.")
        except Exception as e:
            logging.exception(f"Failed to sync study {study['id']} to Supabase: {e}")

    def _delete_study_from_supabase(self, study_id: str):
        client = self._supabase_client
        if not client:
            return
        try:
            client.table("experiments").delete().eq("id", study_id).execute()
            logging.info(f"Deleted study {study_id} from Supabase.")
        except Exception as e:
            logging.exception(f"Failed to delete study {study_id} from Supabase: {e}")

    async def _load_studies_from_supabase(self):
        client = self._supabase_client
        if not client:
            return
        try:
            response = client.table("experiments").select("*").execute()
            data = response.data
            if data:
                auth_state = await self.get_state(AuthState)
                auth_state.studies = data
                logging.info(f"Loaded {len(data)} studies from Supabase.")
        except Exception as e:
            logging.exception(f"Failed to load studies from Supabase: {e}")

    @rx.event
    async def load_studies(self):
        await self._load_studies_from_supabase()

    @rx.var
    async def my_studies(self) -> list[Study]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        user_id = auth_state.current_user["id"]
        return [s for s in auth_state.studies if s["researcher_id"] == user_id]

    @rx.var
    async def stats_total_studies(self) -> int:
        studies = await self.my_studies
        return len(studies)

    @rx.var
    async def stats_active_studies(self) -> int:
        studies = await self.my_studies
        return len([s for s in studies if s["status"] == "Open"])

    @rx.var
    async def stats_closed_studies(self) -> int:
        studies = await self.my_studies
        return len([s for s in studies if s["status"] == "Closed"])

    @rx.var
    async def featured_studies(self) -> list[Study]:
        auth_state = await self.get_state(AuthState)
        open_studies = [s for s in auth_state.studies if s["status"] == "Open"]
        return sorted(open_studies, key=lambda x: x["created_at"], reverse=True)[:3]

    @rx.event
    def reset_form(self):
        self.title = ""
        self.description = ""
        self.study_image = ""
        self.experiment_type = "Computer Based"
        self.sample_size = 0
        self.compensation = ""
        self.psychological_health_type = "No Preference"
        self.age_range_min = 18
        self.age_range_max = 99
        self.gender_requirement = "Any"
        self.custom_criteria = ""
        self.procedure_description = ""
        self.location_type = "Online"
        self.physical_location = ""
        self.duration = ""
        self.contact_info = ""
        self.is_open = True
        self.editing_study_id = ""
        self.form_error = ""

    @rx.event
    def set_experiment_type(self, value: str):
        self.experiment_type = value

    @rx.event
    async def handle_image_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.study_image = file.name

    @rx.event
    def set_is_open_toggle(self, value: bool):
        self.is_open = value

    @rx.event
    async def save_study(self):
        if not self.title or not self.description:
            self.form_error = "عنوان و توضیحات الزامی هستند."
            return
        if self.sample_size < 1:
            self.form_error = "حجم نمونه باید حداقل ۱ باشد."
            return
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            yield rx.redirect("/login")
            return
        user_id = auth_state.current_user["id"]
        study_data: Study = {
            "id": self.editing_study_id if self.editing_study_id else str(uuid.uuid4()),
            "researcher_id": user_id,
            "title": self.title,
            "description": self.description,
            "study_image": self.study_image,
            "experiment_type": self.experiment_type,
            "sample_size": self.sample_size,
            "compensation": self.compensation,
            "participant_criteria": f"Health: {self.psychological_health_type}, Age: {self.age_range_min}-{self.age_range_max}, Gender: {self.gender_requirement}",
            "psychological_health_type": self.psychological_health_type,
            "age_range_min": self.age_range_min,
            "age_range_max": self.age_range_max,
            "gender_requirement": self.gender_requirement,
            "custom_criteria": self.custom_criteria,
            "procedure_description": self.procedure_description,
            "location_type": self.location_type,
            "physical_location": self.physical_location
            if self.location_type == "In-Person"
            else "Online",
            "duration": self.duration,
            "contact_info": self.contact_info,
            "status": "Open" if self.is_open else "Closed",
            "created_at": datetime.datetime.now().isoformat(),
        }
        if self.editing_study_id:
            updated_list = []
            for s in auth_state.studies:
                if s["id"] == self.editing_study_id:
                    updated_list.append(study_data)
                else:
                    updated_list.append(s)
            auth_state.studies = updated_list
        else:
            auth_state.studies.append(study_data)
        self._sync_study_to_supabase(study_data)
        self.reset_form()
        yield rx.toast("مطالعه با موفقیت ذخیره شد!")
        yield rx.redirect("/my-studies")

    @rx.event
    def start_create_new(self):
        self.reset_form()
        return rx.redirect("/create-study")

    @rx.event
    async def handle_edit_study(self, study_id: str):
        auth_state = await self.get_state(AuthState)
        study_to_edit = next(
            (s for s in auth_state.studies if s["id"] == study_id), None
        )
        if study_to_edit:
            self.editing_study_id = study_to_edit["id"]
            self.title = study_to_edit["title"]
            self.description = study_to_edit["description"]
            self.study_image = study_to_edit.get("study_image", "")
            self.experiment_type = study_to_edit.get(
                "experiment_type", "Computer Based"
            )
            self.sample_size = study_to_edit["sample_size"]
            self.compensation = study_to_edit["compensation"]
            self.psychological_health_type = study_to_edit["psychological_health_type"]
            self.age_range_min = study_to_edit["age_range_min"]
            self.age_range_max = study_to_edit["age_range_max"]
            self.gender_requirement = study_to_edit["gender_requirement"]
            self.custom_criteria = study_to_edit["custom_criteria"]
            self.procedure_description = study_to_edit["procedure_description"]
            self.location_type = study_to_edit["location_type"]
            self.physical_location = study_to_edit["physical_location"]
            self.duration = study_to_edit["duration"]
            self.contact_info = study_to_edit["contact_info"]
            self.is_open = study_to_edit["status"] == "Open"
            return rx.redirect("/create-study")

    @rx.event
    async def delete_study(self, study_id: str):
        auth_state = await self.get_state(AuthState)
        auth_state.studies = [s for s in auth_state.studies if s["id"] != study_id]
        self._delete_study_from_supabase(study_id)
        return rx.toast("مطالعه حذف شد.")