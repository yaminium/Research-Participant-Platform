import reflex as rx
from app.states.auth_state import AuthState
from app.states.navbar_state import NavbarState


def navbar_link(text: str, url: str, icon_name: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon_name, class_name="h-5 w-5"),
            rx.el.span(text),
            class_name="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-white/10 text-gray-200 hover:text-blue-400 transition-colors font-medium text-sm",
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
                        rx.icon("brain-circuit", class_name="h-8 w-8 text-blue-500"),
                        rx.el.h1(
                            "نورو ریکروت",
                            class_name="text-xl font-bold text-white tracking-tight",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    href="/",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            NavbarState.is_menu_open,
                            rx.icon("x", class_name="h-6 w-6"),
                            rx.icon("menu", class_name="h-6 w-6"),
                        ),
                        on_click=NavbarState.toggle_menu,
                        class_name="md:hidden p-2 rounded-md text-gray-300 hover:text-white hover:bg-white/10",
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
                            class_name="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-white/10 text-gray-200 hover:text-red-400 transition-colors font-medium text-sm ml-2 cursor-pointer w-full md:w-auto",
                        ),
                        class_name="flex flex-col md:flex-row items-start md:items-center gap-1",
                    ),
                    rx.el.div(
                        navbar_link("خانه", "/", "home"),
                        navbar_link("مرور مطالعات", "/browse", "search"),
                        rx.el.a(
                            "ورود",
                            href="/login",
                            class_name="w-full md:w-auto text-center px-5 py-2 text-sm font-medium text-blue-400 hover:bg-white/10 rounded-full transition-colors",
                            on_click=NavbarState.close_menu,
                        ),
                        rx.el.a(
                            "شروع کنید",
                            href="/register",
                            class_name="w-full md:w-auto text-center px-5 py-2 text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 rounded-full shadow-md hover:shadow-lg transition-all",
                            on_click=NavbarState.close_menu,
                        ),
                        class_name="flex flex-col md:flex-row items-start md:items-center gap-2",
                    ),
                ),
                class_name=rx.cond(
                    NavbarState.is_menu_open,
                    "flex flex-col absolute top-20 left-0 w-full bg-slate-900 p-4 shadow-lg border-b border-white/10 md:static md:flex md:flex-row md:w-auto md:p-0 md:shadow-none md:border-none md:bg-transparent",
                    "hidden md:flex items-center",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex flex-col md:flex-row items-center justify-between",
        ),
        class_name="bg-slate-950/80 backdrop-blur-md border-b border-white/10 sticky top-0 z-50",
    )