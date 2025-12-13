import tkinter as tk

from ColourSchemes import Scheme as Theme


class GameCanvas(tk.Canvas):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def display_text(self, text, colour,
                     font=(Theme.font_bold, 56),
                     outline=None,
                     offset=(0, 0)):
        if outline is None:
            outline = Theme.button_outline
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        center_position = (canvas_width / 2 + offset[0],
                           canvas_height / 2 + offset[1])

        text = self.create_text(center_position,
                                  text=text, fill=colour,
                                  font=font, anchor='center')
        text_bounds = self.bbox(text)
        text_bg = self.create_rectangle(
            text_bounds[0] - 10, text_bounds[1] - 10,
            text_bounds[2] + 10, text_bounds[3] + 10,
            fill=Theme.bg, outline=outline, width=1
        )
        self.tag_raise(text_bg)
        self.tag_raise(text)
        self.update_idletasks()

        return text, text_bg
        # End of function display_text

    def get_center(self):
        return (self.winfo_width() / 2,
                self.winfo_height() / 2)


