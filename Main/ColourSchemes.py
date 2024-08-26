def change_scheme(scheme):
    Scheme.bg = scheme.bg
    Scheme.sec_bg = scheme.sec_bg
    Scheme.game_bg = scheme.game_bg
    Scheme.maze_bg = scheme.maze_bg
    Scheme.text = scheme.text
    Scheme.button_bg = scheme.button_bg
    Scheme.button_text = scheme.button_text
    Scheme.button_outline = scheme.button_outline
    Scheme.disabled_button_bg = scheme.disabled_button_bg
    Scheme.disabled_button_text = scheme.disabled_button_text
    Scheme.disabled_button_outline = scheme.disabled_button_outline
    Scheme.highlight = scheme.highlight
    Scheme.highlight_text = scheme.highlight_text

    Scheme.font_style = scheme.font_style
    Scheme.font_bold = scheme.font_bold


class Scheme:
    bg = None
    sec_bg = None
    game_bg = None
    maze_bg = None
    text = None
    button_bg = None
    button_text = None
    button_outline = None
    disabled_button_bg = None
    disabled_button_text = None
    disabled_button_outline = None
    highlight = None
    highlight_text = None

    font_style = None
    font_bold = None

    def __init__(self):
        self.bg = ""
        self.sec_bg = ""
        self.game_bg = ""
        self.maze_bg = ""
        self.text = ""
        self.button_bg = ""
        self.button_text = ""
        self.button_outline = ""
        self.disabled_button_bg = ""
        self.disabled_button_text = ""
        self.disabled_button_outline = ""
        self.highlight = ""
        self.highlight_text = ""

        self.font_style = ""
        self.font_bold = ""

    def __str__(self):
        return self.__class__.__name__


class Dark(Scheme):
    def __init__(self):
        Scheme.__init__(self)
        self.bg = "gray10"
        self.sec_bg = "slate gray"
        self.game_bg = "gray20"
        self.maze_bg = "gray30"
        self.text = "snow"
        self.button_bg = "gray50"
        self.button_text = "snow"
        self.button_outline = "gold"
        self.disabled_button_bg = "gray30"
        self.disabled_button_text = "gainsboro"
        self.disabled_button_outline = "gold4"
        self.highlight = "light goldenrod"
        self.highlight_text = "gray10"

        self.font_style = 'calibri'
        self.font_bold = 'calibri bold'


class Light(Scheme):
    def __init__(self):
        Scheme.__init__(self)
        self.bg = "snow"
        self.sec_bg = "light steel blue"
        self.game_bg = "gray90"
        self.maze_bg = "gray80"
        self.text = "gray10"
        self.button_bg = "gray80"
        self.button_text = "gray10"
        self.button_outline = "light coral"
        self.disabled_button_bg = "gray60"
        self.disabled_button_text = "gray30"
        self.disabled_button_outline = "coral3"
        self.highlight = "light sky blue1"
        self.highlight_text = "gray10"

        self.font_style = 'calibri'
        self.font_bold = 'calibri bold'


THEMES_LIST = [Dark(), Light()]
