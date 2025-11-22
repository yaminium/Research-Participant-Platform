import reflex as rx
import datetime
from app.states.participant_browser_state import ParticipantBrowserState
from app.models import User


def calculate_age_str(dob_str: str | None) -> str:
    return ""


def request_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-[100] animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.h3(
                        "ارسال درخواست به "
                        + ParticipantBrowserState.get_selected_participant_name,
                        class_name="text-xl font-bold text-white mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "انتخاب مطالعه",
                            class_name="block text-sm font-medium text-gray-300 mb-2",
                        ),
                        rx.el.select(
                            rx.el.option("انتخاب کنید...", value=""),
                            rx.foreach(
                                ParticipantBrowserState.researcher_studies_options,
                                lambda s: rx.el.option(s["title"], value=s["id"]),
                            ),
                            on_change=ParticipantBrowserState.set_request_study_id,
                            class_name="block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2.5 mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "متن پیام",
                            class_name="block text-sm font-medium text-gray-300 mb-2",
                        ),
                        rx.el.textarea(
                            placeholder="پیامی برای شرکت\u200cکننده بنویسید...",
                            on_change=ParticipantBrowserState.set_request_message,
                            rows=4,
                            class_name="block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm mb-6",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "لغو",
                            on_click=ParticipantBrowserState.close_request_modal,
                            class_name="px-4 py-2 border border-white/10 rounded-lg text-gray-300 hover:bg-white/5 text-sm font-medium transition-colors ml-3",
                        ),
                        rx.el.button(
                            "ارسال درخواست",
                            on_click=ParticipantBrowserState.send_request,
                            class_name="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium shadow-lg transition-all",
                        ),
                        class_name="flex justify-end border-t border-white/10 pt-4",
                    ),
                    class_name="bg-slate-900 border border-white/10 rounded-2xl shadow-2xl p-6 w-full max-w-lg relative",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[101] outline-none",
            ),
        ),
        open=ParticipantBrowserState.is_request_modal_open,
        on_open_change=ParticipantBrowserState.handle_modal_open_change,
    )


def participant_card(user: User) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                user["profile_picture"] != "",
                rx.image(
                    src=rx.get_upload_url(user["profile_picture"]),
                    class_name="h-20 w-20 rounded-full object-cover ring-2 ring-white/10 mx-auto mb-4",
                ),
                rx.el.div(
                    rx.icon("user", class_name="h-10 w-10 text-white"),
                    class_name="h-20 w-20 rounded-full bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center ring-2 ring-white/10 mx-auto mb-4",
                ),
            ),
            rx.el.h3(
                user["name"], class_name="text-lg font-bold text-white text-center mb-1"
            ),
            rx.el.div(
                class_name="w-8 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full mx-auto mb-4"
            ),
            rx.el.div(
                rx.cond(
                    user["share_education"] & (user["education_level"] != ""),
                    rx.el.div(
                        rx.icon(
                            "graduation-cap", class_name="h-4 w-4 text-cyan-400 ml-2"
                        ),
                        rx.el.span(
                            user["education_level"], class_name="text-sm text-gray-300"
                        ),
                        class_name="flex items-center mb-2",
                    ),
                ),
                rx.cond(
                    user["share_field_of_study"] & (user["field_of_study"] != ""),
                    rx.el.div(
                        rx.icon("book-open", class_name="h-4 w-4 text-cyan-400 ml-2"),
                        rx.el.span(
                            user["field_of_study"], class_name="text-sm text-gray-300"
                        ),
                        class_name="flex items-center mb-2",
                    ),
                ),
                rx.cond(
                    user["share_occupation"] & (user["occupation"] != ""),
                    rx.el.div(
                        rx.icon("briefcase", class_name="h-4 w-4 text-cyan-400 ml-2"),
                        rx.el.span(
                            user["occupation"], class_name="text-sm text-gray-300"
                        ),
                        class_name="flex items-center mb-2",
                    ),
                ),
                rx.cond(
                    user["share_age"] & (user["date_of_birth"] != ""),
                    rx.el.div(
                        rx.icon("calendar", class_name="h-4 w-4 text-cyan-400 ml-2"),
                        rx.el.span(
                            "تاریخ تولد: " + user["date_of_birth"],
                            class_name="text-sm text-gray-300",
                        ),
                        class_name="flex items-center mb-2",
                    ),
                ),
                class_name="space-y-1 mb-6 px-2",
            ),
            rx.el.button(
                rx.el.span("ارسال درخواست"),
                rx.icon("send", class_name="h-4 w-4 mr-2"),
                on_click=lambda: ParticipantBrowserState.open_request_modal(user["id"]),
                class_name="w-full py-2.5 px-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-cyan-500/30 text-cyan-300 hover:text-cyan-200 font-medium text-sm transition-all flex items-center justify-center group",
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-slate-900/60 backdrop-blur-md rounded-2xl p-6 border border-white/10 hover:border-cyan-500/20 transition-all hover:shadow-[0_0_20px_rgba(6,182,212,0.1)]",
    )


