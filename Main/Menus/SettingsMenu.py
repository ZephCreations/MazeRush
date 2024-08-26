import tkinter as tk

from .utils import create_menu_button, create_drop_down, create_menu_title
from ColourSchemes import Scheme as Theme
import ColourSchemes
from Settings import Settings

MENU_TITLE_TEXT = "Settings"


class SettingsMenu(tk.Frame):

    def __init__(self, parent, bread_crumbs, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

        self.points_to_win = None
        self.show_trails = None
        self.colour_theme = None
        self.maze_size = None

        self.create_widgets()

        # End of __init__

    def create_widgets(self):
        create_menu_title(self, MENU_TITLE_TEXT)

        container = tk.Frame(self, bg=Theme.bg)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8),
                               weight=0, uniform="yes")
        container.columnconfigure(1, weight=2, minsize=220)
        container.columnconfigure((0, 2), weight=3, minsize=80)

        padding_left = tk.Frame(container, width=250,
                                bg=Theme.bg)
        padding_left.grid(row=0, column=0, rowspan=10, sticky='nsew')
        padding_right = tk.Frame(container, width=250,
                                 bg=Theme.bg)
        padding_right.grid(row=0, column=2, rowspan=10, sticky='nsew')

        self.points_to_win = create_drop_down(
            container, "Points to Win",
            1, list(range(Settings.MIN_POINTS, Settings.MAX_POINTS+1)),
            Settings.POINTS_TO_WIN)
        self.show_trails = create_drop_down(
            container, "Trails",
            2, ["Show", "Hide"],
            Settings.SHOW_TRAILS_DISPLAY)
        self.colour_theme = create_drop_down(
            container, "Colour Theme",
            3, ColourSchemes.THEMES_LIST,
            Settings.THEME)
        self.maze_size = self.create_slider(
            container, "Default Maze Size",
            4, Settings.MIN_MAZE_SIZE[0],
            Settings.MAX_MAZE_SIZE[0], 1,
            Settings.DEFAULT_MAZE_SIZE[0]
        )
        container.rowconfigure(4, uniform="no")

        # Save button
        create_menu_button(
            container, "Save",
            6, self.save
        )
        create_menu_button(container, "Back <-",
                           7, self.go_back)

        # End of function create_widgets

    def create_slider(self, parent, text, row,
                      from_=1, to=10, step=1, default=None):
        if default is None:
            default = min
        container = tk.Frame(parent, bg="YELLOW",
                             relief='flat')
        label = tk.Label(container,
                         text=f'{text}',
                         fg=Theme.text,
                         bg=Theme.bg,
                         anchor="w")

        int_var = tk.IntVar(container)
        int_var.set(default)

        slider = tk.Scale(container,
                          from_=from_, to=to,
                          variable=int_var)
        slider.config(bg=Theme.bg, fg=Theme.text,
                      highlightthickness=0,
                      troughcolor=Theme.sec_bg,
                      activebackground=Theme.highlight,
                      orient="horizontal")

        container.grid(row=row, column=1, sticky='nsew', pady=5)
        label.pack(side='top', fill='both')
        slider.pack(side='bottom', fill='both')
        return int_var

    def save(self):
        Settings.POINTS_TO_WIN = int(self.points_to_win.get())

        show_trails = self.show_trails.get()
        Settings.SHOW_TRAILS_DISPLAY = show_trails
        if show_trails == "Show":
            Settings.SHOW_TRAILS = True
        else:
            Settings.SHOW_TRAILS = False

        Settings.DEFAULT_MAZE_SIZE = (self.maze_size.get(),
                                      self.maze_size.get())

        # Put new settings before this one
        colour_theme = self.colour_theme.get()
        for theme in ColourSchemes.THEMES_LIST:
            if theme.__class__.__name__ == colour_theme:
                Settings.THEME = theme
                ColourSchemes.change_scheme(theme)
                SettingsMenu(self.parent, self.bread_crumbs)
                self.destroy()

        # End of function save

    def go_back(self):
        # MainMenu.MainMenu(self.parent)
        self.bread_crumbs.previous()(
            self.parent, self.bread_crumbs)
        self.destroy()

