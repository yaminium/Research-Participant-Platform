import reflex as rx
from app.states.info_modal_state import InfoModalState


def faq_item(question: str, answer: str) -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            question,
            class_name="font-medium text-gray-800 cursor-pointer py-3 list-none flex items-center justify-between hover:text-pink-700 transition-colors",
        ),
        rx.el.p(
            answer,
            class_name="text-gray-600 text-sm mt-1 mb-4 leading-relaxed pr-4 border-r-2 border-pink-200 mr-1",
        ),
        class_name="border-b border-pink-200/60 last:border-0",
    )


def info_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-[9999] animate-in fade-in duration-200"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.radix.primitives.dialog.title(
                                "درباره نورو ریکروت",
                                class_name="text-2xl font-bold text-pink-900",
                            ),
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    rx.icon("x", class_name="h-5 w-5 text-pink-800"),
                                    class_name="p-2 rounded-full hover:bg-pink-200/50 transition-colors",
                                )
                            ),
                            class_name="flex justify-between items-start mb-2",
                        ),
                        rx.radix.primitives.dialog.description(
                            "پلتفرم پیشرو در جذب شرکت\u200cکنندگان برای پژوهش\u200cهای علوم شناختی",
                            class_name="text-sm text-pink-700 mb-6 font-medium",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "درباره ما",
                                    class_name="text-lg font-bold text-pink-900 mb-3 flex items-center gap-2",
                                ),
                                rx.el.p(
                                    "نورو ریکروت پلی است میان پژوهشگران علوم اعصاب و روانشناسی و علاقه\u200cمندان به مشارکت در پیشرفت علم. ما فرآیند جذب نیرو را ساده، سریع و هدفمند می\u200cکنیم. هدف ما تسریع اکتشافات علمی با تسهیل ارتباطات پژوهشی است.",
                                    class_name="text-gray-700 leading-relaxed text-sm text-justify",
                                ),
                                class_name="mb-8 bg-white/40 p-4 rounded-2xl border border-white/50 shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "وابستگی\u200cهای دانشگاهی",
                                    class_name="text-lg font-bold text-pink-900 mb-3",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.icon(
                                            "university",
                                            class_name="h-8 w-8 text-pink-600 mb-2",
                                        ),
                                        rx.el.span(
                                            "دانشگاه تهران",
                                            class_name="font-bold text-gray-800 text-sm",
                                        ),
                                        rx.el.span(
                                            "دانشکده روانشناسی",
                                            class_name="text-xs text-gray-500 mt-1",
                                        ),
                                        class_name="flex flex-col items-center text-center p-4 bg-white/60 rounded-xl border border-white/60 shadow-sm hover:shadow-md transition-shadow",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "brain",
                                            class_name="h-8 w-8 text-pink-600 mb-2",
                                        ),
                                        rx.el.span(
                                            "علوم شناختی",
                                            class_name="font-bold text-gray-800 text-sm",
                                        ),
                                        rx.el.span(
                                            "مرکز پژوهش\u200cهای مغز",
                                            class_name="text-xs text-gray-500 mt-1",
                                        ),
                                        class_name="flex flex-col items-center text-center p-4 bg-white/60 rounded-xl border border-white/60 shadow-sm hover:shadow-md transition-shadow",
                                    ),
                                    class_name="grid grid-cols-2 gap-4",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "سوالات متداول",
                                    class_name="text-lg font-bold text-pink-900 mb-3",
                                ),
                                rx.el.div(
                                    faq_item(
                                        "چگونه می\u200cتوانم در مطالعات شرکت کنم؟",
                                        "کافیست ثبت\u200cنام کنید و در بخش مرور مطالعات، پروژه\u200cهای متناسب با شرایط خود را پیدا کنید.",
                                    ),
                                    faq_item(
                                        "آیا پاداش دریافت می\u200cکنم؟",
                                        "بله، اکثر مطالعات دارای پاداش نقدی یا امتیاز دانشگاهی هستند که در توضیحات ذکر شده است.",
                                    ),
                                    faq_item(
                                        "آیا اطلاعات من محرمانه است؟",
                                        "بله، تمامی اطلاعات شما طبق اصول اخلاقی پژوهش و قوانین حریم خصوصی کاملاً محرمانه باقی می\u200cماند.",
                                    ),
                                    class_name="space-y-1 bg-white/40 p-4 rounded-2xl border border-white/50",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    "پشتیبانی",
                                    class_name="text-lg font-bold text-pink-900 mb-3",
                                ),
                                rx.el.div(
                                    rx.el.a(
                                        rx.el.div(
                                            rx.icon(
                                                "mail",
                                                class_name="h-5 w-5 text-pink-600 ml-2",
                                            ),
                                            "support@neurorecruit.ir",
                                            class_name="flex items-center",
                                        ),
                                        href="mailto:support@neurorecruit.ir",
                                        class_name="flex items-center justify-between text-gray-700 hover:text-pink-700 transition-colors mb-3 p-2 hover:bg-pink-50 rounded-lg",
                                    ),
                                    rx.el.a(
                                        rx.el.div(
                                            rx.icon(
                                                "phone",
                                                class_name="h-5 w-5 text-pink-600 ml-2",
                                            ),
                                            "۰۲۱-۸۸۸۸۸۸۸۸",
                                            class_name="flex items-center",
                                        ),
                                        href="tel:+982188888888",
                                        class_name="flex items-center justify-between text-gray-700 hover:text-pink-700 transition-colors p-2 hover:bg-pink-50 rounded-lg",
                                    ),
                                    class_name="bg-white/60 p-4 rounded-2xl border border-white/60",
                                ),
                            ),
                            class_name="overflow-y-auto max-h-[60vh] pr-2 -mr-2 custom-scrollbar",
                        ),
                        class_name="relative h-full flex flex-col",
                    ),
                    class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[#fce7f3] w-[90vw] max-w-lg max-h-[85vh] p-6 md:p-8 rounded-3xl shadow-2xl z-[10000] border-[6px] border-white outline-none animate-in zoom-in-95 duration-200",
                )
            ),
        ),
        open=InfoModalState.is_open,
        on_open_change=InfoModalState.set_open,
    )