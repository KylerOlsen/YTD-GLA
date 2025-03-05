# Kyler Olsen
# Mar 2024

import tkinter as tk
from tkinter import ttk

class Collection(tk.Canvas):

    def __init__(self, root, links, nav, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.nav = nav

        self.text = tk.Text(self, state='disabled')
        self.text.pack(fill="both", expand=True)

        for name, uri in links:
            self.add_link(name, uri)

    def add_link(self, name, uri):
        button = ttk.Button(
            self.text,
            text=name,
            width=len(name) + 2,
            command=lambda: self.nav(uri),
        )
        # button.pack()
        self.text.window_create('end', window=button)
