import reflex as rx
from typing import Optional, TYPE_CHECKING
import datetime
import uuid
import os
import logging
from supabase import create_client, Client
from app.models import Study

if TYPE_CHECKING:
    from app.states.auth_state import AuthState


class StudyState(rx.State):
    studies: list[Study] = [
        {
            "id": "study_001",
            "researcher_id": "user_1",
            "title": "بررسی حافظه کاری در بزرگسالان جوان",
            "description": "این مطالعه به بررسی نحوه پردازش اطلاعات در حافظه کاری افراد می\u200cپردازد. شرکت\u200cکنندگان باید تکالیف کامپیوتری ساده\u200cای را انجام دهند که توانایی نگهداری و دستکاری اطلاعات را می\u200cسنجد.",
            "study_image": "",
            "experiment_type": "Computer Based",
            "sample_size": 30,
            "compensation": "۵۰۰ هزار تومان",
            "participant_criteria": "Health: Psychologically Healthy, Age: 18-35, Gender: Any",
            "psychological_health_type": "Psychologically Healthy",
            "age_range_min": 18,
            "age_range_max": 35,
            "gender_requirement": "Any",
            "custom_criteria": "راست\u200cدست بودن، داشتن بینایی نرمال یا اصلاح شده",
            "procedure_description": "شرکت\u200cکنندگان باید در مقابل کامپیوتر بنشینند و تکالیف حافظه کاری را انجام دهند. این شامل به خاطر سپردن دنباله\u200cهای عددی و پاسخ به سوالات مربوطه است. جلسه شامل آموزش اولیه و سپس انجام تکالیف اصلی است.",
            "location_type": "In-Person",
            "physical_location": "دانشگاه تهران، دانشکده روانشناسی، اتاق آزمایشگاه شناختی ۲۰۱",
            "duration": "۴۵ دقیقه",
            "contact_info": "dr.ahmadi@ut.ac.ir - ۰۲۱۶۱۱۱۱۲۳۴",
            "status": "Open",
            "created_at": "2024-01-15 10:00:00+00",
        },
        {
            "id": "study_002",
            "researcher_id": "user_1",
            "title": "تاثیر مدیتیشن بر کاهش استرس دانشجویان",
            "description": "در این پژوهش، اثربخشی برنامه مدیتیشن ۸ هفته\u200cای بر میزان استرس و اضطراب دانشجویان بررسی می\u200cشود. این مطالعه آنلاین است و شرکت\u200cکنندگان باید پرسشنامه\u200cهایی را قبل و بعد از مداخله تکمیل کنند.",
            "study_image": "",
            "experiment_type": "Computer Based",
            "sample_size": 50,
            "compensation": "۳۰۰ هزار تومان",
            "participant_criteria": "Health: No Preference, Age: 18-30, Gender: Any",
            "psychological_health_type": "No Preference",
            "age_range_min": 18,
            "age_range_max": 30,
            "gender_requirement": "Any",
            "custom_criteria": "دانشجو بودن، نداشتن سابقه بیماری\u200cهای روانی شدید",
            "procedure_description": "شرکت\u200cکنندگان ابتدا پرسشنامه\u200cهای استرس و اضطراب را به صورت آنلاین تکمیل می\u200cکنند. سپس برای ۸ هفته در جلسات مدیتیشن آنلاین (۲ بار در هفته، هر جلسه ۳۰ دقیقه) شرکت خواهند کرد. در پایان، دوباره پرسشنامه\u200cها را پر می\u200cکنند.",
            "location_type": "Online",
            "physical_location": "Online",
            "duration": "۸ هفته (جلسات ۳۰ دقیقه\u200cای)",
            "contact_info": "meditation.study@gmail.com",
            "status": "Open",
            "created_at": "2024-01-20 09:00:00+00",
        },
        {
            "id": "study_003",
            "researcher_id": "user_1",
            "title": "مطالعه fMRI: پردازش چهره در مغز",
            "description": "این مطالعه تصویربرداری عصبی است که فعالیت مغز را هنگام مشاهده چهره\u200cهای مختلف بررسی می\u200cکند. از دستگاه fMRI برای ثبت تصاویر مغز استفاده می\u200cشود.",
            "study_image": "",
            "experiment_type": "FMRI",
            "sample_size": 20,
            "compensation": "۱ میلیون تومان",
            "participant_criteria": "Health: Psychologically Healthy, Age: 20-40, Gender: Any",
            "psychological_health_type": "Psychologically Healthy",
            "age_range_min": 20,
            "age_range_max": 40,
            "gender_requirement": "Any",
            "custom_criteria": "نداشتن فلزات در بدن، نداشتن کلاستروفوبیا، نداشتن مشکلات بینایی شدید",
            "procedure_description": "شرکت\u200cکنندگان ابتدا غربالگری ایمنی fMRI را طی می\u200cکنند. سپس در دستگاه fMRI قرار می\u200cگیرند و تصاویر چهره\u200cهای مختلف را می\u200cبینند. باید با فشار دادن دکمه، نوع احساس را گزارش کنند. کل جلسه شامل ۱۵ دقیقه آموزش و ۴۵ دقیقه اسکن است.",
            "location_type": "In-Person",
            "physical_location": "بیمارستان امام خمینی، بخش تصویربرداری طبقه سوم",
            "duration": "۱ ساعت",
            "contact_info": "fmri.lab@yahoo.com - ۰۹۱۲۱۲۳۴۵۶۷",
            "status": "Open",
            "created_at": "2024-01-25 11:00:00+00",
        },
        {
            "id": "study_004",
            "researcher_id": "user_1",
            "title": "بررسی الگوهای خواب و عملکرد شناختی",
            "description": "این مطالعه رابطه بین کیفیت خواب و عملکرد حافظه و توجه را بررسی می\u200cکند. شرکت\u200cکنندگان باید یک هفته دفتر خواب نگه دارند و تکالیف شناختی آنلاین را انجام دهند.",
            "study_image": "",
            "experiment_type": "Computer Based",
            "sample_size": 40,
            "compensation": "۴۰۰ هزار تومان",
            "participant_criteria": "Health: Psychologically Healthy, Age: 18-50, Gender: Any",
            "psychological_health_type": "Psychologically Healthy",
            "age_range_min": 18,
            "age_range_max": 50,
            "gender_requirement": "Any",
            "custom_criteria": "",
            "procedure_description": "شرکت\u200cکنندگان برای یک هفته، هر شب قبل از خواب و هر صبح بعد از بیدار شدن، یک پرسشنامه کوتاه درباره کیفیت خواب را تکمیل می\u200cکنند. همچنین روزانه ۱۰ دقیقه تکالیف حافظه و توجه را به صورت آنلاین انجام می\u200cدهند.",
            "location_type": "Online",
            "physical_location": "Online",
            "duration": "۱ هفته (۱۰ دقیقه در روز)",
            "contact_info": "sleep.research@ut.ac.ir",
            "status": "Open",
            "created_at": "2024-02-01 08:00:00+00",
        },
        {
            "id": "study_005",
            "researcher_id": "user_1",
            "title": "تحریک الکتریکی مغز و یادگیری حرکتی",
            "description": "این مطالعه تاثیر تحریک الکتریکی مغز (tDCS) بر بهبود یادگیری مهارت\u200cهای حرکتی را بررسی می\u200cکند. شرکت\u200cکنندگان باید تکالیف حرکتی را انجام دهند در حالی که تحریک الکتریکی دریافت می\u200cکنند.",
            "study_image": "",
            "experiment_type": "tDCS",
            "sample_size": 25,
            "compensation": "۸۰۰ هزار تومان",
            "participant_criteria": "Health: Psychologically Healthy, Age: 18-35, Gender: Any",
            "psychological_health_type": "Psychologically Healthy",
            "age_range_min": 18,
            "age_range_max": 35,
            "gender_requirement": "Any",
            "custom_criteria": "راست\u200cدست، نداشتن سابقه صرع، نداشتن صفحات فلزی در سر",
            "procedure_description": "شرکت\u200cکنندگان در ۵ جلسه شرکت می\u200cکنند. در هر جلسه، الکترودها بر روی سر قرار می\u200cگیرند و جریان الکتریکی ضعیف (2mA) برای ۲۰ دقیقه اعمال می\u200cشود. همزمان، آنها یک تکلیف حرکتی با انگشتان (piano task) را انجام می\u200cدهند.",
            "location_type": "In-Person",
            "physical_location": "دانشگاه شهید بهشتی، پژوهشکده علوم شناختی، طبقه ۴",
            "duration": "۵ جلسه (هر جلسه ۴۰ دقیقه)",
            "contact_info": "tdcs.study@sbu.ac.ir - ۰۹۱۲۳۴۵۶۷۸۹",
            "status": "Open",
            "created_at": "2024-02-05 13:00:00+00",
        },
        {
            "id": "study_006",
            "researcher_id": "user_1",
            "title": "مطالعه دوقلوها: وراثت و شخصیت",
            "description": "این پژوهش به بررسی نقش ژنتیک در ویژگی\u200cهای شخصیتی می\u200cپردازد. ما به دنبال دوقلوهای همسان و ناهمسان برای شرکت در این مطالعه هستیم.",
            "study_image": "",
            "experiment_type": "Paper Based",
            "sample_size": 30,
            "compensation": "۶۰۰ هزار تومان (هر دوقلو)",
            "participant_criteria": "Health: No Preference, Age: 18-60, Gender: Any",
            "psychological_health_type": "No Preference",
            "age_range_min": 18,
            "age_range_max": 60,
            "gender_requirement": "Any",
            "custom_criteria": "دوقلو بودن (همسان یا ناهمسان)، رشد در یک محیط خانوادگی",
            "procedure_description": "هر دو دوقلو باید پرسشنامه\u200cهای شخصیتی جامعی را تکمیل کنند. این شامل تست\u200cهای NEO-PI-R و MBTI است. همچنین یک مصاحبه نیم\u200cساختاریافته ۳۰ دقیقه\u200cای درباره تجربیات زندگی انجام می\u200cشود. جلسه حضوری است.",
            "location_type": "In-Person",
            "physical_location": "دانشگاه علامه طباطبایی، دانشکده روانشناسی، اتاق ۳۰۵",
            "duration": "۲ ساعت",
            "contact_info": "twins.personality@atu.ac.ir",
            "status": "Open",
            "created_at": "2024-02-10 10:00:00+00",
        },
    ]
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
                self.studies = data
                logging.info(f"Loaded {len(data)} studies from Supabase.")
        except Exception as e:
            logging.exception(f"Failed to load studies from Supabase: {e}")

    @rx.event
    async def load_studies(self):
        await self._load_studies_from_supabase()

    @rx.var(cache=True, auto_deps=False)
    async def my_studies(self) -> list[Study]:
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.current_user:
            return []
        user_id = auth_state.current_user["id"]
        return [s for s in self.studies if s["researcher_id"] == user_id]

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
        open_studies = [s for s in self.studies if s["status"] == "Open"]
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
        from app.states.auth_state import AuthState

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
            for s in self.studies:
                if s["id"] == self.editing_study_id:
                    updated_list.append(study_data)
                else:
                    updated_list.append(s)
            self.studies = updated_list
        else:
            self.studies.append(study_data)
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
        study_to_edit = next((s for s in self.studies if s["id"] == study_id), None)
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
        self.studies = [s for s in self.studies if s["id"] != study_id]
        self._delete_study_from_supabase(study_id)
        return rx.toast("مطالعه حذف شد.")