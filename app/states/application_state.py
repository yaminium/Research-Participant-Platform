import reflex as rx
import logging
from typing import Optional
import datetime
import uuid
import os
from supabase import create_client, Client
from app.models import Application, Study
from app.states.auth_state import AuthState
from app.states.study_state import StudyState


class ApplicationState(rx.State):
    applications: list[Application] = []
    form_name: str = ""
    form_age: str = ""
    form_gender: str = "Prefer not to say"
    form_email: str = ""
    form_phone: str = ""
    form_motivation: str = ""
    is_modal_open: bool = False
    form_error: str = ""
    form_success: bool = False
    filter_study_id: str = "All"
    filter_status: str = "All"

    @property
    def _supabase_client(self) -> Client | None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)

    def _sync_application_to_supabase(self, application: Application):
        client = self._supabase_client
        if not client:
            return
        try:
            client.table("applications").upsert(application).execute()
            logging.info(f"Synced application {application['id']} to Supabase.")
        except Exception as e:
            logging.exception(
                f"Failed to sync application {application['id']} to Supabase: {e}"
            )

    def _delete_application_from_supabase(self, application_id: str):
        client = self._supabase_client
        if not client:
            return
        try:
            client.table("applications").delete().eq("id", application_id).execute()
            logging.info(f"Deleted application {application_id} from Supabase.")
        except Exception as e:
            logging.exception(
                f"Failed to delete application {application_id} from Supabase: {e}"
            )

    async def _load_applications_from_supabase(self):
        client = self._supabase_client
        if not client:
            return
        try:
            response = client.table("applications").select("*").execute()
            data = response.data
            if data:
                self.applications = data
                logging.info(f"Loaded {len(data)} applications from Supabase.")
        except Exception as e:
            logging.exception(f"Failed to load applications from Supabase: {e}")

    @rx.event
    async def load_applications(self):
        await self._load_applications_from_supabase()

    @rx.var(cache=True)
    async def researcher_applications(self) -> list[Application]:
        auth_state = await self.get_state(AuthState)
        if (
            not auth_state.current_user
            or auth_state.current_user["role"] != "researcher"
        ):
            return []
        study_state = await self.get_state(StudyState)
        researcher_id = auth_state.current_user["id"]
        my_study_ids = [
            s["id"] for s in study_state.studies if s["researcher_id"] == researcher_id
        ]
        apps = [a for a in self.applications if a["study_id"] in my_study_ids]
        if self.filter_study_id != "All":
            apps = [a for a in apps if a["study_id"] == self.filter_study_id]
        if self.filter_status != "All":
            apps = [a for a in apps if a["status"] == self.filter_status]
        return sorted(apps, key=lambda x: x["created_at"], reverse=True)

    @rx.var(cache=True)
    async def stats_total_applications(self) -> int:
        auth_state = await self.get_state(AuthState)
        if (
            not auth_state.current_user
            or auth_state.current_user["role"] != "researcher"
        ):
            return 0
        study_state = await self.get_state(StudyState)
        researcher_id = auth_state.current_user["id"]
        my_study_ids = [
            s["id"] for s in study_state.studies if s["researcher_id"] == researcher_id
        ]
        apps = [a for a in self.applications if a["study_id"] in my_study_ids]
        return len(apps)

    @rx.var(cache=True)
    async def stats_pending_applications(self) -> int:
        auth_state = await self.get_state(AuthState)
        if (
            not auth_state.current_user
            or auth_state.current_user["role"] != "researcher"
        ):
            return 0
        study_state = await self.get_state(StudyState)
        researcher_id = auth_state.current_user["id"]
        my_study_ids = [
            s["id"] for s in study_state.studies if s["researcher_id"] == researcher_id
        ]
        apps = [
            a
            for a in self.applications
            if a["study_id"] in my_study_ids and a["status"] == "Pending"
        ]
        return len(apps)

    @rx.var(cache=True)
    async def stats_response_rate(self) -> str:
        auth_state = await self.get_state(AuthState)
        if (
            not auth_state.current_user
            or auth_state.current_user["role"] != "researcher"
        ):
            return "0%"
        total = await self.stats_total_applications
        if total == 0:
            return "0%"
        pending = await self.stats_pending_applications
        processed = total - pending
        rate = int(processed / total * 100)
        return f"{rate}%"

    @rx.var(cache=True)
    async def researcher_studies_for_filter(self) -> list[Study]:
        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        study_state = await self.get_state(StudyState)
        return [
            s
            for s in study_state.studies
            if s["researcher_id"] == auth_state.current_user["id"]
        ]

    @rx.event
    async def open_application_modal(self):
        from app.states.browse_state import BrowseState

        auth_state = await self.get_state(AuthState)
        browse_state = await self.get_state(BrowseState)
        if not auth_state.is_authenticated:
            return rx.redirect("/login")
        if auth_state.is_researcher:
            return rx.window_alert("پژوهشگران نمی\u2009توانند در مطالعات شرکت کنند.")
        current_study = await browse_state.current_study
        if not current_study:
            return rx.window_alert("اطلاعات مطالعه یافت نشد.")
        current_user_id = auth_state.current_user["id"]
        study_id = current_study["id"]
        existing_app = next(
            (
                a
                for a in self.applications
                if a["participant_id"] == current_user_id and a["study_id"] == study_id
            ),
            None,
        )
        if existing_app:
            return rx.window_alert("شما قبلاً برای این مطالعه درخواست داده\u2009اید.")
        self.form_name = auth_state.current_user["name"]
        self.form_email = auth_state.current_user["email"]
        self.form_age = ""
        self.form_gender = "Prefer not to say"
        self.form_phone = ""
        self.form_motivation = ""
        self.form_error = ""
        self.form_success = False
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        self.is_modal_open = False
        self.form_success = False

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_age(self, value: str):
        self.form_age = value

    @rx.event
    def set_form_gender(self, value: str):
        self.form_gender = value

    @rx.event
    def set_form_email(self, value: str):
        self.form_email = value

    @rx.event
    def set_form_phone(self, value: str):
        self.form_phone = value

    @rx.event
    def set_form_motivation(self, value: str):
        self.form_motivation = value

    @rx.event
    def set_filter_study_id(self, value: str):
        self.filter_study_id = value

    @rx.event
    def set_filter_status(self, value: str):
        self.filter_status = value

    @rx.event
    async def submit_application(self):
        if (
            not self.form_name
            or not self.form_age
            or (not self.form_email)
            or (not self.form_motivation)
        ):
            self.form_error = (
                "لطفاً تمام فیلدهای الزامی را پر کنید (نام، سن، ایمیل، انگیزه)."
            )
            return
        try:
            age_int = int(self.form_age)
            if age_int < 18 or age_int > 120:
                self.form_error = "لطفاً یک سن معتبر وارد کنید."
                return
        except ValueError as e:
            logging.exception(f"Error parsing age: {e}")
            self.form_error = "سن باید عدد باشد."
            return
        from app.states.browse_state import BrowseState

        auth_state = await self.get_state(AuthState)
        browse_state = await self.get_state(BrowseState)
        current_study = await browse_state.current_study
        if not current_study:
            self.form_error = "اطلاعات مطالعه یافت نشد. لطفاً صفحه را رفرش کنید."
            return
        new_app: Application = {
            "id": str(uuid.uuid4()),
            "study_id": current_study["id"],
            "participant_id": auth_state.current_user["id"],
            "participant_name": self.form_name,
            "age": int(self.form_age),
            "gender": self.form_gender,
            "email": self.form_email,
            "phone": self.form_phone,
            "motivation_message": self.form_motivation,
            "status": "Pending",
            "created_at": datetime.datetime.now().isoformat(),
        }
        self.applications.append(new_app)
        self._sync_application_to_supabase(new_app)
        self.form_success = True
        self.form_error = ""
        return rx.toast("درخواست با موفقیت ارسال شد!")

    @rx.event
    async def update_application_status(self, app_id: str, new_status: str):
        updated_list = []
        updated_app = None
        for app in self.applications:
            if app["id"] == app_id:
                app["status"] = new_status
                updated_app = app
                updated_list.append(app)
            else:
                updated_list.append(app)
        self.applications = updated_list
        if updated_app:
            self._sync_application_to_supabase(updated_app)