import tkinter as tk
from random import randrange

from .Maze import Maze


class Target:
    """Creates a Player Object"""

    def __init__(self, canvas: tk.Canvas, maze: Maze,
                 image=None):
        self.canvas = canvas
        self.maze = maze
        self.image = tk.PhotoImage(file=image)

        # Target is by default half the size of maze widths
        self.size = self.maze.half_size
        self.resize(self.size)

        self.abs_position = None
        self.maze_pos = None

        self.object = (self.canvas
                       .create_image(0, 0,
                                     image=self.image,
                                     anchor='nw'))

    def resize(self, size):
        width = self.image.width()
        height = self.image.height()
        # print(width, height)
        # print(size > width or size > height)
        # print(int(size / width))
        if size >= width or size >= height:
            self.image = self.image.zoom(
                int(size / width), int(size / height))
        else:
            # self.image = self.image.subsample(
            #     int(size / width), int(size / height))
            pass

    def update_position_in_maze(self):
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
        self.update_position_in_maze()
        self.abs_position = self.maze.position(self.object)


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

    p1 = Target(canvas_test, test_maze, "Flag.gif")
    p1.place_random()

    root.mainloop()
