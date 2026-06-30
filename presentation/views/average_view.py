"""Экран калькулятора усреднения позиции."""

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

BG_SCREEN = (1, 1, 1, 1)
TEXT_PRIMARY = (0.118, 0.118, 0.137, 1)
TEXT_SECONDARY = (0.467, 0.471, 0.529, 1)
TEXT_HINT = (0.690, 0.694, 0.749, 1)
ACCENT = (0.388, 0.447, 0.902, 1)
RED = (0.957, 0.263, 0.212, 1)

HEADER_H = dp(48)
FOOTER_H = dp(56)
TOP_GAP = dp(36)


class AverageView(MDBoxLayout):

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

        back_btn = MDButton(
            MDButtonText(
                text="<",
                theme_text_color="Custom",
                text_color=ACCENT,
                font_size=dp(24),
            ),
            style="text",
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            on_release=lambda x: self._on_back(),
        )

        bar.add_widget(back_btn)
        bar.add_widget(MDLabel(
            text="Усреднение",
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

        self._build_input_section()
        self.scroll_container.add_widget(self._accent_button("+ Добавить сделку", self._on_add_deal))
        self._build_deals_section()
        self._build_result_section()

        self.scroll.add_widget(self.scroll_container)
        self.add_widget(self.scroll)

    def _build_input_section(self):
        self.scroll_container.add_widget(self._section_title("ТИКЕР"))
        self.ticker_input = self._text_field("Например, SBER")
        self.scroll_container.add_widget(self.ticker_input)

        self.scroll_container.add_widget(self._section_title("ЦЕНА ЗА АКЦИЮ"))
        self.price_input = self._text_field("0.00")
        self.scroll_container.add_widget(self.price_input)

        self.scroll_container.add_widget(self._section_title("КОЛИЧЕСТВО (ЛОТЫ)"))
        self.quantity_input = self._text_field("0")
        self.scroll_container.add_widget(self.quantity_input)

        self.scroll_container.add_widget(self._section_title("КОМИССИЯ (₽, ОПЦИОНАЛЬНО)"))
        self.commission_input = self._text_field("0.00")
        self.scroll_container.add_widget(self.commission_input)

    def _build_deals_section(self):
        self.deals_label = MDLabel(
            text="Сделки: 0",
            theme_text_color="Custom",
            text_color=TEXT_SECONDARY,
            size_hint_y=None,
            height=dp(24),
            font_size=dp(12),
            bold=True,
        )
        self.scroll_container.add_widget(self.deals_label)

        self.deals_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(4),
            size_hint_y=None,
            height=dp(20),
        )
        self.scroll_container.add_widget(self.deals_container)

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
            spacing=dp(2),
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
            MDButtonText(text="Рассчитать среднюю", bold=True),
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

    def _accent_button(self, text, callback):
        return MDButton(
            MDButtonText(text=text, bold=True),
            style="filled",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(44),
            md_bg_color=ACCENT,
            on_release=lambda x: callback(),
        )

    # ─── ACTIONS ────────────────────────────────────────────────
    def _on_add_deal(self):
        if self.presenter:
            self.presenter.add_deal(
                ticker=self.ticker_input.text.strip().upper(),
                price_text=self.price_input.text,
                quantity_text=self.quantity_input.text,
                commission_text=self.commission_input.text,
            )

    def _on_calculate(self):
        if self.presenter:
            self.presenter.calculate()

    def _on_back(self):
        from kivymd.app import MDApp
        MDApp.get_running_app().go_back()

    # ─── UPDATE UI ──────────────────────────────────────────────
    def update_deals_list(self, deals_data):
        self.deals_container.clear_widgets()
        self.deals_label.text = f"Сделки: {len(deals_data)}"
        total = 0
        for i, d in enumerate(deals_data):
            row = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(26),
                spacing=dp(4),
            )
            row.add_widget(MDLabel(
                text=d['ticker'],
                size_hint_x=0.22,
                theme_text_color="Custom",
                text_color=TEXT_PRIMARY,
                bold=True,
                font_size=dp(12),
            ))
            row.add_widget(MDLabel(
                text=f"×{d['quantity']} @{d['price']}",
                size_hint_x=0.38,
                theme_text_color="Custom",
                text_color=TEXT_SECONDARY,
                font_size=dp(10),
            ))
            row.add_widget(MDLabel(
                text=f"ком.{d['commission']}",
                size_hint_x=0.25,
                theme_text_color="Custom",
                text_color=TEXT_HINT,
                font_size=dp(9),
            ))
            row.add_widget(MDButton(
                MDButtonText(text="✕", theme_text_color="Custom", text_color=RED),
                style="text",
                size_hint_x=0.15,
                on_release=lambda x, idx=i: self._on_remove_deal(idx),
            ))
            self.deals_container.add_widget(row)
            total += dp(26)
        self.deals_container.height = max(dp(20), total)

    def _on_remove_deal(self, index):
        if self.presenter:
            self.presenter.remove_deal(index)

    def show_result(self, result):
        self.result_container.clear_widgets()
        total = 0
        for label, value in result.items():
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
            row.add_widget(MDLabel(
                text=str(value),
                size_hint_x=0.45,
                halign="right",
                theme_text_color="Custom",
                text_color=TEXT_PRIMARY,
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
        self.commission_input.text = ""