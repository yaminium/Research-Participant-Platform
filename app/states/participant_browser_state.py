import reflex as rx
from typing import Optional
import os
import logging
import uuid
import datetime
from supabase import create_client, Client
from app.models import User, Study
from app.states.auth_state import AuthState


class ParticipantBrowserState(rx.State):
    active_participants: list[User] = []
    filtered_participants: list[User] = []
    filter_education: str = "All"
    filter_field_of_study: str = ""
    filter_age_min: int = 18
    filter_age_max: int = 80
    is_request_modal_open: bool = False
    selected_participant: Optional[User] = None
    request_study_id: str = ""
    request_message: str = ""

    @property
    def _supabase_client(self) -> Client | None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)

    def _calculate_age(self, dob_str: str | None) -> int:
        if not dob_str:
            return 0
        try:
            dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            today = datetime.date.today()
            return (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )
        except Exception as e:
            logging.exception(f"Error calculating age: {e}")
            return 0

    @rx.event
    async def load_active_participants(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_researcher:
            return
        client = self._supabase_client
        if not client:
            return
        try:
            response = (
                client.table("participants")
                .select("*")
                .eq("participant_status", "فعال")
                .execute()
            )
            users = []
            for p in response.data:
                user = self._map_to_user(p)
                users.append(user)
            self.active_participants = users
            self.filter_participants()
        except Exception as e:
            logging.exception(f"Error loading active participants: {e}")
            if "42703" in str(e):
                logging.warning(
                    "Migration missing: participant_status column not found."
                )
                self.active_participants = []

    def _map_to_user(self, data: dict) -> User:
        return {
            "id": data.get("user_id"),
            "name": data.get("name", "Unknown"),
            "email": data.get("email", ""),
            "role": "participant",
            "education_level": data.get("education_level"),
            "field_of_study": data.get("field_of_study"),
            "occupation": data.get("occupation"),
            "date_of_birth": data.get("date_of_birth"),
            "profile_picture": data.get("profile_picture"),
            "share_education": data.get("share_education", True),
            "share_age": data.get("share_age", True),
            "share_occupation": data.get("share_occupation", True),
            "share_field_of_study": data.get("share_field_of_study", True),
            "password_hash": "",
            "bookmarks": [],
            "created_at": "",
            "phone_number": "",
            "participant_status": "فعال",
        }

    @rx.event
    def filter_participants(self):
        filtered = []
        for u in self.active_participants:
            if (
                self.filter_education != "All"
                and u.get("education_level") != self.filter_education
            ):
                continue
            if (
                self.filter_field_of_study
                and self.filter_field_of_study.lower()
                not in u.get("field_of_study", "").lower()
            ):
                continue
            age = self._calculate_age(u.get("date_of_birth"))
            if age != 0 and (age < self.filter_age_min or age > self.filter_age_max):
                continue
            filtered.append(u)
        self.filtered_participants = filtered

    @rx.event
    def set_filter_education(self, value: str):
        self.filter_education = value
        self.filter_participants()

    @rx.event
    def set_filter_field_of_study(self, value: str):
        self.filter_field_of_study = value
        self.filter_participants()

    @rx.event
    def set_filter_age_min(self, value: str):
        try:
            self.filter_age_min = int(value)
            self.filter_participants()
        except Exception as e:
            logging.exception(f"Error setting age min: {e}")

    @rx.event
    def set_filter_age_max(self, value: str):
        try:
            self.filter_age_max = int(value)
            self.filter_participants()
        except Exception as e:
            logging.exception(f"Error setting age max: {e}")

    @rx.event
    def handle_modal_open_change(self, value: bool):
        self.is_request_modal_open = value
        if not value:
            self.selected_participant = None

    @rx.event
    def open_request_modal(self, user_id: str):
        for u in self.active_participants:
            if u["id"] == user_id:
                self.selected_participant = u
                break
        self.request_message = ""
        self.request_study_id = ""
        self.is_request_modal_open = True

    @rx.event
    def close_request_modal(self):
        self.is_request_modal_open = False
        self.selected_participant = None

    @rx.event
    def set_request_study_id(self, value: str):
        self.request_study_id = value

    @rx.event
    def set_request_message(self, value: str):
        self.request_message = value

    @rx.event
    async def send_request(self):
        auth = await self.get_state(AuthState)
        if not auth.is_researcher:
            return
        if not self.request_study_id:
            yield rx.toast.error("لطفاً یک مطالعه را انتخاب کنید.")
            return
        if not self.request_message:
            yield rx.toast.error("لطفاً پیام خود را بنویسید.")
            return
        client = self._supabase_client
        if not client:
            return
        try:
            req = {
                "id": str(uuid.uuid4()),
                "researcher_id": auth.current_user["id"],
                "participant_id": self.selected_participant["id"],
                "study_id": self.request_study_id,
                "message": self.request_message,
                "status": "Pending",
                "created_at": datetime.datetime.now().isoformat(),
            }
            client.table("researcher_requests").insert(req).execute()
            self.is_request_modal_open = False
            yield rx.toast.success("درخواست با موفقیت ارسال شد!")
        except Exception as e:
            logging.exception(f"Error sending request: {e}")
            yield rx.toast.error("خطا در ارسال درخواست.")

    @rx.var
    async def researcher_studies_options(self) -> list[Study]:
        auth = await self.get_state(AuthState)
        if not auth.current_user:
            return []
        return [
            s for s in auth.studies if s["researcher_id"] == auth.current_user["id"]
        ]

    @rx.var
    def get_selected_participant_name(self) -> str:
        if self.selected_participant:
            return self.selected_participant["name"]
        return ""