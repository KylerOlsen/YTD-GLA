# Kyler Olsen
# Mar 2024

import tkinter as tk
from tkinter import ttk

from reference import convert_reference, InvalidReference
from load_data import load_uri, ResourceNotFound
from scriptures import Chapter

class Main(ttk.Frame):

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var)
        self.entry.bind("<KeyRelease>", self.open_scripture)
        self.entry.pack()

        self.scripture = ttk.Frame(self)
        self.scripture.pack(fill="both", expand=True)

    def open_scripture(self, event=None):

        try: uri = convert_reference(self.entry_var.get())
        except InvalidReference: pass
        else:
            try: data = load_uri(uri)
            except ResourceNotFound: pass
            else:
                self.scripture.destroy()
                self.scripture = Chapter(self)
                self.scripture.load(data)
                self.scripture.pack(fill="both", expand=True)


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('300x300')

    main = Main(root)
    main.pack(fill="both", expand=True)

    root.mainloop()
