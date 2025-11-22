import reflex as rx
from app.states.browse_state import BrowseState
from app.states.application_state import ApplicationState
from app.states.auth_state import AuthState
from app.models import Study
from app.components.navbar import navbar
from app.components.application_form import application_form


def translate_location(location: str) -> rx.Component:
    return rx.match(location, ("Online", "آنلاین"), ("In-Person", "حضوری"), location)


def translate_experiment(exp_type: str) -> rx.Component:
    return rx.match(
        exp_type,
        ("Paper Based", "کاغذی"),
        ("Computer Based", "کامپیوتری"),
        ("Eye-Tracker", "ردیاب چشم"),
        exp_type,
    )


def translate_health(health: str) -> rx.Component:
    return rx.match(
        health,
        ("No Preference", "بدون ترجیح"),
        ("Psychologically Healthy", "سالم از نظر روانی"),
        ("Specific Psychological Conditions", "شرایط خاص روانشناختی"),
        ("Mental Disorder", "اختلال روانی"),
        ("Twins", "دوقلوها"),
        ("Siblings (Non-Twin)", "خواهر و برادر (غیر دوقلو)"),
        health,
    )


def translate_gender(gender: str) -> rx.Component:
    return rx.match(
        gender,
        ("Any", "هر جنسیتی"),
        ("Male", "مرد"),
        ("Female", "زن"),
        ("Other", "سایر"),
        gender,
    )


def filter_section() -> rx.Component:
    input_class = "w-full rounded-lg border-white/10 bg-slate-950/80 text-white placeholder-gray-400 shadow-sm focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 text-sm transition-colors"
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "فیلترها",
                class_name="text-lg font-bold text-white mb-6 flex items-center gap-2 border-b border-white/10 pb-3",
            ),
            rx.el.div(
                rx.el.label(
                    "جستجو", class_name="block text-sm font-medium text-gray-300 mb-1"
                ),
                rx.el.input(
                    placeholder="عنوان یا کلمه کلیدی...",
                    on_change=BrowseState.set_search_query.debounce(500),
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "پاداش", class_name="block text-sm font-medium text-gray-300 mb-1"
                ),
                rx.el.input(
                    placeholder="مثال: ۵۰۰ تومان",
                    on_change=BrowseState.set_filter_compensation.debounce(500),
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "نوع سلامت",
                    class_name="block text-sm font-medium text-gray-300 mb-1",
                ),
                rx.el.select(
                    rx.el.option("همه انواع", value="All"),
                    rx.el.option("بدون ترجیح", value="No Preference"),
                    rx.el.option("از نظر روانی سالم", value="Psychologically Healthy"),
                    rx.el.option(
                        "شرایط خاص روانشناختی",
                        value="Specific Psychological Conditions",
                    ),
                    rx.el.option("اختلال روانی", value="Mental Disorder"),
                    rx.el.option("دوقلوها", value="Twins"),
                    rx.el.option(
                        "خواهر و برادر (غیر دوقلو)", value="Siblings (Non-Twin)"
                    ),
                    value=BrowseState.filter_health_type,
                    on_change=BrowseState.set_filter_health_type,
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "نوع آزمایش",
                    class_name="block text-sm font-medium text-gray-300 mb-1",
                ),
                rx.el.select(
                    rx.el.option("همه انواع", value="All"),
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
                    value=BrowseState.filter_experiment_type,
                    on_change=BrowseState.set_filter_experiment_type,
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "مکان", class_name="block text-sm font-medium text-gray-300 mb-1"
                ),
                rx.el.select(class_name="block text-sm font-medium text-gray-300 mb-1"),
                rx.el.select(
                    rx.el.option("همه مکان\u200cها", value="All"),
                    rx.el.option("آنلاین", value="Online"),
                    rx.el.option("حضوری", value="In-Person"),
                    value=BrowseState.filter_location_type,
                    on_change=BrowseState.set_filter_location_type,
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "مدت زمان",
                    class_name="block text-sm font-medium text-gray-300 mb-1",
                ),
                rx.el.input(
                    placeholder="مثال: ۳۰ دقیقه",
                    on_change=BrowseState.set_filter_duration.debounce(500),
                    class_name=input_class,
                ),
                class_name="mb-4",
            ),
            class_name="bg-gradient-to-br from-slate-900/95 via-slate-900/95 to-indigo-950/50 backdrop-blur-xl p-6 rounded-2xl shadow-xl border border-white/10 border-t-4 border-t-blue-500 sticky top-24",
        ),
        class_name="w-full md:w-72 flex-shrink-0",
    )


