# Kyler Olsen
# Mar 2024

import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
import importlib

from .reference import convert_reference, InvalidReference
from .load_data import load_uri, COLLECTION_RESOURCES, ResourceNotFound
from .scriptures import Chapter
from .collections_ import Collection

class Main(ttk.Frame):

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack()

        nav_col = 0

        self.home_button = ttk.Button(
            self.nav_frame, text='←', width=2, command=self.nav_back)
        self.home_button.grid(column=nav_col, row=0)
        nav_col += 1

        self.home_button = ttk.Button(
            self.nav_frame, text='→', width=2, command=self.nav_forward)
        self.home_button.grid(column=nav_col, row=0)
        nav_col += 1

        self.home_button = ttk.Button(
            self.nav_frame, text='H', width=2, command=self.nav_home)
        self.home_button.grid(column=nav_col, row=0)
        nav_col += 1

        # self.up_button = ttk.Button(
        #     self.nav_frame, text='↑', width=2, command=self.nav_up)
        # self.up_button.grid(column=nav_col, row=0)
        # nav_col += 1

        self.uri = tk.StringVar()
        self.uri_entry = ttk.Entry(self.nav_frame, textvariable=self.uri)
        # self.uri_entry.bind("<KeyRelease>", self.open_scripture)
        self.uri_entry.grid(column=nav_col, row=0)
        nav_col += 1

        self.uri_button = ttk.Button(
            self.nav_frame, text='→', width=2, command=self.open_scripture)
        self.uri_button.grid(column=nav_col, row=0)
        nav_col += 1

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.nav_frame, textvariable=self.search_var)
        # self.search_entry.bind("<KeyRelease>", self.search)
        self.search_entry.grid(column=nav_col, row=0)
        nav_col += 1

        self.search_button = ttk.Button(
            self.nav_frame, text='→', width=2, command=self.search)
        self.search_button.grid(column=nav_col, row=0)
        nav_col += 1

        self.home_button = ttk.Button(
            self.nav_frame, text='M', width=2, command=self.load_module)
        self.home_button.grid(column=nav_col, row=0)
        nav_col += 1

        self.scripture = ttk.Frame(self)
        self.scripture.pack(fill="both", expand=True)

        self.history = []
        self.future = []
        self.lds_org = None
        self.use_default = True

        try: self.lds_org = importlib.import_module('lds_org')
        except ImportError: pass
        else: self.use_default = False

        self.nav_home()

    def nav(self, uri):
        self.future = []
        self.history.append(self.uri.get())
        self.uri.set(uri)
        self.open_scripture()

    def nav_forward(self):
        if self.future:
            self.history.append(self.uri.get())
            self.uri.set(self.future.pop())
            self.open_scripture()

    def nav_back(self):
        if self.history:
            self.future.append(self.uri.get())
            self.uri.set(self.history.pop())
            self.open_scripture()

    def load_module(self, event=None):
        if self.lds_org is None:
            try: self.lds_org = importlib.import_module('lds_org')
            except ImportError: pass
        if self.lds_org is not None:
            self.use_default = not self.use_default
        self.nav_home()

    def nav_home(self, event=None):
        if self.use_default:
            self.nav('/scriptures')
        else:
            self.nav('/')

    def nav_up(self, event=None):
        self.nav('/'.join(self.uri.get().split('/')[:-1]) or '/')

    def open_scripture(self, event=None):
        if self.use_default:
            self.open_scripture_default()
        else:
            self.open_scripture_new()

    def open_scripture_default(self, event=None):
        try: data, resource_type = load_uri(self.uri.get())
        except ResourceNotFound:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Resource Not Found').pack()
            self.scripture.pack(fill="both", expand=True)
        except OSError:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Resource Missing').pack()
            self.scripture.pack(fill="both", expand=True)
        except Exception:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Unknown Error').pack()
            self.scripture.pack(fill="both", expand=True)
            raise
        else:
            if resource_type in ['scripture.chapter','scripture.section']:
                self.scripture.destroy()
                self.scripture = Chapter(self)
                self.scripture.load(data)
                self.scripture.pack(fill="both", expand=True)
            elif resource_type in COLLECTION_RESOURCES:
                self.scripture.destroy()
                self.scripture = Collection(self, data, self.nav)
                self.scripture.pack(fill="both", expand=True)
            else:
                self.scripture.destroy()
                self.scripture = ttk.Frame(self)
                ttk.Label(self.scripture, text='Resource Not Found').pack()
                self.scripture.pack(fill="both", expand=True)

    def open_scripture_new(self, event=None):
        if self.lds_org is None:
            self.use_default = True
            return
        try: data, resource_type = self.lds_org.load_uri(self.uri.get())
        except self.lds_org.ResourceNotFound:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Resource Not Found').pack()
            self.scripture.pack(fill="both", expand=True)
            raise
        except OSError:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Resource Missing').pack()
            self.scripture.pack(fill="both", expand=True)
        except Exception:
            self.scripture.destroy()
            self.scripture = ttk.Frame(self)
            ttk.Label(self.scripture, text='Unknown Error').pack()
            self.scripture.pack(fill="both", expand=True)
            raise
        else:
            if resource_type == 'collection':
                self.scripture.destroy()
                self.scripture = Collection(self, data, self.nav)
                self.scripture.pack(fill="both", expand=True)
            elif isinstance(data, str):
                self.scripture.destroy()
                self.scripture = ttk.Frame(self)
                html = HtmlFrame(self.scripture, messages_enabled = False)
                html.load_html(data)
                html.pack(fill="both", expand=True)
                self.scripture.pack(fill="both", expand=True)
            else:
                self.scripture.destroy()
                self.scripture = ttk.Frame(self)
                ttk.Label(self.scripture, text='Resource Not Found').pack()
                self.scripture.pack(fill="both", expand=True)

    def search(self, event=None):
        try: uri = '/scriptures' + convert_reference(self.search_var.get())
        except InvalidReference: pass
        else: self.nav(uri)


def main():

    root = tk.Tk()
    root.geometry('500x300')

    main = Main(root)
    main.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()
