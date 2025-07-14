import tkinter as tk
from ColourSchemes import Scheme as Theme


def create_menu_button(parent, text, row, command=None, disabled=False):
    state = 'normal'
    outline = Theme.button_outline
    bg = Theme.button_bg
    fg = Theme.button_text
    if disabled:
        state = 'disabled'
        outline = Theme.disabled_button_outline
        bg = Theme.disabled_button_bg
        fg = Theme.disabled_button_text
    button_bd = tk.Frame(parent,
                         highlightbackground=outline,
                         highlightthickness=2,
                         bd=0)
    button = tk.Button(button_bd,
                       text=f'{text}',
                       bg=bg, fg=fg,
                       bd=4, relief='flat',
                       activebackground=Theme.highlight,
                       activeforeground=Theme.highlight_text,
                       command=command,
                       state=state)
    button_bd.grid(row=row, column=1, sticky='nsew', pady=5)
    button.pack(fill='both', expand=True, side='top')
    return button_bd


def create_menu_title(parent, text):
    title = tk.Label(parent, text=text, font=(Theme.font_bold, 36),
                     fg=Theme.text, bg=Theme.bg, width=10, pady=20)
    title.pack(side='top', fill='both')


def create_label(parent, text, row, side=tk.CENTER):
    container = tk.Frame(parent, bg=Theme.bg,
                         relief='flat')
    label = tk.Label(container,
                     text=f'{text}',
                     fg=Theme.text,
                     bg=Theme.bg,
                     anchor=side)
    container.grid(row=row, column=1, sticky='nsew', pady=5)
    label.pack(side='left', fill='both')


def create_drop_down(parent, text, row, options, default=None):
    if default is None:
        default = options[0]
    container = tk.Frame(parent, bg=Theme.bg,
                         relief='flat')
    label = tk.Label(container,
                     text=f'{text}',
                     fg=Theme.text,
                     bg=Theme.bg)

    str_var = tk.StringVar(container)
    str_var.set(default)

    dropdown = tk.OptionMenu(container,
                             str_var,
                             *options)
    dropdown.config(bg=Theme.sec_bg, fg=Theme.text,
                    activebackground=Theme.highlight,
                    activeforeground=Theme.highlight_text,
                    highlightthickness=0, relief="flat"
                    )
    dropdown['menu'].config(bg=Theme.sec_bg, fg=Theme.text,
                            activebackground=Theme.highlight,
                            activeforeground=Theme.highlight_text)
    container.grid(row=row, column=1, sticky='nsew', pady=5)
    label.pack(side='left', fill='both')
    dropdown.pack(side='right', fill='both')

    return str_var
    # End of function create_drop_down


def create_input_field(parent, text, row, command=None):
    container = tk.Frame(parent, bg=Theme.bg,
                         relief='flat')

    str_var = tk.StringVar(container)
    str_var.set(text)

    entry = tk.Entry(container,
                     highlightbackground=Theme.text,
                     highlightthickness=2,
                     highlightcolor=Theme.text,
                     selectbackground=Theme.bg,
                     selectforeground=Theme.text,
                     relief='flat',
                     bg=Theme.button_bg, fg=Theme.text,
                     textvariable=str_var,
                     command=command,
                     # cursor=f'left_tee',
                     exportselection=0)

    container.grid(row=row, column=1, sticky='nsew', pady=5)
    entry.pack(side='left', fill='both', expand=True)

    return str_var
    # End of function create_input_field
