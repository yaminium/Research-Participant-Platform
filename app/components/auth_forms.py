import reflex as rx
import reflex_google_auth
import os
from app.states.auth_state import AuthState


def form_input(
    label: str,
    placeholder: str,
    type_: str,
    on_change: rx.event.EventType,
    value: str | None = None,
    icon: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-200 mb-1.5"),
        rx.el.div(
            rx.icon(
                icon,
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
            ),
            rx.el.input(
                placeholder=placeholder,
                type=type_,
                on_change=on_change,
                default_value=value,
                class_name="block w-full pl-10 pr-3 py-2.5 border border-white/10 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-white bg-slate-950/50 placeholder-gray-500 transition-all sm:text-sm",
            ),
            class_name="relative",
        ),
        class_name="w-full",
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("brain-circuit", class_name="h-10 w-10 text-blue-500 mb-4"),
                rx.el.h2("خوش آمدید", class_name="text-2xl font-bold text-white"),
                rx.el.p(
                    "برای ادامه وارد حساب کاربری خود شوید",
                    class_name="text-gray-400 mt-2 text-sm",
                ),
                class_name="text-center mb-8 flex flex-col items-center",
            ),
            rx.el.form(
                rx.el.div(
                    form_input(
                        "آدرس ایمیل",
                        "you@example.com",
                        "email",
                        AuthState.handle_login_email_change,
                        icon="mail",
                    ),
                    form_input(
                        "رمز عبور",
                        "••••••••",
                        "password",
                        AuthState.handle_login_password_change,
                        icon="lock",
                    ),
                    class_name="space-y-5",
                ),
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        rx.icon("circle-alert", class_name="h-4 w-4 ml-2"),
                        AuthState.login_error,
                        class_name="flex items-center p-3 mt-4 text-sm text-red-200 bg-red-900/30 rounded-lg border border-red-800/50",
                    ),
                ),
                rx.el.button(
                    "ورود",
                    type="button",
                    on_click=AuthState.login,
                    class_name="w-full mt-6 flex justify-center py-2.5 px-4 border border-transparent rounded-full shadow-sm text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all hover:shadow-lg",
                ),
                class_name="mt-8",
            ),
            rx.el.div(
                rx.el.span("حساب کاربری ندارید؟ ", class_name="text-gray-400"),
                rx.el.a(
                    "ثبت نام کنید",
                    href="/register",
                    class_name="font-semibold text-blue-400 hover:text-blue-300",
                ),
                class_name="mt-6 text-center text-sm",
            ),
            class_name="bg-slate-900/70 backdrop-blur-md py-10 px-6 shadow-xl rounded-2xl border border-white/10 w-full max-w-md",
        ),
        class_name="min-h-[80vh] flex items-center justify-center px-4",
    )


