import tkinter as tk
from socket import gethostbyname, gethostname
from random import randint

from .utils import (create_menu_button, create_menu_title,
                    create_input_field, create_label, create_drop_down)
from ColourSchemes import Scheme as Theme
from .GameScreen import GameScreen
from Networking.Controller import start_server, join_server

MENU_TITLE_TEXT = "Options"


class NetworkMultiplayerOptions(tk.Frame):

    def __init__(self, parent, bread_crumbs, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

        self.host = gethostbyname(gethostname())
        self.port = randint(10000, 65432)
        self.address = None
        self.name = None

        self.colours = ["Blue", "Red", "Green", "Yellow", "Purple", "Orange",
                        "Pink", "Maroon"]

        self.create_widgets()

        self.server = None

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

        create_menu_button(container, f"Host: {self.host}",
                           1, self.host_network_game)
        create_label(container, "Join Game:",
                     3)
        self.address = create_input_field(container, "192.168.1.1:65432",
                                          4)
        self.name = create_drop_down(container, "Colour:",
                                     5,
                                     self.colours)
        create_menu_button(container, "Join",
                           6, self.join_game)

        create_menu_button(container, "Back <-",
                           8, self.go_back)

        # End of function create_widgets

    def host_network_game(self):
        self.server = start_server(self.host, self.port)
        game_screen = self.start_game(0)
        join_server(self.name.get(), self.host, self.port, game_screen)

    def join_game(self):
        game_screen = self.start_game(0)
        host, port = self.address.get().split(':')
        join_server(self.name.get(), host, int(port), game_screen)

    def start_game(self, players, lobby=True):
        state = self.parent.root.state
        self.destroy()
        self.bread_crumbs.add_next(type(self))
        screen = GameScreen(self.parent, self.bread_crumbs, players, state(), lobby=lobby,
                            address=(self.host, self.port), server=self.server)
        return screen
        # End of function start_game

    def go_back(self):
        self.bread_crumbs.previous()(self.parent, self.bread_crumbs)
        self.destroy()