def participant_browser_view() -> rx.Component:
    input_class = "rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2"
    return rx.el.div(
        request_modal(),
        rx.el.div(
            rx.el.h2(
                "مرور شرکت\u200cکنندگان فعال",
                class_name="text-2xl font-bold text-white",
            ),
            rx.el.p(
                "یافتن شرکت\u200cکنندگان مناسب برای پژوهش\u200cهای شما",
                class_name="text-gray-400 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "سطح تحصیلات",
                    class_name="block text-xs font-medium text-gray-400 mb-1.5",
                ),
                rx.el.select(
                    rx.el.option("همه", value="All"),
                    rx.el.option("زیر دیپلم", value="Under Diploma"),
                    rx.el.option("دیپلم", value="Diploma"),
                    rx.el.option("کاردانی", value="Associate"),
                    rx.el.option("کارشناسی", value="Bachelor"),
                    rx.el.option("کارشناسی ارشد", value="Master"),
                    rx.el.option("دکتری", value="Ph.D."),
                    on_change=ParticipantBrowserState.set_filter_education,
                    class_name=input_class + " w-full",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "رشته تحصیلی",
                    class_name="block text-xs font-medium text-gray-400 mb-1.5",
                ),
                rx.el.input(
                    placeholder="جستجو...",
                    on_change=ParticipantBrowserState.set_filter_field_of_study,
                    class_name=input_class + " w-full",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "حداقل سن",
                    class_name="block text-xs font-medium text-gray-400 mb-1.5",
                ),
                rx.el.input(
                    type="number",
                    default_value=ParticipantBrowserState.filter_age_min,
                    on_change=ParticipantBrowserState.set_filter_age_min,
                    class_name=input_class + " w-full",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "حداکثر سن",
                    class_name="block text-xs font-medium text-gray-400 mb-1.5",
                ),
                rx.el.input(
                    type="number",
                    default_value=ParticipantBrowserState.filter_age_max,
                    on_change=ParticipantBrowserState.set_filter_age_max,
                    class_name=input_class + " w-full",
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 bg-slate-900/40 p-6 rounded-2xl border border-white/5",
        ),
        rx.cond(
            ParticipantBrowserState.filtered_participants.length() > 0,
            rx.el.div(
                rx.foreach(
                    ParticipantBrowserState.filtered_participants, participant_card
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("users", class_name="h-12 w-12 text-gray-500 mb-3"),
                    rx.el.h3(
                        "هیچ شرکت\u200cکننده\u200cای یافت نشد",
                        class_name="text-lg font-medium text-white",
                    ),
                    rx.el.p(
                        "با تغییر فیلترها دوباره تلاش کنید.",
                        class_name="text-gray-400 mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center py-16 bg-slate-900/60 backdrop-blur-md rounded-xl border-2 border-dashed border-white/10",
                )
            ),
        ),
        class_name="max-w-7xl mx-auto py-6",
    )