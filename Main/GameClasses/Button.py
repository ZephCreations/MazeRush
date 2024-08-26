import tkinter as tk

from .Maze import Maze
from ColourSchemes import Scheme as Theme


class Button:
    """Creates a Player Object"""

    def __init__(self, canvas: tk.Canvas, maze: Maze, command=None, scale=1):
        self.canvas = canvas
        self.maze = maze
        # Button is by default three quarters the size of maze widths
        self.size = (self.maze.size / 2) * 1.5 * scale
        self.state = False
        self.can_toggle = False
        self.can_block = False
        self.command = command

        self.abs_position = None
        self.maze_pos = None

        self.players = []

        self.object = (self.canvas
                       .create_rectangle(0, 0,
                                         self.size, self.size,
                                         fill=Theme.button_bg,
                                         outline=Theme.button_outline))
        # End of __init__

    def toggle_state(self):
        # Change state to opposite (on to off and vice-versa)
        self.state = not self.state
        if self.state:
            # If on, display on
            self.canvas.itemconfigure(self.object, fill=Theme.highlight,
                                      outline=Theme.highlight_text)
        else:
            # Otherwise display off
            self.canvas.itemconfigure(self.object, fill=Theme.button_bg,
                                      outline=Theme.button_outline)

    def update_position_in_maze(self):
        x_coord, y_coord = self.maze.position(self.object)
        array_x = (x_coord - self.maze.MAZE_TOP_LEFT[0]
                   + (self.size / 2) + 1) / self.maze.size
        array_y = (y_coord - self.maze.MAZE_TOP_LEFT[1]
                   + (self.size / 2) + 1) / self.maze.size
        self.maze_pos = int(array_x), int(array_y)

    def place(self, x_pos, y_pos):
        self.maze.set_pos(self.object,
                          self.maze.MAZE_TOP_LEFT[0]
                          + (x_pos * self.maze.size) - self.size / 2,
                          self.maze.MAZE_TOP_LEFT[1]
                          + (y_pos * self.maze.size) - self.size / 2)
        self.update_position_in_maze()
        self.abs_position = self.maze.position(self.object)
        # End of function place

    def touching(self, player):
        # Check at same position
        value = (player.maze_pos[0] == self.maze_pos[0]
                 and player.maze_pos[1] == self.maze_pos[1])
        if value:
            # If button can toggle, change state
            if self.can_toggle:
                self.toggle_state()
            else:
                # Add the player to the players on the button
                self.players.append(player)
                # If button is off, toggle on
                if not self.state:
                    self.toggle_state()

        return value

    def left(self, player):
        # If button is off and the button can't toggle
        if not (self.can_toggle and self.state):
            # if the player was on the button
            if player in self.players:
                # If the player was the only one on the button
                if len(self.players) == 1:
                    self.toggle_state()
                # regardless remove player from button
                self.players.remove(player)

    def callback(self, *args, **kwargs):
        if self.command is not None:
            if not self.can_toggle and self.can_block:
                # If the button can't toggle, check if first player
                if len(self.players) == 1:
                    self.command(self, *args, **kwargs)
            else:
                self.command(self, *args, **kwargs)


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

    root.mainloop()
