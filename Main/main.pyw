"""
Main loop:

check for player movement
    run logic
    update position
    update scores

update time

update other player positions

call draw screen ___once___
"""

from Menus import RootWindow, MainMenu
import ColourSchemes


if __name__ == "__main__":
    # start game
    ColourSchemes.change_scheme(ColourSchemes.Dark())
    root = RootWindow(_width=500, _height=500, bg="light blue")
    main_menu = MainMenu(root, width=500, height=500)

    root.mainloop()
