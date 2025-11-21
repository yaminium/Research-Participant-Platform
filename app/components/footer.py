import reflex as rx
from app.states.info_modal_state import InfoModalState


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "© ۱۴۰۳ نورو ریکروت. تمامی حقوق محفوظ است.",
                        class_name="text-gray-500 text-sm",
                    )
                ),
                rx.el.div(
                    rx.el.button(
                        "درباره ما و پشتیبانی",
                        on_click=InfoModalState.set_open(True),
                        class_name="text-gray-400 hover:text-white text-sm font-medium transition-colors mr-6 hover:underline underline-offset-4 decoration-blue-500/50",
                    ),
                    rx.el.a(
                        "قوانین و مقررات",
                        href="/terms",
                        class_name="text-gray-400 hover:text-white text-sm font-medium transition-colors mr-6 hover:underline underline-offset-4 decoration-blue-500/50",
                    ),
                    rx.el.a(
                        "حریم خصوصی",
                        href="/privacy",
                        class_name="text-gray-400 hover:text-white text-sm font-medium transition-colors hover:underline underline-offset-4 decoration-blue-500/50",
                    ),
                    class_name="flex flex-wrap items-center justify-center gap-y-2 mt-4 md:mt-0",
                ),
                class_name="flex flex-col md:flex-row justify-between items-center gap-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 border-t border-white/5",
        ),
        class_name="bg-slate-950/50 w-full mt-auto backdrop-blur-sm",
    )