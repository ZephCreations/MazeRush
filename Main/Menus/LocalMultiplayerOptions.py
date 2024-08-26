import tkinter as tk
from .utils import create_menu_button, create_menu_title
from ColourSchemes import Scheme as Theme
from .GameScreen import GameScreen

MENU_TITLE_TEXT = "Options"


class LocalMultiplayerOptions(tk.Frame):

    def __init__(self, parent, bread_crumbs, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

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

        create_menu_button(container, "Two Player",
                           1, self.start_two_player_game)
        create_menu_button(container, "Three Player",
                           2, self.start_three_player_game)
        create_menu_button(container, "Four Player",
                           3, self.start_four_player_game)
        create_menu_button(container, "Back <-",
                           5, self.go_back)

        # End of function create_widgets

    def start_two_player_game(self):
        self.start_game(2)

    def start_three_player_game(self):
        self.start_game(3)

    def start_four_player_game(self):
        self.start_game(4)

    def start_game(self, players, lobby=True):
        state = self.parent.root.state
        self.destroy()
        self.bread_crumbs.add_next(type(self))
        GameScreen(self.parent, self.bread_crumbs, players, state(), lobby=lobby)

        # End of function start_game

    def go_back(self):
        self.bread_crumbs.previous()(self.parent, self.bread_crumbs)
        self.destroy()
