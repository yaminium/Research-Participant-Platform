import reflex as rx
from app.states.auth_state import AuthState
from app.states.study_state import StudyState
from app.states.application_state import ApplicationState


def form_label(text: str) -> rx.Component:
    return rx.el.label(
        text, class_name="block text-xs font-medium text-gray-400 mb-1.5"
    )


def edit_profile_modal() -> rx.Component:
    input_class = "block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2.5"
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
                            class_name="text-xl font-bold text-white mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                form_label("تصویر پروفایل"),
                                rx.el.div(
                                    rx.cond(
                                        AuthState.editing_profile_picture != "",
                                        rx.image(
                                            src=rx.get_upload_url(
                                                AuthState.editing_profile_picture
                                            ),
                                            class_name="h-20 w-20 rounded-full object-cover border-2 border-white/10",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "user",
                                                class_name="h-10 w-10 text-gray-400",
                                            ),
                                            class_name="h-20 w-20 rounded-full bg-slate-800 flex items-center justify-center border-2 border-white/10",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.upload.root(
                                            rx.el.button(
                                                "انتخاب تصویر",
                                                class_name="w-full px-3 py-1.5 text-xs font-medium text-blue-300 bg-blue-900/20 border border-blue-500/20 rounded-lg hover:bg-blue-900/30 transition-colors",
                                            ),
                                            id="upload_profile_pic",
                                            max_files=1,
                                            accept={
                                                "image/png": [".png"],
                                                "image/jpeg": [".jpg", ".jpeg"],
                                                "image/webp": [".webp"],
                                            },
                                        ),
                                        rx.el.button(
                                            "آپلود",
                                            on_click=AuthState.handle_profile_picture_upload(
                                                rx.upload_files(
                                                    upload_id="upload_profile_pic"
                                                )
                                            ),
                                            class_name="w-full mt-2 px-3 py-1.5 text-xs font-medium text-green-300 bg-green-900/20 border border-green-500/20 rounded-lg hover:bg-green-900/30 transition-colors",
                                        ),
                                        class_name="flex flex-col w-32",
                                    ),
                                    class_name="flex items-center gap-4",
                                ),
                                class_name="mb-6 p-4 bg-slate-950/30 rounded-xl border border-white/5",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    form_label("نام و نام خانوادگی"),
                                    rx.el.input(
                                        default_value=AuthState.editing_name,
                                        on_change=AuthState.set_editing_name,
                                        class_name=input_class,
                                    ),
                                ),
                                rx.el.div(
                                    form_label("شماره تماس"),
                                    rx.el.input(
                                        default_value=AuthState.editing_phone_number,
                                        on_change=AuthState.set_editing_phone_number,
                                        placeholder="0912...",
                                        class_name=input_class,
                                    ),
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    form_label("تاریخ تولد"),
                                    rx.el.input(
                                        type="date",
                                        default_value=AuthState.editing_date_of_birth,
                                        on_change=AuthState.set_editing_date_of_birth,
                                        class_name=input_class,
                                    ),
                                ),
                                rx.el.div(
                                    form_label("سطح تحصیلات"),
                                    rx.el.select(
                                        rx.el.option("انتخاب کنید", value=""),
                                        rx.el.option(
                                            "زیر دیپلم", value="Under Diploma"
                                        ),
                                        rx.el.option("دیپلم", value="Diploma"),
                                        rx.el.option("کاردانی", value="Associate"),
                                        rx.el.option("کارشناسی", value="Bachelor"),
                                        rx.el.option("کارشناسی ارشد", value="Master"),
                                        rx.el.option("دکتری", value="Ph.D."),
                                        value=AuthState.editing_education_level,
                                        on_change=AuthState.set_editing_education_level,
                                        class_name=input_class,
                                    ),
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    form_label("رشته تحصیلی"),
                                    rx.el.input(
                                        default_value=AuthState.editing_field_of_study,
                                        on_change=AuthState.set_editing_field_of_study,
                                        placeholder="مثال: روانشناسی",
                                        class_name=input_class,
                                    ),
                                ),
                                rx.el.div(
                                    form_label("شغل"),
                                    rx.el.input(
                                        default_value=AuthState.editing_occupation,
                                        on_change=AuthState.set_editing_occupation,
                                        placeholder="مثال: دانشجو",
                                        class_name=input_class,
                                    ),
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                            ),
                            rx.cond(
                                AuthState.is_participant,
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.h4(
                                            "وضعیت شرکت\u2009کننده",
                                            class_name="text-sm font-bold text-blue-400 mb-4 border-b border-white/10 pb-2",
                                        ),
                                        rx.el.div(
                                            rx.el.label(
                                                rx.el.input(
                                                    type="radio",
                                                    name="status",
                                                    value="فعال",
                                                    checked=AuthState.editing_participant_status
                                                    == "فعال",
                                                    on_change=lambda: AuthState.set_editing_participant_status(
                                                        "فعال"
                                                    ),
                                                    class_name="sr-only peer",
                                                ),
                                                rx.el.div(
                                                    rx.icon(
                                                        "eye",
                                                        class_name="h-5 w-5 mb-1 peer-checked:text-green-400 text-gray-400",
                                                    ),
                                                    rx.el.span(
                                                        "فعال",
                                                        class_name="text-sm font-medium peer-checked:text-white text-gray-400",
                                                    ),
                                                    rx.el.span(
                                                        "قابل مشاهده برای پژوهشگران",
                                                        class_name="text-[10px] peer-checked:text-gray-300 text-gray-500",
                                                    ),
                                                    class_name="flex flex-col items-center justify-center p-3 bg-slate-950/30 border border-white/10 rounded-xl cursor-pointer peer-checked:border-green-500/50 peer-checked:bg-green-900/10 transition-all",
                                                ),
                                                class_name="cursor-pointer",
                                            ),
                                            rx.el.label(
                                                rx.el.input(
                                                    type="radio",
                                                    name="status",
                                                    value="غیر فعال",
                                                    checked=AuthState.editing_participant_status
                                                    == "غیر فعال",
                                                    on_change=lambda: AuthState.set_editing_participant_status(
                                                        "غیر فعال"
                                                    ),
                                                    class_name="sr-only peer",
                                                ),
                                                rx.el.div(
                                                    rx.icon(
                                                        "eye-off",
                                                        class_name="h-5 w-5 mb-1 peer-checked:text-gray-300 text-gray-400",
                                                    ),
                                                    rx.el.span(
                                                        "غیر فعال",
                                                        class_name="text-sm font-medium peer-checked:text-white text-gray-400",
                                                    ),
                                                    rx.el.span(
                                                        "پنهان از پژوهشگران",
                                                        class_name="text-[10px] peer-checked:text-gray-300 text-gray-500",
                                                    ),
                                                    class_name="flex flex-col items-center justify-center p-3 bg-slate-950/30 border border-white/10 rounded-xl cursor-pointer peer-checked:border-gray-500/50 peer-checked:bg-gray-800/20 transition-all",
                                                ),
                                                class_name="cursor-pointer",
                                            ),
                                            class_name="grid grid-cols-2 gap-4 mb-6",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.h4(
                                            "تنظیمات حریم خصوصی",
                                            class_name="text-sm font-bold text-blue-400 mb-4 border-b border-white/10 pb-2",
                                        ),
                                        rx.el.div(
                                            rx.el.label(
                                                rx.el.input(
                                                    type="checkbox",
                                                    checked=AuthState.editing_share_education,
                                                    on_change=AuthState.toggle_editing_share_education,
                                                    class_name="rounded border-gray-600 bg-slate-800 text-cyan-500 focus:ring-cyan-500/40 mr-2",
                                                ),
                                                rx.el.span(
                                                    "نمایش سطح تحصیلات",
                                                    class_name="text-sm text-gray-300 mr-2",
                                                ),
                                                class_name="flex items-center mb-2",
                                            ),
                                            rx.el.label(
                                                rx.el.input(
                                                    type="checkbox",
                                                    checked=AuthState.editing_share_age,
                                                    on_change=AuthState.toggle_editing_share_age,
                                                    class_name="rounded border-gray-600 bg-slate-800 text-cyan-500 focus:ring-cyan-500/40 mr-2",
                                                ),
                                                rx.el.span(
                                                    "نمایش سن",
                                                    class_name="text-sm text-gray-300 mr-2",
                                                ),
                                                class_name="flex items-center mb-2",
                                            ),
                                            rx.el.label(
                                                rx.el.input(
                                                    type="checkbox",
                                                    checked=AuthState.editing_share_occupation,
                                                    on_change=AuthState.toggle_editing_share_occupation,
                                                    class_name="rounded border-gray-600 bg-slate-800 text-cyan-500 focus:ring-cyan-500/40 mr-2",
                                                ),
                                                rx.el.span(
                                                    "نمایش شغل",
                                                    class_name="text-sm text-gray-300 mr-2",
                                                ),
                                                class_name="flex items-center mb-2",
                                            ),
                                            rx.el.label(
                                                rx.el.input(
                                                    type="checkbox",
                                                    checked=AuthState.editing_share_field_of_study,
                                                    on_change=AuthState.toggle_editing_share_field_of_study,
                                                    class_name="rounded border-gray-600 bg-slate-800 text-cyan-500 focus:ring-cyan-500/40 mr-2",
                                                ),
                                                rx.el.span(
                                                    "نمایش رشته تحصیلی",
                                                    class_name="text-sm text-gray-300 mr-2",
                                                ),
                                                class_name="flex items-center",
                                            ),
                                            class_name="bg-slate-950/30 p-4 rounded-xl border border-white/5 mb-8",
                                        ),
                                    ),
                                ),
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
                                    class_name="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium shadow-lg transition-all",
                                ),
                                class_name="flex justify-end border-t border-white/10 pt-6",
                            ),
                        ),
                    ),
                    class_name="bg-slate-900 border border-white/10 rounded-2xl shadow-2xl p-6 w-full max-w-2xl relative max-h-[90vh] overflow-y-auto custom-scrollbar",
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
                rx.cond(
                    AuthState.current_user["profile_picture"] != "",
                    rx.image(
                        src=rx.get_upload_url(
                            AuthState.current_user["profile_picture"]
                        ),
                        class_name="h-24 w-24 rounded-full object-cover ring-4 ring-white/20 shadow-lg",
                    ),
                    rx.el.div(
                        rx.icon("user", class_name="h-12 w-12 text-white"),
                        class_name="h-24 w-24 rounded-full bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center ring-4 ring-white/20 shadow-lg",
                    ),
                ),
                class_name="relative",
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
                rx.cond(
                    AuthState.current_user["phone_number"] != "",
                    rx.el.div(
                        rx.icon("phone", class_name="h-4 w-4 ml-2 text-gray-400"),
                        rx.el.p(
                            AuthState.current_user["phone_number"],
                            class_name="text-gray-300",
                        ),
                        class_name="flex items-center mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.span(
                        rx.cond(
                            AuthState.current_user_role == "researcher",
                            "پژوهشگر",
                            "شرکت\u2009کننده",
                        ),
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/50 text-blue-200 mt-3 uppercase tracking-wide border border-blue-500/20",
                    ),
                    rx.cond(
                        AuthState.is_participant,
                        rx.el.span(
                            rx.cond(
                                AuthState.current_user["participant_status"] == "فعال",
                                "فعال",
                                "غیر فعال",
                            ),
                            class_name=rx.cond(
                                AuthState.current_user["participant_status"] == "فعال",
                                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-300 mt-3 mr-2 border border-green-500/20",
                                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-700 text-gray-400 mt-3 mr-2 border border-gray-600",
                            ),
                        ),
                    ),
                    rx.cond(
                        AuthState.current_user["education_level"] != "",
                        rx.el.span(
                            AuthState.current_user["education_level"],
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-900/50 text-purple-200 mt-3 mr-2 border border-purple-500/20",
                        ),
                    ),
                    rx.cond(
                        AuthState.current_user["occupation"] != "",
                        rx.el.span(
                            AuthState.current_user["occupation"],
                            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-gray-300 mt-3 mr-2 border border-white/10",
                        ),
                    ),
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


def request_card(req: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    req["study_title"],
                    class_name="text-lg font-bold text-white mb-1 line-clamp-1",
                ),
                rx.el.div(
                    rx.icon("user", class_name="h-4 w-4 text-cyan-400"),
                    rx.el.span(
                        req["researcher_name"], class_name="text-sm text-gray-300"
                    ),
                    class_name="flex items-center gap-2 mb-3",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.cond(
                    req["status"] == "Pending",
                    rx.el.span(
                        "در انتظار پاسخ",
                        class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-yellow-500/10 text-yellow-500 border border-yellow-500/20",
                    ),
                    rx.cond(
                        req["status"] == "Accepted",
                        rx.el.span(
                            "پذیرفته شده",
                            class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-green-500/10 text-green-500 border border-green-500/20",
                        ),
                        rx.el.span(
                            "رد شده",
                            class_name="px-2.5 py-1 rounded-full text-xs font-medium bg-red-500/10 text-red-500 border border-red-500/20",
                        ),
                    ),
                ),
                class_name="flex-shrink-0 ml-4",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.p(
                req["message"],
                class_name="text-sm text-gray-400 bg-slate-950/50 p-3 rounded-lg border border-white/5 mb-4",
            ),
            rx.cond(
                req["status"] == "Pending",
                rx.el.div(
                    rx.el.button(
                        "رد کردن",
                        on_click=lambda: AuthState.respond_to_request(
                            req["id"], "Rejected"
                        ),
                        class_name="flex-1 py-2 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500/10 text-sm font-medium transition-colors",
                    ),
                    rx.el.button(
                        "پذیرفتن",
                        on_click=lambda: AuthState.respond_to_request(
                            req["id"], "Accepted"
                        ),
                        class_name="flex-1 py-2 rounded-lg bg-green-600 hover:bg-green-700 text-white text-sm font-medium shadow-lg shadow-green-900/20 transition-all",
                    ),
                    class_name="flex gap-3",
                ),
            ),
            class_name="mt-2",
        ),
        class_name="bg-slate-900/60 backdrop-blur-md rounded-2xl p-5 border border-white/10 hover:border-cyan-500/20 transition-all hover:shadow-[0_0_20px_rgba(6,182,212,0.1)]",
    )


