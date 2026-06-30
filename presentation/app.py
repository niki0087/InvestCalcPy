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
            md_bg_color: app.theme_cls.backgroundColor

            MDTopAppBar:
                id: toolbar
                title: "InvestCalc"
                pos_hint: {'top': 1}
                elevation: 2

            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(12)
                pos_hint: {'center_y': 0.6}
                size_hint_y: 0.6

                MDLabel:
                    text: 'Калькулятор'
                    halign: 'center'
                    theme_text_color: 'Primary'
                    font_size: dp(24)

                MDLabel:
                    text: 'Усреднение • Дивиденды • Прибыль'
                    halign: 'center'
                    theme_text_color: 'Secondary'

                Widget:
                    size_hint_y: 0.05

                MDButton:
                    style: "filled"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    on_release: app.open_average_calculator()

                    MDButtonText:
                        text: 'Калькулятор усреднения'

                MDButton:
                    style: "outlined"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    on_release: app.show_under_construction()

                    MDButtonText:
                        text: 'Дивиденды'

                MDButton:
                    style: "outlined"
                    size_hint_x: 0.7
                    pos_hint: {'center_x': 0.5}
                    on_release: app.show_under_construction()

                    MDButtonText:
                        text: 'Прибыль/убыток'

    Screen:
        name: 'average'
        id: average_screen
'''


class InvestCalcApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Logger.info("InvestCalcApp: Initializing...")

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        Logger.info("InvestCalcApp: Theme configured")
        return Builder.load_string(KV_STRING)

    def on_start(self):
        Logger.info("InvestCalcApp: Application started successfully")
        self._show_welcome_dialog()

    def open_average_calculator(self):
        from presentation.views.average_view import AverageView
        from presentation.presenters.average_presenter import AveragePresenter
        from domain.use_cases.calculate_average import CalculateAverageUseCase

        use_case = CalculateAverageUseCase()
        presenter = AveragePresenter(use_case)
        average_view = AverageView(presenter=presenter)
        presenter.view = average_view

        screen = self.root.get_screen('average')
        screen.clear_widgets()
        screen.add_widget(average_view)
        self.root.current = 'average'

    def go_back(self):
        self.root.current = 'main'

    def show_under_construction(self):
        dialog = MDDialog(
            MDDialogHeadlineText(text="В разработке"),
            MDDialogSupportingText(text="Этот раздел находится в разработке и будет доступен позже."),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    style="text",
                    on_release=lambda x: dialog.dismiss()
                )
            )
        )
        dialog.open()

    def _show_welcome_dialog(self):
        dialog = MDDialog(
            MDDialogHeadlineText(text="InvestCalc v0.1.0"),
            MDDialogSupportingText(
                text="Добро пожаловать в инвестиционный калькулятор!\n\n"
                     "• Расчет средней цены позиции\n"
                     "• Калькулятор дивидендов\n"
                     "• Расчет прибыли/убытка"
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Продолжить"),
                    style="filled",
                    on_release=lambda x: dialog.dismiss()
                )
            )
        )
        dialog.open()