import reflex as rx


class InfoModalState(rx.State):
    is_open: bool = False

    @rx.event
    def toggle(self):
        self.is_open = not self.is_open

    @rx.event
    def set_open(self, value: bool):
        self.is_open = value