def requests_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "درخواست\u2009های دریافتی",
            class_name="text-lg font-bold text-white mb-4 flex items-center gap-2",
        ),
        rx.cond(
            AuthState.participant_enriched_requests.length() > 0,
            rx.el.div(
                rx.foreach(AuthState.participant_enriched_requests, request_card),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.el.div(
                rx.icon("inbox", class_name="h-12 w-12 text-gray-600 mb-3"),
                rx.el.p("هیچ درخواستی دریافت نشده است.", class_name="text-gray-500"),
                class_name="flex flex-col items-center justify-center py-12 bg-slate-900/30 rounded-2xl border border-white/5 border-dashed",
            ),
        ),
        class_name="mt-8",
    )


def participant_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "فعالیت شرکت\u2009کننده", class_name="text-lg font-bold text-white mb-4"
            ),
            rx.el.div(
                stat_card("درخواست\u2009های ارسال شده", "۸", "send", "text-blue-400"),
                stat_card("پذیرفته شده", "۲", "check_check", "text-green-400"),
                stat_card("مشارکت کرده", "۱", "trophy", "text-yellow-400"),
                stat_card("درآمد", "۵۰ هزار تومان", "dollar-sign", "text-emerald-400"),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4",
            ),
        ),
        requests_section(),
    )


def profile_view() -> rx.Component:
    return rx.el.div(
        profile_header(),
        rx.cond(AuthState.is_researcher, researcher_stats(), participant_dashboard()),
        edit_profile_modal(),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
    )