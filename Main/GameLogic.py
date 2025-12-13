from Settings import Settings
from Events import Event
from GameClasses import Maze, Player, Target, Button, Text
from ColourSchemes import Scheme as Theme
from Input import InputController
import time


class Game:

    def __init__(self, canvas, no_players, root, border_padding, has_lobby=False):
        self._canvas = canvas
        self.root = root
        self._lobby = has_lobby
        self._border_padding = border_padding
        self._buttons = []
        self._size_label = self._points_label = None
        self._maze = None
        self._target = None
        self._maze_size = Settings.DEFAULT_MAZE_SIZE

        self.no_players = no_players
        self.players= []
        self.exiting = False

        self.on_new_round: Event = Event()
        self.on_round_start: Event = Event()
        self.on_round_end: Event = Event()
        self.on_start_lobby: Event = Event()

        self.create_players()

    def start_game(self):
        if not self.exiting:
            self.full_reset_game()
            self._canvas.update_idletasks()
            self.start_new_round(text="New Game:")
        # End of function start_game

    def start_new_round(self, text="New Round in:"):
        if not self.exiting:
            self.reset_round()
            if self._lobby:
                self.start_new_round_after_countdown()
            else:
                self.countdown(text)
        # End of function start_new_round

    def start_new_round_after_countdown(self):
        self.create_maze()

        if not self._lobby:
            self.add_target()
        self.add_players()

        if self._lobby:
            self.add_buttons()
            self.on_start_lobby.trigger()
        if not self._lobby:
            self.on_round_start.trigger()

    def countdown(self, title="New Game in:"):
        title_text, title_text_bg = (
            self._canvas.display_text(
                title, Theme.text,
                offset=(0, -100)))
        self.root.after(1000,
                        self.display_countdown_number,
                        3, None, None,
                        title_text, title_text_bg)
        # End of function countdown

    def display_countdown_number(self, number,
                                 text=None, text_bg=None,
                                 title=None, title_bg=None):
        if not self.exiting:
            self.clear_text(text, text_bg)
            if number == 0:
                # Countdown Finished
                self.clear_text(title, title_bg)
                self.start_new_round_after_countdown()

            else:
                _text, _text_bg = (
                    self._canvas.display_text(f'{number}', Theme.text,
                                              (Theme.font_bold, 100),
                                              offset=(0, 100)))
                self._canvas.update_idletasks()
                self.root.after(750, self.display_countdown_number,
                                number - 1, _text, _text_bg,
                                title, title_bg)
        # End of function display_countdown_timer

    def create_maze(self):
        hor_path_size_ = int((self._canvas.winfo_width()
                              - self._border_padding * 10
                              ) / self._maze_size[0])
        ver_path_size_ = int((self._canvas.winfo_height()
                              - self._border_padding * 10
                              ) / self._maze_size[1])

        path_size = hor_path_size_
        if hor_path_size_ > ver_path_size_:
            path_size = ver_path_size_

        self._maze = Maze(self._canvas, path_size,
                          self._maze_size[0],
                          self._maze_size[1],
                          self._lobby)
        self._maze.draw_maze()

        # End of function create_maze

    def add_target(self):
        self._target = Target(self._canvas,
                              self._maze,
                              image="./GameClasses/Flag.gif")
        # self.target.place(2, 2)
        self._target.place_random()

    def create_player(self, colour, number):
        # if default_key_binds:
        #     key_binds = self.key_binds[0]
        # else:
        #     key_binds = self.key_binds[number]
        player = Player(self._canvas,
                        colour,
                        self,
                        number)
        self.players.append(player)

        # Add event listeners for movement
        action_map = InputController().get_map(f"Player_{number+1}")
        action_map.get_action("Move_Left").onAction.add_listener(player.move_left)
        action_map.get_action("Move_Right").onAction.add_listener(player.move_right)
        action_map.get_action("Move_Up").onAction.add_listener(player.move_up)
        action_map.get_action("Move_Down").onAction.add_listener(player.move_down)

        return player 

    def create_players(self):
        colours = ["red", "blue", "green", "orange"]

        for player_no in range(0, self.no_players):
            self.create_player(colours[player_no], player_no)

        # End of function create_players

    def add_player(self, player):
        player.assign_maze(self._maze)
        player.draw_player()
        if self._lobby:
            size = self._maze_size
            player.place(int((size[0] - 1) / 2),
                         int((size[1] - 1) / 2))
        else:
            player.place_random()

        # Enable key binds
        InputController().get_map(f"Player_{player.player_no}").enable_map()

        # self.bind_keys(player, player.movement_keys)

    def add_players(self):

        for player in self.players:
            player.assign_maze(self._maze)
            player.draw_player()
            if self._lobby:
                size = self._maze_size
                player.place(int((size[0] - 1) / 2),
                             int((size[1] - 1) / 2))
            else:
                player.place_random()
            InputController().get_map(f"Player_{player.player_no + 1}").enable_map()
            # self.bind_keys(player, player.movement_keys)
        # End of function add_players

    def add_buttons(self):
        x_pos = 4
        y_center = (self._maze_size[1] - 1) // 2
        x_center = (self._maze_size[0] - 1) // 2

        # Plus Button and Label
        text_title = Text(self._canvas, self._maze,
                          "Maze Size")
        text_title.place(x_pos, y_center - 3)
        text = Text(self._canvas, self._maze,
                    "+")
        text.place(x_pos, y_center - 2)
        text = Text(self._canvas, self._maze,
                    "-")
        text.place(x_pos, y_center + 1)
        self._size_label = Text(self._canvas, self._maze,
                               f"{Settings.DEFAULT_MAZE_SIZE}")
        self._size_label.place(x_pos - 2, y_center - 1.5)

        button = Button(self._canvas, self._maze,
                        self.player_hit_plus_button)
        button.place(x_pos, y_center - 1)
        button.can_block = True
        self._buttons.append(button)
        button = Button(self._canvas, self._maze,
                        self.player_hit_minus_button)
        button.place(x_pos, y_center)
        button.can_block = True
        self._buttons.append(button)

        # Points to Win Button
        text_title = Text(self._canvas, self._maze,
                          "Points to Win")
        text_title.place(self._maze_size[0] - x_pos - 1, y_center - 3)
        text = Text(self._canvas, self._maze,
                    "+")
        text.place(self._maze_size[0] - x_pos - 1, y_center - 2)
        text = Text(self._canvas, self._maze,
                    "-")
        text.place(self._maze_size[0] - x_pos - 1, y_center + 1)
        self._points_label = Text(self._canvas, self._maze,
                               f"{Settings.POINTS_TO_WIN}")
        self._points_label.place(self._maze_size[0] - x_pos + 1, y_center - 1.5)

        button = Button(self._canvas, self._maze,
                        self.player_hit_points_plus_button)
        button.place(self._maze_size[0] - x_pos - 1, y_center - 1)
        button.can_block = True
        self._buttons.append(button)
        button = Button(self._canvas, self._maze,
                        self.player_hit_points_minus_button)
        button.place(self._maze_size[0] - x_pos - 1, y_center)
        button.can_block = True
        self._buttons.append(button)

        # Toggle Trail Button
        toggle = Button(self._canvas, self._maze,
                        self.toggle_trail)
        toggle.place(x_center, self._maze_size[1] - x_pos - 1)
        toggle.can_toggle = True
        text = Text(self._canvas, self._maze,
                    "Toggle Trails")
        text.place(x_center, self._maze_size[1] - x_pos)
        self._buttons.append(toggle)
        if Settings.SHOW_TRAILS:
            toggle.toggle_state()

        # Start Button
        # TODO update colour of Start button
        start_button = Button(self._canvas, self._maze,
                              self.start_button_check, 5 / 3)
        start_button.place(x_center, x_pos)
        text = Text(self._canvas, self._maze,
                    "~ PLAY ~", 2.5)
        text.place(x_center, x_pos - 2)
        self._buttons.append(start_button)

        # Update default maze size
        self._maze_size = Settings.DEFAULT_MAZE_SIZE

        # End of function add_button

    def player_hit_plus_button(self, button, player):
        if self._maze_size[0] >= Settings.MAX_MAZE_SIZE[0]:
            return
        self._maze_size = (self._maze_size[0] + 1,
                           self._maze_size[1] + 1)
        self._size_label.update_text(f"{self._maze_size}")

    def player_hit_minus_button(self, button, player):
        if self._maze_size[0] <= Settings.MIN_MAZE_SIZE[0]:
            return
        self._maze_size = (self._maze_size[0] - 1,
                           self._maze_size[1] - 1)
        self._size_label.update_text(f"{self._maze_size}")

    def player_hit_points_plus_button(self, button, player):
        if Settings.POINTS_TO_WIN >= Settings.MAX_POINTS:
            return
        Settings.POINTS_TO_WIN += 1
        self._points_label.update_text(f"{Settings.POINTS_TO_WIN}")

    def player_hit_points_minus_button(self, button, player):
        if Settings.POINTS_TO_WIN <= Settings.MIN_POINTS:
            return
        Settings.POINTS_TO_WIN -= 1
        self._points_label.update_text(f"{Settings.POINTS_TO_WIN}")

    def toggle_trail(self, button, player):
        Settings.SHOW_TRAILS = not Settings.SHOW_TRAILS
        if Settings.SHOW_TRAILS:
            Settings.SHOW_TRAILS_DISPLAY = "Show"
        else:
            Settings.SHOW_TRAILS_DISPLAY = "Hide"

    def start_button_check(self, button, player):
        # print(f"Players: {len(self.players)}     Button: {len(button.players)}")
        if len(button.players) == len(self.players):
            self._lobby = False
            self.start_game()

    def player_moved(self, player):
        # Update player position with server if needed
        if not self._lobby:
            # Check if at flag
            if (player.maze_pos[0] == self._target.maze_pos[0]
                    and player.maze_pos[1] == self._target.maze_pos[1]):
                player.points += 1
                self.win_process(player)

        # Check if at button
        if self._lobby:
            for button in self._buttons:
                if button.touching(player):
                    # Player at button
                    button.callback(player)
                else:
                    button.left(player)
        # End of function player_moved

    def win_process(self, player: Player):
        if not self.exiting:
            self.on_round_end.trigger()
            InputController().disable_all()

            # Check if all points are achieved
            if player.points >= Settings.POINTS_TO_WIN:
                # All points are achieved
                # print(f"{player.color} has gotten all the points")
                text = f'{player.color} Wins!!!'.title()
                win_text, win_text_bg = self._canvas.display_text(text, player.color)
                self._lobby = True
                self.root.after(4000, lambda: (
                    self.clear_text(win_text, win_text_bg),
                    self.start_game()))
            else:
                # More points needed
                text = f'Point for {player.color}!!'.title()

                win_text, win_text_bg = self._canvas.display_text(text, player.color)
                self.root.after(3000, lambda: (
                    self.clear_text(win_text, win_text_bg),
                    self.start_new_round()))

        # End of function win_process

    def clear_text(self, *text):
        if not self.exiting:
            for text_object in text:
                self._canvas.delete(text_object)
        # End of function clear_text

    def reset_round(self):
        self.on_new_round.trigger()
        for player in self.players:
            player.reset()
        self._canvas.delete("all")
        self._canvas.update_idletasks()
        self._buttons = []
        if self._lobby:
            self._maze_size = (19, 19)

    def full_reset_game(self):
        self.reset_round()

        for player in self.players:
            player.points = 0
        # End function reset_game

    def quit(self):
        InputController().disable_all()
        self.exiting = True
