from .Binding import Binding
import tkinter as tk


class KeyboardBindings(Binding):

    def __init__(self, root: tk.Tk, key):
        super().__init__()
        self.root = root
        self.root.bind(key, self._trigger)




