import reflex as rx


class NavbarState(rx.State):
    is_menu_open: bool = False

    @rx.event
    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def close_menu(self):
        self.is_menu_open = False