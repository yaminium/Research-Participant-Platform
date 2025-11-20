import reflex as rx
from app.components.navbar import navbar
from app.components.auth_forms import login_form, register_form
from app.components.profile_view import profile_view
from app.components.study_form import study_form
from app.components.dashboard import dashboard_nav, my_studies_list
from app.components.applications_view import applications_view
from app.components.browse_views import (
    browse_page,
    study_detail_page,
    favorites_page,
    public_study_card,
)
from app.components.footer import footer
from app.components.info_modal import info_modal
from app.states.auth_state import AuthState
from app.states.study_state import StudyState
from app.states.application_state import ApplicationState


def base_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(content, class_name="flex-grow min-h-screen"),
        footer(),
        info_modal(),
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/background.png')] bg-cover bg-center bg-fixed bg-no-repeat selection:bg-blue-500/30",
        dir="rtl",
    )


def feature_item(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-8 w-8 text-blue-400"),
            class_name="w-16 h-16 bg-blue-900/30 rounded-2xl flex items-center justify-center mb-6",
        ),
        rx.el.h3(title, class_name="text-xl font-bold text-white mb-3"),
        rx.el.p(description, class_name="text-gray-300 leading-relaxed"),
        class_name="bg-slate-900/60 backdrop-blur-sm p-8 rounded-2xl border border-white/10 shadow-lg hover:bg-slate-800/60 transition-all",
    )


def step_item(number: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(number, class_name="text-2xl font-bold text-blue-400"),
            class_name="w-12 h-12 rounded-full bg-blue-900/30 flex items-center justify-center mb-4",
        ),
        rx.el.h4(title, class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(description, class_name="text-gray-300 text-sm"),
        class_name="flex flex-col items-center text-center max-w-xs",
    )


def index() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "پیشرفت علم. مشارکت در پژوهش.",
                        class_name="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight tracking-tight drop-shadow-lg",
                    ),
                    rx.el.p(
                        "با پژوهشگران برجسته جهان ارتباط برقرار کنید یا برای مطالعات پیشگامانه خود شرکت\u200cکننده پیدا کنید. پلتفرمی برای پژوهش\u200cهای روانشناسی و علوم اعصاب.",
                        class_name="text-xl text-gray-200 mb-10 max-w-2xl mx-auto leading-relaxed drop-shadow-md",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "مرور مطالعات",
                                class_name="w-full sm:w-auto px-8 py-4 rounded-full bg-blue-600 text-white font-semibold text-lg shadow-lg hover:bg-blue-700 hover:shadow-xl transition-all transform hover:-translate-y-1",
                            ),
                            href="/browse",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "برای پژوهشگران",
                                class_name="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-blue-600 border border-blue-200 font-semibold text-lg shadow-sm hover:bg-blue-50 transition-all",
                            ),
                            href="/register",
                        ),
                        class_name="flex flex-col sm:flex-row items-center justify-center gap-4",
                    ),
                    class_name="text-center max-w-5xl mx-auto pt-20 pb-16 px-4",
                ),
                rx.el.div(
                    rx.el.img(
                        src="/purple_navy_blue.png",
                        class_name="rounded-2xl shadow-2xl border-4 border-white/10 mx-auto w-full max-w-4xl opacity-90",
                    ),
                    class_name="px-4 pb-20",
                ),
            ),
            rx.cond(
                StudyState.featured_studies.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "مطالعات ویژه",
                            class_name="text-3xl font-bold text-white text-center mb-12",
                        ),
                        rx.el.div(
                            rx.foreach(StudyState.featured_studies, public_study_card),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                        ),
                        rx.el.div(
                            rx.el.a(
                                "مشاهده همه مطالعات",
                                href="/browse",
                                class_name="inline-flex items-center font-semibold text-blue-400 hover:text-blue-300 transition-colors",
                            ),
                            class_name="text-center mt-12",
                        ),
                        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                    ),
                    class_name="py-24",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "چگونه کار می\u200cکند",
                        class_name="text-3xl font-bold text-white text-center mb-16",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "برای شرکت\u200cکنندگان",
                                class_name="text-xl font-bold text-blue-400 mb-8 text-center",
                            ),
                            rx.el.div(
                                step_item(
                                    "۱",
                                    "ایجاد حساب کاربری",
                                    "برای شروع به عنوان شرکت\u200cکننده ثبت\u200cنام کنید.",
                                ),
                                step_item(
                                    "۲",
                                    "مرور مطالعات",
                                    "مطالعاتی که با پروفایل شما مطابقت دارند را پیدا کنید.",
                                ),
                                step_item(
                                    "۳",
                                    "درخواست و مشارکت",
                                    "درخواست ارسال کنید و در پیشرفت علم سهیم باشید.",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
                            ),
                            class_name="bg-slate-900/60 backdrop-blur-sm rounded-3xl p-8 border border-white/10",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "برای پژوهشگران",
                                class_name="text-xl font-bold text-blue-400 mb-8 text-center",
                            ),
                            rx.el.div(
                                step_item(
                                    "۱",
                                    "انتشار مطالعه",
                                    "فراخوان\u200cهای دقیق برای پژوهش خود ایجاد کنید.",
                                ),
                                step_item(
                                    "۲",
                                    "جذب نیرو",
                                    "درخواست\u200cهای شرکت\u200cکنندگان را دریافت و مدیریت کنید.",
                                ),
                                step_item(
                                    "۳",
                                    "انجام پژوهش",
                                    "با شرکت\u200cکنندگان هماهنگ کنید و داده\u200cها را جمع\u200cآوری کنید.",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
                            ),
                            class_name="bg-slate-900/60 backdrop-blur-sm rounded-3xl p-8 border border-white/10",
                        ),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                    ),
                    class_name="py-24",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "چرا نورو ریکروت؟",
                        class_name="text-3xl font-bold text-white text-center mb-16",
                    ),
                    rx.el.div(
                        feature_item(
                            "users",
                            "جذب هدفمند",
                            "با سیستم پیشرفته فیلترینگ ما، دقیقاً شرکت\u200cکنندگان مورد نیاز خود را پیدا کنید.",
                        ),
                        feature_item(
                            "shield-check",
                            "شرکت\u200cکنندگان تایید شده",
                            "با جامعه\u200cای از دانشجویان و اعضای تایید شده علاقه\u200cمند به پژوهش اعتماد بسازید.",
                        ),
                        feature_item(
                            "zap",
                            "فرآیند یکپارچه",
                            "مدیریت درخواست\u200cها، ارتباط با شرکت\u200cکنندگان و سازماندهی مطالعات در یک مکان.",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                    ),
                    class_name="py-24",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "آماده شروع هستید؟",
                        class_name="text-3xl font-bold text-white mb-6",
                    ),
                    rx.el.p(
                        "به هزاران پژوهشگر و شرکت\u200cکننده در پیشبرد روانشناسی و علوم اعصاب بپیوندید.",
                        class_name="text-blue-100 text-lg mb-10 max-w-2xl mx-auto",
                    ),
                    rx.el.div(
                        rx.el.a(
                            rx.el.button(
                                "ایجاد حساب کاربری",
                                class_name="px-8 py-4 rounded-full bg-white text-blue-600 font-bold text-lg shadow-lg hover:bg-gray-100 transition-all",
                            ),
                            href="/register",
                        ),
                        class_name="flex justify-center",
                    ),
                    class_name="max-w-4xl mx-auto text-center px-4",
                ),
                class_name="py-24 bg-blue-600/90 backdrop-blur-sm",
            ),
        )
    )


