import tkinter as tk
from ColourSchemes import Scheme as Theme
from .Instructions import InstructionsMenu
from .LocalMultiplayerOptions import LocalMultiplayerOptions
from .SettingsMenu import SettingsMenu
from .utils import create_menu_button
from .breadcrumbs import BreadCrumbs

MENU_TITLE_TEXT = "Menu"


class MainMenu(tk.Frame):
    def __init__(self, parent, bread_crumbs=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)

        self.create_widgets()

        # End of __init__

    def create_widgets(self):
        title = tk.Label(self, text=MENU_TITLE_TEXT, font=('calibri bold', 36),
                         fg=Theme.text, bg=Theme.bg, width=10, pady=20)
        title.pack(side='top', fill='both')

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

        create_menu_button(container, "Single Player",
                           1, self.single_player, True)
        create_menu_button(container, "Local Multiplayer",
                           2, self.local_multiplayer)
        create_menu_button(container, "Network Multiplayer",
                           3, self.network_multiplayer)
        create_menu_button(container, "Instructions",
                           5, self.instructions)
        create_menu_button(container, "Settings",
                           6, self.settings)
        create_menu_button(container, "Quit",
                           7, self.quit)

        # End of function create_widgets

    def single_player(self):
        print("Single player")

    def local_multiplayer(self):
        self.destroy()
        LocalMultiplayerOptions(
            self.parent, BreadCrumbs(type(self)))

    def network_multiplayer(self):
        print("Network Multiplayer")

    def instructions(self):
        self.destroy()
        InstructionsMenu(self.parent, BreadCrumbs(type(self)))

    def settings(self):
        self.destroy()
        SettingsMenu(self.parent, BreadCrumbs(type(self)))

    def quit(self):
        self.parent.root.destroy()

