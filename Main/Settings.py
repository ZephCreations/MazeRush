import ColourSchemes


class Settings:
    POINTS_TO_WIN = 3
    MIN_POINTS = 3
    MAX_POINTS = 20
    SHOW_TRAILS = True
    SHOW_TRAILS_DISPLAY = "Show"
    THEME = ColourSchemes.Dark()
    DEFAULT_MAZE_SIZE = (20, 20)
    MIN_MAZE_SIZE = (5, 5)
    MAX_MAZE_SIZE = (40, 40)
    PLAYER_1_BINDINGS = ["W", "A", "S", "D", "w", "a", "s", "d"]
    PLAYER_2_BINDINGS = ["<Up>", "<Left>", "<Down>", "<Right>"]
    PLAYER_3_BINDINGS = ["I", "J", "K", "L", "i", "j", "k", "l"]
    PLAYER_4_BINDINGS = ["T", "F", "G", "H", "t", "f", "g", "h"]