def public_study_card(study: Study) -> rx.Component:
    return rx.el.div(
        rx.cond(
            study.get("study_image") != "",
            rx.image(
                src=rx.get_upload_url(study.get("study_image")),
                class_name="w-full h-32 object-cover",
            ),
            rx.el.div(
                class_name="w-full h-32 bg-gradient-to-br from-blue-900/20 to-purple-900/20"
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            translate_location(study["location_type"]),
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/30 text-blue-300 border border-blue-500/20",
                        ),
                        rx.cond(
                            study.get("experiment_type") != "",
                            rx.el.span(
                                translate_experiment(study.get("experiment_type")),
                                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900/30 text-purple-300 border border-purple-500/20 ml-2",
                            ),
                        ),
                    ),
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.el.button(
                            rx.cond(
                                AuthState.bookmarked_study_ids.contains(study["id"]),
                                rx.icon(
                                    "heart",
                                    class_name="h-5 w-5 text-red-500 fill-current",
                                ),
                                rx.icon(
                                    "heart",
                                    class_name="h-5 w-5 text-gray-400 hover:text-red-500",
                                ),
                            ),
                            on_click=lambda: AuthState.toggle_bookmark(study["id"]),
                        ),
                    ),
                    class_name="flex justify-between items-start mb-3",
                ),
                rx.el.h3(
                    study["title"],
                    class_name="text-lg font-bold text-white line-clamp-1 mb-1",
                ),
                rx.el.p(
                    rx.el.span("سلامت: ", class_name="text-gray-500"),
                    translate_health(study["psychological_health_type"]),
                    rx.el.span("، سن: ", class_name="text-gray-500"),
                    study["age_range_min"].to_string(),
                    "-",
                    study["age_range_max"].to_string(),
                    " سال",
                    rx.el.span("، جنسیت: ", class_name="text-gray-500"),
                    translate_gender(study["gender_requirement"]),
                    class_name="text-xs text-gray-300 mb-3 line-clamp-1",
                ),
                rx.el.p(
                    study["description"],
                    class_name="text-gray-300 text-sm mb-4 line-clamp-2 h-10",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("dollar-sign", class_name="h-4 w-4 text-gray-400 ml-1"),
                        rx.el.span(
                            study["compensation"], class_name="text-xs text-gray-400"
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.icon("clock", class_name="h-4 w-4 text-gray-400 ml-1"),
                        rx.el.span(
                            study["duration"], class_name="text-xs text-gray-400"
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center gap-4 mb-4",
                ),
                class_name="flex-1",
            ),
            rx.el.a(
                rx.el.button(
                    "مشاهده جزئیات",
                    class_name="w-full py-2 px-4 border border-white/20 text-blue-300 rounded-lg text-sm font-medium hover:bg-white/10 transition-colors",
                ),
                href=f"/study/{study['id']}",
                class_name="mt-auto",
            ),
            class_name="flex flex-col h-full p-5",
        ),
        class_name="bg-slate-900/60 backdrop-blur-md rounded-2xl shadow-sm border border-white/10 transition-all duration-300 ease-in-out hover:scale-[1.03] hover:shadow-[0_20px_50px_-12px_rgba(59,130,246,0.3)] hover:border-blue-500/50 overflow-hidden h-full flex flex-col relative group z-0 hover:z-10",
    )


def pagination_controls() -> rx.Component:
    return rx.cond(
        BrowseState.total_pages > 1,
        rx.el.div(
            rx.el.button(
                "قبلی",
                on_click=BrowseState.prev_page,
                disabled=BrowseState.current_page <= 1,
                class_name="px-4 py-2 border border-white/10 rounded-md text-sm font-medium text-gray-300 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.el.span(
                f"صفحه {BrowseState.current_page} از {BrowseState.total_pages}",
                class_name="text-sm text-gray-300 font-medium",
            ),
            rx.el.button(
                "بعدی",
                on_click=BrowseState.next_page,
                disabled=BrowseState.current_page >= BrowseState.total_pages,
                class_name="px-4 py-2 border border-white/10 rounded-md text-sm font-medium text-gray-300 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex items-center justify-between w-full max-w-sm mx-auto mt-8 bg-slate-900/60 backdrop-blur-md p-4 rounded-xl shadow-sm border border-white/10",
        ),
    )


def browse_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "مشارکت در پژوهش",
                        class_name="text-3xl font-bold text-white mb-2",
                    ),
                    rx.el.p(
                        "مطالعاتی که با پروفایل شما مطابقت دارند را پیدا کنید و در علم سهیم باشید.",
                        class_name="text-gray-300",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    filter_section(),
                    rx.el.div(
                        rx.cond(
                            BrowseState.total_items > 0,
                            rx.el.div(
                                rx.el.div(
                                    rx.foreach(
                                        BrowseState.paginated_studies, public_study_card
                                    ),
                                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                                ),
                                pagination_controls(),
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "search-x",
                                        class_name="h-16 w-16 text-gray-500 mb-4",
                                    ),
                                    rx.el.h3(
                                        "هیچ مطالعه\u200cای یافت نشد",
                                        class_name="text-lg font-medium text-white",
                                    ),
                                    rx.el.p(
                                        "لطفاً فیلترهای خود را تغییر دهید تا نتایج بیشتری ببینید.",
                                        class_name="text-gray-400 mt-2",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-16 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-white/10",
                                )
                            ),
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex flex-col md:flex-row gap-8",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex-grow min-h-screen",
        ),
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/ChatGPT_page2.png')] bg-cover bg-center bg-fixed bg-no-repeat",
    )


