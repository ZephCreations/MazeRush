import tkinter as tk

from ColourSchemes import Scheme as Theme
from .RootWindow import RootWindow
import GameLogic


class GameScreen(tk.Frame):
    BORDER_PADDING = 10

    def __init__(self, parent: RootWindow, bread_crumbs,
                 players: int, state,
                 menu_width=200, lobby=False, address=None, server=None,
                 *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

        self.parent = parent
        self.menu_width = menu_width
        self.no_players = players
        self.address = address
        self.server = server
        self.player_stats = []
        self.state = state
        self.original_width = self.parent.root.winfo_width()
        self.original_height = self.parent.root.winfo_height()

        self.canvas: tk.Canvas = ...
        self.timer_display = None
        self.timer_val = 0.0000

        self.side_bar_frame = None
        self.canvas_width = None
        self.canvas_height = None

        self.parent.root.state('zoomed')
        self.parent.root.resizable(False, False)

        self.create_canvas()
        self.create_side_bar()

        self.game = GameLogic.Game(self, lobby, address)

        self.create_stats_section()
        self.create_back_button()

        self.game.start_game()

        # End of __init__

    def create_canvas(self):
        self.canvas: tk.Canvas = tk.Canvas(
            self, relief='solid', highlightthickness=4,
            highlightbackground=Theme.sec_bg,
            # highlightcolor=Theme.highlight,
            bg=Theme.maze_bg)
        self.canvas.pack(side='right', fill='both', expand=True,
                         padx=GameScreen.BORDER_PADDING,
                         pady=GameScreen.BORDER_PADDING)

        self.update()
        self.update_idletasks()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

    def create_side_bar(self):
        self.side_bar_frame = tk.Frame(self, bg=Theme.bg,
                                       width=self.menu_width)
        self.side_bar_frame.pack_propagate(False)
        self.side_bar_frame.pack(side='left',
                                 padx=(GameScreen.BORDER_PADDING, 4),
                                 fill='both')

        title = tk.Label(self.side_bar_frame, text="Menu",
                         font=(Theme.font_bold, 20), pady=20,
                         bg=Theme.bg, fg=Theme.text)
        title.pack(side='top', fill='x')

        # End of function create_side_bar

    def create_stats_section(self):
        row = 0
        stats_frame = tk.Frame(self.side_bar_frame,
                               highlightbackground=Theme.highlight,
                               highlightthickness=4,
                               bg=Theme.bg)
        stats_frame.pack(side='top', fill='x', padx=12)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        stats_title = tk.Label(stats_frame, text="Stats",
                               font=(Theme.font_bold, 18),
                               bg=Theme.bg, fg=Theme.text)
        stats_title.grid(row=row, column=0, columnspan=3,
                         sticky='nsew')
        row += 1

        for player in self.game.players:
            points_label = tk.Label(stats_frame, text=f'{player.color.title()} Points:',
                                    anchor='w', bg=Theme.bg, fg=Theme.text)
            points_label.grid(row=row, column=0, sticky='ew', columnspan=2)
            points_display = tk.Label(stats_frame, text=f'{player.points}',
                                      anchor='e', bg=Theme.bg, fg=Theme.text)
            points_display.grid(row=row, column=2, sticky='ew', padx=8)
            player.points_display = points_display
            row += 1

            movement_label = tk.Label(stats_frame,
                                      text=f'{player.color.title()} Movements:',
                                      anchor='w', bg=Theme.bg, fg=Theme.text)
            movement_label.grid(row=row, column=0, sticky='ew', columnspan=2)
            movement_display = tk.Label(stats_frame,
                                        text=f'{player.movements}',
                                        anchor='e', bg=Theme.bg, fg=Theme.text)
            movement_display.grid(row=row, column=2, sticky='ew', padx=8)
            player.movements_display = movement_display
            row += 1

        timer_label = tk.Label(stats_frame, text='Time:', anchor='w',
                               bg=Theme.bg, fg=Theme.text)
        timer_label.grid(row=row, column=0, sticky='ew', columnspan=1)
        self.timer_display = tk.Label(stats_frame, anchor='e',
                                      text=f'{self.timer_val} ',
                                      bg=Theme.bg, fg=Theme.text)
        self.timer_display.grid(row=row, column=1, sticky='ew',
                                padx=8, ipady=4, columnspan=2)

        if self.address is not None:
            row += 1
            address_label = tk.Label(stats_frame,
                                     text=f'Address:',
                                     anchor='w', bg=Theme.bg, fg=Theme.text)
            address_label.grid(row=row, column=0, sticky='ew',
                               columnspan=2, pady=(30,0))
            address_display = tk.Label(stats_frame,
                                       text=f'{self.address[0]} ',
                                       anchor='e', bg=Theme.bg, fg=Theme.text)
            address_display.grid(row=row, column=2, sticky='ew',
                                 columnspan=2, pady=(30,0))
            row += 1
            port_label = tk.Label(stats_frame,
                                  text=f'Port:',
                                  anchor='w', bg=Theme.bg, fg=Theme.text)
            port_label.grid(row=row, column=0, sticky='ew', columnspan=2)
            port_display = tk.Label(stats_frame,
                                    text=f'{self.address[1]} ',
                                    anchor='e', bg=Theme.bg, fg=Theme.text)
            port_display.grid(row=row, column=2, sticky='ew', padx=8)

    def create_back_button(self):
        button_bd = tk.Frame(self.side_bar_frame,
                             highlightbackground=Theme.button_outline,
                             highlightthickness=2,
                             bd=0)
        button = tk.Button(button_bd,
                           text="Back <-",
                           bg=Theme.button_bg, fg=Theme.button_text,
                           bd=4, relief='flat',
                           activebackground=Theme.highlight,
                           activeforeground=Theme.highlight_text,
                           command=self.go_back)
        button_bd.pack(side='bottom', fill='x',
                       pady=GameScreen.BORDER_PADDING)
        button.pack(fill='both', expand=True, side='top')

    def go_back(self):
        if self.server is not None:
            self.server.close_server()
        self.game.quit()
        self.destroy()
        self.parent.root.resizable(True, True)
        self.parent.root.state(self.state)
        x_pos = ((self.parent.root.winfo_screenwidth() / 2)
                 - (self.original_width / 2))
        self.parent.root.geometry(f'{self.original_width}'
                                  f'x{self.original_height}+{int(x_pos)}+0')
        self.bread_crumbs.previous()(
            self.parent, self.bread_crumbs)


if __name__ == "__main__":
    import Main.ColourSchemes as ColourSchemes
    ColourSchemes.change_scheme(ColourSchemes.Dark())

    root = RootWindow(_width=500, _height=600, bg="light blue")
    main_menu = GameScreen(root, None, 2,
                           root.root.state(), (3, 3))

    root.mainloop()
