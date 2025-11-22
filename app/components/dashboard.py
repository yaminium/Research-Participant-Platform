import reflex as rx
from typing import Any
from app.states.study_state import StudyState
from app.states.application_state import ApplicationState
from app.components.profile_view import stat_card


def dashboard_stats() -> rx.Component:
    return rx.el.div(
        rx.el.h3("نمای کلی", class_name="text-lg font-bold text-white mb-4"),
        rx.el.div(
            stat_card(
                "کل مطالعات",
                StudyState.stats_total_studies.to_string(),
                "file-text",
                "text-blue-400",
            ),
            stat_card(
                "مطالعات فعال",
                StudyState.stats_active_studies.to_string(),
                "activity",
                "text-green-400",
            ),
            stat_card(
                "کل درخواست\u200cها",
                ApplicationState.stats_total_applications.to_string(),
                "users",
                "text-purple-400",
            ),
            stat_card(
                "در انتظار بررسی",
                ApplicationState.stats_pending_applications.to_string(),
                "clock",
                "text-orange-400",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8",
        ),
    )


def dashboard_nav(current_tab: str) -> rx.Component:
    base_class = "px-4 py-2 font-medium text-sm rounded-md transition-colors relative"
    active_class = "bg-blue-900/50 text-blue-200 border border-blue-500/30"
    inactive_class = "text-gray-400 hover:text-white hover:bg-white/5"
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                "مطالعات من",
                href="/my-studies",
                class_name=f"{base_class} {(active_class if current_tab == 'my_studies' else inactive_class)}",
            ),
            rx.el.button(
                "ایجاد مطالعه جدید",
                on_click=StudyState.start_create_new,
                class_name=f"{base_class} {(active_class if current_tab == 'create_study' else inactive_class)}",
            ),
            rx.el.a(
                rx.el.span("درخواست\u2009ها"),
                rx.cond(
                    ApplicationState.researcher_applications.length() > 0,
                    rx.el.span(
                        ApplicationState.researcher_applications.length(),
                        class_name="mr-2 inline-flex items-center justify-center px-2 py-0.5 text-xs font-bold leading-none text-white bg-red-600 rounded-full",
                    ),
                ),
                href="/dashboard",
                class_name=f"{base_class} flex items-center {(active_class if current_tab == 'applications' else inactive_class)}",
            ),
            rx.el.a(
                "مرور شرکت\u2009کنندگان",
                href="/dashboard/participants",
                class_name=f"{base_class} {(active_class if current_tab == 'participants' else inactive_class)}",
            ),
            class_name="flex space-x-2",
        ),
        class_name="border-b border-white/10 mb-8 pb-2",
    )


def study_card(study: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    study["title"],
                    class_name="text-lg font-bold text-white line-clamp-1",
                ),
                rx.el.span(
                    rx.cond(study["status"] == "Open", "باز", "بسته"),
                    class_name=rx.cond(
                        study["status"] == "Open",
                        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-300 border border-green-500/20",
                        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-500/20",
                    ),
                ),
                class_name="flex justify-between items-start mb-2",
            ),
            rx.el.p(
                study["description"],
                class_name="text-gray-300 text-sm mb-4 line-clamp-2 h-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("users", class_name="h-4 w-4 text-gray-400 ml-1"),
                    rx.el.span(
                        f"{study['sample_size']} شرکت\u200cکننده نیاز است",
                        class_name="text-xs text-gray-400",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon("dollar-sign", class_name="h-4 w-4 text-gray-400 ml-1"),
                    rx.el.span(
                        study["compensation"], class_name="text-xs text-gray-400"
                    ),
                    class_name="flex items-center mt-1",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.icon("pencil", class_name="h-4 w-4 ml-1"),
                        "ویرایش",
                        class_name="flex items-center",
                    ),
                    on_click=lambda: StudyState.handle_edit_study(study["id"]),
                    class_name="flex-1 text-center px-3 py-2 border border-white/20 shadow-sm text-sm font-medium rounded-md text-gray-200 bg-white/5 hover:bg-white/10",
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon("trash-2", class_name="h-4 w-4 ml-1"),
                        "حذف",
                        class_name="flex items-center",
                    ),
                    on_click=lambda: StudyState.delete_study(study["id"]),
                    class_name="ml-3 flex-1 text-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-red-400 bg-red-900/20 hover:bg-red-900/30",
                ),
                class_name="flex justify-between",
            ),
            class_name="p-5 flex flex-col h-full",
        ),
        class_name="bg-slate-900/60 backdrop-blur-md rounded-xl shadow-sm border border-white/10 hover:border-white/20 transition-all overflow-hidden",
    )


def my_studies_list() -> rx.Component:
    return rx.el.div(
        dashboard_stats(),
        rx.el.div(
            rx.el.h2("مطالعات من", class_name="text-2xl font-bold text-white"),
            rx.el.button(
                rx.el.div(
                    rx.icon("plus", class_name="h-5 w-5 ml-2"),
                    "ایجاد مطالعه جدید",
                    class_name="flex items-center",
                ),
                on_click=StudyState.start_create_new,
                class_name="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            StudyState.my_studies.length() > 0,
            rx.el.div(
                rx.foreach(StudyState.my_studies, study_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("file-question", class_name="h-12 w-12 text-gray-500 mb-3"),
                    rx.el.h3(
                        "هنوز مطالعه\u200cای ندارید",
                        class_name="text-lg font-medium text-white",
                    ),
                    rx.el.p(
                        "با ایجاد اولین مطالعه پژوهشی خود شروع کنید.",
                        class_name="text-gray-400 mt-1",
                    ),
                    rx.el.button(
                        "ایجاد مطالعه",
                        on_click=StudyState.start_create_new,
                        class_name="mt-6 inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-blue-400 bg-blue-900/20 hover:bg-blue-900/30",
                    ),
                    class_name="flex flex-col items-center justify-center py-12 bg-slate-900/30 rounded-xl border-2 border-dashed border-white/10",
                )
            ),
        ),
        class_name="max-w-7xl mx-auto py-6",
    )