def favorites_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "علاقه\u200cمندی\u200cهای من",
                        class_name="text-3xl font-bold text-white mb-2",
                    ),
                    rx.el.p(
                        "مطالعاتی که برای بعد نشان\u200cگذاری کرده\u200cاید.",
                        class_name="text-gray-300",
                    ),
                    class_name="mb-8",
                ),
                rx.cond(
                    AuthState.bookmarked_studies.length() > 0,
                    rx.el.div(
                        rx.foreach(AuthState.bookmarked_studies, public_study_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("heart", class_name="h-16 w-16 text-gray-500 mb-4"),
                            rx.el.h3(
                                "هنوز هیچ علاقه\u200cمندی ندارید",
                                class_name="text-lg font-medium text-white",
                            ),
                            rx.el.p(
                                "مطالعات را نشان\u200cگذاری کنید تا در اینجا ببینید.",
                                class_name="text-gray-400 mt-2",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "مرور مطالعات",
                                    class_name="mt-6 px-6 py-2 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition-colors",
                                ),
                                href="/browse",
                            ),
                            class_name="flex flex-col items-center justify-center py-16 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-white/10",
                        )
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex-grow min-h-screen",
        ),
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/ChatGPT_page2.png')] bg-cover bg-center bg-fixed bg-no-repeat",
    )


def detail_item(label: str, value: rx.Component | str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-8 w-8 text-blue-400 mt-1 flex-shrink-0"),
        rx.el.div(
            rx.el.span(
                label,
                class_name="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-1",
            ),
            rx.el.span(value, class_name="block text-lg text-white font-semibold"),
            class_name="ml-4 flex-grow",
        ),
        class_name="flex items-start p-5 bg-slate-950/50 rounded-2xl border border-white/10 hover:border-blue-500/30 transition-colors group",
    )


