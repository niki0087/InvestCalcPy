"""Главный класс приложения InvestCalc."""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText


KV_STRING = '''
ScreenManager:
    id: screen_manager

    Screen:
        name: 'main'
        MDScreen:
            md_bg_color: 1, 1, 1, 1

            MDTopAppBar:
                id: toolbar
                title: "InvestCalc"
                pos_hint: {'top': 1}
                elevation: 0
                md_bg_color: 1, 1, 1, 1
                specific_text_color: 0.118, 0.118, 0.137, 1

            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(24)
                spacing: dp(16)
                pos_hint: {'center_y': 0.55}
                size_hint_y: 0.6

                MDLabel:
                    text: 'Калькулятор'
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 0.118, 0.118, 0.137, 1
                    font_size: dp(28)
                    bold: True

                MDLabel:
                    text: 'Усреднение • Дивиденды • Прибыль'
                    halign: 'center'
                    theme_text_color: 'Custom'
                    text_color: 0.467, 0.471, 0.529, 1
                    font_size: dp(14)

                Widget:
                    size_hint_y: 0.05

                MDButton:
                    style: "filled"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    height: dp(52)
                    md_bg_color: 0.388, 0.447, 0.902, 1
                    on_release: app.open_average_calculator()

                    MDButtonText:
                        text: 'Калькулятор усреднения'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        bold: True

                MDButton:
                    style: "filled"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    height: dp(52)
                    md_bg_color: 0.388, 0.447, 0.902, 1
                    on_release: app.open_dividend_calculator()

                    MDButtonText:
                        text: 'Дивиденды'
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        bold: True

                MDButton:
                    style: "outlined"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    height: dp(48)
                    line_color: 0.388, 0.447, 0.902, 1
                    on_release: app.show_under_construction()

                    MDButtonText:
                        text: 'Прибыль/убыток'
                        theme_text_color: 'Custom'
                        text_color: 0.388, 0.447, 0.902, 1

    Screen:
        name: 'average'
        id: average_screen

    Screen:
        name: 'dividend'
        id: dividend_screen
'''


class InvestCalcApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("InvestCalcApp: Initializing...")

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        Logger.info("InvestCalcApp: Theme configured")
        return Builder.load_string(KV_STRING)

    def on_start(self):
        Logger.info("InvestCalcApp: Application started successfully")

    def open_average_calculator(self):
        from presentation.views.average_view import AverageView
        from presentation.presenters.average_presenter import AveragePresenter
        from domain.use_cases.calculate_average import CalculateAverageUseCase

        use_case = CalculateAverageUseCase()
        presenter = AveragePresenter(use_case)
        view = AverageView(presenter=presenter)
        presenter.view = view

        screen = self.root.get_screen('average')
        screen.clear_widgets()
        screen.add_widget(view)
        self.root.current = 'average'

    def open_dividend_calculator(self):
        from presentation.views.dividend_view import DividendView
        from presentation.presenters.dividend_presenter import DividendPresenter
        from domain.use_cases.calculate_dividends import CalculateDividendsUseCase

        use_case = CalculateDividendsUseCase()
        presenter = DividendPresenter(use_case)
        view = DividendView(presenter=presenter)
        presenter.view = view

        screen = self.root.get_screen('dividend')
        screen.clear_widgets()
        screen.add_widget(view)
        self.root.current = 'dividend'

    def go_back(self):
        self.root.current = 'main'

    def show_under_construction(self):
        dialog = MDDialog(
            MDDialogHeadlineText(text="В разработке"),
            MDDialogSupportingText(text="Этот раздел будет доступен позже."),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    style="text",
                    on_release=lambda x: dialog.dismiss()
                )
            )
        )
        dialog.open()