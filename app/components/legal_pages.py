import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer


def legal_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                content, class_name="max-w-4xl mx-auto px-4 py-12 sm:px-6 lg:px-8"
            ),
            class_name="flex-grow min-h-screen",
        ),
        footer(),
        class_name="flex flex-col min-h-screen font-sans text-white bg-slate-950 bg-[url('/background.png')] bg-cover bg-center bg-fixed bg-no-repeat selection:bg-blue-500/30",
        dir="rtl",
    )


def privacy_page() -> rx.Component:
    return legal_layout(
        rx.el.div(
            rx.el.h1(
                "سیاست حفظ حریم خصوصی", class_name="text-3xl font-bold text-white mb-8"
            ),
            rx.el.div(
                rx.el.h2(
                    "۱. جمع\u200cآوری اطلاعات",
                    class_name="text-xl font-bold text-blue-400 mb-4",
                ),
                rx.el.p(
                    "ما اطلاعاتی را که شما مستقیماً در اختیار ما قرار می\u200cدهید، جمع\u200cآوری می\u200cکنیم. این شامل اطلاعات ثبت\u200cنام، اطلاعات پروفایل کاربری و پاسخ\u200cهای شما به پرسشنامه\u200cهای اولیه است.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۲. استفاده از اطلاعات",
                    class_name="text-xl font-bold text-blue-400 mb-4",
                ),
                rx.el.p(
                    "ما از اطلاعات جمع\u200cآوری شده برای ارائه خدمات، ارتباط با شما، و بهبود تجربه کاربری استفاده می\u200cکنیم. اطلاعات هویتی شما بدون رضایت صریح شما با اشخاص ثالث به اشتراک گذاشته نخواهد شد.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۳. امنیت داده\u200cها",
                    class_name="text-xl font-bold text-blue-400 mb-4",
                ),
                rx.el.p(
                    "ما اقدامات امنیتی مناسبی را برای محافظت از اطلاعات شما در برابر دسترسی غیرمجاز، تغییر، افشاء یا تخریب به کار می\u200cبریم.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۴. حقوق شما", class_name="text-xl font-bold text-blue-400 mb-4"
                ),
                rx.el.p(
                    "شما حق دارید به اطلاعات شخصی خود دسترسی داشته باشید، آن\u200cها را اصلاح کنید یا درخواست حذف آن\u200cها را بدهید.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                class_name="bg-slate-900/60 backdrop-blur-md p-8 rounded-2xl border border-white/10",
            ),
        )
    )


def terms_page() -> rx.Component:
    return legal_layout(
        rx.el.div(
            rx.el.h1(
                "قوانین و مقررات", class_name="text-3xl font-bold text-white mb-8"
            ),
            rx.el.div(
                rx.el.h2(
                    "۱. پذیرش شرایط", class_name="text-xl font-bold text-blue-400 mb-4"
                ),
                rx.el.p(
                    "با استفاده از این پلتفرم، شما موافقت می\u200cکنید که به تمام قوانین و مقررات مندرج در این صفحه پایبند باشید.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۲. شرایط عضویت", class_name="text-xl font-bold text-blue-400 mb-4"
                ),
                rx.el.p(
                    "برای عضویت در این پلتفرم باید حداقل ۱۸ سال سن داشته باشید. اطلاعات ارائه شده باید دقیق و صحیح باشد.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۳. مسئولیت\u200cهای کاربران",
                    class_name="text-xl font-bold text-blue-400 mb-4",
                ),
                rx.el.p(
                    "کاربران مسئول حفظ محرمانگی حساب کاربری خود هستند. هرگونه فعالیت غیرقانونی یا مزاحمت برای سایر کاربران ممنوع است.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                rx.el.h2(
                    "۴. حقوق مالکیت معنوی",
                    class_name="text-xl font-bold text-blue-400 mb-4",
                ),
                rx.el.p(
                    "تمامی محتویات و طراحی این پلتفرم متعلق به نورو ریکروت است و هرگونه کپی\u200cبرداری بدون اجازه کتبی ممنوع است.",
                    class_name="text-gray-300 mb-6 leading-relaxed",
                ),
                class_name="bg-slate-900/60 backdrop-blur-md p-8 rounded-2xl border border-white/10",
            ),
        )
    )