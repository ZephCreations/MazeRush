import tkinter as tk

from .utils import create_menu_button, create_menu_title
from ColourSchemes import Scheme as Theme

MENU_TITLE_TEXT = "How to Play"


class InstructionsMenu(tk.Frame):
    def __init__(self, parent, bread_crumbs, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg=Theme.bg)
        self.parent = parent
        self.pack(side="top", fill="both", expand=True)
        self.bread_crumbs = bread_crumbs

        self.create_widgets()

        # End of __init__

    def create_widgets(self):
        create_menu_title(self, MENU_TITLE_TEXT)

        container = tk.Frame(self, bg=Theme.bg)
        container.pack(side='top', fill='both', expand=True)
        container.rowconfigure((0, 1, 2, 3, 4, 5,
                                6, 7, 8, 9, 10),
                               weight=1, uniform='yes')
        container.columnconfigure(1, weight=2, minsize=220)
        container.columnconfigure((0, 2), weight=3, minsize=80)

        padding_left = tk.Frame(container, width=250,
                                bg=Theme.bg)
        padding_left.grid(row=0, column=0, rowspan=10, sticky='nsew')
        padding_right = tk.Frame(container, width=250,
                                 bg=Theme.bg)
        padding_right.grid(row=0, column=2, rowspan=10, sticky='nsew')

        middle_frame = tk.Frame(container, bg=Theme.bg,
                                borderwidth=0, pady=20)
        middle_frame.grid(row=0, column=1, rowspan=9, sticky='nsew')

        # Scroll Container
        scroll_container = self.create_scroll_container(middle_frame)

        self.create_paragraph(
            scroll_container, "The Aim:", 1,
            ('The Aim of this game is to reach the Flag as '
             'quickly as possible, in as few movements as possible.')
        )
        self.create_paragraph(
            scroll_container, "Points:", 2,
            ('The Points Needed To Win dropdown is used to select '
             'how many points or times you need to reach the flag '
             'in order to win. Increasing this value increases '
             'the game length.')
        )
        self.create_paragraph(
            scroll_container, 'Controls', 3,
            ('Single Player:\n'
             ' -  WASD and/or Arrow Keys\n'
             'Local Multiplayer:\n'
             ' -  P1 is WASD\n'
             ' -  P2 is Arrow Keys\n'
             ' -  P3 is JIKL Keys\n'
             ' -  P3 is FTGH Keys')
        )

        create_menu_button(container, "Back <-",
                           9, self.go_back)

        # End of function create_widgets

    def create_paragraph(self, parent, title, row, text):
        container = tk.Frame(parent, bg=Theme.bg,
                             relief='flat')
        title = tk.Label(container,
                         text=title, font=('calibri', 17),
                         fg=Theme.text, bg=Theme.bg,
                         justify='left', anchor='w')
        label = tk.Label(container,
                         text=f'{text}', font=('calibri', 12),
                         fg=Theme.text, bg=Theme.bg,
                         justify='left', anchor='w',
                         wraplength=220)

        container.grid(row=row, column=1, sticky='nsew', pady=5)
        title.pack(side='top', fill='both')
        label.pack(side='top', fill='both')

        # End of function create_drop_down

    def create_scroll_container(self, parent):
        # Create outer frame to contain scrollbar

        # Create scroll window and scroll bar
        canvas = tk.Canvas(parent, borderwidth=0,
                           bg=Theme.bg, highlightthickness=0)
        inner_frame = tk.Frame(canvas, bg=Theme.bg)
        scroll_bar = tk.Scrollbar(parent, orient='vertical',
                                  command=canvas.yview,
                                  background="blue",
                                  activebackground="yellow")

        # Display the window
        scroll_bar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.create_window((4, 4), window=inner_frame,
                             anchor='nw', tags='frame')

        # Configure scrolling
        canvas.config(yscrollcommand=scroll_bar.set)
        inner_frame.bind('<Configure>',
                         lambda event:
                         canvas.configure(scrollregion=canvas.bbox("all")))

        return inner_frame

    def go_back(self):
        self.bread_crumbs.previous()(
            self.parent, self.bread_crumbs)
        self.destroy()
