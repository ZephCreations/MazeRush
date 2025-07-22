import tkinter as tk
from math import copysign
from random import randrange

from .Maze import Maze
from Settings import Settings


class Player:
    """Creates a Player Object"""

    def __init__(self, canvas: tk.Canvas,
                 color='black', game=None,
                 player_no=0):
        self.canvas = canvas
        self.maze = None
        self.color = color
        self.game = game
        self.size = 0
        self.player_no = player_no

        self.abs_position = None
        self.maze_pos = None
        self.prev_pos = None
        self.movements = 0
        self.movements_display = None
        self.points = 0
        self.points_display = None
        self.object = None

    def assign_maze(self, maze: Maze):
        self.maze = maze
        # Player is by default half the size of maze widths
        self.size = self.maze.half_size

    def draw_player(self):
        self.object = (self.canvas
                       .create_rectangle(0, 0,
                                         self.size, self.size,
                                         fill=self.color,
                                         outline=''))
        # End of function draw_player

    def update_position_in_maze(self, display=False):
        x_coord, y_coord = self.maze.position(self.object)
        array_x = (x_coord - self.maze.MAZE_TOP_LEFT[0]
                   + (self.size / 2)) / self.maze.size
        array_y = (y_coord - self.maze.MAZE_TOP_LEFT[1]
                   + (self.size / 2)) / self.maze.size
        self.maze_pos = int(array_x), int(array_y)

    def place_random(self):
        # This places the player randomly in the maze.
        x_pos = randrange(0,self.maze.maze_width)
        y_pos = randrange(0,self.maze.maze_width)

        self.place(x_pos, y_pos)
        # End of function place_random

    def place(self, x_pos, y_pos):
        self.maze.set_pos(self.object,
                          self.maze.MAZE_TOP_LEFT[0]
                          + (x_pos * self.maze.size) - self.size / 2,
                          self.maze.MAZE_TOP_LEFT[1]
                          + (y_pos * self.maze.size) - self.size / 2)
        self.update_position_in_maze(True)
        self.abs_position = self.maze.position(self.object)
        # End of function places

    def move_right(self, event):
        self.move("R")

    def move_left(self, event):
        self.move("L")

    def move_up(self, event):
        self.move("U")

    def move_down(self, event):
        self.move("D")

    def move(self, direction):
        if not self.game.exiting:
            # print(f"Move: {direction}")
            self.movements += 1
            self.movements_display.config(text=f'{self.movements}')
            # Update position
            self.update_position_in_maze()

            # Set Values
            check_x, check_y = self.maze_pos[0], self.maze_pos[1]
            move_x, move_y = 0, 0

            # Check direction
            if direction == "U":
                move_y -= self.maze.size
                check_y -= 1
            elif direction == "D":
                move_y += self.maze.size
                check_y += 1
            elif direction == "L":
                move_x -= self.maze.size
                check_x -= 1
            elif direction == "R":
                move_x += self.maze.size
                check_x += 1

            check_walls_exist = self.check_wall(check_x, check_y)
            if not check_walls_exist:
                self.prev_pos = self.maze.position(self.object)
                self.canvas.move(self.object, move_x, move_y)
                self.abs_position = self.maze.position(self.object)
                if Settings.SHOW_TRAILS:
                    self.draw_trail()
                self.update_position_in_maze()

            self.canvas.tag_raise(self.object)
            # self.canvas.update_idletasks()
            self.game.player_moved(self)
        # End of move function

    def check_wall(self, x_check, y_check):
        # This checks the co-ords between the player
        # and the check square for wall, returning
        # None if there isn't a wall.

        if self.maze_pos[0] < 0 or self.maze_pos[1] < 0:
            return "outside map"

        # walls_to_use = None
        if self.maze_pos[0] != x_check:
            # Horizontal movement
            walls_to_use = self.maze.vertical
            if x_check == self.maze_pos[0] - 1:
                x_check = self.maze_pos[0]
        else:
            # Vertical movement
            walls_to_use = self.maze.horizontal
            if y_check == self.maze_pos[1] - 1:
                y_check = self.maze_pos[1]

        try:
            walls = walls_to_use[y_check][x_check]
            if walls == "|  " or walls == "|":
                return "wall"
            elif walls == " --":
                return "wall"
            else:
                return None
        except IndexError:
            return 'outside'

        # End of function check_wall

    def draw_trail(self):
        x_pos, y_pos = self.abs_position
        prev_x, prev_y = self.prev_pos

        ratio = self.player_no / (self.game.no_players - 1)
        span = self.size / 2
        level_offset = span

        if x_pos - prev_x == 0:
            level_offset = (span * ratio) - (span / 2) + span
        elif y_pos - prev_y == 0:
            level_offset = (span * ratio) - (span / 2) + span

        from_x = prev_x + level_offset
        from_y = prev_y + level_offset
        to_x = x_pos + level_offset
        to_y = y_pos + level_offset

        line_width = self.size / self.game.no_players / 2
        line = self.canvas.create_line(from_x, from_y, to_x, to_y,
                                       width=line_width,
                                       fill=self.color,
                                       stipple='gray50')

        self.canvas.tag_lower(line)

    def reset(self):
        self.movements = 0
        self.movements_display.config(text=f'{self.movements}')
        self.canvas.delete(self.object)
        self.object = None
        self.abs_position = None
        self.maze_pos = None
        self.prev_pos = None
        self.size = 0
        self.maze = None


if __name__ == "__main__":
    import tkinter as tk
    import Maze

    root = tk.Tk()
    # root.state('zoomed')
    canvas_test = tk.Canvas(root)
    canvas_test.pack(side='top', fill='both', expand=True)
    test_maze = Maze.Maze(canvas_test, 20,
                          10, 5, True)
    test_maze.draw_maze()

    p1 = Player(canvas_test)
    p1.assign_maze(test_maze)
    p1.draw_player()
    p1.place_random()

    root.mainloop()
