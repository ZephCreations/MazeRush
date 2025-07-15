from .Binding import Binding
import tkinter as tk


class KeyboardBindings(Binding):

    def __init__(self, root: tk.Tk, key):
        super().__init__()
        self.root = root
        self.key = key
        self.root.bind(key, self._trigger)

    def __repr__(self):
        return self.key




