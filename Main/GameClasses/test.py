from tail_recursion import recurse, tail_recursive

MAZE_WIDTH = MAZE_HEIGHT = 3
# Creates a grid of zeroes, with a 1
# on the outer right and bottom
visited = (
        [[0] * MAZE_WIDTH + [1]
         for _ in range(MAZE_HEIGHT)]
        + [[1] * (MAZE_WIDTH + 1)]
)
# Creates a grid of "|  ", with a "|"
# on the outer right and a blank row at the bottom
ver = ([["|  "] * MAZE_WIDTH + ['|']
        for _ in range(MAZE_HEIGHT)]
       + [[]])
# Creates a grid of " --", with a " "
# on the outer right and the same row at the bottom
hor = [[" --"] * MAZE_WIDTH + [' ']
       for _ in range(MAZE_HEIGHT + 1)]


def walk(x_cell, y_cell):
    print(f"cell: ({x_cell}, {y_cell})")


def check_neighbours(self, x, y):
    direction = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    d_sorted = direction
    for neighbour in direction:
        if (neighbour[0] < 0) or (
                neighbour[0] > self.maze_width) or (
                neighbour[1] < 0) or (
                neighbour[1] > self.maze_height):
            d_sorted.remove(neighbour)

    return d_sorted

walk(0,0)


@tail_recursive
def walk(self, posx, posy):
    self._map[posx][posy] = 'V'  # Mark the cell as visited
    while True:
        # hasNeighbors returns a empty list if no valid neighbors ar found
        # but returns a list of cardinal dir_ections corresponding to valid neighbors if found such as ["N", "E"]
        # if there is a valid neighbor on the right and beneath.
        dir_ = self._hasNeighbors(posx, posy)  # refactor dir to dir_ to avoid overwriting builtin function
        lenght = len(dir_)

        # If there is no valid neighbors this is a dead end then return to backtrack
        if lenght == 0:
            return

        # select a random direction to move to and remove it from the list
        toBreak = dir_.pop(dir_.index(random.choice(dir_)))

        # Replace '#' by '.'
        self._map[posx + self._dic[toBreak][0]][posy + self._dic[toBreak][1]] = '.'

        # If there is only one valid neightbor break the wall and update posx and posy
        # It uses the while loop to keep visiting cells without recursion as long as there is only one choice
        if lenght == 1:
            posx += self._dic[toBreak][0] * 2
            posy += self._dic[toBreak][1] * 2
            self._map[posx][posy] = 'V'

        # recursive call of the backtrack function with the position of the cell we want to visit
        else:
            # Replace call with tail recursive call
            # self._backtrack(posx + self._dic[toBreak][0] * 2, posy + self._dic[toBreak][1] * 2)
            recurse(self, posx + self._dic[toBreak][0] * 2, posy + self._dic[toBreak][1] * 2)


