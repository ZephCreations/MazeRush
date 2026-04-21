import tkinter as tk
import time

from ColourSchemes import Scheme as Theme
from .RootWindow import RootWindow
from GameClasses import GameCanvas
import GameLogic


class GameMenu(tk.Frame):
    BORDER_PADDING = 10

    def __init__(self, parent: RootWindow, bread_crumbs,
                 players: int, state,
                 menu_width=200, lobby=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

        self.parent = parent
        self.menu_width = menu_width
        self.no_players = players
        self.player_stats = []
        self.state = state
        self.original_width = self.parent.root.winfo_width()
        self.original_height = self.parent.root.winfo_height()

        self.exiting = False

        self.canvas: tk.Canvas = ...
        self.timer_display = None
        self.timer_running = False
        self.timer_val = 0.0000

        self.side_bar_frame = None
        self.stats_frame = None
        self.movement_display = None
        self.points_display = None

        self.parent.root.state('zoomed')
        self.parent.root.resizable(False, False)

        self.create_canvas()
        self.create_side_bar()
        self.create_stats_section()

        self.game = GameLogic.Game(self.canvas, players, self.parent.root, lobby)
        self.game.on_round_start.add_listener(self.start_timer)
        self.game.on_round_end.add_listener(self.pause_timer)
        self.game.on_new_round.add_listener(self.reset_timer)
        self.game.on_start_lobby.add_listener(self.wait_timer)

        self.add_player_stats()

        self.create_back_button()

        self.game.start_game()

        # End of __init__

    def create_canvas(self):
        self.canvas = GameCanvas(
            self, relief='solid', highlightthickness=4,
            highlightbackground=Theme.sec_bg,
            # highlightcolor=Theme.highlight,
            bg=Theme.maze_bg)
        self.canvas.pack(side='right', fill='both', expand=True)

        # self.canvas = Canvas(canvas)
        self.update()
        self.update_idletasks()

    def create_side_bar(self):
        self.side_bar_frame = tk.Frame(self, bg=Theme.bg,
                                       width=self.menu_width)
        self.side_bar_frame.pack_propagate(False)
        self.side_bar_frame.pack(side='left',
                                 padx=(GameMenu.BORDER_PADDING, 4),
                                 fill='both')

        title = tk.Label(self.side_bar_frame, text="Menu",
                         font=(Theme.font_bold, 20), pady=20,
                         bg=Theme.bg, fg=Theme.text)
        title.pack(side='top', fill='x')

        # End of function create_side_bar

    def create_stats_section(self):
        row = 0
        self.stats_frame = tk.Frame(self.side_bar_frame,
                               highlightbackground=Theme.highlight,
                               highlightthickness=4,
                               bg=Theme.bg)
        self.stats_frame.pack(side='top', fill='x', padx=12)
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)
        self.stats_frame.columnconfigure(2, weight=1)

        stats_title = tk.Label(self.stats_frame, text="Stats",
                               font=(Theme.font_bold, 18),
                               bg=Theme.bg, fg=Theme.text)
        stats_title.grid(row=row, column=0, columnspan=3,
                         sticky='nsew')

        row = 1 + self.no_players * 2
        timer_label = tk.Label(self.stats_frame, text='Time:', anchor='w',
                               bg=Theme.bg, fg=Theme.text)
        timer_label.grid(row=row, column=0, sticky='ew', columnspan=1)
        self.timer_display = tk.Label(self.stats_frame, anchor='e',
                                      text='0.0000',
                                      bg=Theme.bg, fg=Theme.text)
        self.timer_display.grid(row=row, column=1, sticky='ew',
                                padx=8, ipady=4, columnspan=2)

    def add_player_stats(self):
        row = 1

        for player in self.game.players:
            points_label = tk.Label(self.stats_frame, text=f'{player.color.title()} Points:',
                                    anchor='w', bg=Theme.bg, fg=Theme.text)
            points_label.grid(row=row, column=0, sticky='ew', columnspan=2)
            points_display = tk.Label(self.stats_frame, text=f'{player.points}',
                                      anchor='e', bg=Theme.bg, fg=Theme.text)
            points_display.grid(row=row, column=2, sticky='ew', padx=8)
            player.points_display = points_display
            row += 1

            movement_label = tk.Label(self.stats_frame,
                                      text=f'{player.color.title()} Movements:',
                                      anchor='w', bg=Theme.bg, fg=Theme.text)
            movement_label.grid(row=row, column=0, sticky='ew', columnspan=2)
            movement_display = tk.Label(self.stats_frame,
                                        text=f'{player.movements}',
                                        anchor='e', bg=Theme.bg, fg=Theme.text)
            movement_display.grid(row=row, column=2, sticky='ew', padx=8)

            # Listen for player movements
            player.on_move.add_listener(
                lambda points=0, disp=movement_display : (self.update_player_movements(points, disp))
            )
            player.on_point.add_listener(
                lambda points=0, disp=points_display : (self.update_player_points(points, disp))
            )
            row += 1

    def update_player_movements(self, movements, display: tk.Label):
        display.config(text=f'{movements}')

    def update_player_points(self, points, display: tk.Label):
        display.config(text=f'{points}')

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
                       pady=GameMenu.BORDER_PADDING)
        button.pack(fill='both', expand=True, side='top')

    def go_back(self):
        self.exiting = True
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

    def start_timer(self):
        self.timer_running = True
        self.after(10, self.update_timer, time.time())

    def update_timer(self, start_time):
        if self.timer_running and not self.exiting:
            timer_value = round(time.time() - start_time, 4)
            timer_value = self.convert_time(timer_value)
            self.timer_display.config(
                text=f'{timer_value}'
            )
            self.timer_val = timer_value
            self.after(10, self.update_timer, start_time)

    @staticmethod
    def convert_time(time_value):
        # Converts time into minutes and seconds
        minutes = time_value // 60
        time_value = time_value % 60
        minutes = minutes % 60
        return f"{int(minutes)}:" + "{:.4f}".format(time_value)

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_val = 00.000
        self.timer_display.config(text=f'{self.timer_val}')

    def wait_timer(self):
        self.timer_display.config(
            text=f'WAITING'
        )

if __name__ == "__main__":
    import Main.ColourSchemes as ColourSchemes
    ColourSchemes.change_scheme(ColourSchemes.Dark())

    root = RootWindow(_width=500, _height=600, bg="light blue")
    main_menu = GameMenu(root, None, 2,
                         root.root.state())

    root.mainloop()
