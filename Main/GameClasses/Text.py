import tkinter as tk

from .Maze import Maze
from ColourSchemes import Scheme as Theme


class Text:
    """Creates a Player Object"""

    def __init__(self, canvas: tk.Canvas, maze: Maze, text, font_scale=1):
        self.canvas = canvas
        self.maze = maze
        self.text = text
        # Player is by default half the size of maze widths
        self.size = int(self.maze.size / 2 * font_scale)
        self.abs_position = None
        self.maze_pos = None

        self.object = (self.canvas
                       .create_text(0, 0,
                                    text=self.text,
                                    fill=Theme.button_text,
                                    font=(Theme.font_bold, self.size),
                                    anchor="center"))

        # End of __init__

    def update_text(self, text):
        self.canvas.itemconfigure(self.object, text=text)
        self.text = text

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
                          + (x_pos * self.maze.size),
                          self.maze.MAZE_TOP_LEFT[1]
                          + (y_pos * self.maze.size))
        self.update_position_in_maze()
        self.abs_position = self.maze.position(self.object)
        # End of function place


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
