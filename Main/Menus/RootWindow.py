
import tkinter as tk
from pathlib import Path


class RootWindow(tk.Frame):
    def __init__(self, *args, _width=500, _height=600, **kwargs):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        # self.root.state('zoomed')
        self.root.title("Maze Rush")
        self.root.minsize(width=400, height=500)

        filepath = Path(__file__).parent / "Icon.ico"
        self.root.iconbitmap(filepath)

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # calculate x and y coordinates for the Tk root window
        x = (screen_width / 2) - (_width / 2)
        y = (screen_height / 2) - (_height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.root.geometry(f'{_width}x{_height}+{int(x)}+0')

        # Make the main frame
        tk.Frame.__init__(self, self.root, *args, **kwargs)
        self.config(width=_width, height=_height)
        self.parent = self.root
        self.width = _width
        self.height = _height
        self.pack(side="top", fill="both", expand=True)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    root = RootWindow(width=500, height=500)
    root.mainloop()