import reflex as rx
from app.states.auth_state import AuthState
from app.states.navbar_state import NavbarState


def navbar_link(text: str, url: str, icon_name: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_name, class_name="h-5 w-5"),
            rx.el.span(text),
            class_name="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-white/5 text-gray-300 hover:text-cyan-300 transition-all duration-300 font-medium text-sm hover:shadow-[0_0_15px_rgba(34,211,238,0.15)] border border-transparent hover:border-cyan-500/20",
        ),
        href=url,
        on_click=NavbarState.close_menu,
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon(
                            "brain-circuit",
                            class_name="h-12 w-12 text-cyan-400 drop-shadow-[0_0_15px_rgba(34,211,238,0.6)] transition-transform hover:scale-110 duration-300",
                        ),
                        rx.el.h1(
                            "نورو ریکروت",
                            class_name="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-blue-400 to-purple-500 tracking-tighter drop-shadow-[0_2px_10px_rgba(59,130,246,0.5)]",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    href="/",
                    class_name="hover:opacity-90 transition-opacity",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            NavbarState.is_menu_open,
                            rx.icon("x", class_name="h-8 w-8 text-cyan-400"),
                            rx.icon("menu", class_name="h-8 w-8 text-cyan-400"),
                        ),
                        on_click=NavbarState.toggle_menu,
                        class_name="md:hidden p-2 rounded-xl text-gray-300 hover:text-white hover:bg-white/10 transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between w-full md:w-auto",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.cond(
                            AuthState.is_researcher,
                            navbar_link("داشبورد", "/dashboard", "layout-dashboard"),
                        ),
                        rx.cond(
                            AuthState.is_researcher,
                            navbar_link("مطالعات من", "/my-studies", "file-text"),
                            navbar_link(
                                "علاقه\u200cمندی\u200cها", "/favorites", "heart"
                            ),
                        ),
                        navbar_link("مرور مطالعات", "/browse", "search"),
                        navbar_link("پروفایل من", "/profile", "user"),
                        rx.el.button(
                            rx.el.div(
                                rx.icon("log-out", class_name="h-5 w-5"),
                                rx.el.span("خروج"),
                                class_name="flex items-center gap-2",
                            ),
                            on_click=[AuthState.logout, NavbarState.close_menu],
                            class_name="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-red-500/10 text-gray-300 hover:text-red-400 transition-all duration-300 font-medium text-sm ml-2 cursor-pointer w-full md:w-auto border border-transparent hover:border-red-500/20 hover:shadow-[0_0_15px_rgba(248,113,113,0.2)]",
                        ),
                        class_name="flex flex-col md:flex-row items-start md:items-center gap-2 md:gap-1",
                    ),
                    rx.el.div(
                        navbar_link("خانه", "/", "home"),
                        navbar_link("مرور مطالعات", "/browse", "search"),
                        rx.el.a(
                            "ورود",
                            href="/login",
                            class_name="w-full md:w-auto text-center px-6 py-2.5 text-sm font-semibold text-cyan-300 hover:text-cyan-200 hover:bg-cyan-500/10 rounded-full transition-all duration-300 border border-cyan-500/30 hover:border-cyan-400 hover:shadow-[0_0_15px_rgba(34,211,238,0.2)]",
                            on_click=NavbarState.close_menu,
                        ),
                        rx.el.a(
                            "شروع کنید",
                            href="/register",
                            class_name="w-full md:w-auto text-center px-6 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-full shadow-[0_0_20px_rgba(79,70,229,0.4)] hover:shadow-[0_0_30px_rgba(79,70,229,0.6)] transition-all duration-300 transform hover:-translate-y-0.5 border border-white/10",
                            on_click=NavbarState.close_menu,
                        ),
                        class_name="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-3",
                    ),
                ),
                class_name=rx.cond(
                    NavbarState.is_menu_open,
                    "flex flex-col absolute top-24 left-0 w-full bg-slate-950/95 backdrop-blur-xl p-6 shadow-2xl border-b border-cyan-500/20 md:static md:flex md:flex-row md:w-auto md:p-0 md:shadow-none md:border-none md:bg-transparent animate-in slide-in-from-top-5 duration-200",
                    "hidden md:flex items-center",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-24 flex flex-col md:flex-row items-center justify-between relative",
        ),
        class_name="bg-slate-950/80 backdrop-blur-xl border-b border-cyan-500/20 shadow-[0_0_30px_-10px_rgba(34,211,238,0.15)] sticky top-0 z-50 transition-all duration-300",
    )