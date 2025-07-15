from Settings import Settings
from GameClasses import Maze, Player, Target, Button, Text
from ColourSchemes import Scheme as Theme
from Input import InputController
import time


class Game:
    def __init__(self,
                 game_screen,
                 has_lobby=False):
        self.game_screen = game_screen
        self.lobby = has_lobby
        self.buttons = []
        self.size_label = self.points_label = None
        self.maze = None
        self.target = None
        self.maze_size = Settings.DEFAULT_MAZE_SIZE
        self.no_players = self.game_screen.no_players
        self.players: [Player] = []
        self.exiting = False
        self.timer_running = False

        self.create_players()

    def start_game(self):
        if not self.exiting:
            self.full_reset_game()
            self.game_screen.canvas.update_idletasks()
            self.start_new_round(text="New Game:")
        # End of function start_game

    def start_new_round(self, text="New Round in:"):
        if not self.exiting:
            self.reset_round()
            if self.lobby:
                self.start_new_round_after_countdown()
            else:
                self.countdown(text)
        # End of function start_new_round

    def start_new_round_after_countdown(self):
        self.create_maze()

        if not self.lobby:
            self.add_target()
        self.add_players()

        if self.lobby:
            self.add_buttons()
            self.game_screen.timer_display.config(
                text=f'WAITING'
            )
        if not self.lobby:
            self.timer_running = True
            self.game_screen.parent.root.after(
                0, lambda val1=time.time(): self.update_timer(val1))

    def countdown(self, title="New Game in:"):
        title_text, title_text_bg = (
            self.display_text(
                title, Theme.text,
                offset=(0, -100)))
        self.game_screen.after(1000,
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
                    self.display_text(f'{number}', Theme.text,
                                      (Theme.font_bold, 100),
                                      offset=(0, 100)))
                self.game_screen.canvas.update_idletasks()
                root = self.game_screen.parent.root
                root.after(750, self.display_countdown_number,
                           number - 1, _text, _text_bg,
                           title, title_bg)
        # End of function display_countdown_timer

    def create_maze(self):
        hor_path_size_ = int((self.game_screen.canvas_width
                              - self.game_screen.BORDER_PADDING * 10
                              ) / self.maze_size[0])
        ver_path_size_ = int((self.game_screen.canvas_height
                              - self.game_screen.BORDER_PADDING * 10
                              ) / self.maze_size[1])

        path_size = hor_path_size_
        if hor_path_size_ > ver_path_size_:
            path_size = ver_path_size_

        self.maze = Maze(self.game_screen.canvas, path_size,
                         self.maze_size[0],
                         self.maze_size[1],
                         self.lobby)
        self.maze.draw_maze()

        # End of function create_maze

    def add_target(self):
        self.target = Target(self.game_screen.canvas,
                             self.maze,
                             image="./GameClasses/Flag.gif")
        # self.target.place(2, 2)
        self.target.place_random()

    def create_player(self, colour, number):
        # if default_key_binds:
        #     key_binds = self.key_binds[0]
        # else:
        #     key_binds = self.key_binds[number]
        player = Player(self.game_screen.canvas,
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
        player.assign_maze(self.maze)
        player.draw_player()
        if self.lobby:
            size = self.maze_size
            player.place(int((size[0] - 1) / 2),
                         int((size[1] - 1) / 2))
        else:
            player.place_random()

        # Enable key binds
        InputController().get_map(f"Player_{player.player_no}").enable_map()

        # self.bind_keys(player, player.movement_keys)

    def add_players(self):

        for player in self.players:
            player.assign_maze(self.maze)
            player.draw_player()
            if self.lobby:
                size = self.maze_size
                player.place(int((size[0] - 1) / 2),
                             int((size[1] - 1) / 2))
            else:
                player.place_random()
            InputController().get_map(f"Player_{player.player_no + 1}").enable_map()
            # self.bind_keys(player, player.movement_keys)
        # End of function add_players

    def add_buttons(self):
        x_pos = 4
        y_center = (self.maze_size[1] - 1) // 2
        x_center = (self.maze_size[0] - 1) // 2

        # Plus Button and Label
        text_title = Text(self.game_screen.canvas, self.maze,
                          "Maze Size")
        text_title.place(x_pos, y_center - 3)
        text = Text(self.game_screen.canvas, self.maze,
                    "+")
        text.place(x_pos, y_center - 2)
        text = Text(self.game_screen.canvas, self.maze,
                    "-")
        text.place(x_pos, y_center + 1)
        self.size_label = Text(self.game_screen.canvas, self.maze,
                               f"{Settings.DEFAULT_MAZE_SIZE}")
        self.size_label.place(x_pos - 2, y_center - 1.5)

        button = Button(self.game_screen.canvas, self.maze,
                        self.player_hit_plus_button)
        button.place(x_pos, y_center - 1)
        button.can_block = True
        self.buttons.append(button)
        button = Button(self.game_screen.canvas, self.maze,
                        self.player_hit_minus_button)
        button.place(x_pos, y_center)
        button.can_block = True
        self.buttons.append(button)

        # Points to Win Button
        text_title = Text(self.game_screen.canvas, self.maze,
                          "Points to Win")
        text_title.place(self.maze_size[0] - x_pos - 1, y_center - 3)
        text = Text(self.game_screen.canvas, self.maze,
                    "+")
        text.place(self.maze_size[0] - x_pos - 1, y_center - 2)
        text = Text(self.game_screen.canvas, self.maze,
                    "-")
        text.place(self.maze_size[0] - x_pos - 1, y_center + 1)
        self.points_label = Text(self.game_screen.canvas, self.maze,
                               f"{Settings.POINTS_TO_WIN}")
        self.points_label.place(self.maze_size[0] - x_pos + 1, y_center - 1.5)

        button = Button(self.game_screen.canvas, self.maze,
                        self.player_hit_points_plus_button)
        button.place(self.maze_size[0] - x_pos - 1, y_center - 1)
        button.can_block = True
        self.buttons.append(button)
        button = Button(self.game_screen.canvas, self.maze,
                        self.player_hit_points_minus_button)
        button.place(self.maze_size[0] - x_pos - 1, y_center)
        button.can_block = True
        self.buttons.append(button)

        # Toggle Trail Button
        toggle = Button(self.game_screen.canvas, self.maze,
                        self.toggle_trail)
        toggle.place(x_center, self.maze_size[1] - x_pos - 1)
        toggle.can_toggle = True
        text = Text(self.game_screen.canvas, self.maze,
                    "Toggle Trails")
        text.place(x_center, self.maze_size[1] - x_pos)
        self.buttons.append(toggle)
        if Settings.SHOW_TRAILS:
            toggle.toggle_state()

        # Start Button
        # TODO update colour of Start button
        start_button = Button(self.game_screen.canvas, self.maze,
                              self.start_button_check, 5/3)
        start_button.place(x_center, x_pos)
        text = Text(self.game_screen.canvas, self.maze,
                    "~ PLAY ~", 2.5)
        text.place(x_center, x_pos - 2)
        self.buttons.append(start_button)

        # Update default maze size
        self.maze_size = Settings.DEFAULT_MAZE_SIZE

        # End of function add_button

    def player_hit_plus_button(self, button, player):
        if self.maze_size[0] >= Settings.MAX_MAZE_SIZE[0]:
            return
        self.maze_size = (self.maze_size[0] + 1,
                          self.maze_size[1] + 1)
        self.size_label.update_text(f"{self.maze_size}")

    def player_hit_minus_button(self, button, player):
        if self.maze_size[0] <= Settings.MIN_MAZE_SIZE[0]:
            return
        self.maze_size = (self.maze_size[0] - 1,
                          self.maze_size[1] - 1)
        self.size_label.update_text(f"{self.maze_size}")

    def player_hit_points_plus_button(self, button, player):
        if Settings.POINTS_TO_WIN >= Settings.MAX_POINTS:
            return
        Settings.POINTS_TO_WIN += 1
        self.points_label.update_text(f"{Settings.POINTS_TO_WIN}")

    def player_hit_points_minus_button(self, button, player):
        if Settings.POINTS_TO_WIN <= Settings.MIN_POINTS:
            return
        Settings.POINTS_TO_WIN -= 1
        self.points_label.update_text(f"{Settings.POINTS_TO_WIN}")

    def toggle_trail(self, button, player):
        Settings.SHOW_TRAILS = not Settings.SHOW_TRAILS
        if Settings.SHOW_TRAILS:
            Settings.SHOW_TRAILS_DISPLAY = "Show"
        else:
            Settings.SHOW_TRAILS_DISPLAY = "Hide"

    def start_button_check(self, button, player):
        # print(f"Players: {len(self.players)}     Button: {len(button.players)}")
        if len(button.players) == len(self.players):
            self.lobby = False
            self.start_game()

    def bind_keys(self, player, keys: list):
        # print(f"Player: {player.color}\n Keys: {keys}")
        root = self.game_screen.parent.root
        root.bind(keys[0], lambda event: player.move_up(event))
        root.bind(keys[1], lambda event: player.move_left(event))
        root.bind(keys[2], lambda event: player.move_down(event))
        root.bind(keys[3], lambda event: player.move_right(event))
        if len(keys) > 4:
            root.bind(keys[4], lambda event: player.move_up(event))
            root.bind(keys[5], lambda event: player.move_left(event))
            root.bind(keys[6], lambda event: player.move_down(event))
            root.bind(keys[7], lambda event: player.move_right(event))
        # End of function bind_keys

    def unbind_all_keys(self):
        root = self.game_screen.parent.root
        for player_no in range(0, self.no_players):
            keys = self.key_binds[player_no]
            root.unbind(keys[0])
            root.unbind(keys[1])
            root.unbind(keys[2])
            root.unbind(keys[3])
            if len(keys) > 4:
                root.unbind(keys[4])
                root.unbind(keys[5])
                root.unbind(keys[6])
                root.unbind(keys[7])

        # End of function unbind_all_keys

    def player_moved(self, player):
        # Update player position with server if needed
        if not self.lobby:
            # Check if at flag
            if (player.maze_pos[0] == self.target.maze_pos[0]
                    and player.maze_pos[1] == self.target.maze_pos[1]):
                player.points += 1
                player.points_display.config(text=f'{player.points}')
                self.win_process(player)

        # Check if at button
        if self.lobby:
            for button in self.buttons:
                if button.touching(player):
                    # Player at button
                    button.callback(player)
                else:
                    button.left(player)
        # End of function player_moved

    def win_process(self, player: Player):
        if not self.exiting:
            self.timer_running = False
            InputController().disable_all()
            # self.unbind_all_keys()
            root = self.game_screen.parent.root

            # Check if all points are achieved
            if player.points >= Settings.POINTS_TO_WIN:
                # All points are achieved
                # print(f"{player.color} has gotten all the points")
                text = f'{player.color} Wins!!!'.title()
                win_text, win_text_bg = self.display_text(text,
                                                          player.color)
                self.lobby = True
                root.after(4000, lambda: (
                    self.clear_text(win_text, win_text_bg),
                    self.start_game()))
            else:
                # More points needed
                text = f'Point for {player.color}!!'.title()

                win_text, win_text_bg = self.display_text(text,
                                                          player.color)
                root.after(3000, lambda: (
                    self.clear_text(win_text, win_text_bg),
                    self.start_new_round()))

        # End of function win_process

    def display_text(self, text, colour,
                     font=(Theme.font_bold, 56),
                     outline=None,
                     offset=(0, 0)):
        if outline is None:
            outline = Theme.button_outline
        canvas = self.game_screen.canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        center_position = (canvas_width / 2 + offset[0],
                           canvas_height / 2 + offset[1])

        text = canvas.create_text(center_position,
                                  text=text, fill=colour,
                                  font=font, anchor='center')
        text_bounds = canvas.bbox(text)
        text_bg = canvas.create_rectangle(
            text_bounds[0] - 10, text_bounds[1] - 10,
            text_bounds[2] + 10, text_bounds[3] + 10,
            fill=Theme.bg, outline=outline, width=1
        )
        canvas.tag_raise(text_bg)
        canvas.tag_raise(text)
        canvas.update_idletasks()

        return text, text_bg
        # End of function display_text

    def clear_text(self, *text):
        if not self.exiting:
            for text_object in text:
                self.game_screen.canvas.delete(text_object)
        # End of function clear_text

    def update_timer(self, start_time):
        screen = self.game_screen
        if self.timer_running and not self.exiting:
            timer_value = round(time.time() - start_time, 4)
            timer_value = self.convert_time(timer_value)
            screen.timer_display.config(
                text=f'{timer_value}'
            )
            screen.timer_val = timer_value
            screen.parent.root.after(
                10, lambda var1=start_time: self.update_timer(start_time)
            )

    @staticmethod
    def convert_time(time_value):
        # Converts time into minutes and seconds
        minutes = time_value // 60
        time_value = time_value % 60
        minutes = minutes % 60
        return f"{int(minutes)}:" + "{:.4f}".format(time_value)

    def reset_round(self):
        self.game_screen.timer_val = 00.000
        self.game_screen.timer_display.config(
            text=f'{self.game_screen.timer_val}')
        for player in self.players:
            player.reset()
        self.game_screen.canvas.delete("all")
        self.game_screen.canvas.update_idletasks()
        self.buttons = []
        if self.lobby:
            self.maze_size = (19, 19)

    def full_reset_game(self):
        self.reset_round()

        for player in self.players:
            player.points = 0
            player.points_display.config(text=f'{player.points}')
        # End function reset_game

    def quit(self):
        InputController().disable_all()
        self.exiting = True
