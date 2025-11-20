import reflex as rx
from app.states.browse_state import BrowseState
from app.states.application_state import ApplicationState
from app.states.auth_state import AuthState
from app.models import Study
from app.components.navbar import navbar
from app.components.application_form import application_form


def filter_section() -> rx.Component:
    input_class = "w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
    return rx.el.div(
        rx.el.div(
            rx.el.h3("فیلترها", class_name="text-lg font-semibold text-white mb-4"),
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
            class_name="bg-slate-900/60 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/10",
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
                            study["location_type"],
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/30 text-blue-300 border border-blue-500/20",
                        ),
                        rx.cond(
                            study.get("experiment_type") != "",
                            rx.el.span(
                                study.get("experiment_type"),
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
                    study["participant_criteria"],
                    class_name="text-xs text-gray-400 mb-3 line-clamp-1",
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
        class_name="bg-slate-900/60 backdrop-blur-md rounded-2xl shadow-sm border border-white/10 hover:border-white/20 hover:shadow-md transition-all overflow-hidden h-full flex flex-col relative",
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
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/background.png')] bg-cover bg-center bg-fixed bg-no-repeat",
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
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/background.png')] bg-cover bg-center bg-fixed bg-no-repeat",
    )


def detail_item(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-5 w-5 text-blue-400 mt-0.5 flex-shrink-0"),
        rx.el.div(
            rx.el.span(
                label,
                class_name="block text-xs font-medium text-gray-400 uppercase tracking-wider",
            ),
            rx.el.span(value, class_name="block text-sm text-white mt-0.5 font-medium"),
            class_name="ml-3",
        ),
        class_name="flex items-start p-4 bg-slate-950/30 rounded-xl border border-white/5",
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
                                    rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                                    "بازگشت به مرور",
                                    class_name="flex items-center text-sm font-medium text-gray-400 hover:text-white mb-6",
                                ),
                                href="/browse",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h1(
                                        study["title"],
                                        class_name="text-3xl md:text-4xl font-bold text-white leading-tight",
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
                                                    class_name="h-8 w-8 text-red-500 fill-current",
                                                ),
                                                rx.icon(
                                                    "heart",
                                                    class_name="h-8 w-8 text-gray-400 hover:text-red-500",
                                                ),
                                            ),
                                            on_click=lambda: AuthState.toggle_bookmark(
                                                study["id"]
                                            ),
                                        ),
                                    ),
                                    class_name="flex justify-between items-start mb-4",
                                ),
                                rx.el.div(
                                    rx.el.span(
                                        study["status"],
                                        class_name="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-900/30 text-green-300 border border-green-500/20",
                                    ),
                                    rx.el.span(
                                        f"ارسال شده توسط {BrowseState.current_study_researcher_name}",
                                        class_name="text-sm text-gray-400 flex items-center",
                                    ),
                                    class_name="flex items-center gap-4",
                                ),
                                class_name="mb-8",
                            ),
                        ),
                        class_name="max-w-4xl mx-auto",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.cond(
                                    study.get("study_image") != "",
                                    rx.image(
                                        src=rx.get_upload_url(study.get("study_image")),
                                        class_name="w-full h-64 object-cover rounded-2xl mb-8 shadow-md border border-white/10",
                                    ),
                                ),
                                rx.el.h2(
                                    "درباره مطالعه",
                                    class_name="text-xl font-bold text-white mb-4",
                                ),
                                rx.el.p(
                                    study["description"],
                                    class_name="text-gray-300 leading-relaxed whitespace-pre-wrap mb-8",
                                ),
                                rx.el.h2(
                                    "روش اجرا",
                                    class_name="text-xl font-bold text-white mb-4",
                                ),
                                rx.el.p(
                                    study["procedure_description"],
                                    class_name="text-gray-300 leading-relaxed whitespace-pre-wrap mb-8",
                                ),
                                rx.el.h2(
                                    "معیارهای شرکت\u200cکنندگان",
                                    class_name="text-xl font-bold text-white mb-4",
                                ),
                                rx.el.div(
                                    rx.el.ul(
                                        rx.el.li(
                                            rx.el.strong("نوع سلامت: "),
                                            study["psychological_health_type"],
                                        ),
                                        rx.el.li(
                                            rx.el.strong("محدوده سنی: "),
                                            f"{study['age_range_min']} - {study['age_range_max']} سال",
                                        ),
                                        rx.el.li(
                                            rx.el.strong("جنسیت: "),
                                            study["gender_requirement"],
                                        ),
                                        rx.cond(
                                            study["custom_criteria"] != "",
                                            rx.el.li(
                                                rx.el.strong("موارد اضافی: "),
                                                study["custom_criteria"],
                                            ),
                                        ),
                                        class_name="list-disc list-inside space-y-2 text-gray-300",
                                    ),
                                    class_name="bg-blue-900/20 p-6 rounded-2xl border border-blue-500/20",
                                ),
                                class_name="bg-slate-900/60 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-white/10",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "جزئیات مطالعه",
                                        class_name="text-lg font-bold text-white mb-6",
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
                                            study["location_type"],
                                            "map-pin",
                                        ),
                                        detail_item(
                                            "نوع آزمایش",
                                            study.get("experiment_type", "مشخص نشده"),
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
                                        class_name="space-y-3 mb-8",
                                    ),
                                    rx.el.button(
                                        "درخواست شرکت در مطالعه",
                                        class_name="w-full py-3 px-4 bg-blue-600 text-white rounded-xl font-semibold shadow-md hover:bg-blue-700 hover:shadow-lg transition-all transform hover:-translate-y-0.5",
                                        on_click=ApplicationState.open_application_modal,
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "info",
                                            class_name="h-4 w-4 text-gray-400 ml-2",
                                        ),
                                        rx.el.span(
                                            "ممکن است برای درخواست نیاز به ورود داشته باشید.",
                                            class_name="text-xs text-gray-400",
                                        ),
                                        class_name="flex items-center mt-4 justify-center",
                                    ),
                                    class_name="bg-slate-900/60 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/10 sticky top-24",
                                ),
                                class_name="space-y-6",
                            ),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-7xl mx-auto",
                        )
                    ),
                    class_name="px-4 sm:px-6 lg:px-8 py-8",
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
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/background.png')] bg-cover bg-center bg-fixed bg-no-repeat",
    )