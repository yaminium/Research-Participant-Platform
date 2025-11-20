import reflex as rx
from app.states.application_state import ApplicationState
from app.models import Application


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Pending",
            rx.el.span(
                "در انتظار بررسی",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-900/30 text-yellow-300 border border-yellow-500/20",
            ),
        ),
        (
            "Contacted",
            rx.el.span(
                "تماس گرفته شد",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-900/30 text-blue-300 border border-blue-500/20",
            ),
        ),
        (
            "Accepted",
            rx.el.span(
                "پذیرفته شده",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-300 border border-green-500/20",
            ),
        ),
        (
            "Rejected",
            rx.el.span(
                "رد شده",
                class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-500/20",
            ),
        ),
        rx.el.span(
            status,
            class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300 border border-gray-600",
        ),
    )


def application_card(app: Application) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        app["participant_name"],
                        class_name="text-lg font-bold text-white",
                    ),
                    rx.el.p(
                        f"{app['age']} سال • {app['gender']}",
                        class_name="text-sm text-gray-400",
                    ),
                    class_name="mb-2",
                ),
                status_badge(app["status"]),
                class_name="flex justify-between items-start mb-3",
            ),
            rx.el.div(
                rx.el.p(
                    app["motivation_message"],
                    class_name="text-gray-300 text-sm bg-slate-950/30 p-3 rounded-lg italic mb-4 border border-white/5",
                ),
                rx.el.div(
                    rx.el.a(
                        rx.el.div(
                            rx.icon("mail", class_name="h-4 w-4 ml-2 text-gray-500"),
                            app["email"],
                            class_name="flex items-center text-sm text-gray-400 hover:text-blue-400 transition-colors",
                        ),
                        href=f"mailto:{app['email']}",
                    ),
                    rx.cond(
                        app["phone"] != "",
                        rx.el.div(
                            rx.icon("phone", class_name="h-4 w-4 ml-2 text-gray-500"),
                            app["phone"],
                            class_name="flex items-center text-sm text-gray-400 mt-1",
                        ),
                    ),
                    class_name="mb-4",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "تغییر وضعیت:",
                    class_name="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1 block",
                ),
                rx.el.select(
                    rx.el.option("در انتظار", value="Pending"),
                    rx.el.option("تماس گرفته شد", value="Contacted"),
                    rx.el.option("پذیرفته شده", value="Accepted"),
                    rx.el.option("رد شده", value="Rejected"),
                    value=app["status"],
                    on_change=lambda val: ApplicationState.update_application_status(
                        app["id"], val
                    ),
                    class_name="block w-full pl-3 pr-10 py-2 text-sm border-white/10 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md bg-slate-900 text-white shadow-sm cursor-pointer",
                ),
                class_name="mt-auto bg-slate-950/30 -mx-6 -mb-6 p-4 border-t border-white/5",
            ),
            class_name="p-6 flex flex-col h-full",
        ),
        class_name="bg-slate-900/60 backdrop-blur-md rounded-xl shadow-sm border border-white/10 hover:shadow-md transition-shadow overflow-hidden",
    )


def applications_view() -> rx.Component:
    input_class = "rounded-lg border-white/10 bg-slate-950/50 text-white shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm"
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "صندوق درخواست\u200cها", class_name="text-2xl font-bold text-white"
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("همه مطالعات", value="All"),
                    rx.foreach(
                        ApplicationState.researcher_studies_for_filter,
                        lambda s: rx.el.option(s["title"], value=s["id"]),
                    ),
                    value=ApplicationState.filter_study_id,
                    on_change=ApplicationState.set_filter_study_id,
                    class_name=f"{input_class} ml-4 min-w-[200px]",
                ),
                rx.el.select(
                    rx.el.option("همه وضعیت\u200cها", value="All"),
                    rx.el.option("در انتظار", value="Pending"),
                    rx.el.option("تماس گرفته شد", value="Contacted"),
                    rx.el.option("پذیرفته شده", value="Accepted"),
                    rx.el.option("رد شده", value="Rejected"),
                    value=ApplicationState.filter_status,
                    on_change=ApplicationState.set_filter_status,
                    class_name=input_class,
                ),
                class_name="flex items-center mt-4 md:mt-0",
            ),
            class_name="flex flex-col md:flex-row justify-between items-center mb-8",
        ),
        rx.cond(
            ApplicationState.researcher_applications.length() > 0,
            rx.el.div(
                rx.foreach(ApplicationState.researcher_applications, application_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("inbox", class_name="h-12 w-12 text-gray-500 mb-3"),
                    rx.el.h3(
                        "هیچ درخواستی یافت نشد",
                        class_name="text-lg font-medium text-white",
                    ),
                    rx.el.p(
                        "در انتظار ارسال درخواست شرکت\u200cکنندگان برای مطالعات شما.",
                        class_name="text-gray-400 mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center py-16 bg-slate-900/60 backdrop-blur-md rounded-xl border-2 border-dashed border-white/10",
                )
            ),
        ),
        class_name="max-w-7xl mx-auto px-4 py-8",
    )