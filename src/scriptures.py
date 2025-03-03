# Kyler Olsen
# Mar 2024

import tkinter as tk
from tkinter import ttk
from enum import Enum


class ScriptureFormatting(Enum):

    BOOK_TITLE = 'book_title'
    BOOK_SUBTITLE = 'book_subtitle'
    BOOK_INTRODUCTION = 'book_introduction'
    CHAPTER_HEADER = 'chapter_header'
    STUDY_SUMMARY = 'study_summary'
    VERSE_NUMBER = 'verse_number'
    VERSE_TEXT = 'verse_text'
    FOOTNOTE = 'footnote'
    FOOTNOTE_MARKER = 'footnote_marker'
    UPPERCASE = 'uppercase'
    SMALL_CAPS = 'small_caps'
    ITALICS = 'italics'

    def text(self, text: str) -> str:
        if self == ScriptureFormatting.UPPERCASE:
            text = text.upper()
        elif self == ScriptureFormatting.SMALL_CAPS:
            text = text.upper()
        return text

    @property
    def format(self):
        format = {
            'font': ("Times New Roman", 12,),
            'justify': 'left',
            'wrap': 'word',
            'spacing3': 8,
            'lmargin1': 4,
            'lmargin2': 4,
            'rmargin': 4,
        }
        if self == ScriptureFormatting.VERSE_NUMBER:
            format['font'] = ("Times New Roman", 12, "bold",)
            format['lmargin1'] = 12
        elif self == ScriptureFormatting.FOOTNOTE:
            format['foreground'] = 'blue'
        elif self == ScriptureFormatting.FOOTNOTE_MARKER:
            format['font'] = ("Times New Roman", 8, "italic")
            format['foreground'] = 'blue'
            format['offset'] = 4
        elif self == ScriptureFormatting.SMALL_CAPS:
            format['font'] = ("Times New Roman", 10)
        elif self == ScriptureFormatting.ITALICS:
            format['font'] = ("Times New Roman", 12, "italic")
        return format


class Chapter(ttk.Frame):

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.text = tk.Text(self, state='disabled')
        self.text.pack(fill="both", expand=True)

        for tag in ScriptureFormatting:
            self.text.tag_configure(tag.value, **tag.format) # type: ignore

    def load(self, data):
        self.text['state'] = 'normal'
        self.text.delete('1.0','end')
        for verse in data['verses']:
            self.text.insert('end', str(verse['verse']) + ' ', (
                ScriptureFormatting.VERSE_NUMBER.value,
            ))
            self.text.insert('end', verse['text'] + '\n', (
                ScriptureFormatting.VERSE_TEXT.value,
            ))
            length = len(verse['text']) + 2
            if 'formatting' in verse:
                for fm in verse['formatting']:
                    start = length - fm['location']
                    end = start - len(fm['text'])
                    fm_e = ScriptureFormatting(fm['format'])
                    text = fm_e.text(fm['text'])
                    if fm_e == ScriptureFormatting.SMALL_CAPS:
                        start -= 1
                        text = text[1:]
                    self.text.delete(f"end-{start}c", f"end-{end}c")
                    self.text.insert(f"end-{end}c", text, fm_e.value)
            if 'footnotes' in verse:
                for fn in verse['footnotes']:
                    start = length - fn['start']
                    end = start - len(fn['text'])
                    self.text.tag_add(
                        ScriptureFormatting.FOOTNOTE.value,
                        f"end-{start}c",
                        f"end-{end}c",
                    )
                    self.text.insert(
                        f"end-{start}c",
                        fn['marker'][-1],
                        (ScriptureFormatting.FOOTNOTE_MARKER.value,),
                    )
        self.text['state'] = 'disabled'


if __name__ == '__main__':

    from json import load

    with open('data/pearl-of-great-price.json', 'r', encoding='utf-8') as file:
        data = load(file)

    root = tk.Tk()

    chapter = Chapter(root)
    chapter.pack(fill="both", expand=True)
    chapter.load(data['books'][0]['chapters'][6])

    root.mainloop()
