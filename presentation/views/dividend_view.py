"""Экран калькулятора дивидендов."""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

BG_SCREEN = (1, 1, 1, 1)
TEXT_PRIMARY = (0.118, 0.118, 0.137, 1)
TEXT_SECONDARY = (0.467, 0.471, 0.529, 1)
ACCENT = (0.388, 0.447, 0.902, 1)
GREEN = (0.318, 0.780, 0.471, 1)
RED = (0.957, 0.263, 0.212, 1)

HEADER_H = dp(48)
FOOTER_H = dp(56)
TOP_GAP = dp(36)


class DividendView(MDBoxLayout):

    def __init__(self, presenter=None, **kwargs):
        super().__init__(**kwargs)
        self.presenter = presenter
        self.orientation = 'vertical'
        self.md_bg_color = BG_SCREEN
        self.padding = (0, 0, 0, 0)
        self.spacing = 0

        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_header(self):
        bar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=HEADER_H,
            spacing=dp(4),
            padding=(dp(8), 0, dp(16), 0),
            md_bg_color=BG_SCREEN,
        )
        bar.add_widget(MDButton(
            MDButtonText(
                text="<",
                theme_text_color="Custom",
                text_color=ACCENT,
                font_size=dp(32),
            ),
            style="text",
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            on_release=lambda x: self._on_back(),
        ))
        bar.add_widget(MDLabel(
            text="Дивиденды",
            halign="left",
            valign="center",
            theme_text_color="Custom",
            text_color=TEXT_PRIMARY,
            font_size=dp(18),
            bold=True,
            size_hint_x=1,
        ))
        self.add_widget(bar)

    def _build_body(self):
        self.scroll = ScrollView(bar_width=0, do_scroll_x=False)
        self.scroll_container = MDBoxLayout(
            orientation='vertical',
            padding=(dp(16), TOP_GAP, dp(16), dp(8)),
            spacing=dp(12),
            size_hint_y=None,
        )
        self.scroll_container.bind(minimum_height=self.scroll_container.setter('height'))

        self.scroll_container.add_widget(self._section_title("ТИКЕР"))
        self.ticker_input = self._text_field("Например, SBER")
        self.scroll_container.add_widget(self.ticker_input)

        self.scroll_container.add_widget(self._section_title("ЦЕНА АКЦИИ"))
        self.price_input = self._text_field("0.00")
        self.scroll_container.add_widget(self.price_input)

        self.scroll_container.add_widget(self._section_title("КОЛИЧЕСТВО АКЦИЙ"))
        self.quantity_input = self._text_field("0")
        self.scroll_container.add_widget(self.quantity_input)

        self.scroll_container.add_widget(self._section_title("ДИВИДЕНД НА АКЦИЮ"))
        self.dividend_input = self._text_field("0.00")
        self.scroll_container.add_widget(self.dividend_input)

        self.scroll_container.add_widget(self._section_title("КЛЮЧЕВАЯ СТАВКА ЦБ (%)"))
        self.key_rate_input = self._text_field("16.0")
        self.scroll_container.add_widget(self.key_rate_input)

        self._build_result_section()

        self.scroll.add_widget(self.scroll_container)
        self.add_widget(self.scroll)

    def _build_result_section(self):
        self.result_title = MDLabel(
            text="Результаты",
            theme_text_color="Custom",
            text_color=TEXT_SECONDARY,
            size_hint_y=None,
            height=dp(24),
            font_size=dp(12),
            bold=True,
        )
        self.scroll_container.add_widget(self.result_title)

        self.result_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4),
            size_hint_y=None,
            height=dp(20),
        )
        self.scroll_container.add_widget(self.result_container)

    def _build_footer(self):
        bar = MDBoxLayout(
            size_hint_y=None,
            height=FOOTER_H,
            padding=(dp(16), dp(4), dp(16), dp(4)),
            md_bg_color=BG_SCREEN,
        )
        bar.add_widget(MDButton(
            MDButtonText(text="Рассчитать дивиденды", bold=True),
            style="filled",
            size_hint_x=1,
            height=dp(48),
            md_bg_color=ACCENT,
            on_release=lambda x: self._on_calculate(),
        ))
        self.add_widget(bar)

    # ─── HELPERS ────────────────────────────────────────────────
    def _text_field(self, hint):
        return MDTextField(
            MDTextFieldHintText(text=hint),
            mode="outlined",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(48),
        )

    def _section_title(self, text):
        return MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=TEXT_SECONDARY,
            size_hint_y=None,
            height=dp(20),
            font_size=dp(10),
            bold=True,
        )

    # ─── ACTIONS ────────────────────────────────────────────────
    def _on_calculate(self):
        if self.presenter:
            self.presenter.calculate(
                ticker=self.ticker_input.text.strip().upper(),
                price_text=self.price_input.text,
                quantity_text=self.quantity_input.text,
                dividend_text=self.dividend_input.text,
                key_rate_text=self.key_rate_input.text,
            )

    def _on_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_back()

    # ─── UPDATE UI ──────────────────────────────────────────────
    def show_result(self, result):
        self.result_container.clear_widgets()
        total = 0
        for label, value, is_positive in result:
            row = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(20),
                spacing=dp(4),
            )
            row.add_widget(MDLabel(
                text=label,
                size_hint_x=0.55,
                theme_text_color="Custom",
                text_color=TEXT_SECONDARY,
                font_size=dp(11),
            ))
            color = GREEN if is_positive else TEXT_PRIMARY
            row.add_widget(MDLabel(
                text=str(value),
                size_hint_x=0.45,
                halign="right",
                theme_text_color="Custom",
                text_color=color,
                bold=True,
                font_size=dp(12),
            ))
            self.result_container.add_widget(row)
            total += dp(20)
        self.result_container.height = max(dp(20), total)

    def show_error(self, message):
        self.result_container.clear_widgets()
        self.result_container.add_widget(MDLabel(
            text=f"⚠ {message}",
            theme_text_color="Custom",
            text_color=RED,
            size_hint_y=None,
            height=dp(20),
            font_size=dp(12),
        ))
        self.result_container.height = dp(24)

    def clear_inputs(self):
        self.ticker_input.text = ""
        self.price_input.text = ""
        self.quantity_input.text = ""
        self.dividend_input.text = ""
        self.key_rate_input.text = "16.0"