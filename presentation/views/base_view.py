"""Базовый класс для View."""

from abc import ABC, abstractmethod
from kivymd.uix.screen import MDScreen


class BaseView(MDScreen, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._presenter = None

    @abstractmethod
    def init_ui(self):
        ...

    @abstractmethod
    def bind_events(self):
        ...

    def show_loading(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.spinner import MDSpinner
        self._loading = MDDialog(
            auto_dismiss=False,
            size_hint=(None, None),
            size=("100dp", "100dp"),
        )
        spinner = MDSpinner(size_hint=(1, 1))
        self._loading.add_widget(spinner)
        self._loading.open()

    def hide_loading(self):
        if hasattr(self, '_loading'):
            self._loading.dismiss()

    def show_error(self, message: str):
        from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
        from kivy.metrics import dp
        MDSnackbar(
            MDSnackbarText(text=message),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
        ).open()