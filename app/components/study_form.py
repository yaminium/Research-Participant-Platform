import reflex as rx
from app.states.study_state import StudyState


def form_field(label: str, input_component: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-300 mb-1"),
        input_component,
        class_name="mb-4",
    )


def study_form() -> rx.Component:
    input_class = "block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500"
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                rx.cond(
                    StudyState.editing_study_id != "",
                    "ویرایش مطالعه",
                    "ایجاد مطالعه جدید",
                ),
                class_name="text-2xl font-bold text-white mb-6",
            ),
            rx.el.div(
                rx.el.h3(
                    "اطلاعات اولیه",
                    class_name="text-lg font-semibold text-blue-400 mb-4 border-b border-white/10 pb-2",
                ),
                form_field(
                    "عنوان مطالعه",
                    rx.el.input(
                        on_change=StudyState.set_title,
                        placeholder="مثال: پردازش حافظه دیداری در بزرگسالان",
                        class_name=input_class,
                        default_value=StudyState.title,
                    ),
                ),
                form_field(
                    "توضیحات",
                    rx.el.textarea(
                        on_change=StudyState.set_description,
                        rows=3,
                        class_name=input_class,
                        default_value=StudyState.description,
                    ),
                ),
                form_field(
                    "تصویر مطالعه",
                    rx.el.div(
                        rx.upload.root(
                            rx.el.button(
                                "انتخاب تصویر",
                                type="button",
                                class_name="px-4 py-2 bg-slate-800 border border-white/10 rounded-lg text-sm text-gray-300 hover:bg-slate-700 transition-colors",
                            ),
                            id="upload_study_image",
                            max_files=1,
                            accept={
                                "image/png": [".png"],
                                "image/jpeg": [".jpg", ".jpeg"],
                                "image/webp": [".webp"],
                            },
                            class_name="mb-2",
                        ),
                        rx.el.div(
                            rx.foreach(
                                rx.selected_files("upload_study_image"),
                                lambda file: rx.el.p(
                                    file, class_name="text-xs text-blue-400 mb-2"
                                ),
                            )
                        ),
                        rx.el.button(
                            "آپلود تصویر انتخاب شده",
                            type="button",
                            on_click=StudyState.handle_image_upload(
                                rx.upload_files(upload_id="upload_study_image")
                            ),
                            class_name="text-xs bg-blue-600/20 text-blue-300 px-3 py-1.5 rounded border border-blue-500/30 hover:bg-blue-600/30",
                        ),
                        rx.cond(
                            StudyState.study_image != "",
                            rx.el.div(
                                rx.el.p(
                                    "تصویر فعلی:",
                                    class_name="text-xs text-gray-400 mt-2",
                                ),
                                rx.image(
                                    src=rx.get_upload_url(StudyState.study_image),
                                    class_name="h-20 w-auto rounded mt-1 border border-white/10",
                                ),
                            ),
                        ),
                        class_name="p-4 bg-slate-950/30 rounded-lg border border-white/5",
                    ),
                ),
                rx.el.div(
                    form_field(
                        "حجم نمونه مورد نیاز",
                        rx.el.input(
                            type="number",
                            on_change=StudyState.set_sample_size,
                            class_name=input_class,
                            default_value=StudyState.sample_size.to_string(),
                        ),
                    ),
                    form_field(
                        "پاداش",
                        rx.el.input(
                            on_change=StudyState.set_compensation,
                            placeholder="مثال: ۵۰۰ هزار تومان",
                            class_name=input_class,
                            default_value=StudyState.compensation,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "معیارهای شرکت\u200cکنندگان",
                    class_name="text-lg font-semibold text-blue-400 mb-4 border-b border-white/10 pb-2",
                ),
                rx.el.div(
                    form_field(
                        "وضعیت سلامت روان",
                        rx.el.select(
                            rx.el.option("بدون ترجیح", value="No Preference"),
                            rx.el.option(
                                "از نظر روانی سالم", value="Psychologically Healthy"
                            ),
                            rx.el.option(
                                "شرایط خاص روانشناختی",
                                value="Specific Psychological Conditions",
                            ),
                            rx.el.option("اختلال روانی", value="Mental Disorder"),
                            rx.el.option("دوقلوها", value="Twins"),
                            rx.el.option(
                                "خواهر و برادر (غیر دوقلو)", value="Siblings (Non-Twin)"
                            ),
                            value=StudyState.psychological_health_type,
                            on_change=StudyState.set_psychological_health_type,
                            class_name=input_class,
                        ),
                    ),
                    form_field(
                        "الزامات جنسیتی",
                        rx.el.select(
                            rx.el.option("هر جنسیتی", value="Any"),
                            rx.el.option("مرد", value="Male"),
                            rx.el.option("زن", value="Female"),
                            rx.el.option("سایر", value="Other"),
                            value=StudyState.gender_requirement,
                            on_change=StudyState.set_gender_requirement,
                            class_name=input_class,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    form_field(
                        "حداقل سن",
                        rx.el.input(
                            type="number",
                            on_change=StudyState.set_age_range_min,
                            class_name=input_class,
                            default_value=StudyState.age_range_min.to_string(),
                        ),
                    ),
                    form_field(
                        "حداکثر سن",
                        rx.el.input(
                            type="number",
                            on_change=StudyState.set_age_range_max,
                            class_name=input_class,
                            default_value=StudyState.age_range_max.to_string(),
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                form_field(
                    "معیارهای سفارشی",
                    rx.el.textarea(
                        on_change=StudyState.set_custom_criteria,
                        rows=2,
                        placeholder="هرگونه الزامات اضافی...",
                        class_name=input_class,
                        default_value=StudyState.custom_criteria,
                    ),
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "لجستیک مطالعه",
                    class_name="text-lg font-semibold text-blue-400 mb-4 border-b border-white/10 pb-2",
                ),
                form_field(
                    "نوع آزمایش",
                    rx.el.select(
                        rx.el.option("مبتنی بر کاغذ", value="Paper Based"),
                        rx.el.option("مبتنی بر کامپیوتر", value="Computer Based"),
                        rx.el.option("MRI", value="MRI"),
                        rx.el.option("FMRI", value="FMRI"),
                        rx.el.option("DTI", value="DTI"),
                        rx.el.option("EEG", value="EEG"),
                        rx.el.option("fNIRS", value="fNIRS"),
                        rx.el.option("TMS", value="TMS"),
                        rx.el.option("tDCS", value="tDCS"),
                        rx.el.option("tACS", value="tACS"),
                        rx.el.option("ردیاب چشم (Eye-Tracker)", value="Eye-Tracker"),
                        value=StudyState.experiment_type,
                        on_change=StudyState.set_experiment_type,
                        class_name=input_class,
                    ),
                ),
                form_field(
                    "توضیحات روش اجرا",
                    rx.el.textarea(
                        on_change=StudyState.set_procedure_description,
                        rows=3,
                        placeholder="شرکت\u200cکنندگان چه کاری انجام خواهند داد؟",
                        class_name=input_class,
                        default_value=StudyState.procedure_description,
                    ),
                ),
                form_field(
                    "نوع مکان",
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="location_type",
                                value="Online",
                                checked=StudyState.location_type == "Online",
                                on_change=lambda: StudyState.set_location_type(
                                    "Online"
                                ),
                                class_name="ml-2 text-blue-500 focus:ring-blue-500 bg-slate-900 border-white/20",
                            ),
                            "آنلاین",
                            class_name="inline-flex items-center ml-6 text-white",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="location_type",
                                value="In-Person",
                                checked=StudyState.location_type == "In-Person",
                                on_change=lambda: StudyState.set_location_type(
                                    "In-Person"
                                ),
                                class_name="ml-2 text-blue-500 focus:ring-blue-500 bg-slate-900 border-white/20",
                            ),
                            "حضوری",
                            class_name="inline-flex items-center text-white",
                        ),
                        class_name="flex items-center mt-2",
                    ),
                ),
                rx.cond(
                    StudyState.location_type == "In-Person",
                    form_field(
                        "آدرس مکان فیزیکی",
                        rx.el.input(
                            on_change=StudyState.set_physical_location,
                            placeholder="ساختمان، شماره اتاق...",
                            class_name=input_class,
                            default_value=StudyState.physical_location,
                        ),
                    ),
                ),
                rx.el.div(
                    form_field(
                        "مدت زمان",
                        rx.el.input(
                            on_change=StudyState.set_duration,
                            placeholder="مثال: ۳۰ دقیقه",
                            class_name=input_class,
                            default_value=StudyState.duration,
                        ),
                    ),
                    form_field(
                        "اطلاعات تماس",
                        rx.el.input(
                            on_change=StudyState.set_contact_info,
                            placeholder="ایمیل یا تلفن",
                            class_name=input_class,
                            default_value=StudyState.contact_info,
                        ),
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            checked=StudyState.is_open,
                            on_change=StudyState.set_is_open_toggle,
                            class_name="sr-only peer",
                        ),
                        rx.el.div(
                            class_name="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-800 rounded-full peer peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"
                        ),
                        rx.el.span(
                            "وضعیت مطالعه: ",
                            class_name="mr-3 text-sm font-medium text-gray-300 ml-1",
                        ),
                        rx.el.span(
                            rx.cond(
                                StudyState.is_open,
                                "باز برای درخواست\u200cها",
                                "بسته شده",
                            ),
                            class_name=rx.cond(
                                StudyState.is_open,
                                "text-green-400 font-bold",
                                "text-red-400 font-bold",
                            ),
                        ),
                        class_name="relative inline-flex items-center cursor-pointer",
                    ),
                    class_name="mt-4",
                ),
                class_name="mb-8",
            ),
            rx.cond(
                StudyState.form_error != "",
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-5 w-5 ml-2"),
                    StudyState.form_error,
                    class_name="bg-red-900/30 text-red-200 p-4 rounded-lg flex items-center mb-6 border border-red-800/50",
                ),
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "لغو",
                        class_name="px-6 py-3 border border-white/20 shadow-sm text-sm font-medium rounded-md text-gray-200 bg-white/5 hover:bg-white/10 focus:outline-none",
                    ),
                    href="/my-studies",
                ),
                rx.el.button(
                    rx.cond(
                        StudyState.editing_study_id != "",
                        "بروزرسانی مطالعه",
                        "انتشار مطالعه",
                    ),
                    on_click=StudyState.save_study,
                    class_name="px-8 py-3 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                class_name="flex items-center justify-end gap-4",
            ),
            class_name="bg-slate-900/60 backdrop-blur-md shadow-xl rounded-2xl p-8 border border-white/10",
        ),
        class_name="max-w-3xl mx-auto py-8 px-4",
    )