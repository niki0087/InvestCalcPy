"""Экран калькулятора усреднения позиции."""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldHelperText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.logger import Logger


class AverageView(ScrollView):
    """Экран калькулятора усреднения с прокруткой."""

    def __init__(self, presenter=None, **kwargs):
        super().__init__(**kwargs)
        self.presenter = presenter
        self._commission_type = "percent"

        self.container = MDBoxLayout(
            orientation='vertical',
            padding=dp(16),
            spacing=dp(8),
            size_hint_y=None,
        )
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_widget(self.container)

        self.init_ui()

    def init_ui(self):
        self.container.add_widget(MDLabel(
            text="Калькулятор усреднения",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40),
        ))

        self.ticker_input = MDTextField(
            MDTextFieldHintText(text="Тикер (например, SBER)"),
            mode="outlined",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(56),
        )
        self.container.add_widget(self.ticker_input)

        self.price_input = MDTextField(
            MDTextFieldHintText(text="Цена за акцию"),
            mode="outlined",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(56),
            input_filter="float",
        )
        self.container.add_widget(self.price_input)

        self.quantity_input = MDTextField(
            MDTextFieldHintText(text="Количество (лоты)"),
            mode="outlined",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(56),
            input_filter="int",
        )
        self.container.add_widget(self.quantity_input)

        self.commission_type_switcher = MDSegmentedButton(
            size_hint_x=1,
            size_hint_y=None,
            height=dp(40),
        )
        percent_btn = MDSegmentedButtonItem(text="Комиссия %")
        rubles_btn = MDSegmentedButtonItem(text="Комиссия ₽")
        self.commission_type_switcher.add_widget(percent_btn)
        self.commission_type_switcher.add_widget(rubles_btn)
        self.container.add_widget(self.commission_type_switcher)

        self.commission_input = MDTextField(
            MDTextFieldHintText(text="Комиссия (%)"),
            mode="outlined",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(56),
            input_filter="float",
            text="0.05",
        )
        self.container.add_widget(self.commission_input)

        self.container.add_widget(MDButton(
            MDButtonText(text="Добавить сделку"),
            style="filled",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._on_add_deal(),
        ))

        self.deals_label = MDLabel(
            text="Сделки: 0",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(30),
        )
        self.container.add_widget(self.deals_label)

        self.deals_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4),
            size_hint_y=None,
            height=dp(60),
        )
        self.container.add_widget(self.deals_container)

        self.container.add_widget(MDButton(
            MDButtonText(text="Рассчитать среднюю"),
            style="filled",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._on_calculate(),
        ))

        self.result_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4),
            size_hint_y=None,
            height=dp(120),
        )
        self.container.add_widget(self.result_container)

        self.container.add_widget(MDButton(
            MDButtonText(text="Назад"),
            style="text",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self._on_back(),
        ))

    def _on_add_deal(self):
        if self.presenter:
            self.presenter.add_deal(
                ticker=self.ticker_input.text.strip().upper(),
                price_text=self.price_input.text,
                quantity_text=self.quantity_input.text,
                commission_text=self.commission_input.text,
                commission_type=self._commission_type,
            )

    def _on_calculate(self):
        if self.presenter:
            self.presenter.calculate()

    def _on_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_back()

    def update_deals_list(self, deals_data: list):
        self.deals_container.clear_widgets()
        self.deals_label.text = f"Сделки: {len(deals_data)}"
        for i, deal in enumerate(deals_data):
            card = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(32),
                spacing=dp(8),
            )
            card.add_widget(MDLabel(text=deal['ticker'], size_hint_x=0.2))
            card.add_widget(MDLabel(text=f"×{deal['quantity']}", size_hint_x=0.15))
            card.add_widget(MDLabel(text=f"@{deal['price']}", size_hint_x=0.3))
            card.add_widget(MDLabel(text=f"ком.{deal['commission']}", size_hint_x=0.2))
            card.add_widget(MDButton(
                MDButtonText(text="✕"),
                style="text",
                size_hint_x=0.15,
                on_release=lambda x, idx=i: self._on_remove_deal(idx),
            ))
            self.deals_container.add_widget(card)

    def _on_remove_deal(self, index: int):
        if self.presenter:
            self.presenter.remove_deal(index)

    def show_result(self, result: dict):
        self.result_container.clear_widgets()
        self.result_container.add_widget(MDLabel(
            text="Результаты:",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(24),
        ))
        for label, value in result.items():
            row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(22))
            row.add_widget(MDLabel(text=label, size_hint_x=0.6, theme_text_color="Secondary"))
            row.add_widget(MDLabel(text=str(value), size_hint_x=0.4, halign="right"))
            self.result_container.add_widget(row)

    def show_error(self, message: str):
        self.result_container.clear_widgets()
        self.result_container.add_widget(MDLabel(
            text=f"Ошибка: {message}",
            theme_text_color="Error",
            size_hint_y=None,
            height=dp(24),
        ))

    def clear_inputs(self):
        self.ticker_input.text = ""
        self.price_input.text = ""
        self.quantity_input.text = ""
        self.commission_input.text = "0.05"