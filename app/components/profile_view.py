import reflex as rx
from app.states.auth_state import AuthState
from app.states.study_state import StudyState
from app.states.application_state import ApplicationState


def edit_profile_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-[100] animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "ویرایش پروفایل",
                            class_name="text-xl font-bold text-white mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "نام و نام خانوادگی",
                                class_name="block text-sm font-medium text-gray-300 mb-1.5",
                            ),
                            rx.el.input(
                                default_value=AuthState.editing_name,
                                on_change=AuthState.set_editing_name,
                                class_name="block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2.5",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "لغو",
                                    class_name="px-4 py-2 border border-white/10 rounded-lg text-gray-300 hover:bg-white/5 text-sm font-medium transition-colors ml-3",
                                    on_click=AuthState.close_edit_profile,
                                )
                            ),
                            rx.el.button(
                                "ذخیره تغییرات",
                                on_click=AuthState.save_profile,
                                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium shadow-lg transition-all",
                            ),
                            class_name="flex justify-end",
                        ),
                    ),
                    class_name="bg-slate-900 border border-white/10 rounded-2xl shadow-2xl p-6 w-full max-w-md relative",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[101] outline-none",
            ),
        ),
        open=AuthState.is_edit_profile_open,
        on_open_change=lambda open: rx.cond(
            open, AuthState.open_edit_profile, AuthState.close_edit_profile
        ),
    )


def stat_card(
    label: str, value: str, icon: str, color_class: str = "text-blue-400"
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color_class}"),
            class_name="p-3 bg-slate-950/50 rounded-xl border border-white/5",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-400"),
            rx.el.p(value, class_name="text-2xl font-bold text-white mt-1"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-6 bg-slate-900/60 backdrop-blur-sm rounded-2xl shadow-sm border border-white/10",
    )


def profile_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user", class_name="h-12 w-12 text-white"),
                class_name="h-24 w-24 rounded-full bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center ring-4 ring-white/20 shadow-lg",
            ),
            rx.el.div(
                rx.el.h1(
                    AuthState.current_user_name,
                    class_name="text-2xl font-bold text-white",
                ),
                rx.el.div(
                    rx.icon("mail", class_name="h-4 w-4 ml-2 text-gray-400"),
                    rx.el.p(AuthState.current_user_email, class_name="text-gray-300"),
                    class_name="flex items-center mt-1",
                ),
                rx.el.div(
                    rx.el.span(
                        rx.cond(
                            AuthState.current_user_role == "researcher",
                            "پژوهشگر",
                            "شرکت\u200cکننده",
                        ),
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/50 text-blue-200 mt-3 uppercase tracking-wide border border-blue-500/20",
                    )
                ),
                class_name="mr-6",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "ویرایش پروفایل",
            on_click=AuthState.open_edit_profile,
            class_name="px-4 py-2 border border-white/20 rounded-lg text-sm font-medium text-gray-200 hover:bg-white/10 transition-colors",
        ),
        class_name="flex flex-col sm:flex-row sm:items-center justify-between bg-slate-900/60 backdrop-blur-md p-8 rounded-2xl shadow-sm border border-white/10 mb-8 gap-4",
    )


def researcher_stats() -> rx.Component:
    return rx.el.div(
        rx.el.h3("داشبورد پژوهشگر", class_name="text-lg font-bold text-white mb-4"),
        rx.el.div(
            stat_card(
                "مطالعات فعال",
                StudyState.stats_active_studies.to_string(),
                "file-text",
                "text-blue-400",
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
            stat_card(
                "نرخ پاسخگویی",
                ApplicationState.stats_response_rate,
                "activity",
                "text-green-400",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
        ),
    )


def participant_stats() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "فعالیت شرکت\u200cکننده", class_name="text-lg font-bold text-white mb-4"
        ),
        rx.el.div(
            stat_card("درخواست\u200cهای ارسال شده", "۸", "send", "text-blue-400"),
            stat_card("پذیرفته شده", "۲", "check_check", "text-green-400"),
            stat_card("مشارکت کرده", "۱", "trophy", "text-yellow-400"),
            stat_card("درآمد", "۵۰ هزار تومان", "dollar-sign", "text-emerald-400"),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
        ),
    )


def profile_view() -> rx.Component:
    return rx.el.div(
        profile_header(),
        rx.cond(AuthState.is_researcher, researcher_stats(), participant_stats()),
        edit_profile_modal(),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )