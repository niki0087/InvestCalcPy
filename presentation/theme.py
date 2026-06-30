"""Material Design 3 тема для InvestCalcPy."""

PRIMARY = "#1A73E8"
SECONDARY = "#34A853"
SURFACE = "#FFFFFF"
BACKGROUND = "#F8F9FA"
ERROR = "#EA4335"
ON_PRIMARY = "#FFFFFF"
ON_SURFACE = "#1F1F1F"

PADDING_H = 16
PADDING_V = 12
PADDING_CARD = 16

FONT_H1 = 24
FONT_H2 = 20
FONT_H3 = 18
FONT_BODY = 16
FONT_CAPTION = 14
FONT_SMALL = 12

KV_STYLES = '''
<MDCard[card_style="result"]>:
    size_hint_y: None
    height: self.minimum_height
    padding: dp(16)
    elevation: 2
    radius: [12]
    md_bg_color: app.theme_cls.surfaceColor

<MDTextField[field_style="calculator"]>:
    mode: "outlined"
    size_hint_x: 1
    helper_text_mode: "on_error"

<MDRaisedButton[button_style="primary"]>:
    md_bg_color: app.theme_cls.primaryColor
    elevation: 2
    font_style: "Button"

<MDLabel[label_style="result_value"]>:
    font_style: "H6"
    halign: "right"
    theme_text_color: "Primary"

<MDLabel[label_style="result_title"]>:
    font_style: "Caption"
    theme_text_color: "Secondary"
    halign: "left"
'''