def register_form() -> rx.Component:
    google_client_id = os.getenv("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
    show_google_auth = (
        google_client_id != "YOUR_CLIENT_ID_HERE" and google_client_id != ""
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user-plus", class_name="h-10 w-10 text-blue-500 mb-4"),
                rx.el.h2(
                    "ایجاد حساب کاربری", class_name="text-2xl font-bold text-white"
                ),
                rx.el.p(
                    "همین امروز به جامعه پژوهشی بپیوندید",
                    class_name="text-gray-400 mt-2 text-sm",
                ),
                class_name="text-center mb-8 flex flex-col items-center",
            ),
            rx.el.div(
                rx.cond(
                    show_google_auth,
                    rx.el.div(
                        reflex_google_auth.google_oauth_provider(
                            reflex_google_auth.google_login(
                                on_success=AuthState.on_google_login,
                                width="100%",
                                theme="filled_blue",
                                class_name="w-full",
                            ),
                            client_id=google_client_id,
                        ),
                        rx.el.div(
                            rx.el.div(class_name="h-px bg-white/10 w-full"),
                            rx.el.span(
                                "یا",
                                class_name="px-4 text-xs text-gray-500 uppercase font-medium",
                            ),
                            rx.el.div(class_name="h-px bg-white/10 w-full"),
                            class_name="flex items-center justify-between my-8",
                        ),
                        class_name="w-full",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    form_input(
                        "نام و نام خانوادگی",
                        "علی رضایی",
                        "text",
                        AuthState.set_reg_name,
                        icon="user",
                    ),
                    form_input(
                        "آدرس ایمیل",
                        "you@example.com",
                        "email",
                        AuthState.set_reg_email,
                        icon="mail",
                    ),
                    class_name="space-y-5",
                ),
                rx.el.div(
                    form_input(
                        "رمز عبور",
                        "رمز عبور خود را وارد کنید",
                        "password",
                        AuthState.set_reg_password,
                        icon="lock",
                    ),
                    form_input(
                        "تکرار رمز عبور",
                        "رمز عبور را تکرار کنید",
                        "password",
                        AuthState.set_reg_confirm_password,
                        icon="lock",
                    ),
                    class_name="space-y-5 mt-5",
                ),
                rx.el.div(
                    rx.el.label(
                        "من یک ... هستم",
                        class_name="block text-sm font-medium text-gray-200 mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="role",
                                value="participant",
                                checked=AuthState.reg_role == "participant",
                                on_change=lambda: AuthState.set_reg_role("participant"),
                                class_name="sr-only peer",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "users",
                                    class_name="h-6 w-6 mb-2 text-gray-400 peer-checked:text-blue-500",
                                ),
                                rx.el.span(
                                    "شرکت\u200cکننده",
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.span(
                                    "می\u200cخواهم در مطالعات شرکت کنم",
                                    class_name="text-xs text-gray-400 mt-1",
                                ),
                                class_name="flex flex-col items-center justify-center p-4 bg-slate-950/30 border-2 border-white/10 rounded-xl cursor-pointer transition-all hover:bg-white/5 peer-checked:border-blue-600 peer-checked:bg-blue-900/20",
                            ),
                            class_name="cursor-pointer w-full",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="role",
                                value="researcher",
                                checked=AuthState.reg_role == "researcher",
                                on_change=lambda: AuthState.set_reg_role("researcher"),
                                class_name="sr-only peer",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "microscope",
                                    class_name="h-6 w-6 mb-2 text-gray-400 peer-checked:text-blue-500",
                                ),
                                rx.el.span(
                                    "پژوهشگر",
                                    class_name="text-sm font-semibold text-white",
                                ),
                                rx.el.span(
                                    "می\u200cخواهم شرکت\u200cکننده جذب کنم",
                                    class_name="text-xs text-gray-400 mt-1",
                                ),
                                class_name="flex flex-col items-center justify-center p-4 bg-slate-950/30 border-2 border-white/10 rounded-xl cursor-pointer transition-all hover:bg-white/5 peer-checked:border-blue-600 peer-checked:bg-blue-900/20",
                            ),
                            class_name="cursor-pointer w-full",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    class_name="mt-6",
                ),
                rx.cond(
                    AuthState.reg_error != "",
                    rx.el.div(
                        rx.icon("circle-alert", class_name="h-4 w-4 ml-2"),
                        AuthState.reg_error,
                        class_name="flex items-center p-3 mt-6 text-sm text-red-200 bg-red-900/30 rounded-lg border border-red-800/50",
                    ),
                ),
                rx.el.button(
                    "ایجاد حساب کاربری",
                    on_click=AuthState.register,
                    class_name="w-full mt-8 flex justify-center py-3 px-4 border border-transparent rounded-full shadow-md text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all hover:shadow-xl",
                ),
                class_name="mt-2",
            ),
            rx.el.div(
                rx.el.span(
                    "قبلاً ثبت\u200cنام کرده\u200cاید؟ ", class_name="text-gray-400"
                ),
                rx.el.a(
                    "وارد شوید",
                    href="/login",
                    class_name="font-semibold text-blue-400 hover:text-blue-300",
                ),
                class_name="mt-6 text-center text-sm",
            ),
            class_name="bg-slate-900/70 backdrop-blur-md py-10 px-8 shadow-xl rounded-2xl border border-white/10 w-full max-w-lg",
        ),
        class_name="min-h-[80vh] flex items-center justify-center px-4 py-12",
    )