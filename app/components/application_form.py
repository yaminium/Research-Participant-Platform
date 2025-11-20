import reflex as rx
from app.states.application_state import ApplicationState


def form_input(
    label: str,
    value: str,
    on_change: rx.event.EventType,
    type_: str = "text",
    required: bool = False,
    placeholder: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            rx.el.span(label, class_name="text-sm font-medium text-gray-300"),
            rx.cond(required, rx.el.span(" *", class_name="text-red-500")),
            class_name="block mb-1.5",
        ),
        rx.el.input(
            type=type_,
            default_value=value,
            on_change=on_change,
            placeholder=placeholder,
            class_name="block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2.5",
        ),
        class_name="mb-4",
    )


def application_form() -> rx.Component:
    input_class = "block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm py-2.5"
    return rx.el.div(
        rx.cond(
            ApplicationState.form_success,
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "check_check",
                        class_name="h-12 w-12 text-green-400 mx-auto mb-4",
                    ),
                    rx.el.h3(
                        "درخواست ارسال شد!",
                        class_name="text-xl font-bold text-white text-center",
                    ),
                    rx.el.p(
                        "پژوهشگر درخواست شما را دریافت کرده و به زودی با شما تماس خواهد گرفت.",
                        class_name="text-gray-400 text-center mt-2",
                    ),
                    rx.el.button(
                        "بستن",
                        on_click=ApplicationState.close_modal,
                        class_name="mt-6 w-full py-2.5 bg-white/10 text-gray-200 font-semibold rounded-lg hover:bg-white/20 transition-colors",
                    ),
                    class_name="py-8",
                )
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "درخواست شرکت در مطالعه",
                        class_name="text-xl font-bold text-white",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x", class_name="h-5 w-5 text-gray-400 hover:text-white"
                        ),
                        on_click=ApplicationState.close_modal,
                    ),
                    class_name="flex justify-between items-center mb-6 border-b border-white/10 pb-4",
                ),
                rx.el.div(
                    form_input(
                        "نام و نام خانوادگی",
                        ApplicationState.form_name,
                        ApplicationState.set_form_name,
                        required=True,
                        placeholder="نام شما",
                    ),
                    rx.el.div(
                        form_input(
                            "سن",
                            ApplicationState.form_age,
                            ApplicationState.set_form_age,
                            type_="number",
                            required=True,
                            placeholder="مثال: ۲۵",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "جنسیت",
                                class_name="block text-sm font-medium text-gray-300 mb-1.5",
                            ),
                            rx.el.select(
                                rx.el.option("مرد", value="Male"),
                                rx.el.option("زن", value="Female"),
                                rx.el.option("سایر", value="Other"),
                                rx.el.option(
                                    "ترجیح می\u200cدهم نگویم", value="Prefer not to say"
                                ),
                                value=ApplicationState.form_gender,
                                on_change=ApplicationState.set_form_gender,
                                class_name=input_class,
                            ),
                            class_name="mb-4",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        form_input(
                            "آدرس ایمیل",
                            ApplicationState.form_email,
                            ApplicationState.set_form_email,
                            type_="email",
                            required=True,
                            placeholder="you@example.com",
                        ),
                        form_input(
                            "شماره تلفن (اختیاری)",
                            ApplicationState.form_phone,
                            ApplicationState.set_form_phone,
                            type_="tel",
                            placeholder="0912...",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.span(
                                "پیام انگیزه",
                                class_name="text-sm font-medium text-gray-300",
                            ),
                            rx.el.span(" *", class_name="text-red-500"),
                            class_name="block mb-1.5",
                        ),
                        rx.el.textarea(
                            default_value=ApplicationState.form_motivation,
                            on_change=ApplicationState.set_form_motivation,
                            rows=4,
                            placeholder="چرا می\u200cخواهید در این مطالعه شرکت کنید؟",
                            class_name="block w-full rounded-lg border-white/10 bg-slate-950/50 text-white placeholder-gray-500 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm",
                        ),
                        class_name="mb-6",
                    ),
                    rx.cond(
                        ApplicationState.form_error != "",
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-4 w-4 ml-2"),
                            ApplicationState.form_error,
                            class_name="bg-red-900/30 text-red-200 p-3 rounded-lg flex items-center text-sm mb-6 border border-red-800/50",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "لغو",
                            on_click=ApplicationState.close_modal,
                            class_name="px-5 py-2.5 border border-white/20 text-gray-200 font-medium rounded-lg hover:bg-white/10 transition-colors ml-3",
                        ),
                        rx.el.button(
                            "ارسال درخواست",
                            on_click=ApplicationState.submit_application,
                            class_name="px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 shadow-md hover:shadow-lg transition-all",
                        ),
                        class_name="flex justify-end",
                    ),
                ),
            ),
        ),
        class_name="bg-slate-900/90 backdrop-blur-md border border-white/10 rounded-2xl shadow-xl max-w-2xl w-full p-6 m-4 relative animate-in fade-in zoom-in duration-200",
    )