def study_detail_page() -> rx.Component:
    study = BrowseState.current_study
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                study,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.a(
                                rx.el.div(
                                    rx.icon("arrow-right", class_name="h-5 w-5 ml-2"),
                                    "بازگشت به مرور",
                                    class_name="flex items-center text-base font-medium text-gray-400 hover:text-white mb-8 transition-colors",
                                ),
                                href="/browse",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h1(
                                        study["title"],
                                        class_name="text-4xl md:text-5xl font-extrabold text-white leading-tight drop-shadow-lg mb-6",
                                    ),
                                    rx.cond(
                                        AuthState.is_authenticated,
                                        rx.el.button(
                                            rx.cond(
                                                AuthState.bookmarked_study_ids.contains(
                                                    study["id"]
                                                ),
                                                rx.icon(
                                                    "heart",
                                                    class_name="h-10 w-10 text-red-500 fill-current drop-shadow-md",
                                                ),
                                                rx.icon(
                                                    "heart",
                                                    class_name="h-10 w-10 text-gray-400 hover:text-red-500 transition-colors",
                                                ),
                                            ),
                                            on_click=lambda: AuthState.toggle_bookmark(
                                                study["id"]
                                            ),
                                            class_name="p-2 rounded-full hover:bg-white/5 transition-colors",
                                        ),
                                    ),
                                    class_name="flex justify-between items-start",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        study["status"],
                                        class_name="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-bold bg-green-900/40 text-green-300 border border-green-500/30 shadow-[0_0_10px_rgba(34,197,94,0.2)]",
                                    ),
                                    rx.el.span(
                                        f"ارسال شده توسط {BrowseState.current_study_researcher_name}",
                                        class_name="text-base text-gray-400 flex items-center",
                                    ),
                                    class_name="flex items-center gap-6 mt-4",
                                ),
                                class_name="mb-12",
                            ),
                        ),
                        class_name="max-w-5xl mx-auto px-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.cond(
                                    study.get("study_image") != "",
                                    rx.image(
                                        src=rx.get_upload_url(study.get("study_image")),
                                        class_name="w-full h-80 object-cover rounded-3xl mb-10 shadow-2xl border border-white/10",
                                    ),
                                ),
                                rx.el.h2(
                                    "درباره مطالعه",
                                    class_name="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 mb-6",
                                ),
                                rx.el.p(
                                    study["description"],
                                    class_name="text-gray-300 text-lg leading-loose whitespace-pre-wrap mb-10",
                                ),
                                rx.el.h2(
                                    "روش اجرا",
                                    class_name="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 mb-6",
                                ),
                                rx.el.p(
                                    study["procedure_description"],
                                    class_name="text-gray-300 text-lg leading-loose whitespace-pre-wrap mb-10",
                                ),
                                rx.el.h2(
                                    "معیارهای شرکت\u200cکنندگان",
                                    class_name="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 mb-6",
                                ),
                                rx.el.div(
                                    rx.el.ul(
                                        rx.el.li(
                                            rx.el.span(
                                                "نوع سلامت: ",
                                                class_name="text-blue-300 font-semibold",
                                            ),
                                            translate_health(
                                                study["psychological_health_type"]
                                            ),
                                        ),
                                        rx.el.li(
                                            rx.el.span(
                                                "محدوده سنی: ",
                                                class_name="text-blue-300 font-semibold",
                                            ),
                                            f"{study['age_range_min']} - {study['age_range_max']} سال",
                                        ),
                                        rx.el.li(
                                            rx.el.span(
                                                "جنسیت: ",
                                                class_name="text-blue-300 font-semibold",
                                            ),
                                            translate_gender(
                                                study["gender_requirement"]
                                            ),
                                        ),
                                        rx.cond(
                                            study["custom_criteria"] != "",
                                            rx.el.li(
                                                rx.el.span(
                                                    "موارد اضافی: ",
                                                    class_name="text-blue-300 font-semibold",
                                                ),
                                                study["custom_criteria"],
                                            ),
                                        ),
                                        class_name="space-y-4 text-gray-200 text-lg list-none",
                                    ),
                                    class_name="bg-slate-900/50 p-8 rounded-3xl border border-white/10 hover:border-blue-500/30 transition-colors",
                                ),
                                class_name="bg-slate-900/40 backdrop-blur-xl p-10 rounded-[2rem] shadow-xl border border-white/5 h-full",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "جزئیات کلیدی",
                                        class_name="text-xl font-bold text-white mb-8 flex items-center gap-3",
                                    ),
                                    rx.el.div(
                                        detail_item(
                                            "پاداش",
                                            study["compensation"],
                                            "dollar-sign",
                                        ),
                                        detail_item(
                                            "مدت زمان", study["duration"], "clock"
                                        ),
                                        detail_item(
                                            "نوع مکان",
                                            translate_location(study["location_type"]),
                                            "map-pin",
                                        ),
                                        detail_item(
                                            "نوع آزمایش",
                                            translate_experiment(
                                                study.get(
                                                    "experiment_type", "مشخص نشده"
                                                )
                                            ),
                                            "microscope",
                                        ),
                                        rx.cond(
                                            study["location_type"] == "In-Person",
                                            detail_item(
                                                "آدرس",
                                                study["physical_location"],
                                                "building",
                                            ),
                                        ),
                                        detail_item(
                                            "حجم نمونه",
                                            f"{study['sample_size']} شرکت\u200cکننده",
                                            "users",
                                        ),
                                        class_name="space-y-4 mb-10",
                                    ),
                                    rx.el.button(
                                        "درخواست شرکت در مطالعه",
                                        class_name="w-full py-4 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-2xl font-bold text-lg shadow-lg hover:shadow-blue-500/25 hover:from-blue-500 hover:to-indigo-500 transition-all transform hover:-translate-y-1",
                                        on_click=ApplicationState.open_application_modal,
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "info",
                                            class_name="h-5 w-5 text-gray-400 ml-2",
                                        ),
                                        rx.el.span(
                                            "ممکن است برای درخواست نیاز به ورود داشته باشید.",
                                            class_name="text-sm text-gray-400",
                                        ),
                                        class_name="flex items-center mt-6 justify-center bg-slate-950/30 p-3 rounded-xl border border-white/5",
                                    ),
                                    class_name="bg-slate-900/60 backdrop-blur-md p-8 rounded-[2rem] shadow-2xl border border-white/10 sticky top-28",
                                ),
                                class_name="space-y-6",
                            ),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-10 max-w-7xl mx-auto",
                        )
                    ),
                    class_name="px-4 sm:px-6 lg:px-8 py-12",
                ),
                rx.el.div(
                    "مطالعه یافت نشد.",
                    class_name="text-center text-gray-500 text-xl py-20",
                ),
            ),
            rx.cond(
                ApplicationState.is_modal_open,
                rx.el.div(
                    rx.el.div(
                        application_form(),
                        class_name="flex items-center justify-center min-h-screen px-4",
                    ),
                    class_name="fixed inset-0 bg-slate-950/80 z-[100] overflow-y-auto backdrop-blur-sm",
                ),
            ),
            class_name="flex-grow min-h-screen",
        ),
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/ChatGPT_homepage.png')] bg-cover bg-center bg-fixed bg-no-repeat",
    )