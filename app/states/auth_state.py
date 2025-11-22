import reflex as rx
from typing import Optional
import hashlib
import datetime
import uuid
import os
from supabase import create_client, Client
from app.models import User, Study, Application, ResearcherRequest
import logging


class AuthState(rx.State):
    users: list[User] = [
        {
            "id": "user_1",
            "email": "researcher@example.com",
            "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "name": "Dr. Sarah Connor",
            "role": "researcher",
            "bookmarks": [],
            "created_at": "2023-01-01",
            "education_level": "Ph.D.",
            "field_of_study": "Neuroscience",
            "occupation": "Senior Researcher",
            "date_of_birth": "1985-05-12",
            "phone_number": "09120000001",
            "profile_picture": "",
        },
        {
            "id": "user_2",
            "email": "participant@example.com",
            "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "name": "John Doe",
            "role": "participant",
            "bookmarks": [],
            "created_at": "2023-01-02",
            "education_level": "Bachelor",
            "field_of_study": "Computer Science",
            "occupation": "Student",
            "date_of_birth": "1998-08-20",
            "phone_number": "09120000002",
            "profile_picture": "",
            "participant_status": "فعال",
            "share_education": True,
            "share_age": True,
            "share_occupation": True,
            "share_field_of_study": True,
        },
    ]
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
    applications: list[Application] = []
    researcher_requests: list[ResearcherRequest] = []
    current_user: User | None = None
    is_authenticated: bool = False
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    reg_name: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    reg_role: str = "participant"
    reg_error: str = ""
    is_edit_profile_open: bool = False
    editing_name: str = ""
    editing_education_level: str = ""
    editing_field_of_study: str = ""
    editing_occupation: str = ""
    editing_date_of_birth: str = ""
    editing_phone_number: str = ""
    editing_profile_picture: str = ""
    editing_participant_status: str = "غیر فعال"
    editing_share_education: bool = True
    editing_share_age: bool = True
    editing_share_occupation: bool = True
    editing_share_field_of_study: bool = True

    @property
    def _supabase_client(self) -> Client | None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            return None
        return create_client(url, key)

    def _sync_user_to_supabase(self, user: User):
        """Sync user data to Supabase researchers or participants table."""
        client = self._supabase_client
        if not client:
            return
        table_name = "researchers" if user["role"] == "researcher" else "participants"
        data = {
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "password_hash": user["password_hash"],
            "bookmarks": user.get("bookmarks", []),
            "created_at": user["created_at"],
            "date_of_birth": user.get("date_of_birth"),
            "phone_number": user.get("phone_number", ""),
            "profile_picture": user.get("profile_picture", ""),
        }
        if user["role"] == "researcher":
            data.update(
                {
                    "education_level": user.get("education_level", ""),
                    "field_of_study": user.get("field_of_study", ""),
                    "occupation": user.get("occupation", ""),
                }
            )
        elif user["role"] == "participant":
            data.update(
                {
                    "participant_status": user.get("participant_status", "غیر فعال"),
                    "share_education": user.get("share_education", True),
                    "share_age": user.get("share_age", True),
                    "share_occupation": user.get("share_occupation", True),
                    "share_field_of_study": user.get("share_field_of_study", True),
                }
            )
        try:
            res = (
                client.table(table_name)
                .select("id")
                .eq("email", user["email"])
                .execute()
            )
            if res.data:
                client.table(table_name).update(data).eq(
                    "email", user["email"]
                ).execute()
                logging.info(f"Updated user {user['email']} in Supabase {table_name}.")
            else:
                client.table(table_name).insert(data).execute()
                logging.info(
                    f"Inserted user {user['email']} into Supabase {table_name}."
                )
        except Exception as e:
            logging.exception(f"Supabase Sync Error: {e}")

    async def _load_researcher_requests(self):
        """Load researcher requests from Supabase."""
        client = self._supabase_client
        if not client:
            return
        try:
            response = client.table("researcher_requests").select("*").execute()
            if response.data:
                self.researcher_requests = response.data
                logging.info(
                    f"Loaded {len(response.data)} researcher requests from Supabase."
                )
        except Exception as e:
            logging.exception(f"Failed to load researcher requests: {e}")

    def _check_supabase_login(self, email: str, password_hash: str) -> User | None:
        """Check if user exists in Supabase tables and matches credentials."""
        client = self._supabase_client
        if not client:
            return None
        try:
            res = client.table("researchers").select("*").eq("email", email).execute()
            if res.data:
                r_data = res.data[0]
                if r_data.get("password_hash") == password_hash:
                    return self._map_supabase_to_user(r_data, "researcher")
        except Exception as e:
            logging.exception(f"Supabase Login Error (Researchers): {e}")
        try:
            res = client.table("participants").select("*").eq("email", email).execute()
            if res.data:
                p_data = res.data[0]
                if p_data.get("password_hash") == password_hash:
                    return self._map_supabase_to_user(p_data, "participant")
        except Exception as e:
            logging.exception(f"Supabase Login Error (Participants): {e}")
        return None

    def _map_supabase_to_user(self, data: dict, role: str) -> User:
        """Map Supabase record to User model."""
        user_data = {
            "id": data.get("user_id") or str(uuid.uuid4()),
            "email": data.get("email", ""),
            "password_hash": data.get("password_hash", ""),
            "name": data.get("name", "Unknown"),
            "role": role,
            "bookmarks": data.get("bookmarks") or [],
            "created_at": data.get("created_at", datetime.datetime.now().isoformat()),
            "education_level": data.get("education_level", ""),
            "field_of_study": data.get("field_of_study", ""),
            "occupation": data.get("occupation", ""),
            "date_of_birth": data.get("date_of_birth", ""),
            "phone_number": data.get("phone_number", ""),
            "profile_picture": data.get("profile_picture", ""),
        }
        if role == "participant":
            user_data.update(
                {
                    "participant_status": data.get("participant_status", "غیر فعال"),
                    "share_education": data.get("share_education", True),
                    "share_age": data.get("share_age", True),
                    "share_occupation": data.get("share_occupation", True),
                    "share_field_of_study": data.get("share_field_of_study", True),
                }
            )
        return user_data

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @rx.event
    def on_google_login(self, data: dict):
        """Handle Google Login success."""
        try:
            email = data.get("email")
            if not email:
                self.login_error = "Google Login failed: No email provided in response."
                return
            name = data.get("name", "")
            found_user = None
            for user in self.users:
                if user["email"] == email:
                    found_user = user
                    break
            if found_user:
                self.current_user = found_user
                self.is_authenticated = True
                self.login_error = ""
                self._sync_user_to_supabase(found_user)
                return rx.redirect("/profile")
            else:
                new_user: User = {
                    "id": str(uuid.uuid4()),
                    "email": email,
                    "password_hash": "google_oauth_user",
                    "name": name,
                    "role": "participant",
                    "bookmarks": [],
                    "created_at": datetime.datetime.now().isoformat(),
                    "education_level": "",
                    "field_of_study": "",
                    "occupation": "",
                    "date_of_birth": None,
                    "phone_number": "",
                    "profile_picture": "",
                }
                self.users.append(new_user)
                self.current_user = new_user
                self.is_authenticated = True
                self.login_error = ""
                self._sync_user_to_supabase(new_user)
                return (
                    rx.toast("حساب کاربری با گوگل ایجاد شد!"),
                    rx.redirect("/profile"),
                )
        except Exception as e:
            logging.exception(f"Google Login Error: {e}")
            self.login_error = "An error occurred during Google Login."

    @rx.event
    def handle_login_email_change(self, value: str):
        self.login_email = value

    @rx.event
    def handle_login_password_change(self, value: str):
        self.login_password = value

    @rx.event
    def login(self):
        hashed_pw = self._hash_password(self.login_password)
        found_user = None
        for user in self.users:
            if user["email"] == self.login_email and user["password_hash"] == hashed_pw:
                found_user = user
                break
        if not found_user:
            found_user = self._check_supabase_login(self.login_email, hashed_pw)
            if found_user:
                self.users.append(found_user)
        if found_user:
            self.current_user = found_user
            self.is_authenticated = True
            self.login_error = ""
            self.login_email = ""
            self.login_password = ""
            return rx.redirect("/profile")
        else:
            self.login_error = "ایمیل یا رمز عبور اشتباه است."

    @rx.event
    def logout(self):
        self.current_user = None
        self.is_authenticated = False
        return rx.redirect("/login")

    @rx.event
    def set_reg_name(self, value: str):
        self.reg_name = value

    @rx.event
    def set_reg_email(self, value: str):
        self.reg_email = value

    @rx.event
    def set_reg_password(self, value: str):
        self.reg_password = value

    @rx.event
    def set_reg_confirm_password(self, value: str):
        self.reg_confirm_password = value

    @rx.event
    def set_reg_role(self, value: str):
        self.reg_role = value

    @rx.event
    def register(self):
        if not self.reg_name or not self.reg_email or (not self.reg_password):
            self.reg_error = "تمام فیلدها الزامی هستند."
            return
        if self.reg_password != self.reg_confirm_password:
            self.reg_error = "رمز عبور و تکرار آن مطابقت ندارند."
            return
        if len(self.reg_password) < 6:
            self.reg_error = "رمز عبور باید حداقل ۶ کاراکتر باشد."
            return
        for user in self.users:
            if user["email"] == self.reg_email:
                self.reg_error = "این ایمیل قبلاً ثبت شده است."
                return
        new_user: User = {
            "id": str(uuid.uuid4()),
            "email": self.reg_email,
            "password_hash": self._hash_password(self.reg_password),
            "name": self.reg_name,
            "role": self.reg_role,
            "bookmarks": [],
            "created_at": datetime.datetime.now().isoformat(),
            "education_level": "",
            "field_of_study": "",
            "occupation": "",
            "date_of_birth": None,
            "phone_number": "",
            "profile_picture": "",
        }
        self.users.append(new_user)
        self._sync_user_to_supabase(new_user)
        self.reg_error = ""
        self.reg_name = ""
        self.reg_email = ""
        self.reg_password = ""
        self.reg_confirm_password = ""
        yield rx.toast("حساب کاربری با موفقیت ایجاد شد! لطفاً وارد شوید.")
        yield rx.redirect("/login")

    @rx.event
    def toggle_bookmark(self, study_id: str):
        if not self.current_user:
            return
        user_index = -1
        for i, u in enumerate(self.users):
            if u["id"] == self.current_user["id"]:
                user_index = i
                break
        if user_index != -1:
            bookmarks = self.users[user_index].get("bookmarks", [])
            message = ""
            if study_id in bookmarks:
                bookmarks.remove(study_id)
                message = "از علاقه\u200cمندی\u200cها حذف شد"
            else:
                bookmarks.append(study_id)
                message = "به علاقه\u200cمندی\u200cها اضافه شد"
            self.users[user_index]["bookmarks"] = bookmarks
            self.current_user = self.users[user_index]
            yield rx.toast(message)

    @rx.var
    def bookmarked_study_ids(self) -> list[str]:
        if not self.current_user:
            return []
        return self.current_user.get("bookmarks", [])

    @rx.var
    def bookmarked_studies(self) -> list[Study]:
        if not self.current_user:
            return []
        bookmark_ids = self.bookmarked_study_ids
        return [s for s in self.studies if s["id"] in bookmark_ids]

    @rx.var
    def current_user_name(self) -> str:
        if self.current_user:
            return self.current_user["name"]
        return ""

    @rx.var
    def current_user_role(self) -> str:
        if self.current_user:
            return self.current_user["role"]
        return ""

    @rx.var
    def current_user_email(self) -> str:
        if self.current_user:
            return self.current_user["email"]
        return ""

    @rx.var
    def is_researcher(self) -> bool:
        return self.current_user_role == "researcher"

    @rx.var
    def is_participant(self) -> bool:
        return self.current_user_role == "participant"

    @rx.event
    def open_edit_profile(self):
        if self.current_user:
            self.editing_name = self.current_user["name"]
            self.editing_education_level = self.current_user.get("education_level", "")
            self.editing_field_of_study = self.current_user.get("field_of_study", "")
            self.editing_occupation = self.current_user.get("occupation", "")
            self.editing_date_of_birth = self.current_user.get("date_of_birth", "")
            self.editing_phone_number = self.current_user.get("phone_number", "")
            self.editing_profile_picture = self.current_user.get("profile_picture", "")
            if self.current_user["role"] == "participant":
                self.editing_participant_status = self.current_user.get(
                    "participant_status", "غیر فعال"
                )
                self.editing_share_education = self.current_user.get(
                    "share_education", True
                )
                self.editing_share_age = self.current_user.get("share_age", True)
                self.editing_share_occupation = self.current_user.get(
                    "share_occupation", True
                )
                self.editing_share_field_of_study = self.current_user.get(
                    "share_field_of_study", True
                )
            self.is_edit_profile_open = True

    @rx.event
    def close_edit_profile(self):
        self.is_edit_profile_open = False

    @rx.event
    def set_editing_name(self, value: str):
        self.editing_name = value

    @rx.event
    def set_editing_education_level(self, value: str):
        self.editing_education_level = value

    @rx.event
    def set_editing_field_of_study(self, value: str):
        self.editing_field_of_study = value

    @rx.event
    def set_editing_occupation(self, value: str):
        self.editing_occupation = value

    @rx.event
    def set_editing_date_of_birth(self, value: str):
        self.editing_date_of_birth = value

    @rx.event
    def set_editing_phone_number(self, value: str):
        self.editing_phone_number = value

    @rx.event
    async def handle_profile_picture_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.editing_profile_picture = file.name

    @rx.event
    def set_editing_participant_status(self, value: str):
        self.editing_participant_status = value

    @rx.event
    def toggle_editing_share_education(self, value: bool):
        self.editing_share_education = value

    @rx.event
    def toggle_editing_share_age(self, value: bool):
        self.editing_share_age = value

    @rx.event
    def toggle_editing_share_occupation(self, value: bool):
        self.editing_share_occupation = value

    @rx.event
    def toggle_editing_share_field_of_study(self, value: bool):
        self.editing_share_field_of_study = value

    @rx.event
    async def load_user_data(self):
        """Load data specific to the current user."""
        if not self.current_user:
            return
        await self._load_researcher_requests()
        if self.current_user["role"] == "participant":
            my_requests = [
                r
                for r in self.researcher_requests
                if r["participant_id"] == self.current_user["id"]
            ]
            researcher_ids = list(set((r["researcher_id"] for r in my_requests)))
            existing_ids = [u["id"] for u in self.users]
            missing_ids = [rid for rid in researcher_ids if rid not in existing_ids]
            if missing_ids:
                client = self._supabase_client
                if client:
                    try:
                        res = (
                            client.table("researchers")
                            .select("*")
                            .in_("user_id", missing_ids)
                            .execute()
                        )
                        for r_data in res.data:
                            self.users.append(
                                self._map_supabase_to_user(r_data, "researcher")
                            )
                    except Exception as e:
                        logging.exception(f"Error loading researchers: {e}")

    @rx.var
    def participant_enriched_requests(self) -> list[dict]:
        if not self.current_user or self.current_user["role"] != "participant":
            return []
        user_id = self.current_user["id"]
        my_requests = sorted(
            [r for r in self.researcher_requests if r["participant_id"] == user_id],
            key=lambda x: x["created_at"],
            reverse=True,
        )
        enriched = []
        for req in my_requests:
            study = next((s for s in self.studies if s["id"] == req["study_id"]), None)
            study_title = study["title"] if study else "مطالعه نامشخص"
            researcher_name = "پژوهشگر"
            res_user = next(
                (u for u in self.users if u["id"] == req["researcher_id"]), None
            )
            if res_user:
                researcher_name = res_user["name"]
            enriched.append(
                {**req, "study_title": study_title, "researcher_name": researcher_name}
            )
        return enriched

    @rx.event
    async def respond_to_request(self, request_id: str, status: str):
        client = self._supabase_client
        if client:
            try:
                client.table("researcher_requests").update({"status": status}).eq(
                    "id", request_id
                ).execute()
                new_requests = []
                for req in self.researcher_requests:
                    if req["id"] == request_id:
                        updated_req = req.copy()
                        updated_req["status"] = status
                        new_requests.append(updated_req)
                    else:
                        new_requests.append(req)
                self.researcher_requests = new_requests
                action = "پذیرفته" if status == "Accepted" else "رد"
                yield rx.toast.success(f"درخواست با موفقیت {action} شد.")
            except Exception as e:
                logging.exception(f"Error updating request: {e}")
                yield rx.toast.error("خطا در بروزرسانی وضعیت درخواست.")

    @rx.var
    def pending_requests_count(self) -> int:
        if not self.current_user or self.current_user["role"] != "participant":
            return 0
        user_id = self.current_user["id"]
        return len(
            [
                r
                for r in self.researcher_requests
                if r["participant_id"] == user_id and r["status"] == "Pending"
            ]
        )

    @rx.event
    def save_profile(self):
        if not self.current_user:
            return
        if not self.editing_name.strip():
            return rx.toast.error("نام نمی\u2009تواند خالی باشد.")
        updated_user = self.current_user.copy()
        updated_user["name"] = self.editing_name
        updated_user["education_level"] = self.editing_education_level
        updated_user["field_of_study"] = self.editing_field_of_study
        updated_user["occupation"] = self.editing_occupation
        updated_user["date_of_birth"] = self.editing_date_of_birth
        updated_user["phone_number"] = self.editing_phone_number
        updated_user["profile_picture"] = self.editing_profile_picture
        if self.current_user["role"] == "participant":
            updated_user["participant_status"] = self.editing_participant_status
            updated_user["share_education"] = self.editing_share_education
            updated_user["share_age"] = self.editing_share_age
            updated_user["share_occupation"] = self.editing_share_occupation
            updated_user["share_field_of_study"] = self.editing_share_field_of_study
        new_users = []
        for u in self.users:
            if u["id"] == self.current_user["id"]:
                new_users.append(updated_user)
            else:
                new_users.append(u)
        self.users = new_users
        self.current_user = updated_user
        self._sync_user_to_supabase(updated_user)
        self.is_edit_profile_open = False
        return rx.toast.success("پروفایل با موفقیت بروزرسانی شد.")