def login_page() -> rx.Component:
    return base_layout(login_form())


def register_page() -> rx.Component:
    return base_layout(register_form())


def profile_page() -> rx.Component:
    return base_layout(
        rx.cond(
            AuthState.is_authenticated,
            profile_view(),
            rx.el.div(
                rx.el.div(
                    rx.icon("lock", class_name="h-12 w-12 text-gray-400 mb-4 mx-auto"),
                    rx.el.h2(
                        "دسترسی غیرمجاز", class_name="text-2xl font-bold text-white"
                    ),
                    rx.el.p(
                        "لطفاً برای مشاهده پروفایل خود وارد شوید.",
                        class_name="text-gray-400 mt-2",
                    ),
                    rx.el.a(
                        "رفتن به صفحه ورود",
                        href="/login",
                        class_name="mt-6 inline-block px-6 py-2.5 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition-colors",
                    ),
                    class_name="text-center py-20 bg-slate-900/60 backdrop-blur-md rounded-xl border border-white/10 max-w-lg mx-auto mt-20",
                )
            ),
        )
    )


def dashboard_page() -> rx.Component:
    return base_layout(
        rx.cond(
            AuthState.is_researcher,
            rx.el.div(
                dashboard_nav("applications"),
                applications_view(),
                class_name="max-w-7xl mx-auto px-4 py-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("lock", class_name="h-12 w-12 text-gray-400 mb-4 mx-auto"),
                    rx.el.h2(
                        "دسترسی غیرمجاز", class_name="text-2xl font-bold text-white"
                    ),
                    rx.el.p(
                        "این داشبورد فقط برای پژوهشگران است.",
                        class_name="text-gray-400 mt-2",
                    ),
                    rx.el.a(
                        "رفتن به پروفایل من",
                        href="/profile",
                        class_name="mt-6 inline-block px-6 py-2.5 bg-blue-600 text-white rounded-full font-medium hover:bg-blue-700 transition-colors",
                    ),
                    class_name="text-center py-20 bg-slate-900/60 backdrop-blur-md rounded-xl border border-white/10 max-w-lg mx-auto mt-20",
                )
            ),
        )
    )


def my_studies_page() -> rx.Component:
    return base_layout(
        rx.cond(
            AuthState.is_researcher,
            rx.el.div(
                dashboard_nav("my_studies"),
                my_studies_list(),
                class_name="max-w-7xl mx-auto px-4 py-8",
            ),
            rx.el.div(
                "دسترسی غیرمجاز: فقط پژوهشگران",
                class_name="text-center p-10 text-white",
            ),
        )
    )


def create_study_page() -> rx.Component:
    return base_layout(
        rx.cond(
            AuthState.is_researcher,
            rx.el.div(
                dashboard_nav("create_study"),
                study_form(),
                class_name="max-w-7xl mx-auto px-4 py-8",
            ),
            rx.el.div(
                "دسترسی غیرمجاز: فقط پژوهشگران",
                class_name="text-center p-10 text-white",
            ),
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap",
            rel="stylesheet",
        ),
    ],
    style={"font_family": "Vazirmatn"},
)
app.add_page(index, route="/", on_load=StudyState.load_studies)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(profile_page, route="/profile")
app.add_page(
    dashboard_page, route="/dashboard", on_load=ApplicationState.load_applications
)
app.add_page(my_studies_page, route="/my-studies")
app.add_page(create_study_page, route="/create-study")
app.add_page(browse_page, route="/browse")
app.add_page(favorites_page, route="/favorites")
app.add_page(study_detail_page, route="/study/[id]")