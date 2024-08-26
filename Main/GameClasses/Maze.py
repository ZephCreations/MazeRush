from random import shuffle, randrange
from ColourSchemes import Scheme as Theme
# from tail_recursion import tail_recursive, recurse


class Maze:
    def __init__(self, canvas, path_size=20, maze_width=20, maze_height=20, empty=False):
        # This defines variables to use later in the Class.
        # It also creates the lists that contain the walls
        # of the maze
        self.canvas = canvas
        self.size = path_size
        self.half_size = self.size / 2
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.MAZE_TOTAL_WIDTH = self.maze_width * self.size
        self.MAZE_TOTAL_HEIGHT = self.maze_height * self.size

        self.canvas.update()
        self.canvas_center_x = self.canvas.winfo_width() / 2
        self.canvas_center_y = self.canvas.winfo_height() / 2

        self.MAZE_TOP_LEFT = (int(
            self.canvas_center_x - (self.MAZE_TOTAL_WIDTH / 2)
            + self.half_size), int(
            self.canvas_center_y - (self.MAZE_TOTAL_HEIGHT / 2)
            + self.half_size))
        ''' Maze top left is the center of the grid square'''
        self.MAZE_BOTTOM_RIGHT = (int(
            self.canvas_center_x + (self.MAZE_TOTAL_WIDTH / 2)
            + self.half_size), int(
            self.canvas_center_y + (self.MAZE_TOTAL_HEIGHT / 2)
            + self.half_size))
        ''' Maze bottom right is the center of the grid square'''

        # Reference object used to draw maze
        self.reference = self.canvas.create_rectangle(self.half_size, self.half_size,
                                                      self.half_size, self.half_size,
                                                      outline='')
        self.horizontal, self.vertical = None, None
        if empty:
            self.create_empty_maze()
        else:
            self.create_maze()

        # End of __init__

    def create_empty_maze(self):
        solid_row = [[" --"] * self.maze_width + [" "]]
        # print(solid_row)
        hor = solid_row + [
            ["   "] * self.maze_width + [' ']
            for _ in range(self.maze_height - 1)
        ] + solid_row
        # print(hor)
        ver = ([
            ["|  "] + ["   "] * (self.maze_width - 1) + ["|"]
            for _ in range(self.maze_height)] + [[]])

        self.horizontal = hor
        self.vertical = ver

    def create_maze(self):
        # This is the original code for the maze
        visited = (
                [[0] * self.maze_width + [1]
                 for _ in range(self.maze_height)]
                + [[1] * (self.maze_width + 1)]
        )
        ver = ([["|  "] * self.maze_width + ['|']
                for _ in range(self.maze_height)]
               + [[]])
        hor = [[" --"] * self.maze_width + [' ']
               for _ in range(self.maze_height + 1)]

        def walk(x, y):
            visited[y][x] = 1
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if visited[yy][xx]:
                    continue
                # Remove horizontal wall, turns "-" into " "
                if xx == x:
                    hor[max(y, yy)][x] = "   "
                # Remove vertical wall, turns "|" into " "
                if yy == y:
                    ver[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(randrange(self.maze_width),
             randrange(self.maze_height))

        self.horizontal, self.vertical = hor, ver
        # print(hor)

    def draw_maze(self):
        self.draw_maze_section(self.horizontal)
        self.draw_maze_section(self.vertical)

    def draw_maze_section(self, wall_list):
        # This draw the lines for the maze, moving a reference object to do so.
        self.set_pos(self.reference,
                     self.MAZE_TOP_LEFT[0], self.MAZE_TOP_LEFT[1])
        displacement_x = self.MAZE_TOP_LEFT[0]
        displacement_y = self.MAZE_TOP_LEFT[1]

        for sublist in wall_list:
            for wall in sublist:
                if wall == ' --':
                    self.draw_wall('A')
                elif wall == '|  ' or wall == '|':
                    self.draw_wall('L')
                # Move reference to next cell across
                self.canvas.move(self.reference,
                                 self.size, 0)

            # Move reference down
            displacement_y += self.size
            self.set_pos(self.reference,
                         displacement_x, displacement_y)

    def draw_wall(self, side):
        # This draws a wall above or to the left of the reference object
        x_coord, y_coord = self.position(self.reference)
        if side == 'L':
            # Left
            self.canvas.create_line(x_coord-self.half_size,
                                    y_coord-self.half_size,
                                    x_coord-self.half_size,
                                    y_coord+self.half_size,
                                    width=1, fill=Theme.text)
        elif side == 'A':
            # Above
            self.canvas.create_line(x_coord-self.half_size,
                                    y_coord-self.half_size,
                                    x_coord+self.half_size,
                                    y_coord-self.half_size,
                                    width=1, fill=Theme.text)
        # End of function draw_wall

    def clear(self):
        self.canvas.delete("all")

    def position(self, item):
        # This returns the top-left coordinates of the item
        pos = self.canvas.coords(item)
        del pos[2:]
        return pos

    def set_pos(self, item, x, y):
        # This sets the position of the item,
        # using the top-left coords as reference
        x_coord, y_coord = self.position(item)
        x_move = x - x_coord
        y_move = y - y_coord
        self.canvas.move(item, x_move, y_move)

    def __str__(self):
        # Used for debugging purposes
        return f'{self.horizontal}, {self.vertical}'


if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    # root.state('zoomed')
    canvas_test = tk.Canvas(root)
    canvas_test.pack(side='top', fill='both', expand=True)
    maze = Maze(canvas_test, 10,
                3, 3)
    maze.draw_maze()

    root.mainloop()
